"""
Agent API v1 - 简化版

直接在当前进程内执行操作，不使用 LangGraph workflow，
避免 checkpoint/Playwright 等线程问题。
"""
import json
import sys
import os
import traceback

from fastapi import APIRouter
from fastapi import HTTPException

from app.schemas.agent import WorkflowRequest, ApprovalRequest

# Add agent dir to path
AGENT_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "agent")
AGENT_DIR = os.path.abspath(AGENT_DIR)
if AGENT_DIR not in sys.path:
    sys.path.insert(0, AGENT_DIR)

router = APIRouter(prefix="/api/v1/agent", tags=["Agent"])


def _run_workflow_simple(state: dict) -> dict:
    """Simplified workflow: plan → execute each task directly."""
    from agents.planner.agent import PlannerAgent
    from agents.resume.agent import ResumeAgent
    from agents.jd.agent import JDAgent
    from agents.rewrite.agent import RewriteAgent
    from agents.interview.agent import InterviewAgent

    msg = state.get("message", "")
    profile = state.get("profile", {})
    preferences = state.get("preferences", {})

    # 1. Plan
    plan = PlannerAgent.plan(msg, profile=profile, preferences=preferences)
    task_plan = plan.model_dump()["tasks"]
    state["task_plan"] = task_plan

    # 2. Execute tasks in order (respecting depends)
    task_map = {t["id"]: t for t in task_plan}
    completed = set()
    resume = ResumeAgent()
    jd_agent = JDAgent()
    rewrite = RewriteAgent()
    interview = InterviewAgent()

    for task in task_plan:
        # Check dependencies
        deps = task.get("depends", [])
        if not all(d in completed for d in deps):
            continue  # skip if deps not met

        agent = task.get("agent", "")
        try:
            if agent == "resume_agent":
                state = resume.run(state)
            elif agent == "jd_agent":
                state = jd_agent.run(state)
            elif agent == "rewrite_agent":
                state = rewrite.plan(state)
                # auto-execute if not approved
                if not state.get("approved"):
                    state = rewrite.execute(state)
            elif agent == "interview_agent":
                state = interview.run(state)
            elif agent == "browser_agent":
                from tools.browser_tools import BrowserSearchTool
                tool = BrowserSearchTool()
                keyword = state.get("jd", msg)
                result = tool.run(keyword)
                state["jd"] = result
            completed.add(task["id"])
        except Exception as e:
            print(f"[worker:{agent}] Error: {e}\n{traceback.format_exc()}", flush=True)

    state["task_plan"] = task_plan
    return state


@router.post("/workflow")
def workflow(req: WorkflowRequest):
    try:
        state = {
            "message": req.message,
            "intent": "",
            "task_plan": [],
            "current_task": {},
            "completed_tasks": [],
            "failed_tasks": [],
            "current_agent": "",
            "next_agent": "",
            "resume_path": req.resume_path,
            "jd": req.jd,
            "resume_id": req.resume_id,
            "resume_json": {},
            "match_result": {},
            "rewrite_plan": {},
            "approved": req.approved,
            "rewrite_result": "",
            "interview_questions": [],
            "filesystem_path": "",
            "filesystem_result": [],
            "github_result": {},
            "profile": {},
            "preferences": {},
            "experiences": [],
        }

        result = _run_workflow_simple(state)

        return {
            "rewrite_result": result.get("rewrite_result", ""),
            "rewrite_plan": result.get("rewrite_plan", {}),
            "interview_questions": result.get("interview_questions", []),
            "task_plan": result.get("task_plan", []),
            "match_result": result.get("match_result", {}),
            "resume_json": result.get("resume_json", {}),
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}\n{traceback.format_exc()}")


@router.post("/workflow/approve")
def approve_workflow(req: ApprovalRequest):
    try:
        state = {
            "message": "",
            "intent": "",
            "task_plan": [],
            "current_task": {},
            "completed_tasks": [],
            "failed_tasks": [],
            "current_agent": "",
            "next_agent": "",
            "resume_path": "",
            "jd": "",
            "resume_id": req.resume_id,
            "resume_json": {},
            "match_result": {},
            "rewrite_plan": {},
            "approved": True,
            "rewrite_result": "",
            "interview_questions": [],
            "filesystem_path": "",
            "filesystem_result": [],
            "github_result": {},
            "profile": {},
            "preferences": {},
            "experiences": [],
        }

        result = _run_workflow_simple(state)

        return {
            "rewrite_result": result.get("rewrite_result", ""),
            "approved": True,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
