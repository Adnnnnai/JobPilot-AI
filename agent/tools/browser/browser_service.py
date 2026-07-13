"""
BrowserService

负责浏览器操作。不包含 AI 逻辑。
"""
from playwright.sync_api import sync_playwright

CHROME_PATH = "C:/Program Files/Google/Chrome/Application/chrome.exe"


class BrowserService:

    _playwright = None
    _browser = None

    @classmethod
    def _get_browser(cls, headless: bool = True):
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
        browser = cls._get_browser(headless=True)
        page = browser.new_page()
        page.set_extra_http_headers({
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/130.0.0.0 Safari/537.36"
            )
        })
        return page

    # ── Public API ─────────────────────────────

    @classmethod
    def open(cls, url: str, timeout: int = 30000) -> str:
        """打开页面，返回 body 文本"""
        page = cls._new_page()
        try:
            page.goto(url, timeout=timeout, wait_until="domcontentloaded")
            return page.inner_text("body") or ""
        except Exception:
            return ""
        finally:
            page.close()

    @classmethod
    def search(cls, keyword: str, site: str = "indeed") -> str:
        """搜索岗位，返回页面文本"""
        urls = {
            "indeed": f"https://www.indeed.com/jobs?q={keyword}&limit=10",
            "liepin": f"https://www.liepin.com/zhaopin/?key={keyword}",
        }
        url = urls.get(site, urls["indeed"])
        return cls.open(url)

    @classmethod
    def close(cls):
        if cls._browser:
            cls._browser.close()
            cls._browser = None
        if cls._playwright:
            cls._playwright.stop()
            cls._playwright = None
