"""依赖注入"""

import uuid

from fastapi import Cookie, Depends

from app.exceptions import BusinessException, ErrorCode
from app.schemas.user import LoginUserVO
from app.utils.session import get_session


async def get_session_id(
    session_id: str | None = Cookie(None, alias="SESSION"),
) -> str | None:
    """从 Cookie 中获取 Session ID"""
    return session_id


async def get_current_user(
    session_id: str | None = Depends(get_session_id),
) -> LoginUserVO | None:
    """获取当前登录用户（可选）"""
    if not session_id:
        return None

    session_data = await get_session(session_id)
    if not session_data or "user" not in session_data:
        return None

    user_data = session_data["user"]
    return LoginUserVO(**user_data)


async def require_login(
    current_user: LoginUserVO | None = Depends(get_current_user),
) -> LoginUserVO:
    """要求必须登录"""
    if not current_user:
        raise BusinessException(ErrorCode.NOT_LOGIN_ERROR)
    return current_user


async def require_admin(
    current_user: LoginUserVO = Depends(require_login),
) -> LoginUserVO:
    """要求必须是管理员"""
    if current_user.user_role != "admin":
        raise BusinessException(ErrorCode.NO_AUTH_ERROR)
    return current_user


def generate_session_id() -> str:
    """生成 Session ID"""
    return str(uuid.uuid4())
