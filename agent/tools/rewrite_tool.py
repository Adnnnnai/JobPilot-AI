import json

from .base_tool import BaseTool

from app.services.llm_service import LLMService


class RewriteTool(BaseTool):

    name = "resume_rewrite"

    description = "Rewrite Resume"

    def run(self, resume):
        prompt = f"""
Optimize this resume:

{resume}
"""
        return prompt


class RewritePlanTool(BaseTool):

    name = "rewrite_plan"
    description = "生成简历修改计划"

    def run(self, resume_json: dict, jd: str = ""):
        prompt = f"""你是一名专业简历优化师。请分析以下简历，给出修改计划。

简历：
{json.dumps(resume_json, ensure_ascii=False, indent=2)}

岗位要求：
{jd if jd else "通用优化"}

请输出 JSON（不要 Markdown，不要解释），格式如下：
{{
    "changes": [
        "修改项1",
        "修改项2",
        "修改项3"
    ],
    "reason": "整体修改思路说明"
}}"""

        result = LLMService.chat(prompt)
        try:
            return json.loads(result)
        except json.JSONDecodeError:
            return {"changes": [], "reason": result}


class RewriteExecuteTool(BaseTool):

    name = "rewrite_execute"
    description = "根据修改计划执行简历优化"

    def run(self, resume_json: dict, plan: dict):
        prompt = f"""你是一名专业简历优化师。请根据修改计划优化简历。

原始简历：
{json.dumps(resume_json, ensure_ascii=False, indent=2)}

修改计划：
{json.dumps(plan, ensure_ascii=False, indent=2)}

请严格按照修改计划，输出优化后的简历 JSON（保持相同结构，不要 Markdown，不要解释）。"""

        result = LLMService.chat(prompt)
        try:
            return json.loads(result)
        except json.JSONDecodeError:
            return {"result": result}
