"""
Event

每个节点执行前后发送 Event，供 Streaming 和日志使用。
"""
import time
from datetime import datetime

from .trace import Trace


class EventBus:

    @staticmethod
    def emit(node: str, status: str, detail: dict = None):
        trace = Trace.current()
        trace.events.append({
            "ts": datetime.now().isoformat(),
            "node": node,
            "status": status,  # started | finished | failed
            "detail": detail or {},
        })
