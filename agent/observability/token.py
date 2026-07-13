"""
Token

记录每次 LLM 调用的 Token 用量和预估费用。
"""
from datetime import datetime


class TokenUsage:

    _records = []

    @classmethod
    def record(cls, prompt_tokens: int, completion_tokens: int, model: str = ""):
        cls._records.append({
            "time": datetime.now().isoformat(),
            "model": model,
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": prompt_tokens + completion_tokens,
            "cost_usd": cls._estimate_cost(model, prompt_tokens, completion_tokens),
        })

    @classmethod
    def total(cls) -> dict:
        return {
            "calls": len(cls._records),
            "total_tokens": sum(r["total_tokens"] for r in cls._records),
            "total_cost_usd": round(sum(r["cost_usd"] for r in cls._records), 6),
        }

    @classmethod
    def _estimate_cost(cls, model: str, prompt: int, completion: int) -> float:
        # DeepSeek 定价 (V2): prompt $0.14/1M, completion $0.28/1M
        rates = {
            "deepseek": (0.14, 0.28),
            "openai": (2.50, 10.00),
            "claude": (3.00, 15.00),
        }
        rate = rates.get("deepseek")
        return (prompt * rate[0] + completion * rate[1]) / 1_000_000
