from .base_tool import BaseTool
from .mcp_tools import read_file_sync
from .mcp_tools import list_directory_sync


class MCPReadFileTool(BaseTool):

    name = "mcp_read_file"
    description = "通过 MCP Filesystem Server 读取本地文件"

    def run(self, path: str):
        return read_file_sync(path)


class MCPListDirectoryTool(BaseTool):

    name = "mcp_list_directory"
    description = "通过 MCP Filesystem Server 列出目录内容"

    def run(self, path: str):
        return list_directory_sync(path)
