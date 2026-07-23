# 创建SQLAlchemy orm模型
from datetime import datetime
from sqlalchemy import Column, BigInteger, String, DateTime, SmallInteger, Text
from sqlalchemy.sql import func

from app.database import Base


class User(Base):
    """用户表"""

    __tablename__ = "user"

    id = Column(BigInteger, primary_key=True, autoincrement=True, comment="id")
    user_account = Column(
        "userAccount", String(256), nullable=False, unique=True, comment="用户账号"
    )
    user_password = Column(
        "userPassword", String(512), nullable=False, comment="用户密码"
    )
    user_name = Column("userName", String(256), nullable=True, comment="用户昵称")

    user_avatar = Column("userAvatar", String(1024), nullable=True, comment="用户头像")

    user_profile = Column("userProfile", String(512), nullable=True, comment="用户简介")

    user_role = Column(
        "userRole",
        String(256),
        nullable=False,
        default="user",
        comment="用户角色，user普通用户，admin管理员",
    )

    edit_time = Column(
        "editTime",
        DateTime,
        nullable=False,
        default=func.now(),
        comment="编辑时间",
    )

    create_time = Column(
        "createTime",
        DateTime,
        nullable=False,
        default=func.now(),
        comment="创建时间",
    )

    update_time = Column(
        "updateTime",
        DateTime,
        nullable=False,
        default=func.now(),
        comment="更新时间",
    )

    is_delete = Column(
        "isDelete",
        SmallInteger,
        nullable=False,
        default=0,
        comment="是否删除，0未删除，1已删除",
    )

    quota = Column("quota", SmallInteger, nullable=False, default=5, comment="用户额度")

    vip_time = Column("vipTime", DateTime, nullable=True, comment="成为会员时间")
    vip_expire_time = Column(
        "vipExpireTime", DateTime, nullable=True, comment="VIP过期时间，NULL表示永久会员"
    )
