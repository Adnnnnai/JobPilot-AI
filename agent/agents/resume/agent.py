from tools.resume_tool import ResumeTool
from tools.rag_tools import ResumeRAGTool


class ResumeAgent:

    name = "resume_agent"
    description = "简历分析专家：解析简历、搜索简历知识库"

    def __init__(self):
        self.tools = [
            ResumeTool(),
            ResumeRAGTool(),
        ]

    def run(self, state: dict) -> dict:
        filepath = state.get("resume_path", "")
        if filepath and not state.get("resume_json"):
            tool = self.tools[0]  # ResumeTool
            state["resume_json"] = tool.run(filepath=filepath)

            from app.rag.knowledge.resume_kb import ResumeKB
            resume_id = state.get("resume_id", 0)
            ResumeKB.index(state["resume_json"], resume_id)

        return state
