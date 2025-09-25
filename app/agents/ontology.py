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


class OntologyAgent:
    """Ontology Agent 클래스"""

    def __init__(self) -> None:
        self.agent = self._build_graph(state_schema=OntologyAgentState)

    def _build_graph(
        self,
        state_schema: OntologyAgentState,
    ) -> CompiledStateGraph[Any, None, Any, Any]:
        # Agent 초기화
        workflow = StateGraph(state_schema=state_schema)

        # 노드 추가
        workflow.add_node(
            node="SQL Table Analysis",
            action=self.sql_query_analyze_node,
        )
        workflow.add_node(
            node="Ontology Schema Generation",
            action=self.ontology_schema_generate_node,
        )
        workflow.add_node(
            node="Create Check List",
            action=self.create_check_list_node,
        )

        # 엣지 추가
        workflow.add_edge(
            start_key=START,
            end_key="SQL Table Analysis",
        )
        workflow.add_edge(
            start_key="SQL Table Analysis",
            end_key="Ontology Schema Generation",
        )
        workflow.add_edge(
            start_key="Ontology Schema Generation",
            end_key="Create Check List",
        )
        workflow.add_edge(
            start_key="Create Check List",
            end_key=END,
        )

        return workflow.compile()

    def invoke(
        self,
        sql_query: str,
    ) -> OntologyAgentState:
        """Ontology Agent의 응답을 생성하는 메서드

        Parameters
        ----------
        initial_state : OntologyAgentState
            초기 상태

        Returns
        -------
        OntologyAgentState
            최종 상태
        """

        state = OntologyAgentState(
            sql_query=sql_query,
            sql_query_analyzed="",
            current_ontology={},
            check_list_items=[],
            analysis_stage="initial",
        )

        return self.agent.invoke(state)

    def sql_query_analyze_node(self, state: OntologyAgentState):
        sql_query = state["sql_query"]

        contexts = [
            HumanMessage(content=sql_query_analysis.BASE_PROMPT),
            HumanMessage(content=sql_query),
        ]
        response = generate(contexts=contexts)

        return {"sql_query_analyzed": response.content}

    def ontology_schema_generate_node(self, state: OntologyAgentState):
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
        return {"current_ontology": response.model_dump_json()}

    def create_check_list_node(self, state: OntologyAgentState):
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
            HumanMessage(content=insight_checklist.BASE_PROMPT),
            HumanMessage(content=sql_query_prompt),
            HumanMessage(content=sql_analysis_prompt),
            HumanMessage(content=current_ontology_prompt),
        ]
        response: InsightChecklistSchema = generate(
            contexts=contexts,
            structured_output=InsightChecklistSchema,
        )
        return {"check_list_items": response}

    # def check_list_refinement_node(self, state: OntologyAgentState):
    #     pass
