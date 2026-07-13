"""
Memory Strategy

决定哪些消息应该保存到长期记忆，哪些不需要。
"""
import re


class MemoryStrategy:

    # 值得保存的关键词模式
    SAVE_PATTERNS = [
        r"(以后|从现在开始|往后|今后).*(要|想|找|做|干|搞|写|用|开发|从事)",
        r"(目标岗位|目标公司|期望薪资|工作地点|工作模式).*",
        r"(不要|排除|避免|讨厌|不喜欢).*(Java|Python|Go|前端|后端|算法|测试|运维)",
        r"(远程|在家|办公室|混合|出差|加班)",
        r"(本科|硕士|博士|专科|毕业|学校|专业).*",
        r"(简历|面试|JD|岗位|职位|offer).*",
        r"(优化|润色|修改|更新|重写).*",
        r"帮我.*(分析|匹配|搜索|查找|推荐).*",
    ]

    # 不值得保存的消息
    SKIP_PATTERNS = [
        r"^(你好|嗨|hello|hi|hey|在吗|谢谢|好的|OK|ok|知道了?|明白了?)[!！。.]*$",
        r"^\s*$",
        r"^(天气|今天|明天|星期|现在几点|几点了).*",
        r"^(测试|test|随便|无所谓|随便说说|试试).*",
    ]

    @classmethod
    def should_save(cls, message: str) -> bool:
        for pattern in cls.SKIP_PATTERNS:
            if re.match(pattern, message, re.IGNORECASE):
                return False
        for pattern in cls.SAVE_PATTERNS:
            if re.search(pattern, message, re.IGNORECASE):
                return True
        return False

    @classmethod
    def extract_preferences(cls, message: str) -> dict:
        """从消息中提取偏好 key-value"""
        prefs = {}

        if "不要" in message or "排除" in message or "避免" in message:
            for skill in ["Java", "Python", "Go", "C++", "前端", "后端", "算法"]:
                if skill in message:
                    prefs["avoid_skill"] = skill
                    break

        if "远程" in message:
            prefs["work_mode"] = "remote"
        elif "办公室" in message:
            prefs["work_mode"] = "onsite"

        if "目标岗位" in message or "想做" in message or "要找" in message:
            match = re.search(r"(?:岗位|做|找|从事|开发)\s*[是为要]?\s*(.+)", message)
            if match:
                prefs["target_job"] = match.group(1).strip().rstrip("。.")

        return prefs
