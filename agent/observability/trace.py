"""
Trace

每次 Workflow 执行生成一个唯一 trace_id，贯穿全部节点。
"""
import uuid
import time


class Trace:

    _current = None

    def __init__(self, trace_id: str = None):
        self.trace_id = trace_id or str(uuid.uuid4())[:8]
        self.start_time = time.time()
        self.events = []

    @classmethod
    def current(cls) -> "Trace":
        if cls._current is None:
            cls._current = Trace()
        return cls._current

    @classmethod
    def start(cls, trace_id: str = None) -> "Trace":
        cls._current = Trace(trace_id)
        return cls._current
