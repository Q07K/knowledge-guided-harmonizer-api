from typing import overload

from langchain_core.messages import BaseMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel

from app.core.config import get_settings


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
    str | T
        LLM 응답 또는 구조화된 출력 객체
    """
    settings = get_settings()
    client = ChatGoogleGenerativeAI(
        model=settings.model,
        temperature=settings.temperature,
        max_tokens=settings.max_tokens,
        google_api_key=settings.gemini_api_key,
    )

    if structured_output:
        client = client.with_structured_output(schema=structured_output)

    return client.invoke(input=contexts)
