"""
多 Agent 协作 Nodes

START → Planner → Supervisor → Worker → task_complete → next_task → END

职责链：
- Planner:   LLM 理解用户意图 → 输出 TaskPlan(tasks 列表)
- Supervisor: 读取 task_plan → 按依赖顺序路由到对应 Worker
- Worker:     执行具体任务（resume/jd/rewrite/interview/filesystem/github）
"""
import json
import sys
import os

from langgraph.types import interrupt

BACKEND_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "backend")
)
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

from agents.planner.agent import PlannerAgent
from agents.supervisor.agent import SupervisorAgent
from agents.resume.agent import ResumeAgent
from agents.jd.agent import JDAgent
from agents.rewrite.agent import RewriteAgent
from agents.interview.agent import InterviewAgent

_resume = ResumeAgent()
_jd = JDAgent()
_rewrite = RewriteAgent()
_interview = InterviewAgent()


# ── Memory Nodes ──────────────────────────────

def load_memory_node(state):
    """Workflow 开始时加载长期记忆"""
    from memory.manager import MemoryManager
    from memory.strategy import MemoryStrategy

    memory = MemoryManager.load(1)
    state["profile"] = memory["profile"]
    state["preferences"] = memory["preferences"]
    state["experiences"] = memory["experiences"]

    # 从消息中提取即时偏好
    msg = state.get("message", "")
    if msg and MemoryStrategy.should_save(msg):
        new_prefs = MemoryStrategy.extract_preferences(msg)
        existing_prefs = state.get("preferences", {})
        existing_prefs.update(new_prefs)
        state["preferences"] = existing_prefs

    return state


def save_memory_node(state):
    """Workflow 结束时保存有价值的记忆"""
    from memory.manager import MemoryManager
    from memory.strategy import MemoryStrategy

    msg = state.get("message", "")
    if msg and MemoryStrategy.should_save(msg):
        MemoryManager.save(state, user_id=1)

    state["current_agent"] = "save_memory"
    return state


# ── Planner Node ─────────────────────────────

def planner_node(state):
    """LLM 分析用户意图，输出 TaskPlan。注入用户画像和偏好。"""
    if state.get("task_plan"):
        return state

    if state.get("approved"):
        return state

    planner = PlannerAgent()

    # 异常恢复：如果有失败任务，重新规划
    failed = state.get("failed_tasks", [])
    if failed:
        failed_names = [t.get("name", "unknown") for t in failed]
        retry_message = f"之前以下任务失败了：{failed_names}。请重新规划。原始消息：{state.get('message', '')}"
        plan = PlannerAgent.plan(
            retry_message,
            profile=state.get("profile", {}),
            preferences=state.get("preferences", {}),
        )
        state["task_plan"] = plan.model_dump()["tasks"]
        state["failed_tasks"] = []
        state["current_agent"] = "planner"
        return state

    plan = PlannerAgent.plan(
        state.get("message", ""),
        profile=state.get("profile", {}),
        preferences=state.get("preferences", {}),
    )
    state["task_plan"] = plan.model_dump()["tasks"]
    state["current_agent"] = "planner"

    return state


# ── Supervisor Node ──────────────────────────

def supervisor_node(state):
    """读取 task_plan，按依赖顺序路由到对应 Worker"""
    supervisor = SupervisorAgent()
    route = supervisor.route(state)
    state["next_agent"] = route
    state["current_agent"] = "supervisor"
    return state


def route_from_supervisor(state):
    """供 graph 条件路由使用，返回字符串而非 state dict"""
    supervisor = SupervisorAgent()
    return supervisor.route(state)


# ── Worker Nodes ─────────────────────────────

def resume_worker_node(state):
    state["current_agent"] = "resume_agent"
    # 如果 task_plan 中有 parse_resume 且未被跳过，执行解析
    if not state.get("resume_json"):
        state = _resume.run(state)
    return state


def jd_worker_node(state):
    state["current_agent"] = "jd_agent"
    state = _jd.run(state)
    return state


def rewrite_plan_node(state):
    state["current_agent"] = "rewrite_agent"
    state = _rewrite.plan(state)

    if not state.get("approved"):
        interrupt({
            "type": "approval",
            "message": "请确认修改计划",
            "plan": state.get("rewrite_plan", {}),
        })

    return state


def rewrite_execute_node(state):
    state["current_agent"] = "rewrite_agent"
    state = _rewrite.execute(state)
    return state


def interview_worker_node(state):
    state["current_agent"] = "interview_agent"
    state = _interview.run(state)
    return state


# ── MCP Nodes ────────────────────────────────

def filesystem_node(state):
    from tools.mcp_tools import read_file_sync, list_directory_sync

    path = state.get("filesystem_path", "")
    if not path:
        state["filesystem_result"] = []
        return state

    try:
        entries = list_directory_sync(path)
        state["filesystem_result"] = entries
    except Exception as e:
        state["filesystem_result"] = [f"[MCP Error] {e}"]

    return state


def github_node(state):
    state["github_result"] = {"status": "github mcp not yet configured"}
    return state
