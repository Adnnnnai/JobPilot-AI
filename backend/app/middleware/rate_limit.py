"""Rate Limit Middleware"""
import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from app.exceptions.errors import RateLimitError


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, max_requests: int = 30, window_sec: int = 60):
        super().__init__(app)
        self.max_requests = max_requests
        self.window_sec = window_sec
        self._clients = {}

    async def dispatch(self, request: Request, call_next):
        client = request.client.host if request.client else "unknown"
        now = time.time()
        records = self._clients.get(client, [])
        records = [t for t in records if now - t < self.window_sec]
        if len(records) >= self.max_requests:
            raise RateLimitError()
        records.append(now)
        self._clients[client] = records
        return await call_next(request)
