"""API 요청/응답 로깅 미들웨어"""

import logging
import time
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request as StarletteRequest
from starlette.types import ASGIApp

from .config import MIDDLEWARE_LOGGER
from .context import clear_request_id, set_request_id

logger = logging.getLogger(MIDDLEWARE_LOGGER)


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    HTTP 요청/응답 로깅 미들웨어

    각 요청에 대해 request_id를 생성하고
    요청/응답 정보를 로깅
    """

    def __init__(self, app: ASGIApp):
        super().__init__(app=app)

    async def dispatch(
        self, request: Request, call_next: Callable
    ) -> Response:
        """
        요청 처리 및 로깅

        Args:
            request: HTTP 요청 객체
            call_next: 다음 미들웨어/핸들러

        Returns:
            HTTP 응답 객체
        """
        # request_id 생성 및 설정
        request_id = request.headers.get("X-Request-ID", default=None)
        request_id = set_request_id(request_id=request_id)

        # 요청 정보 로깅
        start_time = time.perf_counter()

        request_body = None
        if request.method in ["POST", "PUT", "PATCH"]:
            try:
                body_bytes = await request.body()
                request_body = body_bytes.decode(encoding="utf-8")
                # Request 객체 재구성 필요

                async def receive():
                    return {"type": "http.request", "body": body_bytes}

                request = StarletteRequest(request.scope, receive)
            except Exception:
                request_body = "Could not read body"
        msg = (
            f"Request started: {request.method} "
            f"{request.url.path} "
            f"query={dict(request.query_params)} "
            f"body={request_body}"
        )
        logger.info(msg=msg)

        # 요청 처리
        response = await call_next(request)

        # 응답 정보 로깅
        process_time = time.perf_counter() - start_time

        # 응답 헤더에 request_id 추가
        response.headers["X-Request-ID"] = request_id
        msg = (
            f"Request completed: {request.method} "
            f"{request.url.path} "
            f"status={response.status_code} "
            f"duration={process_time:.3f}s"
        )
        logger.info(msg=msg)

        # 컨텍스트 정리
        clear_request_id()

        return response


