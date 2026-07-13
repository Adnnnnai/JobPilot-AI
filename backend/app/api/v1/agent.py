import json
import sys
import os

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi.responses import StreamingResponse

from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.match_record import MatchRecord
from app.models.rewrite_record import RewriteRecord
from app.repository.match_repository import MatchRepository
from app.repository.rewrite_repository import RewriteRepository

from app.schemas.agent import WorkflowRequest
from app.schemas.agent import ApprovalRequest

# 将 agent 目录加入 Python 路径
AGENT_DIR = os.path.join(
    os.path.dirname(__file__),
    "..", "..", "..", "..",
    "agent"
)
AGENT_DIR = os.path.abspath(AGENT_DIR)
if AGENT_DIR not in sys.path:
    sys.path.insert(0, AGENT_DIR)

from agent import JobPilotAgent

router = APIRouter(
    prefix="/api/v1/agent",
    tags=["Agent"]
)

agent = JobPilotAgent()


@router.post("/workflow")
def workflow(
    req: WorkflowRequest,
    db: Session = Depends(get_db)
):

    try:
        state = {
            "message": req.message,
            "intent": "",
            "task_plan": [],
            "current_task": {},
            "completed_tasks": [],
            "failed_tasks": [],
            "current_agent": "",
            "next_agent": "",
            "resume_path": req.resume_path,
            "jd": req.jd,
            "resume_id": req.resume_id,
            "resume_json": {},
            "match_result": {},
            "rewrite_plan": {},
            "approved": req.approved,
            "rewrite_result": "",
            "interview_questions": [],
            "filesystem_path": "",
            "filesystem_result": [],
            "github_result": {},
            "profile": {},
            "preferences": {},
            "experiences": [],
        }

        result = agent.invoke(state, thread_id=req.thread_id)

        # 保存 match_result 到 PostgreSQL
        if result.get("match_result"):
            match = MatchRecord(
                user_id=req.user_id,
                resume_id=req.resume_id,
                jd=req.jd,
                match_result=json.dumps(
                    result["match_result"],
                    ensure_ascii=False
                )
            )
            MatchRepository.create(db, match)

        # 保存 rewrite_result 到 PostgreSQL
        if result.get("rewrite_result"):
            rewrite = RewriteRecord(
                user_id=req.user_id,
                resume_id=req.resume_id,
                original_json=json.dumps(
                    result.get("resume_json", {}),
                    ensure_ascii=False
                ),
                rewrite_result=result["rewrite_result"]
            )
            RewriteRepository.create(db, rewrite)

        return {
            "rewrite_result": result.get("rewrite_result", ""),
            "rewrite_plan": result.get("rewrite_plan", {}),
            "interview_questions": result.get("interview_questions", []),
            "task_plan": result.get("task_plan", []),
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@router.post("/workflow/stream")
def workflow_stream(
    req: WorkflowRequest,
    db: Session = Depends(get_db)
):
    """流式执行 workflow，SSE 推送每个节点完成事件"""

    def generate():
        try:
            state = {
                "message": req.message,
                "resume_path": req.resume_path,
                "jd": req.jd,
                "resume_id": req.resume_id,
                "resume_json": {},
                "match_result": {},
                "rewrite_plan": {},
                "approved": req.approved,
                "rewrite_result": "",
            }

            for event in agent.stream(state, thread_id=req.thread_id):
                node_name = list(event.keys())[0]
                node_data = event[node_name]

                sse_data = json.dumps(
                    {"node": node_name, "data": node_data},
                    ensure_ascii=False,
                    default=str
                )
                yield f"data: {sse_data}\n\n"

            yield "data: [DONE]\n\n"

        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)}, ensure_ascii=False)}\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream"
    )


@router.post("/workflow/approve")
def approve_workflow(
    req: ApprovalRequest,
    db: Session = Depends(get_db)
):
    """前端点击"确认修改"后调用，继续执行改写"""

    try:
        state = {
            "message": "",
            "resume_path": "",
            "jd": "",
            "resume_id": req.resume_id,
            "resume_json": {},
            "match_result": {},
            "rewrite_plan": {},
            "approved": True,
            "rewrite_result": "",
        }

        result = agent.invoke(state, thread_id=req.thread_id)

        if result.get("rewrite_result"):
            rewrite = RewriteRecord(
                user_id=req.user_id,
                resume_id=req.resume_id,
                original_json=json.dumps(
                    result.get("resume_json", {}),
                    ensure_ascii=False
                ),
                rewrite_result=result["rewrite_result"]
            )
            RewriteRepository.create(db, rewrite)

        return {
            "rewrite_result": result.get("rewrite_result", ""),
            "approved": True,
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
