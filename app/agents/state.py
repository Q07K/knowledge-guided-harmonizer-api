from typing import TypedDict


class OntologyAgentState(TypedDict):
    """Ontology Agent 상태를 나타내는 타입"""

    sql_query: str
    sql_query_analyzed: str
    current_ontology: str
    check_list_items: list
    analysis_stage: str  # e.g., "initial", "refined", "completed"
