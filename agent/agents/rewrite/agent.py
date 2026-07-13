from tools.rewrite_tool import RewritePlanTool, RewriteExecuteTool


class RewriteAgent:

    name = "rewrite_agent"
    description = "简历优化专家：生成修改计划，执行简历优化"

    def __init__(self):
        self.tools = [
            RewritePlanTool(),
            RewriteExecuteTool(),
        ]

    def plan(self, state: dict) -> dict:
        tool = self.tools[0]  # RewritePlanTool
        state["rewrite_plan"] = tool.run(
            resume_json=state.get("resume_json", {}),
            jd=state.get("jd", "")
        )
        return state

    def execute(self, state: dict) -> dict:
        import json
        tool = self.tools[1]  # RewriteExecuteTool
        result = tool.run(
            resume_json=state.get("resume_json", {}),
            plan=state.get("rewrite_plan", {})
        )
        state["rewrite_result"] = json.dumps(result, ensure_ascii=False, indent=2)
        return state
