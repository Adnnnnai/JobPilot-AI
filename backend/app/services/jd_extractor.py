"""
JD Extraction Service

从招聘网站抓取的页面中提取结构化 JD 信息。
"""
import json

from app.services.llm_service import LLMService


class JDExtractor:

    @staticmethod
    def extract(jd_text: str) -> dict:
        """用 LLM 从招聘页面文本中提取 JD 结构化信息"""
        prompt = f"""你是专业的岗位分析专家。请从以下招聘页面内容中提取岗位信息。

内容：
{jd_text[:4000]}

请输出 JSON（不要 Markdown，不要解释）：
{{
    "title": "岗位名称",
    "company": "公司名称",
    "location": "工作地点",
    "salary": "薪资范围",
    "requirements": ["要求1", "要求2"],
    "responsibilities": ["职责1", "职责2"],
    "tech_stack": ["技术栈1", "技术栈2"],
    "description": "岗位简介"
}}

注意：如果某项信息没有找到，设为空字符串或空数组。"""

        result = LLMService.chat(prompt)
        try:
            return json.loads(result)
        except json.JSONDecodeError:
            return {"title": "", "description": result[:500]}
