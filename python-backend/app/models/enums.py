"""枚举类型定义"""

from enum import Enum
from typing import Optional


class ArticleStatusEnum(str, Enum):
    """文章状态枚举"""

    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class ArticleStyleEnum(str, Enum):
    """文章风格枚举"""

    TECH = "tech"
    EMOTIONAL = "emotional"
    EDUCATIONAL = "educational"
    HUMOROUS = "humorous"

    @classmethod
    def is_valid(cls, value: Optional[str]) -> bool:
        """校验是否为有效的风格值"""
        if not value:
            return True  # 允许为空
        return value in [e.value for e in cls]


class ImageMethodEnum(str, Enum):
    """配图方式枚举"""

    PEXELS = "PEXELS"
    NANO_BANANA = "NANO_BANANA"
    MERMAID = "MERMAID"
    ICONIFY = "ICONIFY"
    EMOJI_PACK = "EMOJI_PACK"
    SVG_DIAGRAM = "SVG_DIAGRAM"
    PICSUM = "PICSUM"

    def is_ai_generated(self) -> bool:
        """是否为 AI 生图方式"""
        return self in [
            ImageMethodEnum.NANO_BANANA,
            ImageMethodEnum.MERMAID,
            ImageMethodEnum.SVG_DIAGRAM,
        ]

    def is_fallback(self) -> bool:
        """是否为降级方案"""
        return self == ImageMethodEnum.PICSUM

    @classmethod
    def get_default_search_method(cls):
        return cls.PEXELS

    @classmethod
    def get_fallback_method(cls):
        return cls.PICSUM


class SseMessageTypeEnum(str, Enum):
    """SSE 消息类型枚举"""

    AGENT1_COMPLETE = "AGENT1_COMPLETE"  # 智能体1完成（生成标题）
    AGENT2_STREAMING = "AGENT2_STREAMING"  # 智能体2流式输出（大纲）
    AGENT2_COMPLETE = "AGENT2_COMPLETE"  # 智能体2完成
    AGENT3_STREAMING = "AGENT3_STREAMING"  # 智能体3流式输出（正文）
    AGENT3_COMPLETE = "AGENT3_COMPLETE"  # 智能体3完成
    AGENT4_COMPLETE = "AGENT4_COMPLETE"  # 智能体4完成（配图需求）
    IMAGE_COMPLETE = "IMAGE_COMPLETE"  # 单张配图完成
    AGENT5_COMPLETE = "AGENT5_COMPLETE"  # 智能体5完成
    MERGE_COMPLETE = "MERGE_COMPLETE"  # 图文合成完成
    ALL_COMPLETE = "ALL_COMPLETE"  # 全部完成
    ERROR = "ERROR"  # 错误

    def get_streaming_prefix(self) -> str:
        """获取流式输出消息前缀"""
        return f"{self.value}:"
