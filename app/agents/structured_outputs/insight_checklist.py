from enum import Enum

from pydantic import BaseModel, Field


class QuestionType(str, Enum):
    """질문 유형 분류"""

    ANALYSIS = "분석"
    COMPARISON = "비교"
    PREDICTION = "예측"
    SOLUTION = "해결방안"
    VALIDATION = "검증"


class PriorityLevel(str, Enum):
    """우선순위 레벨"""

    HIGH = "높음"
    MEDIUM = "보통"
    LOW = "낮음"


class InsightQuestion(BaseModel):
    """개별 인사이트 확장 질문"""

    question: str = Field(description="사용자에게 직접 묻는 형태의 질문")
    question_type: QuestionType = Field(description="질문의 유형 분류")
    priority: PriorityLevel = Field(description="질문의 우선순위")
    expected_outcome: str = Field(
        description="예상되는 결과나 얻고자 하는 정보",
    )
    expected_question: str = Field(
        description="사용자에게 직접 묻는 형태의 질문",
    )


class InsightChecklistSchema(BaseModel):
    """인사이트 확장을 위한 질문 체크리스트"""

    topic: str = Field(description="주요 주제나 분석 대상", max_length=100)
    expansion_questions: list[InsightQuestion] = Field(
        description="인사이트 확장을 위한 질문들",
    )
    next_steps: list[str] = Field(description="권장 다음 단계 액션 아이템")
