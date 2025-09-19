"""모든 로거에서 공통으로 사용할 로그 메시지 포맷 정의 모듈"""

import logging
from datetime import datetime, timezone

from .context import get_request_id


class CustomFormatter(logging.Formatter):
    """
    request_id를 포함한 커스텀 로그 포맷터

    포맷: [timestamp] [level] [request_id] [module] message
    """

    def format(self, record: logging.LogRecord) -> str:
        """로그 레코드 포맷팅

        Parameters
        ----------
        record : logging.LogRecord
            로그 레코드 객체

        Returns
        -------
        str
            포맷된 로그 메시지
        """
        # request_id 추가
        record.request_id = get_request_id() or "no-request"

        # UTC 타임스탬프 사용
        timestamp = datetime.now(timezone.utc).isoformat()
        record.timestamp = timestamp

        # 기본 포맷 적용
        return super().format(record)


def get_formatter() -> CustomFormatter:
    """커스텀 로그 포맷터 반환

    Returns
    -------
    CustomFormatter
        설정된 CustomFormatter 인스턴스
    """
    format_string = (
        "[%(timestamp)s] "
        "[%(levelname)8s] "
        "[%(request_id)s] "
        "[%(name)s.%(funcName)s:%(lineno)d] "
        "%(message)s"
    )
    return CustomFormatter(format_string)
