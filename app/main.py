from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import users
from app.database import engine, Base
import os

# 创建数据库表
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="DayDayUp Backend API",
    description="A FastAPI backend with PostgreSQL database",
    version="1.0.0"
)

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应指定具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(users.router, prefix="/api/v1", tags=["users"])

@app.get("/")
def read_root():
    return {"message": "Welcome to DayDayUp Backend API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}