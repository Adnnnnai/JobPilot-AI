"""
Span

一个 Trace 包含多个 Span，记录每个节点/工具的耗时。
"""
import time

from .trace import Trace


class Span:

    def __init__(self, name: str, parent: "Span" = None):
        self.name = name
        self.parent = parent
        self.start_time = None
        self.end_time = None
        self.meta = {}

    def __enter__(self):
        self.start_time = time.time()
        return self

    def __exit__(self, *args):
        self.end_time = time.time()
        trace = Trace.current()
        trace.events.append(self)

    @property
    def duration_ms(self) -> float:
        if self.start_time and self.end_time:
            return (self.end_time - self.start_time) * 1000
        return 0
