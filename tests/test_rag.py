"""
测试 RAG 知识库: Resume, JD, Interview 三个知识库的索引和搜索
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "agent"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))


def test_resume_kb():
    from app.rag.knowledge.resume_kb import ResumeKB
    ResumeKB.index({"name": "张三", "skills": ["Python", "FastAPI", "LangGraph"], "projects": [{"title": "JobPilot AI"}]}, 9999)
    results = ResumeKB.search("Python", n_results=3)
    assert results["documents"] is not None
    assert len(results["documents"][0]) > 0


def test_jd_kb():
    from app.rag.knowledge.jd_kb import JDKB
    JDKB.index("AI Agent开发工程师，要求Python LangGraph FastAPI经验", "test_jd_1")
    results = JDKB.search("Python LangGraph", n_results=3)
    assert results["documents"] is not None


def test_interview_kb():
    from app.rag.knowledge.interview_kb import InterviewKB
    InterviewKB.index("请介绍LangGraph的checkpoint机制", "Checkpoint是LangGraph的状态持久化机制...", ["LangGraph", "技术"])
    results = InterviewKB.search("LangGraph checkpoint", n_results=3)
    assert results["documents"] is not None


def test_chunk():
    from app.rag.chunk import ResumeChunker
    resume = {"name": "张三", "skills": ["Python", "FastAPI"], "projects": [{"title": "电商平台"}]}
    chunks = ResumeChunker.from_json(resume)
    assert len(chunks) >= 1
    assert "张三" in chunks[0] or "Python" in str(chunks)
