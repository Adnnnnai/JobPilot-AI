from typing import Optional

from pydantic_settings import BaseSettings


class MCPServerConfig:
    def __init__(self, name: str, command: str, args: list[str], env: Optional[dict] = None):
        self.name = name
        self.command = command
        self.args = args
        self.env = env or {}


MCP_SERVERS = {
    "filesystem": MCPServerConfig(
        name="filesystem",
        command="npx",
        args=[
            "-y",
            "@modelcontextprotocol/server-filesystem",
            "D:/JobPilot"
        ]
    ),
    # 后续启用时取消注释即可
    # "github": MCPServerConfig(
    #     name="github",
    #     command="npx",
    #     args=["-y", "@modelcontextprotocol/server-github"],
    #     env={"GITHUB_PERSONAL_ACCESS_TOKEN": "your_token_here"}
    # ),
    # "browser": MCPServerConfig(
    #     name="browser",
    #     command="npx",
    #     args=["-y", "@anthropic/mcp-server-browser"]
    # ),
}


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str

    LLM_API_KEY: str
    LLM_BASE_URL: str
    MODEL_NAME: str

    class Config:
        env_file = ".env"


settings = Settings()
