class IntentRouter:

    @staticmethod
    def route(message):

        msg = message.lower()

        if "润色" in msg or "优化" in msg:
            return "rewrite"

        if "岗位" in msg or "匹配" in msg:
            return "jd"

        if "面试" in msg or "题库" in msg:
            return "interview_rag"

        if "github" in msg or "仓库" in msg or "代码" in msg:
            return "github"

        if "文件" in msg or "目录" in msg or "项目结构" in msg:
            return "filesystem"

        if "解析" in msg or "分析" in msg:
            return "resume"

        if "简历" in msg or "经历" in msg or "技能" in msg or "项目" in msg or "经验" in msg:
            return "resume_rag"

        if "岗位" in msg and ("要求" in msg or "技术栈" in msg or "职责" in msg):
            return "jd_rag"

        return "resume"
