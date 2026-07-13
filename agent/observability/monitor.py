"""
Workflow Monitor

跟踪 Workflow 状态：running / completed / failed / retry
"""
from datetime import datetime
from enum import Enum


class WorkflowStatus(str, Enum):
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    RETRY = "retry"


class WorkflowMonitor:

    _records = []

    @classmethod
    def start(cls, trace_id: str, message: str = ""):
        cls._records.append({
            "trace_id": trace_id,
            "message": message,
            "status": WorkflowStatus.RUNNING,
            "started_at": datetime.now().isoformat(),
        })

    @classmethod
    def finish(cls, trace_id: str, status: WorkflowStatus, error: str = ""):
        for r in cls._records:
            if r["trace_id"] == trace_id and r["status"] == WorkflowStatus.RUNNING:
                r["status"] = status
                r["finished_at"] = datetime.now().isoformat()
                if error:
                    r["error"] = error
                break

    @classmethod
    def history(cls, limit: int = 20) -> list[dict]:
        return cls._records[-limit:]
