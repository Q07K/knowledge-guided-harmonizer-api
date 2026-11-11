from typing import Any

from langchain_core.messages import HumanMessage
from langgraph.graph import END, START, StateGraph
from langgraph.graph.state import CompiledStateGraph

from app.agents.llm import generate
from app.agents.prompts import insight_checklist, sql_query_analysis
from app.agents.state import OntologyAgentState
from app.agents.structured_outputs.insight_checklist import (
    InsightChecklistSchema,
)
from app.agents.structured_outputs.ontology_meta_model import OntologyMetaModel
from app.utils.custom_print import node_print


def sql_query_analyze_node(state: OntologyAgentState):
    node_print("SQL Query Analysis Node")

    sql_query = state["sql_query"]

    contexts = [
        HumanMessage(content=sql_query_analysis.BASE_PROMPT),
        HumanMessage(content=sql_query),
    ]
    response = generate(contexts=contexts)

    return {
        "sql_query_analyzed": response.content,
        "node_state": "sql_query_analyzed",
    }


def ontology_schema_generate_node(state: OntologyAgentState):
    node_print("Ontology Schema Generation Node")

    sql_query = state["sql_query"]
    sql_query_analyzed = state["sql_query_analyzed"]

    context = [
        HumanMessage(content=sql_query),
        HumanMessage(content=sql_query_analyzed),
    ]
    response: OntologyMetaModel = generate(
        contexts=context,
        structured_output=OntologyMetaModel,
    )
    return {
        "current_ontology": response.model_dump_json(),
        "node_state": "current_ontology",
    }


def create_check_list_node(state: OntologyAgentState):
    node_print("Create Check List Node")

    sql_query = state["sql_query"]
    sql_query_analyzed = state["sql_query_analyzed"]
    current_ontology = state["current_ontology"]

    sql_query_prompt = "<SQL_QUERY>\n" + sql_query + "\n</SQL_QUERY>"
    sql_analysis_prompt = (
        "<SQL_ANALYSIS>\n" + sql_query_analyzed + "\n</SQL_ANALYSIS>"
    )
    current_ontology_prompt = (
        "<CURRENT_ONTOLOGY>\n" + current_ontology + "\n</CURRENT_ONTOLOGY>"
    )

    contexts = [
        HumanMessage(content=insight_checklist.PROMPT),
        HumanMessage(content=sql_query_prompt),
        HumanMessage(content=sql_analysis_prompt),
        HumanMessage(content=current_ontology_prompt),
    ]
    response: InsightChecklistSchema = generate(
        contexts=contexts,
        structured_output=InsightChecklistSchema,
    )
    return {
        "check_list_items": response,
        "node_state": "check_list_items",
    }


# def check_list_refinement_node(state: OntologyAgentState):
#     pass


# 순차 실행되는 노드 정의 - 그래프 구성과 진행 상황 안내의 단일 기준
NODES: tuple[tuple[str, Any], ...] = (
    ("SQL Table Analysis", sql_query_analyze_node),
    ("Ontology Schema Generation", ontology_schema_generate_node),
    ("Create Check List", create_check_list_node),
)

# 진행 순서대로 나열된 노드 이름
NODE_SEQUENCE: tuple[str, ...] = tuple(name for name, _ in NODES)


def _build_graph(
    state_schema: OntologyAgentState,
) -> CompiledStateGraph[Any, None, Any, Any]:
    # Agent 초기화
    workflow = StateGraph(state_schema=state_schema)

    # 노드 추가
    for node_name, action in NODES:
        workflow.add_node(node=node_name, action=action)

    # 엣지 추가 - START -> 노드들을 순서대로 연결 -> END
    previous_key = START
    for node_name in NODE_SEQUENCE:
        workflow.add_edge(start_key=previous_key, end_key=node_name)
        previous_key = node_name

    workflow.add_edge(start_key=previous_key, end_key=END)

    return workflow.compile()


agent = _build_graph(state_schema=OntologyAgentState)
