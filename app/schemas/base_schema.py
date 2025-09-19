from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class BaseSchema(BaseModel):
    """모든 DTO(Schemas)의 기본이 되는 클래스입니다."""

    model_config = ConfigDict(
        populate_by_name=True,
        alias_generator=to_camel,
    )
