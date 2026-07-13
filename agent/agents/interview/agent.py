import json
import os

from tools.rag_tools import InterviewRAGTool
from app.services.llm_service import LLMService


PROMPT_PATH = os.path.join(os.path.dirname(__file__), "prompt.md")


class InterviewAgent:

    name = "interview_agent"
    description = "模拟面试专家：基于简历和JD生成针对性面试题"

    def __init__(self):
        self.tools = [
            InterviewRAGTool(),
        ]

    def run(self, state: dict) -> dict:
        with open(PROMPT_PATH, encoding="utf8") as f:
            system_prompt = f.read()

        resume = state.get("resume_json", {})
        jd = state.get("jd", "")

        prompt = system_prompt + "\n\n"
        prompt += f"简历：{json.dumps(resume, ensure_ascii=False, indent=2)}\n\n"
        prompt += f"岗位：{jd if jd else '通用'}\n\n"
        prompt += "请生成面试题 JSON。"

        result = LLMService.chat(prompt)
        try:
            questions = json.loads(result)
        except json.JSONDecodeError:
            questions = {"questions": [{"category": "通用", "question": result[:200]}]}
        state["interview_questions"] = questions.get("questions", [])
        return state
