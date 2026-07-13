from workflow.graph import graph


class JobPilotAgent:

    def invoke(self, state, thread_id=None):
        config = {}
        if thread_id:
            config = {
                "configurable": {
                    "thread_id": thread_id
                }
            }
        return graph.invoke(state, config=config)

    def stream(self, state, thread_id=None):
        """流式执行 workflow，每个节点完成后 yield 事件"""
        config = {}
        if thread_id:
            config = {
                "configurable": {
                    "thread_id": thread_id
                }
            }

        for event in graph.stream(state, config=config, stream_mode="updates"):
            yield event
