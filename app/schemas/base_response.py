from pydantic import BaseModel

from app.schemas.base_schema import BaseSchema


class BaseResponse[T: BaseModel](BaseSchema):
    """모든 Response DTO(Schemas)의 기본이 되는 클래스입니다."""

    state_code: int
    message: str
    data: T | None = None
