from fastapi import Request
from fastapi.responses import JSONResponse

from .errors import (
    ResumeParseError,
    LLMServiceError,
    RAGSearchError,
    MemoryError,
    BrowserError,
    RateLimitError,
)
from .codes import ERROR_MESSAGES, E_RESUME_PARSE, E_LLM_SERVICE, E_RAG_SEARCH, E_MEMORY_ERROR, E_BROWSER_ERROR, E_RATE_LIMIT


_handler_map = {
    ResumeParseError: (E_RESUME_PARSE, 400),
    LLMServiceError: (E_LLM_SERVICE, 502),
    RAGSearchError: (E_RAG_SEARCH, 500),
    MemoryError: (E_MEMORY_ERROR, 500),
    BrowserError: (E_BROWSER_ERROR, 500),
    RateLimitError: (E_RATE_LIMIT, 429),
}


def register_handlers(app):
    for exc_cls, (code, status) in _handler_map.items():
        app.add_exception_handler(exc_cls, _make_handler(code, status))


def _make_handler(code: int, status: int):
    async def handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=status,
            content={
                "code": code,
                "message": ERROR_MESSAGES.get(code, str(exc)),
                "detail": str(exc),
            }
        )
    return handler
