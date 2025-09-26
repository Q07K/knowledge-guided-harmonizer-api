from app.schemas.base_schema import BaseSchema


class InitMessageRequest(BaseSchema):
    sql_query: str
