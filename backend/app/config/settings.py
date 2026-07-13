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
        args=["-y", "@modelcontextprotocol/server-filesystem", "D:/JobPilot"]
    ),
}


class Settings(BaseSettings):
    # Database
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "jobpilot"
    DB_USER: str = "postgres"
    DB_PASSWORD: str = ""

    # LLM
    LLM_API_KEY: str = ""
    LLM_BASE_URL: str = "https://api.deepseek.com"
    MODEL_NAME: str = "deepseek-chat"

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # Chroma
    CHROMA_PATH: str = "./chroma_db"

    class Config:
        env_file = ".env"


settings = Settings()
