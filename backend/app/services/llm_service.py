from openai import OpenAI

from app.core.config import settings

client = OpenAI(
    api_key=settings.LLM_API_KEY,
    base_url=settings.LLM_BASE_URL
)


class LLMService:

    @staticmethod
    def chat(prompt):
        response = client.chat.completions.create(
            model=settings.MODEL_NAME,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        return response.choices[0].message.content

    @staticmethod
    def chat_stream(prompt):
        stream = client.chat.completions.create(
            model=settings.MODEL_NAME,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            stream=True
        )
        for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
