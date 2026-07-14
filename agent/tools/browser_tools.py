"""
Browser Tool

JDGenerator → LLM 兜底生成 JD → 写入 PostgreSQL
(Playwright BrowserService disabled due to thread-safety issues with LangGraph)
"""
import json

from .base_tool import BaseTool

from app.services.jd_generator import JDGenerator
from app.services.jd_writer import JDWriter


class BrowserSearchTool(BaseTool):

    name = "browser_search"
    description = "搜索岗位JD：LLM 生成结构化 JD + 保存到数据库"

    def run(self, keyword: str, site: str = "indeed") -> str:
        # JDGenerator: LLM 生成
        jd = JDGenerator.generate(keyword)
        jd["keywords"] = keyword
        jd["source"] = "llm_generated"
        JDWriter.save(jd)
        return json.dumps(jd, ensure_ascii=False, indent=2)


class BrowserFetchTool(BaseTool):

    name = "browser_fetch"
    description = "抓取网页内容：获取任意网页的文本内容"

    def run(self, url: str) -> str:
        jd = JDGenerator.generate(url)
        jd["source"] = "llm_generated"
        return json.dumps(jd, ensure_ascii=False, indent=2)
