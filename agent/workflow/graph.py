"""
多 Agent 协作 Workflow

START → Planner → Supervisor → Workers → task_complete → END

Supervisor+Worker 模式：
- Planner:    LLM 输出 TaskPlan
- Supervisor: 轻量调度，根据 Executor 的依赖检查路由
- Workers:    执行具体任务
"""
from langgraph.graph import StateGraph
from langgraph.graph import START
from langgraph.graph import END

from memory.checkpointer import memory

from workflow.state import AgentState
from workflow.nodes import (
    load_memory_node,
    save_memory_node,
    planner_node,
    supervisor_node,
    resume_worker_node,
    jd_worker_node,
    rewrite_plan_node,
    rewrite_execute_node,
    interview_worker_node,
    browser_search_node,
    filesystem_node,
    github_node
)
from agents.supervisor.agent import SupervisorAgent


def task_router(state):
    return supervisor_node(state)


def task_complete(state):
    current = state.get("current_task", {})
    if current:
        # 检查是否失败
        if current.get("status") == "failed":
            failed = list(state.get("failed_tasks", []))
            failed.append(current)
            state["failed_tasks"] = failed
            plan = list(state.get("task_plan", []))
            plan = [t for t in plan if t.get("id") != current.get("id")]
            state["task_plan"] = plan
        else:
            completed = list(state.get("completed_tasks", []))
            current["status"] = "done"
            completed.append(current)
            state["completed_tasks"] = completed
            plan = list(state.get("task_plan", []))
            plan = [t for t in plan if t.get("id") != current.get("id")]
            state["task_plan"] = plan
    state["current_task"] = {}
    return state


def next_task(state):
    if state.get("failed_tasks"):
        return "planner"

    if state.get("task_plan"):
        return "task_router"

    # 所有任务完成 → 保存记忆
    return "save_memory"


def route_after_plan(state):
    if state.get("approved"):
        return "rewrite_execute"
    return "task_complete"


def route_after_task_complete(state):
    result = next_task(state)
    if result == "save_memory":
        return "save_memory"
    if result == "planner":
        return "planner"
    if result == END:
        return END
    return "task_router"


builder = StateGraph(AgentState)

builder.add_node("load_memory", load_memory_node)
builder.add_node("planner", planner_node)
builder.add_node("supervisor", supervisor_node)
builder.add_node("task_router", task_router)
builder.add_node("task_complete", task_complete)
builder.add_node("save_memory", save_memory_node)

builder.add_node("resume_worker", resume_worker_node)
builder.add_node("jd_worker", jd_worker_node)
builder.add_node("rewrite_plan", rewrite_plan_node)
builder.add_node("rewrite_execute", rewrite_execute_node)
builder.add_node("interview_worker", interview_worker_node)
builder.add_node("browser_search", browser_search_node)
builder.add_node("filesystem", filesystem_node)
builder.add_node("github", github_node)

def route_from_supervisor(state):
    return SupervisorAgent.route(state)


def route_from_task_router(state):
    return SupervisorAgent.route(state)


# 主流程
# 主流程: START → load_memory → planner → supervisor → ... → save_memory → END
builder.add_edge(START, "load_memory")
builder.add_edge("load_memory", "planner")
builder.add_edge("planner", "supervisor")

builder.add_conditional_edges("supervisor", route_from_supervisor, {
    "resume_worker": "resume_worker", "jd_worker": "jd_worker",
    "rewrite_plan": "rewrite_plan", "interview_worker": "interview_worker",
    "browser_search": "browser_search",
    "filesystem": "filesystem", "github": "github",
    "END": END,
})

for w in ["resume_worker", "jd_worker", "interview_worker", "browser_search", "filesystem", "github"]:
    builder.add_edge(w, "task_complete")

builder.add_conditional_edges("rewrite_plan", route_after_plan, {
    "rewrite_execute": "rewrite_execute", "task_complete": "task_complete",
})
builder.add_edge("rewrite_execute", "task_complete")

builder.add_conditional_edges("task_complete", route_after_task_complete, {
    "task_router": "task_router", "planner": "planner", "save_memory": "save_memory",
    "END": END,
})

builder.add_conditional_edges("task_router", route_from_task_router, {
    "resume_worker": "resume_worker", "jd_worker": "jd_worker",
    "rewrite_plan": "rewrite_plan", "interview_worker": "interview_worker",
    "browser_search": "browser_search",
    "filesystem": "filesystem", "github": "github",
    "END": END,
})

graph = builder.compile(checkpointer=memory)
