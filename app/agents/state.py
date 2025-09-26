from typing import TypedDict

from app.agents.structured_outputs.insight_checklist import (
    InsightChecklistSchema,
)


class OntologyAgentState(TypedDict):
    """Ontology Agent 상태를 나타내는 타입"""

    sql_query: str
    sql_query_analyzed: str
    current_ontology: str
    check_list_items: InsightChecklistSchema
    analysis_stage: str  # e.g., "initial", "refined", "completed"
    node_state: str  # 현재 노드 상태를 나타내는 문자열
