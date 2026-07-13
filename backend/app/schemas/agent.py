from pydantic import BaseModel


class ChatRequest(BaseModel):
    message: str
    resume_id: int


class WorkflowRequest(BaseModel):
    message: str = ""
    resume_path: str
    jd: str = ""
    thread_id: str = "default"
    user_id: int = 1
    resume_id: int = 1
    approved: bool = False


class ApprovalRequest(BaseModel):
    thread_id: str
    resume_id: int = 1
    user_id: int = 1

