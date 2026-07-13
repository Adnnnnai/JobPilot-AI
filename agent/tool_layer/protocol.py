"""
统一 Tool 接口

所有 Tool — 无论是本地、RAG 还是 MCP — 都遵循这个协议。
"""
from typing import Protocol, runtime_checkable


@runtime_checkable
class ToolProtocol(Protocol):
    """工具协议：所有工具必须实现 name, description, run()"""

    name: str
    description: str

    def run(self, **kwargs) -> str:
        ...
