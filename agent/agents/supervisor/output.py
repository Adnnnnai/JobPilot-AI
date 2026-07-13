"""
Supervisor 输出格式

统一使用 TaskPlan：
{
    "tasks": [
        {"id":1, "name":"parse_resume",  "description":"解析简历",    "agent":"resume_agent"},
        {"id":2, "name":"analyze_jd",    "description":"分析岗位要求", "agent":"jd_agent"},
        {"id":3, "name":"rewrite",       "description":"优化简历",    "depends":[1,2], "agent":"rewrite_agent"},
        {"id":4, "name":"interview",     "description":"模拟面试",    "depends":[3],   "agent":"interview_agent"}
    ]
}

规则：
- id 从 1 开始递增
- depends 列表中的 id 必须在本计划的 tasks 中存在
- agent 必须是已注册的 Agent name
- 无依赖的任务可以并行执行
"""
