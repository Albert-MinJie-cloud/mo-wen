"""支付路由"""

import logging
from typing import List, Optional

from databases import Database
from fastapi import APIRouter, Depends, Header, Request

from app.database import get_db
from app.constants.user import UserConstant
from app.deps import require_login
from app.exceptions import BusinessException, ErrorCode
from app.schemas.common import BaseResponse
from app.schemas.payment import CreatePaymentSessionRequest, PaymentRecordVO
from app.schemas.user import LoginUserVO
from app.services.payment_service import PaymentService
from app.models.enums import ProductTypeEnum

logger = logging.getLogger(__name__)

payment_router = APIRouter(prefix="/payment", tags=["Payment"])
webhook_router = APIRouter(prefix="/webhook", tags=["Webhook"])


@payment_router.post("/create-vip-session", response_model=BaseResponse[str])
async def create_vip_payment_session(
    request: CreatePaymentSessionRequest = None,
    db: Database = Depends(get_db),
    current_user: LoginUserVO = Depends(require_login),
):
    """创建 VIP 支付会话

    productType 可选值：VIP_MONTHLY（月付）/ VIP_YEARLY（年付）/ VIP_PERMANENT（永久，默认）
    """
    try:
        product_type = ProductTypeEnum(
            request.product_type if request else "VIP_PERMANENT"
        )
    except ValueError:
        raise BusinessException(
            ErrorCode.PARAMS_ERROR,
            f"无效的产品类型，可选值：{[e.value for e in ProductTypeEnum]}",
        )

    service = PaymentService(db)
    session_url = await service.create_vip_payment_session(
        current_user.id, product_type
    )
    return BaseResponse.success(data=session_url)


@payment_router.post("/refund", response_model=BaseResponse[bool])
async def refund(
    reason: Optional[str] = None,
    db: Database = Depends(get_db),
    current_user: LoginUserVO = Depends(require_login),
):
    """申请退款"""
    if current_user.user_role != UserConstant.VIP_ROLE:
        raise BusinessException(ErrorCode.NO_AUTH_ERROR, "仅 VIP 会员可退款")
    service = PaymentService(db)
    success = await service.handle_refund(current_user.id, reason)
    return BaseResponse.success(data=success)


@payment_router.get("/records", response_model=BaseResponse[List[PaymentRecordVO]])
async def get_payment_records(
    db: Database = Depends(get_db),
    current_user: LoginUserVO = Depends(require_login),
):
    """获取当前用户支付记录"""
    service = PaymentService(db)
    records = await service.get_payment_records(current_user.id)
    return BaseResponse.success(data=records)


@webhook_router.post("/stripe")
async def stripe_webhook(
    http_request: Request,
    stripe_signature: str = Header(..., alias="Stripe-Signature"),
    db: Database = Depends(get_db),
):
    """Stripe webhook 回调"""
    payload = (await http_request.body()).decode("utf-8")
    service = PaymentService(db)
    try:
        event = service.construct_event(payload, stripe_signature)
        event_type = getattr(event, "type", None) or event.get("type")
        logger.info(f"Webhook received: type={event_type}")

        data_object = None
        if hasattr(event, "data") and getattr(event.data, "object", None):
            data_object = event.data.object
        elif isinstance(event, dict):
            data_object = event.get("data", {}).get("object")

        if event_type in {
            "checkout.session.completed",
            "checkout.session.async_payment_succeeded",
        }:
            session_id = (
                getattr(data_object, "id", None)
                or (data_object.get("id") if isinstance(data_object, dict) else None)
            )
            logger.info(f"Processing payment success: session_id={session_id}")
            await service.handle_payment_success(data_object)
        return "success"
    except Exception as e:
        logger.error(f"Webhook error: {e}", exc_info=True)
        return "error"
