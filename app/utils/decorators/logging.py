"""함수 실행 로깅 데코레이터 모듈"""

import asyncio
import functools
import logging
import time
from typing import Any, Callable

from app.core.logging import DECORATOR_LOGGER

logger = logging.getLogger(name=DECORATOR_LOGGER)


def log_execution(log_args: bool = True, log_result: bool = False) -> Callable:
    """로그 실행 데코레이터

    Parameters
    ----------
    log_args : bool, optional
        함수 인자 로깅 여부, by default True
    log_result : bool, optional
        함수 결과 로깅 여부, by default False

    Returns
    -------
    Callable
        데코레이터 함수
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(wrapped=func)
        async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
            """비동기 함수 래퍼

            Returns
            -------
            Any
                함수 실행 결과
            """
            func_name = func.__name__

            # 실행 시작 로깅
            if log_args:
                msg = (
                    f"Executing {func_name} with "
                    f"args={args}, kwargs={kwargs}"
                )
            else:
                msg = f"Executing {func_name}"
            logger.debug(msg=msg)

            # 함수 실행 및 시간 측정
            start_time = time.perf_counter()
            try:
                result = await func(*args, **kwargs)
                execution_time = time.perf_counter() - start_time

                # 실행 완료 로깅
                log_msg = f"Completed {func_name} in " f"{execution_time:.4f}s"
                if log_result:
                    log_msg += f" with result={result}"

                logger.debug(log_msg)
                return result

            except Exception as e:
                execution_time = time.perf_counter() - start_time
                msg = f"Failed {func_name} after {execution_time:.4f}s: {e}"
                logger.error(msg=msg)
                raise

        @functools.wraps(wrapped=func)
        def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
            """동기 함수 래퍼

            Returns
            -------
            Any
                함수 실행 결과
            """

            func_name = func.__name__

            # 실행 시작 로깅
            if log_args:
                msg = (
                    f"Executing {func_name} with "
                    f"args={args}, kwargs={kwargs}"
                )
            else:
                msg = f"Executing {func_name}"
            logger.debug(msg=msg)

            # 함수 실행 및 시간 측정
            start_time = time.perf_counter()
            try:
                result = func(*args, **kwargs)
                execution_time = time.perf_counter() - start_time

                # 실행 완료 로깅
                log_msg = f"Completed {func_name} in " f"{execution_time:.4f}s"
                if log_result:
                    log_msg += f" with result={result}"

                logger.debug(msg=log_msg)
                return result

            except Exception as e:
                execution_time = time.perf_counter() - start_time
                msg = f"Failed {func_name} after {execution_time:.4f}s: {e}"
                logger.error(msg=msg)
                raise

        # 함수 타입에 따라 적절한 래퍼 반환
        if asyncio.iscoroutinefunction(func=func):
            return async_wrapper
        return sync_wrapper

    return decorator
