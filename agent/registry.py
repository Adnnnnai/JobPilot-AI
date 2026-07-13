from tools.resume_tool import ResumeTool
from tools.jd_tool import JDTool
from tools.rewrite_tool import RewriteTool
from tools.rewrite_tool import RewritePlanTool
from tools.rewrite_tool import RewriteExecuteTool
from tools.retriever_tool import RetrieverTool
from tools.rag_tools import ResumeRAGTool
from tools.rag_tools import JDRAGTool
from tools.rag_tools import InterviewRAGTool
from tools.mcp_file_tools import MCPReadFileTool
from tools.mcp_file_tools import MCPListDirectoryTool
from tools.external_tools import GitHubTool
from tools.external_tools import BrowserTool

TOOLS = {
    "resume": ResumeTool(),
    "jd": JDTool(),
    "rewrite": RewriteTool(),
    "rewrite_plan": RewritePlanTool(),
    "rewrite_execute": RewriteExecuteTool(),
    "retriever": RetrieverTool(),
    "resume_rag": ResumeRAGTool(),
    "jd_rag": JDRAGTool(),
    "interview_rag": InterviewRAGTool(),
    "mcp_read_file": MCPReadFileTool(),
    "mcp_list_directory": MCPListDirectoryTool(),
    "github": GitHubTool(),
    "browser": BrowserTool(),
}

# LangChain Tool 格式：供 LLM Tool Calling 使用
LANGCHAIN_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "resume_analyze",
            "description": "解析简历文件，提取姓名、技能、项目经历等结构化信息",
            "parameters": {
                "type": "object",
                "properties": {
                    "filepath": {"type": "string", "description": "简历文件路径"}
                },
                "required": ["filepath"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "jd_match",
            "description": "匹配简历与岗位描述，计算匹配度",
            "parameters": {
                "type": "object",
                "properties": {
                    "resume_json": {"type": "object", "description": "结构化简历数据"},
                    "jd": {"type": "string", "description": "岗位描述文本"}
                },
                "required": ["resume_json", "jd"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "resume_rewrite",
            "description": "优化简历内容",
            "parameters": {
                "type": "object",
                "properties": {
                    "resume_json": {"type": "object", "description": "结构化简历数据"},
                    "plan": {"type": "object", "description": "修改计划"}
                },
                "required": ["resume_json"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "resume_rag",
            "description": "搜索简历知识库，回答用户的经历、技能、项目等问题",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "自然语言查询"}
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "jd_rag",
            "description": "搜索岗位知识库，查询岗位要求、技术栈、职责",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "自然语言查询"}
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "interview_rag",
            "description": "搜索面试题库，检索相关面试题和答案",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "自然语言查询"}
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "filesystem_read",
            "description": "通过 MCP 读取本地文件",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "文件路径"}
                },
                "required": ["path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "filesystem_list",
            "description": "通过 MCP 列出目录内容",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "目录路径"}
                },
                "required": ["path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "github_summary",
            "description": "分析 GitHub 仓库结构和技术栈",
            "parameters": {
                "type": "object",
                "properties": {
                    "repo_url": {"type": "string", "description": "GitHub 仓库 URL"}
                },
                "required": ["repo_url"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "browser_search",
            "description": "通过浏览器抓取网页内容",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {"type": "string", "description": "目标网页 URL"}
                },
                "required": ["url"]
            }
        }
    }
]
