"""
三类工具定义：Local / RAG / MCP
"""
from tools.resume_tool import ResumeTool
from tools.jd_tool import JDTool
from tools.rewrite_tool import RewriteTool, RewritePlanTool, RewriteExecuteTool

from tools.rag_tools import ResumeRAGTool, JDRAGTool, InterviewRAGTool

from tools.mcp_file_tools import MCPReadFileTool, MCPListDirectoryTool
from tools.external_tools import GitHubTool, BrowserTool


# ── Local Tools ────────────────────────────
LOCAL_TOOLS = [
    ResumeTool(),
    JDTool(),
    RewriteTool(),
    RewritePlanTool(),
    RewriteExecuteTool(),
]

# ── RAG Tools ──────────────────────────────
RAG_TOOLS = [
    ResumeRAGTool(),
    JDRAGTool(),
    InterviewRAGTool(),
]

# ── MCP Tools ──────────────────────────────
MCP_TOOLS = [
    MCPReadFileTool(),
    MCPListDirectoryTool(),
    GitHubTool(),
    BrowserTool(),
]

# ── 统一列表 ────────────────────────────────
ALL_TOOLS = LOCAL_TOOLS + RAG_TOOLS + MCP_TOOLS
