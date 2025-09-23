from functools import cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # LLM 설정
    model: str = "gemini-2.5-flash"
    temperature: float = 0.55
    max_tokens: int | None = None

    # Gemini API KEY
    gemini_api_key: str

    # Settings Config
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


@cache
def get_settings() -> Settings:
    """Settings 객체를 반환하는 함수

    Returns
    -------
    Settings
        설정 객체
    """
    return Settings()
