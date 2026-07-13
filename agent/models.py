"""
统一任务模型

整个项目所有 Agent 的任务都使用这个格式。
"""
from typing import Optional

from pydantic import BaseModel


class Task(BaseModel):
    id: int
    name: str
    description: str = ""
    depends: list[int] = []
    agent: str
    status: str = "pending"

    def mark_running(self):
        self.status = "running"

    def mark_done(self):
        self.status = "done"

    def mark_failed(self):
        self.status = "failed"

    @property
    def is_ready(self) -> bool:
        """依赖全部完成时才能执行"""
        return self.status == "pending"

    @property
    def is_done(self) -> bool:
        return self.status == "done"


class TaskPlan(BaseModel):
    """Supervisor 输出的任务计划"""
    tasks: list[Task]

    @property
    def pending(self) -> list[Task]:
        return [t for t in self.tasks if t.status == "pending"]

    @property
    def done(self) -> list[Task]:
        return [t for t in self.tasks if t.status == "done"]

    def next_task(self) -> Optional[Task]:
        """获取下一个可执行的任务（依赖已满足）"""
        done_ids = {t.id for t in self.done}
        for t in self.pending:
            if all(d in done_ids for d in t.depends):
                return t
        return None

    @property
    def is_complete(self) -> bool:
        return all(t.status == "done" for t in self.tasks)
