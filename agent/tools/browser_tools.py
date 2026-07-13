"""
Browser Tool

Agent 可调用的浏览器工具。
- search_jd(keyword)  → 搜索岗位 JD（优先抓取，抓不到则 LLM 生成）
- fetch_page(url)     → 抓取任意网页
"""
from .base_tool import BaseTool
from .browser.manager import BrowserManager

from app.services.jd_generator import JDGenerator


class BrowserSearchTool(BaseTool):

    name = "browser_search"
    description = "搜索岗位JD：优先从招聘网站抓取，失败则LLM生成标准模板"

    def run(self, keyword: str, source: str = "indeed"):
        # 1. 尝试浏览器抓取
        scraped = BrowserManager.fetch_text(
            f"https://www.indeed.com/jobs?q={keyword}&limit=5",
            timeout=15000
        )
        if scraped and len(scraped) > 200:
            return scraped

        # 2. 回退到 LLM 生成 JD 模板
        jd = JDGenerator.generate(keyword)
        return f"JD模板（LLM生成）:\n{jd}"


class BrowserFetchTool(BaseTool):

    name = "browser_fetch"
    description = "抓取网页内容：获取任意网页的文本内容"

    def run(self, url: str):
        return BrowserManager.fetch_text(url)
