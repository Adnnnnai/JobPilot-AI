from .base_tool import BaseTool


class GitHubTool(BaseTool):

    name = "github_summary"
    description = "通过 GitHub MCP 分析仓库结构和技术栈"

    def run(self, repo_url: str):
        return {
            "status": "placeholder",
            "repo": repo_url,
            "message": "GitHub MCP Server 未配置。配置后将自动分析仓库。"
        }


class BrowserTool(BaseTool):

    name = "browser_search"
    description = "通过 Browser MCP 抓取网页内容"

    def run(self, url: str):
        return {
            "status": "placeholder",
            "url": url,
            "message": "Browser MCP Server 未配置。配置后将自动抓取网页。"
        }
