"""API 요청 전체에서 request_id를 추적하기 위한 컨텍스트 변수 관리 모듈"""

from contextvars import ContextVar
from uuid import uuid4

request_id_var: ContextVar[str | None] = ContextVar("request_id", default=None)


def get_request_id() -> str | None:
    """현재 컨텍스트의 request_id 반환

    Returns
    -------
    str | None
        현재 컨텍스트의 request_id 또는 None
    """
    return request_id_var.get()


def set_request_id(request_id: str | None = None) -> str:
    """request_id 설정, 없으면 생성

    Parameters
    ----------
    request_id : str | None, optional
        request_id, by default None

    Returns
    -------
    str
        현재 컨텍스트의 request_id
    """
    rid = request_id or str(object=uuid4())
    request_id_var.set(rid)
    return rid


def clear_request_id() -> None:
    """request_id 컨텍스트 초기화

    Returns
    -------
    None
    """
    request_id_var.set(None)
