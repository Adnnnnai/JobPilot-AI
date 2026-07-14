import json
import os

from .base_tool import BaseTool

from app.services.llm_service import LLMService


class JDTool(BaseTool):

    name = "jd_match"
    description = "Match Resume And JD using LLM"

    def run(self, resume_json, jd):
        prompt = f"""
你是一名专业的简历匹配分析师。请根据以下简历和岗位描述进行匹配分析。

简历：
{json.dumps(resume_json, ensure_ascii=False, indent=2)}

岗位描述：
{jd}

请输出 JSON（不要 Markdown，不要解释）：
{{
    "score": 85,
    "matched_skills": ["Python", "FastAPI"],
    "missing_skills": ["Docker", "Kubernetes"],
    "summary": "总体匹配度分析"
}}
"""
        try:
            result = LLMService.chat(prompt)
            return json.loads(result)
        except Exception as e:
            return {{"score": 0, "matched_skills": [], "missing_skills": [], "summary": str(e), "raw": jd}}
