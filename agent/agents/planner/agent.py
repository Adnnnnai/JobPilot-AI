"""
Planner Agent - 纯规则引擎

不再依赖 LLM 生成 TaskPlan，改用关键词匹配规则。
"""
import json
from models import TaskPlan, Task


class PlannerAgent:

    name = "planner"
    description = "任务规划专家：将用户目标拆解为结构化 TaskPlan"

    @classmethod
    def plan(cls, message: str, profile: dict = None, preferences: dict = None) -> TaskPlan:
        """基于关键词规则生成 TaskPlan，保证 depends 引用始终合法。"""
        msg = message.lower()

        has_browser = any(kw in msg for kw in ["搜索", "找", "搜", "查", "浏览", "招聘", "岗位", "jd", "工作"])
        has_match = any(kw in msg for kw in ["匹配", "对比", "分析", "比较"])
        has_rewrite = any(kw in msg for kw in ["优化", "改写", "润色", "修改简历", "改简历"])
        has_interview = any(kw in msg for kw in ["面试", "面试题", "模拟面试"])

        tasks = []
        next_id = 1

        # 1. browser → 采集JD
        browser_id = None
        if has_browser:
            browser_id = next_id
            tasks.append(Task(id=next_id, name="browser_search", description="搜索岗位JD", depends=[], agent="browser_agent"))
            next_id += 1

        # 2. resume → 解析简历（始终需要）
        resume_id = next_id
        tasks.append(Task(id=next_id, name="parse_resume", description="解析简历", depends=[], agent="resume_agent"))
        next_id += 1

        # 3. jd → 匹配分析
        jd_id = None
        if has_match or has_browser:
            jd_id = next_id
            jd_deps = [browser_id] if browser_id else []
            tasks.append(Task(id=next_id, name="analyze_jd", description="分析岗位并匹配", depends=jd_deps, agent="jd_agent"))
            next_id += 1

        # 4. rewrite → 优化简历
        if has_rewrite:
            deps = [resume_id]
            if jd_id:
                deps.append(jd_id)
            tasks.append(Task(id=next_id, name="rewrite", description="优化简历", depends=deps, agent="rewrite_agent"))
            next_id += 1

        # 5. interview → 面试题
        if has_interview:
            deps = [next_id - 1] if next_id > 1 else []
            tasks.append(Task(id=next_id, name="interview", description="生成面试题", depends=deps, agent="interview_agent"))
            next_id += 1

        # fallback：仅解析简历
        if not tasks:
            tasks.append(Task(id=1, name="parse_resume", description="解析简历", depends=[], agent="resume_agent"))

        return TaskPlan(tasks=tasks)
