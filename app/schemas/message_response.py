from typing import Any

from app.schemas.base_schema import BaseSchema


class InitMessageResponse(BaseSchema):
    name: str
    state: str
    message: Any
    # 진행 상황 표시용 - 몇 번째 단계인지 / 전체 몇 단계인지
    step: int | None = None
    total_steps: int | None = None
