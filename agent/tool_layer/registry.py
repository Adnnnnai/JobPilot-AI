"""
Tool Layer → LangChain Tool 转换

把项目中三类工具统一转成 OpenAI function calling 格式：
  - LocalTool  (Resume / JD / Rewrite)
  - RAGTool    (ResumeRAG / JDRAG / InterviewRAG)
  - MCPTool    (Filesystem / GitHub / Browser)
"""


def _to_function_spec(tool) -> dict:
    """单个 Tool 实例 → OpenAI function calling dict"""
    return {
        "type": "function",
        "function": {
            "name": tool.name,
            "description": tool.description,
            "parameters": tool.parameters if hasattr(tool, "parameters") else {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    }


def build_tool_specs(local_tools: list, rag_tools: list, mcp_tools: list) -> list[dict]:
    """
    将三类工具合并成一个统一的 function calling 列表。

    用法:
        specs = build_tool_specs(LOCAL_TOOLS, RAG_TOOLS, MCP_TOOLS)
        llm_with_tools = llm.bind_tools(specs)
    """
    specs = []
    for tool in local_tools + rag_tools + mcp_tools:
        specs.append(_to_function_spec(tool))
    return specs


def dispatch_tool(tool_name: str, kwargs: dict,
                  local_tools: list, rag_tools: list, mcp_tools: list):
    """
    根据工具名分发到正确的工具实例。

    返回: tool.run(**kwargs) 的结果
    """
    all_tools = {t.name: t for t in local_tools + rag_tools + mcp_tools}
    tool = all_tools.get(tool_name)
    if not tool:
        raise ValueError(f"Tool '{tool_name}' not found")
    return tool.run(**kwargs)
