from typing import Optional, TypedDict


class AgentState(TypedDict):

    message: str

    intent: str

    # 任务计划（Planner 输出）
    task_plan: list

    # 当前任务 & 历史
    current_task: dict
    completed_tasks: list
    failed_tasks: list

    # 当前执行的 Agent 和下一个 Agent
    current_agent: str
    next_agent: str

    # 简历相关
    resume_path: str
    resume_json: dict

    # JD 相关
    jd: str
    match_result: dict

    # 改写相关
    rewrite_plan: dict
    approved: bool
    rewrite_result: str

    # 面试相关
    interview_questions: list

    # MCP 相关
    filesystem_path: str
    filesystem_result: list
    github_result: dict

    # 四层记忆
    profile: dict
    preferences: dict
    accepted_versions: list
