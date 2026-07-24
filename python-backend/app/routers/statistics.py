"""数据统计路由"""

from fastapi import APIRouter, Depends
from databases import Database

from app.database import get_db
from app.schemas import (
    BaseResponse,
    StatisticsQueryRequest,
    DashboardStatsVO,
    LoginUserVO,
)
from app.services.statistics_service import StatisticsService
from app.deps import require_admin

router = APIRouter(prefix="/statistics", tags=["Statistics"])


@router.post("/dashboard", response_model=BaseResponse[DashboardStatsVO])
async def get_dashboard_stats(
    request: StatisticsQueryRequest,
    db: Database = Depends(get_db),
    current_user: LoginUserVO = Depends(require_admin),
):
    """获取仪表盘统计数据（管理员）"""
    service = StatisticsService(db)
    stats = await service.get_dashboard_stats(request)
    return BaseResponse.success(data=stats)
