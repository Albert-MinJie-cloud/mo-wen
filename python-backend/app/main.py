# FastAPI 主应用入口

import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import settings
from app.database import database
from app.exceptions import BusinessException, ErrorCode
from app.routers import (
    article_router,
    health_router,
    payment_router,
    statistics_router,
    topic_router,
    user_router,
    webhook_router,
)
from app.services.hot_topic_service import HotTopicService
from app.utils.session import close_redis, init_redis


@asynccontextmanager
# 定义应用生命周期管理器
async def lifespan(app: FastAPI):
    # 应用启动时执行的代码
    await database.connect()
    await init_redis()
    print(f"数据库连接成功：{settings.database_url}")
    print(f"Redis连接成功：{settings.redis_url}")

    # 启动热门选题定时刷新任务
    hot_topic_service = HotTopicService()
    scheduler_task = asyncio.create_task(hot_topic_service.start_scheduler())

    # 使用yield分隔启动和关闭逻辑
    yield

    # 应用关闭时执行的代码
    scheduler_task.cancel()
    await database.disconnect()
    await close_redis()
    print("应用已关闭")


# 创建 FastAPI 应用实例
app = FastAPI(
    title="mo-wen",
    description="mo-wen 是一个基于 FastAPI 的后端服务，提供用户管理、健康检查等功能。",
    version="0.0.1",
    lifespan=lifespan,  # 注册生命周期管理器
)

# 配置 CORS 中间件，允许跨域请求
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源
    # 允许前端开发地址
    allow_credentials=True,  # 运行跨域请求带cookies
    allow_methods=["*"],  # 允许所有方法
    allow_headers=["*"],  # 允许所有请求头
)


# 全局异常处理
# 业务异常
@app.exception_handler(BusinessException)
async def business_exception_handler(request: Request, exc: BusinessException):
    """自定义异常处理器"""
    return JSONResponse(
        status_code=200,
        content={"code": exc.error_code.code, "data": None, "message": exc.message},
    )


# 异常
@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    """全局异常处理器"""
    print(f"未处理的异常: {exc}")
    return JSONResponse(
        status_code=200,
        content={
            "code": ErrorCode.SYSTEM_ERROR.code,
            "data": None,
            "message": f"系统内部的异常: {exc!s}",
        },
    )


# 注册路由
app.include_router(user_router, prefix="/api")
app.include_router(health_router, prefix="/api")
app.include_router(article_router, prefix="/api")
app.include_router(payment_router, prefix="/api")
app.include_router(webhook_router, prefix="/api")
app.include_router(statistics_router, prefix="/api")
app.include_router(topic_router, prefix="/api")
