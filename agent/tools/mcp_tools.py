import asyncio
import os
import sys

from mcp_integration.client import mcp_manager


async def mcp_read_file(path: str) -> str:
    """通过 MCP Filesystem Server 读取文件"""
    result = await mcp_manager.call_tool(
        "filesystem",
        "read_file",
        {"path": path}
    )
    content = result.content
    # MCP 返回的是 list[TextContent]
    for item in content:
        if hasattr(item, "text"):
            return item.text
    return ""


async def mcp_list_directory(path: str) -> list:
    """通过 MCP Filesystem Server 列出目录"""
    result = await mcp_manager.call_tool(
        "filesystem",
        "list_directory",
        {"path": path}
    )
    items = []
    for item in result.content:
        if hasattr(item, "text"):
            items.append(item.text)
    return items


def read_file_sync(path: str) -> str:
    """同步封装，供 Tool 使用"""
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # 在已有事件循环中，用 run_until_complete
            future = asyncio.ensure_future(mcp_read_file(path))
            return asyncio.get_event_loop().run_until_complete(future)
        else:
            return asyncio.run(mcp_read_file(path))
    except RuntimeError:
        return asyncio.run(mcp_read_file(path))


def list_directory_sync(path: str) -> list:
    """同步封装，供 Tool 使用"""
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            future = asyncio.ensure_future(mcp_list_directory(path))
            return asyncio.get_event_loop().run_until_complete(future)
        else:
            return asyncio.run(mcp_list_directory(path))
    except RuntimeError:
        return asyncio.run(mcp_list_directory(path))
