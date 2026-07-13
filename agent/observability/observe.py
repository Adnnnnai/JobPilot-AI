"""
Observability

统一入口：Trace + Span + Metrics + Token + Event + Monitor 全部在此接入 Workflow。
"""
import time
import functools

from .trace import Trace
from .span import Span
from .metrics import ToolMetrics
from .token import TokenUsage
from .monitor import WorkflowMonitor, WorkflowStatus
from .event import EventBus


def observe_node(node_name: str):
    """装饰器：自动记录 Span + Event + 耗时"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(state):
            EventBus.emit(node_name, "started")
            with Span(node_name):
                try:
                    result = func(state)
                    EventBus.emit(node_name, "finished")
                    return result
                except Exception as e:
                    EventBus.emit(node_name, "failed", {"error": str(e)})
                    raise
        return wrapper
    return decorator


def observe_tool(tool_name: str):
    """装饰器：自动记录 Tool Metrics + 耗时"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            t0 = time.time()
            result = func(*args, **kwargs)
            elapsed = (time.time() - t0) * 1000
            ToolMetrics.record(tool_name, elapsed)
            return result
        return wrapper
    return decorator
