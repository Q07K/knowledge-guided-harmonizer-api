from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import init_message

# FastAPI 인스턴스 생성
app = FastAPI()


app.add_middleware(
    middleware_class=CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "*",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(router=init_message.router)
