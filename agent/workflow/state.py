from typing import Optional, TypedDict


class AgentState(TypedDict, total=False):
    """Workflow 状态。total=False 表示所有字段都是可选的。"""
    message: str
    intent: str
    task_plan: list
    current_task: dict
    completed_tasks: list
    failed_tasks: list
    current_agent: str
    next_agent: str
    resume_path: str
    resume_json: dict
    jd: str
    match_result: dict
    rewrite_plan: dict
    approved: bool
    rewrite_result: str
    interview_questions: list
    filesystem_path: str
    filesystem_result: list
    github_result: dict
    profile: dict
    preferences: dict
    accepted_versions: list
    experiences: list
