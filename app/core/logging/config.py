"""미들웨어와 데코레이터 로거의 설정과 파일 핸들러 관리 모듈"""

import logging
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

from .formatter import get_formatter

# 로그 디렉토리 생성
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

# 로거 이름 상수
MIDDLEWARE_LOGGER = "api.middleware"
DECORATOR_LOGGER = "api.decorator"


def get_daily_log_filename(suffix: str = "") -> str:
    """현재 날짜 기반 로그 파일명 생성

    Parameters
    ----------
    suffix : str, optional
        파일명 접미사, by default ""

    Returns
    -------
    str
        날짜 기반 로그 파일명
    """
    today = datetime.now().strftime("%Y-%m-%d")
    return f"{today}{suffix}.log"


def setup_file_handler(
    filename: str,
    when: str = "midnight",
    interval: int = 1,
    backup_count: int = 30,
) -> TimedRotatingFileHandler:
    """설정된 TimedRotatingFileHandler 반환

    Parameters
    ----------
    filename : str
        로그 파일명
    when : str, optional
        롤링 주기, by default "midnight"
    interval : int, optional
        롤링 간격, by default 1
    backup_count : int, optional
        보관할 백업 파일 수, by default 30

    Returns
    -------
    TimedRotatingFileHandler
        설정된 TimedRotatingFileHandler 인스턴스
    """
    filepath = LOG_DIR / filename
    handler = TimedRotatingFileHandler(
        filename=filepath,
        when=when,
        interval=interval,
        backupCount=backup_count,
        encoding="utf-8",
    )
    # 파일명 포맷 설정 (롤링 시 날짜 형식)
    handler.suffix = "%Y-%m-%d"

    handler.setFormatter(fmt=get_formatter())
    return handler


def setup_middleware_logger() -> logging.Logger:
    """미들웨어 로거 설정

    Returns
    -------
    logging.Logger
        설정된 미들웨어 로거
    """
    logger = logging.getLogger(name=MIDDLEWARE_LOGGER)
    logger.setLevel(level=logging.INFO)
    logger.handlers.clear()

    # 파일 핸들러 추가 (YYYY-MM-DD.log)
    filename = get_daily_log_filename()
    file_handler = setup_file_handler(filename=filename)
    file_handler.setLevel(level=logging.INFO)
    logger.addHandler(hdlr=file_handler)

    logger.propagate = False
    return logger


def setup_decorator_logger() -> logging.Logger:
    """데코레이터 로거 설정

    Returns
    -------
    logging.Logger
        설정된 데코레이터 로거
    """
    logger = logging.getLogger(name=DECORATOR_LOGGER)
    logger.setLevel(level=logging.DEBUG)
    logger.handlers.clear()

    # 파일 핸들러 추가 (YYYY-MM-DD-debug.log)
    filename = get_daily_log_filename(suffix="-debug")
    file_handler = setup_file_handler(filename=filename)
    file_handler.setLevel(level=logging.DEBUG)
    logger.addHandler(hdlr=file_handler)

    logger.propagate = False
    return logger


def initialize_loggers() -> tuple[logging.Logger, logging.Logger]:
    """모든 로거 초기화

    Returns
    -------
    tuple[logging.Logger, logging.Logger]
        초기화된 미들웨어 및 데코레이터 로거 튜플
    """
    middleware_logger = setup_middleware_logger()
    decorator_logger = setup_decorator_logger()
    return middleware_logger, decorator_logger
