from app.core.logging import initialize_loggers
from app.utils.decorators.logging import log_execution


@log_execution(log_args=True, log_result=True)
def main():
    print("Hello from knowledge-guided-harmonizer-api!")


if __name__ == "__main__":
    # 로거 초기화
    initialize_loggers()
    main()
