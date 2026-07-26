"""支付相关请求/响应模型"""

from pydantic import BaseModel, Field


class RefundRequest(BaseModel):
    """退款请求"""

    reason: str | None = Field(None, description="退款原因")


class CreatePaymentSessionRequest(BaseModel):
    """创建支付会话请求"""

    product_type: str = Field(
        default="VIP_PERMANENT",
        alias="productType",
        description="产品类型：VIP_MONTHLY/VIP_YEARLY/VIP_PERMANENT",
    )


class PaymentRecordVO(BaseModel):
    """支付记录视图"""

    id: int
    user_id: int = Field(..., alias="userId")
    stripe_session_id: str | None = Field(None, alias="stripeSessionId")
    stripe_payment_intent_id: str | None = Field(None, alias="stripePaymentIntentId")
    amount: float
    currency: str
    status: str
    product_type: str = Field(..., alias="productType")
    description: str | None = None
    refund_time: str | None = Field(None, alias="refundTime")
    refund_reason: str | None = Field(None, alias="refundReason")
    create_time: str = Field(..., alias="createTime")
    update_time: str = Field(..., alias="updateTime")

    class Config:
        populate_by_name = True
