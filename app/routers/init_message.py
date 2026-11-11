from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.schemas.base_response import BaseResponse
from app.schemas.message_request import InitMessageRequest
from app.schemas.message_response import InitMessageResponse
from app.services.ontology import STATE_ERROR, stream_ontology_agent

router = APIRouter(
    prefix="/init-message",
    tags=["Init Message"],
)


@router.post("")
async def create_init_message(body: InitMessageRequest) -> StreamingResponse:
    ontology_service = stream_ontology_agent(sql_query=body.sql_query)

    async def generate():
        data: InitMessageResponse
        async for data in ontology_service:
            is_error = data.state == STATE_ERROR

            response_data = BaseResponse[InitMessageResponse](
                state_code=500 if is_error else 200,
                message="분석 중 오류가 발생했습니다." if is_error else "스트리밍 중...",
                data=data,
            )
            yield f"data: {response_data.model_dump_json()}\n\n"

    return StreamingResponse(
        content=generate(),
        media_type="text/event-stream",
    )
