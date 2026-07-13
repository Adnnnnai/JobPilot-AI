import json
import os

from app.services.llm_service import LLMService
from models import TaskPlan, Task


PROMPT_PATH = os.path.join(os.path.dirname(__file__), "prompt.md")


class PlannerAgent:

    name = "planner"
    description = "任务规划专家：将用户目标拆解为结构化 TaskPlan"

    @classmethod
    def _load_prompt(cls) -> str:
        with open(PROMPT_PATH, encoding="utf8") as f:
            return f.read()

    @classmethod
    def plan(cls, message: str, profile: dict = None, preferences: dict = None) -> TaskPlan:
        prompt = cls._load_prompt()

        # 注入用户画像和偏好到 prompt
        if profile and any(profile.values()):
            prompt += f"\n\n用户画像：{json.dumps(profile, ensure_ascii=False, indent=2)}"
        if preferences:
            prompt += f"\n\n用户偏好：{json.dumps(preferences, ensure_ascii=False, indent=2)}"

        prompt += f"\n\n用户：{message}\n\n请输出 JSON："

        result = LLMService.chat(prompt)
        data = json.loads(result)
        tasks = [Task(**t) for t in data.get("tasks", [])]
        return TaskPlan(tasks=tasks)
