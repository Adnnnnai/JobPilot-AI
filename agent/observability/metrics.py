"""
Metrics

统计每个 Tool 的调用次数、总耗时、Token 用量。
"""
from datetime import datetime
from collections import defaultdict


class ToolMetrics:

    _records = defaultdict(list)

    @classmethod
    def record(cls, tool_name: str, duration_ms: float, tokens: int = 0):
        cls._records[tool_name].append({
            "time": datetime.now().isoformat(),
            "duration_ms": round(duration_ms, 2),
            "tokens": tokens,
        })

    @classmethod
    def summary(cls) -> dict:
        result = {}
        for name, records in cls._records.items():
            durations = [r["duration_ms"] for r in records]
            result[name] = {
                "calls": len(records),
                "total_ms": round(sum(durations), 2),
                "avg_ms": round(sum(durations) / len(durations), 2) if durations else 0,
                "max_ms": round(max(durations), 2) if durations else 0,
                "tokens": sum(r["tokens"] for r in records),
            }
        return result
