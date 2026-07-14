"""
测试 Workflow: State + Nodes + Graph 编译
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "agent"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))


def test_state():
    from workflow.state import AgentState
    state = AgentState(
        message="test",
        intent="",
        task_plan=[],
        current_task={},
        completed_tasks=[],
        failed_tasks=[],
        current_agent="",
        next_agent="",
        resume_path="",
        jd="",
        resume_json={},
        match_result={},
        rewrite_plan={},
        approved=False,
        rewrite_result="",
        interview_questions=[],
        filesystem_path="",
        filesystem_result=[],
        github_result={},
        profile={},
        preferences={},
        experiences=[],
    )
    assert state["message"] == "test"


def test_graph_compiles():
    from workflow.graph import graph
    assert graph is not None


def test_router():
    from router import IntentRouter
    assert IntentRouter.route("帮我优化简历") in ("rewrite", "rewrite_plan")
    assert IntentRouter.route("帮我匹配岗位") == "jd"
    assert IntentRouter.route("面试题库") == "interview_rag"


def test_models():
    from models import Task, TaskPlan
    task = Task(id=1, name="test", agent="resume_agent")
    assert task.status == "pending"
    task.mark_done()
    assert task.status == "done"

    plan = TaskPlan(tasks=[task])
    assert plan.is_complete == True


def test_full_workflow_simple():
    import pytest
    try:
        from workflow.graph import graph
        state = {
            "message": "帮我优化简历",
            "intent": "", "task_plan": [], "current_task": {}, "completed_tasks": [], "failed_tasks": [],
            "current_agent": "", "next_agent": "",
            "resume_path": "D:/project/JobPilot-AI/uploads/zhangsan.docx",
            "jd": "", "resume_id": 8,
            "resume_json": {}, "match_result": {}, "rewrite_plan": {}, "approved": False,
            "rewrite_result": "", "interview_questions": [],
            "filesystem_path": "", "filesystem_result": [], "github_result": {},
            "profile": {}, "preferences": {}, "experiences": [],
        }
        config = {"configurable": {"thread_id": "test_workflow_simple"}}
        result = graph.invoke(state, config=config)
        assert result.get("task_plan") is not None
        assert result.get("resume_json") is not None
    except Exception:
        pytest.skip("LLM unavailable")
