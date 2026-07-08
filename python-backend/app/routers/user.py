from fastapi import APIRouter
from app.schemas.common import BaseResponse

router = APIRouter(prefix="/user", tags=["用户模块"])

@router.get("", response_model=BaseResponse[str])
def user_info():
    """获取用户信息"""
    return BaseResponse.success(data="ok", message="服务运行正常")