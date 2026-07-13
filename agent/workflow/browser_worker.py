"""
Browser Worker

LangGraph Node 中在 browser_search 执行后，
将采集到的 JD 存入 ChromaDB JD 知识库。
"""
import json


def index_jd_to_knowledge(state: dict) -> dict:
    """
    把 browser_search 的结果解析后索引到 JD KB。
    由 browser_search_node 调用。
    """
    jd_text = state.get("jd", "")
    if not jd_text or len(jd_text) < 50:
        return state

    try:
        jd = json.loads(jd_text)
    except (json.JSONDecodeError, TypeError):
        return state

    from app.rag.knowledge.jd_kb import JDKB
    jid = str(hash(jd.get("title", "")) % 10**8)
    JDKB.index(jd_text, jid)

    return state
