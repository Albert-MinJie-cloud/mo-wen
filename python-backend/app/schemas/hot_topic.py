"""热门选题相关请求/响应模型"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class HotTopicVO(BaseModel):
    """热门选题视图对象"""

    id: int
    emoji: str
    text: str = Field(alias="topicText")

    model_config = ConfigDict(populate_by_name=True)


class HotTopicResponse(BaseModel):
    """热门选题响应"""

    topics: list[HotTopicVO]
    update_time: datetime = Field(alias="updateTime")

    model_config = ConfigDict(populate_by_name=True)
