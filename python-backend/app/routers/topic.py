"""热门选题路由"""

from datetime import datetime

from fastapi import APIRouter

from app.schemas import BaseResponse, HotTopicResponse, HotTopicVO
from app.services.hot_topic_service import HotTopicService

router = APIRouter(prefix="/topic", tags=["Topic"])


@router.get("/hot", response_model=BaseResponse[HotTopicResponse])
async def get_hot_topics():
    """获取当前月份的热门选题（无需登录）"""
    now = datetime.now()
    service = HotTopicService()
    topics = await service.get_hot_topics(now.year, now.month)

    # 将 dict 列表转换为 VO 列表，取最新更新时间
    vos = [HotTopicVO(**t) for t in topics]
    update_time = topics[0]["updateTime"] if topics else now

    return BaseResponse.success(
        data=HotTopicResponse(topics=vos, updateTime=update_time)
    )
