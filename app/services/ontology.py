import logging

from app.agents import ontology
from app.agents.state import OntologyAgentState
from app.schemas.message_response import InitMessageResponse

logger = logging.getLogger(__name__)

# 노드 진행 상태
STATE_RUNNING = "running"
STATE_ERROR = "error"


def _progress(name: str) -> tuple[int | None, int]:
    """노드 이름으로 진행 단계(step)와 전체 단계 수를 구한다."""
    total_steps = len(ontology.NODE_SEQUENCE)

    if name not in ontology.NODE_SEQUENCE:
        return None, total_steps

    return ontology.NODE_SEQUENCE.index(name) + 1, total_steps


def _running(name: str) -> InitMessageResponse:
    """해당 노드가 시작되었음을 알리는 응답"""
    step, total_steps = _progress(name)

    return InitMessageResponse(
        name=name,
        state=STATE_RUNNING,
        message=None,
        step=step,
        total_steps=total_steps,
    )


async def stream_ontology_agent(
    sql_query: str,
):
    agent = ontology.agent
    state = OntologyAgentState(
        sql_query=sql_query,
        sql_query_analyzed="",
        current_ontology={},
        check_list_items=[],
        analysis_stage="initial",
    )

    node_sequence = ontology.NODE_SEQUENCE
    total_steps = len(node_sequence)

    # 첫 노드는 결과가 나오기 전부터 실행 중이므로 미리 알린다.
    if node_sequence:
        yield _running(node_sequence[0])

    try:
        for chunk in agent.stream(state):
            node_name = list(chunk.keys())[0]
            node_response = chunk[node_name]
            node_state = node_response.get("node_state", "in_progress")
            step, _ = _progress(node_name)

            # 완료된 노드의 결과
            yield InitMessageResponse(
                name=node_name,
                state=node_state,
                message=node_response.get(node_state, ""),
                step=step,
                total_steps=total_steps,
            )

            # 다음 노드가 있으면 실행 중임을 알린다.
            if step is not None and step < total_steps:
                yield _running(node_sequence[step])

    except Exception as error:  # noqa: BLE001 - 스트림을 끊지 않고 클라이언트에 전달
        logger.exception("온톨로지 에이전트 실행 중 오류가 발생했습니다.")

        yield InitMessageResponse(
            name="Ontology Agent",
            state=STATE_ERROR,
            message=str(error) or "분석 중 알 수 없는 오류가 발생했습니다.",
            step=None,
            total_steps=total_steps,
        )
