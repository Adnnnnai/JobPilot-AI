from workflow.graph import graph
from observability.trace import Trace
from observability.token import TokenUsage
from observability.monitor import WorkflowMonitor, WorkflowStatus


class JobPilotAgent:

    def invoke(self, state, thread_id=None):
        trace = Trace.start()
        config = {}
        if thread_id:
            config = {"configurable": {"thread_id": thread_id}}

        WorkflowMonitor.start(trace.trace_id, state.get("message", ""))

        try:
            result = graph.invoke(state, config=config)
            WorkflowMonitor.finish(trace.trace_id, WorkflowStatus.COMPLETED)
            return result
        except Exception as e:
            WorkflowMonitor.finish(trace.trace_id, WorkflowStatus.FAILED, str(e))
            raise

    def stream(self, state, thread_id=None):
        trace = Trace.start()
        config = {}
        if thread_id:
            config = {"configurable": {"thread_id": thread_id}}

        WorkflowMonitor.start(trace.trace_id, state.get("message", ""))

        try:
            for event in graph.stream(state, config=config, stream_mode="updates"):
                yield event
            WorkflowMonitor.finish(trace.trace_id, WorkflowStatus.COMPLETED)
        except Exception as e:
            WorkflowMonitor.finish(trace.trace_id, WorkflowStatus.FAILED, str(e))
            raise
