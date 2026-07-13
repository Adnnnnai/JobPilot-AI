from .base_tool import BaseTool


class JDTool(BaseTool):

    name = "jd_match"

    description = "Match Resume And JD"

    def run(self, resume_json, jd):

        prompt = f"""
Resume:

{resume_json}

Job Description:

{jd}

Please calculate matching score.
"""

        return prompt
