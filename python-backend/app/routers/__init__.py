"""API 路由"""

from app.routers.article import router as article_router
from app.routers.health import router as health_router
from app.routers.payment import payment_router, webhook_router
from app.routers.statistics import router as statistics_router
from app.routers.topic import router as topic_router
from app.routers.user import router as user_router

__all__ = [
    "article_router",
    "health_router",
    "payment_router",
    "statistics_router",
    "topic_router",
    "user_router",
    "webhook_router",
]
