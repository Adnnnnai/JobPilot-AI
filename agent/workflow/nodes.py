"""
多 Agent 协作 Nodes

简化的任务执行流程：
- Planner:    规则引擎输出 TaskPlan
- Supervisor: 调度路由
- Workers:    执行任务 (resume/jd/rewrite/interview/browser)
"""
import json
import sys
import os
import traceback

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
    try:
        from memory.manager import MemoryManager
        from memory.strategy import MemoryStrategy
        memory_data = MemoryManager.load(1)
        state["profile"] = memory_data.get("profile", {})
        state["preferences"] = memory_data.get("preferences", {})
        state["experiences"] = memory_data.get("experiences", [])
        msg = state.get("message", "")
        if msg and MemoryStrategy.should_save(msg):
            new_prefs = MemoryStrategy.extract_preferences(msg)
            existing_prefs = state.get("preferences", {})
            existing_prefs.update(new_prefs)
            state["preferences"] = existing_prefs
    except Exception as e:
        print(f"[load_memory] Warning: {e}", flush=True)
    state["current_agent"] = "load_memory"
    return state


def save_memory_node(state):
    """Workflow 结束时保存有价值的记忆"""
    try:
        from memory.manager import MemoryManager
        from memory.strategy import MemoryStrategy
        msg = state.get("message", "")
        if msg and MemoryStrategy.should_save(msg):
            MemoryManager.save(state, user_id=1)
    except Exception as e:
        print(f"[save_memory] Warning: {e}", flush=True)
    state["current_agent"] = "save_memory"
    return state


# ── Planner Node ─────────────────────────────

def planner_node(state):
    """基于关键词规则分析用户意图，输出 TaskPlan。"""
    if state.get("task_plan"):
        return state
    if state.get("approved"):
        return state

    msg = state.get("message", "")
    try:
        plan = PlannerAgent.plan(
            msg,
            profile=state.get("profile", {}),
            preferences=state.get("preferences", {}),
        )
        state["task_plan"] = plan.model_dump()["tasks"]
    except Exception as e:
        print(f"[planner] Error: {e}", flush=True)
        # fallback: 至少解析简历
        state["task_plan"] = [{"id": 1, "name": "parse_resume", "description": "解析简历", "depends": [], "agent": "resume_agent"}]

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


# ── Browser Node ─────────────────────────────

def browser_search_node(state):
    """用 LLM 生成 JD 并存储"""
    state["current_agent"] = "browser_search"
    try:
        from tools.browser_tools import BrowserSearchTool
        keyword = state.get("jd", state.get("message", ""))
        tool = BrowserSearchTool()
        result = tool.run(keyword)
        state["jd"] = result

        try:
            from workflow.browser_worker import index_jd_to_knowledge
            state = index_jd_to_knowledge(state)
        except Exception:
            pass
    except Exception as e:
        print(f"[browser_search] Error: {e}", flush=True)
    return state


# ── Worker Nodes ─────────────────────────────

def resume_worker_node(state):
    state["current_agent"] = "resume_agent"
    try:
        if not state.get("resume_json"):
            state = _resume.run(state)
    except Exception as e:
        print(f"[resume_worker] Error: {e}\n{traceback.format_exc()}", flush=True)
    return state


def jd_worker_node(state):
    state["current_agent"] = "jd_agent"
    try:
        state = _jd.run(state)
    except Exception as e:
        print(f"[jd_worker] Error: {e}\n{traceback.format_exc()}", flush=True)
    return state


def rewrite_plan_node(state):
    state["current_agent"] = "rewrite_agent"
    try:
        state = _rewrite.plan(state)
        if not state.get("approved"):
            interrupt({
                "type": "approval",
                "message": "请确认修改计划",
                "plan": state.get("rewrite_plan", {}),
            })
    except Exception as e:
        print(f"[rewrite_plan] Error: {e}\n{traceback.format_exc()}", flush=True)
    return state


def rewrite_execute_node(state):
    state["current_agent"] = "rewrite_agent"
    try:
        state = _rewrite.execute(state)
    except Exception as e:
        print(f"[rewrite_execute] Error: {e}\n{traceback.format_exc()}", flush=True)
    return state


def interview_worker_node(state):
    state["current_agent"] = "interview_agent"
    try:
        state = _interview.run(state)
    except Exception as e:
        print(f"[interview_worker] Error: {e}\n{traceback.format_exc()}", flush=True)
    return state


# ── Filesystem / GitHub ──────────────────────

def filesystem_node(state):
    """Filesystem Worker: 搜索/操作本地文件"""
    state["current_agent"] = "filesystem_agent"
    try:
        from tools.filesystem_tool import FilesystemTool
        from memory.strategy import MemoryStrategy
        tool = FilesystemTool()
        keyword = state.get("message", "")
        path = state.get("filesystem_path", "")
        result = tool.search(keyword, path)
        state["filesystem_result"] = result or []
        if result and MemoryStrategy.should_save(keyword):
            from memory.manager import MemoryManager
            MemoryManager.save(state, user_id=1)
    except Exception as e:
        print(f"[filesystem] Error: {e}", flush=True)
    return state


def github_node(state):
    """GitHub Worker: 搜索开源项目/代码"""
    state["current_agent"] = "github_agent"
    try:
        from tools.github_tool import GitHubTool
        state["github_result"] = GitHubTool.search(state.get("message", ""))
    except Exception as e:
        print(f"[github] Error: {e}", flush=True)
    return state
