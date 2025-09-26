from typing import Any

from app.schemas.base_schema import BaseSchema


class InitMessageResponse(BaseSchema):
    name: str
    state: str
    message: Any
