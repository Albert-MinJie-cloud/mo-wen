from fastapi import APIRouter
from app.schemas.common import BaseResponse

router = APIRouter(prefix="/health", tags=["Health"])

@router.get("", response_model=BaseResponse[str])
def health_check():
    """健康检查接口"""
    return BaseResponse.success(data="ok", message="服务运行正常")