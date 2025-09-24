from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class PropertyType(str, Enum):
    STRING = "string"
    INTEGER = "integer"
    BOOLEAN = "boolean"
    FLOAT = "float"
    DATETIME = "datetime"
    ENUM = "enum"
    REFERENCE = "reference"


class PropertyDefinition(BaseModel):
    """속성 정의"""

    name: str = Field(default=..., description="속성 이름")
    type: PropertyType = Field(default=..., description="속성 데이터 타입")
    description: str = Field(default=..., description="속성 설명")
    required: bool = Field(default=False, description="필수 여부")
    enum_values: list[str] | None = Field(
        default=None, description="ENUM 타입인 경우 가능한 값들"
    )
    reference_entity_type: str | None = Field(
        default=None,
        description="참조 타입인 경우 참조할 엔티티 타입",
    )
    default_value: Any = Field(None, description="기본값")


class EntityType(BaseModel):
    """엔티티 타입 정의"""

    name: str = Field(default=..., description="엔티티 타입 이름 (고유)")
    display_name: str = Field(default=..., description="화면 표시용 이름")
    description: str = Field(default=..., description="엔티티 타입 설명")
    properties: list[PropertyDefinition] = Field(
        default_factory=list, description="이 엔티티 타입이 가질 속성들"
    )
    examples: list[str] = Field(
        default_factory=list, description="이 엔티티 타입의 실제 예시들"
    )


class RelationType(BaseModel):
    """관계 타입 정의"""

    name: str = Field(default=..., description="관계 타입 이름 (고유)")
    display_name: str = Field(default=..., description="화면 표시용 이름")
    description: str = Field(default=..., description="관계 타입 설명")
    source_entity_types: list[str] = Field(
        default_factory=list,
        description="이 관계의 출발점이 될 수 있는 엔티티 타입들",
    )
    target_entity_types: list[str] = Field(
        default_factory=list,
        description="이 관계의 도착점이 될 수 있는 엔티티 타입들",
    )
    properties: list[PropertyDefinition] = Field(
        default_factory=list,
        description="이 관계가 가질 속성들",
    )
    bidirectional: bool = Field(False, description="양방향 관계 여부")
    cardinality: str = Field(
        default="many-to-many",
        description="관계 다중성 (one-to-one, one-to-many, many-to-many)",
    )


class OntologyMetaModel(BaseModel):
    """LLM이 생성할 온톨로지 메타모델"""

    name: str = Field(default=..., description="온톨로지 이름")
    description: str = Field(default=..., description="온톨로지 설명")
    domain: str = Field(
        default=...,
        description="도메인 분야 (예: 이커머스, 금융, 의료)",
    )
    entity_types: list[EntityType] = Field(
        default_factory=list,
        description="도출된 엔티티 타입들",
    )
    relation_types: list[RelationType] = Field(
        default_factory=list,
        description="도출된 관계 타입들",
    )
    key_insights: list[str] = Field(
        default_factory=list,
        description="SQL 분석으로부터 얻은 핵심 인사이트들",
    )
    limitations: list[str] = Field(
        default_factory=list,
        description="현재 메타모델의 한계점들",
    )
    completeness_score: float = Field(
        default=0.3,
        ge=0.0,
        le=1.0,
        description="현재 메타모델의 완성도 (0.0~1.0)",
    )
