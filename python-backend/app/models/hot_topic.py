"""HotTopic ORM 模型"""

from sqlalchemy import BigInteger, Column, DateTime, SmallInteger, String, Text
from sqlalchemy.sql import func

from app.database import Base


class HotTopic(Base):
    """热门选题表"""

    __tablename__ = "hot_topic"

    id = Column(BigInteger, primary_key=True, autoincrement=True, comment="id")
    topic_text = Column(
        "topicText", String(500), nullable=False, comment="选题文本"
    )
    emoji = Column(String(20), nullable=False, default="🔥", comment="选题图标")
    year = Column(SmallInteger, nullable=False, comment="目标年份")
    month = Column(SmallInteger, nullable=False, comment="目标月份")
    source = Column(
        String(50), nullable=False, default="AI", comment="来源：AI/MANUAL/DATA"
    )
    sort_order = Column(
        "sortOrder", SmallInteger, nullable=False, default=0, comment="排序"
    )
    is_active = Column(
        "isActive", SmallInteger, nullable=False, default=1, comment="是否启用"
    )
    create_time = Column(
        "createTime", DateTime, nullable=False, default=func.now(), comment="创建时间"
    )
    update_time = Column(
        "updateTime",
        DateTime,
        nullable=False,
        default=func.now(),
        onupdate=func.now(),
        comment="更新时间",
    )
    is_delete = Column(
        "isDelete", SmallInteger, nullable=False, default=0, comment="是否删除"
    )
