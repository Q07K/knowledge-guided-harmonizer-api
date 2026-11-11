from typing import overload

from langchain_core.messages import BaseMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel

from app.core.config import get_settings

# 구조화 출력 실패 시 재시도 횟수
STRUCTURED_OUTPUT_MAX_ATTEMPTS = 3


class StructuredOutputError(RuntimeError):
    """LLM이 구조화된 출력을 생성하지 못했을 때 발생하는 예외"""


@overload
def generate[T: BaseModel](
    contexts: list[BaseMessage],
    structured_output: type[T],
) -> T: ...


@overload
def generate(
    contexts: list[BaseMessage],
    structured_output: None = None,
) -> BaseMessage: ...


def generate[T: BaseModel](
    contexts: list[BaseMessage],
    structured_output: type[T] | None = None,
) -> BaseMessage | T:
    """LLM 응답을 생성하는 함수

    Returns
    -------
    BaseMessage | T
        LLM 응답 또는 구조화된 출력 객체

    Raises
    ------
    StructuredOutputError
        재시도 후에도 구조화된 출력을 얻지 못한 경우
    """
    settings = get_settings()
    client = ChatGoogleGenerativeAI(
        model=settings.model,
        temperature=settings.temperature,
        max_tokens=settings.max_tokens,
        google_api_key=settings.gemini_api_key,
    )

    if structured_output is None:
        return client.invoke(input=contexts)

    # 기본값인 function calling 방식은 모델이 도구 호출을 생략하면 조용히 None을
    # 반환한다. json_mode 는 응답 스키마를 직접 강제하므로 훨씬 안정적이다.
    structured_client = client.with_structured_output(
        schema=structured_output,
        method="json_mode",
    )

    last_error: Exception | None = None

    for _ in range(STRUCTURED_OUTPUT_MAX_ATTEMPTS):
        try:
            response = structured_client.invoke(input=contexts)
        except Exception as error:  # noqa: BLE001 - 재시도 후 원인과 함께 전달
            last_error = error
            continue

        if response is not None:
            return response

    message = (
        f"{structured_output.__name__} 구조화 출력을 "
        f"{STRUCTURED_OUTPUT_MAX_ATTEMPTS}회 시도했지만 생성하지 못했습니다."
    )
    raise StructuredOutputError(message) from last_error
