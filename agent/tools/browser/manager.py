"""
Browser Manager

基于 Playwright + 本地 Chrome，封装为 Agent 调用的统一浏览器工具。

JD 来源策略：
  1. 优先通过浏览器抓取 JD
  2. 如果页面需要登录，回退到 LLM 内置知识生成 JD 模板
"""
from playwright.sync_api import sync_playwright

CHROME_PATH = "C:/Program Files/Google/Chrome/Application/chrome.exe"


class BrowserManager:

    _playwright = None
    _browser = None

    @classmethod
    def get_browser(cls, headless: bool = True):
        if cls._browser is None or not cls._browser.is_connected():
            cls._playwright = sync_playwright().start()
            cls._browser = cls._playwright.chromium.launch(
                executable_path=CHROME_PATH,
                headless=headless,
                args=[
                    "--disable-blink-features=AutomationControlled",
                    "--no-sandbox",
                ]
            )
        return cls._browser

    @classmethod
    def _new_page(cls):
        browser = cls.get_browser(headless=True)
        page = browser.new_page()
        page.set_extra_http_headers({
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/130.0.0.0 Safari/537.36"
            )
        })
        return page

    @classmethod
    def fetch_text(cls, url: str, timeout: int = 30000) -> str:
        page = cls._new_page()
        try:
            page.goto(url, timeout=timeout, wait_until="domcontentloaded")
            text = page.inner_text("body")
            return text if text else ""
        except Exception:
            return ""
        finally:
            page.close()

    @classmethod
    def fetch_with_retry(cls, url: str, timeout: int = 30000) -> str:
        """多源尝试抓取"""
        result = cls.fetch_text(url, timeout)
        if len(result) > 100:
            return result
        return ""

    @classmethod
    def close(cls):
        if cls._browser:
            cls._browser.close()
            cls._browser = None
        if cls._playwright:
            cls._playwright.stop()
            cls._playwright = None
