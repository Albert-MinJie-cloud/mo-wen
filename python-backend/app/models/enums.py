"""枚举类型定义"""

from enum import Enum
from typing import Optional
from decimal import Decimal


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
    TITLES_GENERATED = "TITLES_GENERATED"  # 标题方案生成完成（等待用户选择）
    AGENT2_STREAMING = "AGENT2_STREAMING"  # 智能体2流式输出（大纲）
    OUTLINE_GENERATED = "OUTLINE_GENERATED"  # 大纲生成完成（等待用户编辑）
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


class ArticlePhaseEnum(str, Enum):
    """文章阶段枚举"""

    PENDING = "PENDING"
    TITLE_GENERATING = "TITLE_GENERATING"
    TITLE_SELECTING = "TITLE_SELECTING"
    OUTLINE_GENERATING = "OUTLINE_GENERATING"
    OUTLINE_EDITING = "OUTLINE_EDITING"
    CONTENT_GENERATING = "CONTENT_GENERATING"

    def can_transition_to(self, target_phase: "ArticlePhaseEnum") -> bool:
        """校验是否可流转到目标阶段"""
        transitions = {
            ArticlePhaseEnum.PENDING: {ArticlePhaseEnum.TITLE_GENERATING},
            ArticlePhaseEnum.TITLE_GENERATING: {ArticlePhaseEnum.TITLE_SELECTING},
            ArticlePhaseEnum.TITLE_SELECTING: {ArticlePhaseEnum.OUTLINE_GENERATING},
            ArticlePhaseEnum.OUTLINE_GENERATING: {ArticlePhaseEnum.OUTLINE_EDITING},
            ArticlePhaseEnum.OUTLINE_EDITING: {ArticlePhaseEnum.CONTENT_GENERATING},
            ArticlePhaseEnum.CONTENT_GENERATING: set(),
        }
        return target_phase in transitions.get(self, set())


class PaymentStatusEnum(str, Enum):
    """支付状态枚举"""

    PENDING = "PENDING"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"
    REFUNDED = "REFUNDED"


class ProductTypeEnum(str, Enum):
    """产品类型枚举

    VIP 多档位扩展设计：
    - VIP_MONTHLY / VIP_YEARLY / VIP_PERMANENT 三个档位
    - duration_days 返回有效期天数，None 表示永久
    - 用户表需新增 vipExpireTime 字段（DATETIME, NULL=永久）
    - 支付成功时根据 duration_days 计算并写入 vipExpireTime
    - 登录时检查 vipExpireTime，过期自动降级为 user 角色
    """

    VIP_MONTHLY = "VIP_MONTHLY"
    VIP_YEARLY = "VIP_YEARLY"
    VIP_PERMANENT = "VIP_PERMANENT"

    @property
    def description(self) -> str:
        descriptions = {
            ProductTypeEnum.VIP_MONTHLY: "月度会员",
            ProductTypeEnum.VIP_YEARLY: "年度会员",
            ProductTypeEnum.VIP_PERMANENT: "永久会员",
        }
        return descriptions[self]

    @property
    def price(self) -> Decimal:
        prices = {
            ProductTypeEnum.VIP_MONTHLY: Decimal("9.90"),
            ProductTypeEnum.VIP_YEARLY: Decimal("99.00"),
            ProductTypeEnum.VIP_PERMANENT: Decimal("199.00"),
        }
        return prices[self]

    @property
    def duration_days(self) -> int | None:
        """返回有效期天数，None 表示永久会员"""
        durations = {
            ProductTypeEnum.VIP_MONTHLY: 30,
            ProductTypeEnum.VIP_YEARLY: 365,
            ProductTypeEnum.VIP_PERMANENT: None,
        }
        return durations[self]
