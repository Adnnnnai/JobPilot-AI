"""
Executor: 根据 depends 依赖关系决定任务执行顺序

- 所有依赖已完成的 pending 任务 → 可运行
- 依赖未完成的任务 → 阻塞等待
"""


class TaskExecutor:

    @staticmethod
    def can_run(task: dict, completed_ids: set[int]) -> bool:
        """检查任务的依赖是否全部完成"""
        depends = task.get("depends", [])
        return all(d in completed_ids for d in depends)

    @staticmethod
    def get_next_tasks(task_plan: list, completed_tasks: list, failed_tasks: list) -> list[dict]:
        """获取所有可以立即执行的任务"""
        completed_ids = {t.get("id") for t in completed_tasks}
        failed_ids = {t.get("id") for t in failed_tasks}

        ready = []
        for task in task_plan:
            tid = task.get("id")
            if tid in completed_ids or tid in failed_ids:
                continue
            if TaskExecutor.can_run(task, completed_ids):
                ready.append(task)

        return ready

    @staticmethod
    def is_complete(task_plan: list, completed_tasks: list) -> bool:
        """检查整个计划是否全部完成"""
        plan_ids = {t.get("id") for t in task_plan}
        completed_ids = {t.get("id") for t in completed_tasks}
        return plan_ids == completed_ids
