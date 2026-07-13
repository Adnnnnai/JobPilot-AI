"""
JD Generation Service

当浏览器无法抓取 JD 时，用 LLM 根据岗位名称生成标准 JD 模板。
"""
import json

from app.services.llm_service import LLMService


class JDGenerator:

    JD_PROMPT = """你是专业的招聘专家。请根据以下岗位名称，生成一份标准的、详细的岗位描述（JD）。

岗位：{keyword}

请输出 JSON（不要 Markdown，不要解释）：
{{
    "title": "岗位名称",
    "company": "示例公司（请标注"模板"）",
    "location": "行业常见地点",
    "salary": "行业常见薪资范围",
    "requirements": ["要求1（具体、专业）", "要求2", "要求3", "要求4", "要求5"],
    "responsibilities": ["职责1（具体、专业）", "职责2", "职责3", "职责4"],
    "tech_stack": ["技术栈1", "技术栈2", "技术栈3", "技术栈4", "技术栈5"],
    "description": "200字以内的岗位简介",
    "source": "llm_generated"
}}

要求：
- 所有内容必须专业、具体，符合真实招聘市场
- requirements 要包含具体的技能、年限、学历要求
- tech_stack 要列出该岗位常用的具体技术/框架/工具
- 不要留空，每个字段都要填充"""

    @classmethod
    def generate(cls, keyword: str) -> dict:
        prompt = cls.JD_PROMPT.format(keyword=keyword)
        result = LLMService.chat(prompt)
        try:
            return json.loads(result)
        except json.JSONDecodeError:
            return {
                "title": keyword,
                "source": "llm_generated",
                "description": result[:500],
                "requirements": [],
                "responsibilities": [],
                "tech_stack": [],
            }
