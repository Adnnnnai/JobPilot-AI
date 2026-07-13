"""
Browser Tool

三层协作:
  BrowserService  → 浏览器操作（打开页面、搜索）
  JDExtractor     → HTML → 结构化 JSON
  JDGenerator     → LLM 兜底生成 JD
"""
import json

from .base_tool import BaseTool
from .browser.browser_service import BrowserService

from app.services.jd_extractor import JDExtractor
from app.services.jd_generator import JDGenerator


class BrowserSearchTool(BaseTool):

    name = "browser_search"
    description = "搜索岗位JD：浏览器抓取 + LLM 解析为结构化 JSON"

    def run(self, keyword: str, site: str = "indeed") -> str:
        # 1. BrowserService: 浏览器抓取
        html_text = BrowserService.search(keyword, site=site)

        # 2. JDExtractor: HTML → 结构化 JSON
        if html_text and len(html_text) > 200:
            jd = JDExtractor.extract(html_text)
            if jd.get("title"):
                return json.dumps(jd, ensure_ascii=False, indent=2)

        # 3. JDGenerator: LLM 兜底
        jd = JDGenerator.generate(keyword)
        return json.dumps(jd, ensure_ascii=False, indent=2)


class BrowserFetchTool(BaseTool):

    name = "browser_fetch"
    description = "抓取网页内容：获取任意网页的文本内容"

    def run(self, url: str) -> str:
        return BrowserService.open(url)
