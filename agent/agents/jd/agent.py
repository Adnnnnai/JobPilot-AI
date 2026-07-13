from tools.jd_tool import JDTool
from tools.rag_tools import JDRAGTool


class JDAgent:

    name = "jd_agent"
    description = "岗位分析专家：匹配简历与JD，分析技能差距"

    def __init__(self):
        self.tools = [
            JDTool(),
            JDRAGTool(),
        ]

    def run(self, state: dict) -> dict:
        jd_text = state.get("jd", "")
        if jd_text:
            from app.rag.knowledge.jd_kb import JDKB
            jid = str(state.get("resume_id", 0))
            JDKB.index(jd_text, jid)

            tool = self.tools[0]  # JDTool
            state["match_result"] = tool.run(
                resume_json=state.get("resume_json", {}),
                jd=jd_text
            )

        return state
