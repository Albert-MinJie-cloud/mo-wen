"""数据统计路由"""

from databases import Database
from fastapi import APIRouter, Depends

from app.database import get_db
from app.deps import require_admin
from app.schemas import (
    BaseResponse,
    DashboardStatsVO,
    LoginUserVO,
    StatisticsQueryRequest,
)
from app.services.statistics_service import StatisticsService

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
