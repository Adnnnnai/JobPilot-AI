import asyncio
import os
import sys

from mcp import StdioServerParameters
from mcp.client.session import ClientSession
from mcp.client.stdio import stdio_client

BACKEND_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "backend")
)
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

from app.core.config import MCP_SERVERS


class MCPManager:

    def __init__(self):
        self._clients = {}

    async def connect_all(self):
        for name, config in MCP_SERVERS.items():
            try:
                params = StdioServerParameters(
                    command=config.command,
                    args=config.args,
                    env=config.env or None
                )
                read, write = await stdio_client(params)
                session = ClientSession(read, write)
                await session.initialize()
                self._clients[name] = session
                print(f"[MCP] {name} connected")
            except Exception as e:
                print(f"[MCP] {name} failed: {e}")

    def get_client(self, name: str):
        client = self._clients.get(name)
        if not client:
            raise ValueError(f"MCP server '{name}' not connected")
        return client

    async def list_tools(self, server_name: str):
        client = self.get_client(server_name)
        result = await client.list_tools()
        return [{"name": t.name, "description": t.description, "inputSchema": t.inputSchema} for t in result.tools]

    async def call_tool(self, server_name: str, tool_name: str, arguments: dict):
        client = self.get_client(server_name)
        return await client.call_tool(tool_name, arguments=arguments)

    async def close_all(self):
        for name, client in list(self._clients.items()):
            try:
                await client.aclose()
            except Exception:
                pass
        self._clients.clear()

    def is_connected(self, server_name: str) -> bool:
        return server_name in self._clients


# 全局单例
mcp_manager = MCPManager()
