"""
Supervisor Agent (轻量级)

职责：只负责 Task → Agent 映射，不做业务逻辑。
"""
from executor import TaskExecutor


AGENT_ROUTE_MAP = {
    "resume_agent": "resume_worker",
    "jd_agent": "jd_worker",
    "rewrite_agent": "rewrite_plan",
    "interview_agent": "interview_worker",
    "browser_agent": "browser_search",
    "filesystem_agent": "filesystem",
    "github_agent": "github",
}


class SupervisorAgent:

    name = "supervisor"
    description = "轻量调度器：根据依赖于已完成任务的路由到对应 Worker"

    @classmethod
    def route(cls, state: dict) -> str:
        plan = state.get("task_plan", [])
        completed = state.get("completed_tasks", [])
        failed = state.get("failed_tasks", [])

        if not plan:
            return "END"

        ready = TaskExecutor.get_next_tasks(plan, completed, failed)

        if not ready:
            return "END"

        # 取第一个就绪任务的 agent
        next_task = ready[0]
        state["current_task"] = next_task

        agent = next_task.get("agent", "")
        return AGENT_ROUTE_MAP.get(agent, "END")
