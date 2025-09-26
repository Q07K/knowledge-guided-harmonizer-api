from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.agents.ontology import OntologyAgent
from app.schemas.base_response import BaseResponse
from app.schemas.message_request import InitMessageRequest
from app.schemas.message_response import InitMessageResponse

router = APIRouter(
    prefix="/init-message",
    tags=["Init Message"],
)


@router.post("")
async def create_init_message(body: InitMessageRequest):
    async def generate():
        print("Received SQL Query:", body.sql_query)
        agent = OntologyAgent()

        # 스트리밍 처리 예시
        chunk: dict
        for chunk in agent.stream(sql_query=body.sql_query):
            node_name = list(chunk.keys())[0]
            node_response = chunk[node_name]
            node_state = node_response.get("node_state", "in_progress")

            response_data = BaseResponse[InitMessageResponse](
                state_code=200,
                message="스트리밍 중...",
                data=InitMessageResponse(
                    name=node_name,
                    state=node_state,
                    message=node_response.get(node_state, ""),
                ),
            )
            yield f"data: {response_data.model_dump_json()}\n\n"

    return StreamingResponse(
        content=generate(), media_type="text/event-stream"
    )
