"""支付服务"""

import logging
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Any, List, Optional

import stripe
from databases import Database

from app.config import settings
from app.constants.user import UserConstant
from app.exceptions import BusinessException, ErrorCode
from app.models.enums import PaymentStatusEnum, ProductTypeEnum
from app.schemas.payment import PaymentRecordVO

logger = logging.getLogger(__name__)


def is_vip_active(user_role: str, vip_expire_time: Any) -> bool:
    """检查 VIP 是否在有效期内

    可用于依赖注入、中间件等场景判断用户会员状态。

    Args:
        user_role: 用户角色（userRole 字段）
        vip_expire_time: VIP 过期时间（vipExpireTime 字段），None 表示永久会员

    Returns:
        True 表示 VIP 有效（永久会员或未过期），False 表示非会员或已过期
    """
    if user_role != UserConstant.VIP_ROLE:
        return False
    if vip_expire_time is None:
        return True  # 永久会员
    if isinstance(vip_expire_time, str):
        vip_expire_time = datetime.fromisoformat(vip_expire_time)
    return vip_expire_time > datetime.now()


class PaymentService:
    """支付服务"""

    CURRENCY_USD = "usd"
    CENTS_MULTIPLIER = Decimal("100")

    def __init__(self, db: Database):
        self.db = db
        stripe.api_key = settings.stripe_api_key

    async def create_vip_payment_session(
        self, user_id: int, product_type: ProductTypeEnum
    ) -> str:
        """创建 VIP 支付会话

        Args:
            user_id: 用户 ID
            product_type: 产品类型（月付/年付/永久）
        """
        self._ensure_stripe_ready(require_webhook=False)
        user = await self._get_user_or_throw(user_id)

        # 检查是否已是永久会员
        if self._is_permanent_vip(user):
            raise BusinessException(
                ErrorCode.OPERATION_ERROR, "您已经是永久会员，无需再次购买"
            )

        # 检查是否在有效期内（允许升级，拦截降级和同档重复购买）
        if self._is_vip_active(user):
            current_tier = await self._get_current_vip_tier(user_id)
            if current_tier is None:
                raise BusinessException(
                    ErrorCode.OPERATION_ERROR, "您的会员仍在有效期内"
                )
            if product_type.tier <= current_tier.tier:
                raise BusinessException(
                    ErrorCode.OPERATION_ERROR,
                    f"您已是{current_tier.description}，"
                    f"无法降级或重复购买同档方案，请选择更高档位",
                )
            # 升级放行，继续创建支付会话

        amount_cents = int(product_type.price * self.CENTS_MULTIPLIER)

        # 根据产品类型动态生成描述
        if product_type.duration_days is None:
            duration_desc = "终身有效"
        elif product_type.duration_days == 30:
            duration_desc = "有效期30天"
        elif product_type.duration_days == 365:
            duration_desc = "有效期365天"
        else:
            duration_desc = f"有效期{product_type.duration_days}天"

        session = stripe.checkout.Session.create(
            mode="payment",
            success_url=settings.stripe_success_url,
            cancel_url=settings.stripe_cancel_url,
            line_items=[
                {
                    "price_data": {
                        "currency": self.CURRENCY_USD,
                        "unit_amount": amount_cents,
                        "product_data": {
                            "name": product_type.description,
                            "description": f"解锁全部高级功能，无限创作配额，{duration_desc}",
                        },
                    },
                    "quantity": 1,
                }
            ],
            metadata={
                "userId": str(user_id),
                "productType": product_type.value,
            },
        )

        await self.db.execute(
            query="""
                INSERT INTO payment_record (
                    userId, stripeSessionId, amount, currency, status, productType, description
                )
                VALUES (
                    :userId, :stripeSessionId, :amount, :currency, :status, :productType, :description
                )
            """,
            values={
                "userId": user_id,
                "stripeSessionId": session.id,
                "amount": str(product_type.price),
                "currency": self.CURRENCY_USD,
                "status": PaymentStatusEnum.PENDING.value,
                "productType": product_type.value,
                "description": product_type.description,
            },
        )
        return session.url

    def construct_event(self, payload: str, sig_header: str) -> Any:
        """验证 Stripe webhook 签名并构造事件"""
        self._ensure_stripe_ready(require_webhook=True)
        return stripe.Webhook.construct_event(
            payload, sig_header, settings.stripe_webhook_secret
        )

    async def handle_payment_success(self, session: Any):
        """处理支付成功回调（幂等）"""

        # 安全提取值：先尝试 dict-like，再尝试属性访问
        def _safe_get(obj, key, default=None):
            if obj is None:
                return default
            if isinstance(obj, dict):
                return obj.get(key, default)
            try:
                return getattr(obj, key, default)
            except Exception:
                return default

        def _safe_metadata(obj):
            raw = _safe_get(obj, "metadata")
            if raw is None:
                return {}
            if isinstance(raw, dict):
                return raw
            # StripeObject：使用 to_dict() 方法
            if hasattr(raw, "to_dict"):
                return raw.to_dict()
            # 兜底
            return {}

        session_id = _safe_get(session, "id")
        metadata = _safe_metadata(session)
        user_id_value = metadata.get("userId")
        payment_intent = _safe_get(session, "payment_intent")
        payment_intent_id = (
            payment_intent
            if isinstance(payment_intent, str)
            else _safe_get(payment_intent, "id")
        )

        logger.info(
            f"handle_payment_success: session_id={session_id}, user_id_value={user_id_value}, metadata={metadata}"
        )

        if not session_id or not user_id_value:
            return

        # --- Code Review 添加：校验支付金额是否与产品定价一致 ---
        product_type_value = metadata.get("productType")
        product_type = None
        if product_type_value:
            try:
                product_type = ProductTypeEnum(product_type_value)
                expected_amount_cents = int(product_type.price * self.CENTS_MULTIPLIER)
                actual_amount = _safe_get(session, "amount_total", 0)
                if actual_amount != expected_amount_cents:
                    logger.warning(
                        f"Payment amount mismatch for session {session_id}: "
                        f"expected {expected_amount_cents}, got {actual_amount}"
                    )
            except ValueError:
                pass

        if product_type is None:
            logger.warning(
                f"Cannot determine product type for session {session_id}, skipping"
            )
            return

        record = await self.db.fetch_one(
            query="""
                SELECT id, status
                FROM payment_record
                WHERE stripeSessionId = :stripeSessionId
            """,
            values={"stripeSessionId": session_id},
        )
        if not record:
            return

        if record["status"] == PaymentStatusEnum.SUCCEEDED.value:
            return

        # 计算 VIP 过期时间
        user = await self.db.fetch_one(
            query="SELECT id, userRole, vipExpireTime FROM user WHERE id = :id AND isDelete = 0",
            values={"id": int(user_id_value)},
        )
        now = datetime.now()
        # 如果用户已有 VIP 且未过期，在现有到期时间上累加；否则从现在开始计算
        existing_expire = None
        if (
            user
            and user["userRole"] == UserConstant.VIP_ROLE
            and self._value(user, "vipExpireTime")
        ):
            et = user["vipExpireTime"]
            if isinstance(et, str):
                et = datetime.fromisoformat(et)
            if et > now:
                existing_expire = et

        if product_type.duration_days is None:
            vip_expire_time = None  # 永久会员
        elif existing_expire:
            vip_expire_time = existing_expire + timedelta(
                days=product_type.duration_days
            )
        else:
            vip_expire_time = now + timedelta(days=product_type.duration_days)

        # 首次成为 VIP 才设置 vipTime，升级时保留原值
        vip_time = now
        if user and user["userRole"] == UserConstant.VIP_ROLE:
            vip_time = self._value(user, "vipTime", now)

        async with self.db.transaction():
            await self.db.execute(
                query="""
                    UPDATE payment_record
                    SET status = :status, stripePaymentIntentId = :stripePaymentIntentId
                    WHERE id = :id
                """,
                values={
                    "id": record["id"],
                    "status": PaymentStatusEnum.SUCCEEDED.value,
                    "stripePaymentIntentId": payment_intent_id,
                },
            )
            await self.db.execute(
                query="""
                    UPDATE user
                    SET userRole = :userRole, vipTime = :vipTime, vipExpireTime = :vipExpireTime
                    WHERE id = :id
                """,
                values={
                    "id": int(user_id_value),
                    "userRole": UserConstant.VIP_ROLE,
                    "vipTime": vip_time,
                    "vipExpireTime": vip_expire_time,
                },
            )

    async def handle_refund(self, user_id: int, reason: Optional[str]) -> bool:
        """处理退款并撤销 VIP"""
        self._ensure_stripe_ready(require_webhook=False)
        user = await self._get_user_or_throw(user_id)
        if user["userRole"] != UserConstant.VIP_ROLE:
            raise BusinessException(ErrorCode.OPERATION_ERROR, "您不是会员，无法退款")

        payment_record = await self.db.fetch_one(
            query="""
                SELECT id, stripePaymentIntentId
                FROM payment_record
                WHERE userId = :userId
                  AND status = :status
                ORDER BY createTime DESC
                LIMIT 1
            """,
            values={
                "userId": user_id,
                "status": PaymentStatusEnum.SUCCEEDED.value,
            },
        )
        if not payment_record:
            raise BusinessException(ErrorCode.NOT_FOUND_ERROR, "未找到支付记录")
        if not payment_record["stripePaymentIntentId"]:
            raise BusinessException(ErrorCode.OPERATION_ERROR, "支付记录无效")

        refund = stripe.Refund.create(
            payment_intent=payment_record["stripePaymentIntentId"],
            reason="requested_by_customer",
        )
        if getattr(refund, "status", None) != "succeeded":
            return False

        async with self.db.transaction():
            await self.db.execute(
                query="""
                    UPDATE payment_record
                    SET status = :status, refundTime = :refundTime, refundReason = :refundReason
                    WHERE id = :id
                """,
                values={
                    "id": payment_record["id"],
                    "status": PaymentStatusEnum.REFUNDED.value,
                    "refundTime": datetime.now(),
                    "refundReason": reason,
                },
            )
            await self.db.execute(
                query="""
                    UPDATE user
                    SET userRole = :userRole, vipTime = NULL, vipExpireTime = NULL, quota = :quota
                    WHERE id = :id
                """,
                values={
                    "id": user_id,
                    "userRole": UserConstant.DEFAULT_ROLE,
                    "quota": UserConstant.DEFAULT_QUOTA,
                },
            )
        return True

    async def get_payment_records(self, user_id: int) -> List[PaymentRecordVO]:
        """获取用户支付记录"""
        records = await self.db.fetch_all(
            query="""
                SELECT *
                FROM payment_record
                WHERE userId = :userId
                ORDER BY createTime DESC
                """,
            values={"userId": user_id},
        )
        return [self._to_payment_record_vo(record) for record in records]

    async def _get_user_or_throw(self, user_id: int):
        user = await self.db.fetch_one(
            query="SELECT id, userRole, vipExpireTime FROM user WHERE id = :id AND isDelete = 0",
            values={"id": user_id},
        )
        if not user:
            raise BusinessException(ErrorCode.NOT_FOUND_ERROR, "用户不存在")
        return user

    async def _get_current_vip_tier(self, user_id: int) -> Optional[ProductTypeEnum]:
        """从最新支付记录获取用户当前 VIP 档次"""
        record = await self.db.fetch_one(
            query="""
                SELECT productType FROM payment_record
                WHERE userId = :uid AND status = :status
                ORDER BY createTime DESC
                LIMIT 1
            """,
            values={
                "uid": user_id,
                "status": PaymentStatusEnum.SUCCEEDED.value,
            },
        )
        if not record:
            return None
        try:
            return ProductTypeEnum(record["productType"])
        except ValueError:
            return None

    @staticmethod
    def _value(user, key, default=None):
        """安全获取值，兼容 Record 对象和 dict"""
        if isinstance(user, dict):
            return user.get(key, default)
        try:
            return user[key]
        except (KeyError, TypeError):
            return default

    @classmethod
    def _is_permanent_vip(cls, user) -> bool:
        """检查用户是否为永久会员"""
        return (
            user["userRole"] == UserConstant.VIP_ROLE
            and cls._value(user, "vipExpireTime") is None
        )

    @classmethod
    def _is_vip_active(cls, user) -> bool:
        """检查用户 VIP 是否在有效期内"""
        if user["userRole"] != UserConstant.VIP_ROLE:
            return False
        expire_time = cls._value(user, "vipExpireTime")
        if expire_time is None:
            return True  # 永久会员
        if isinstance(expire_time, str):
            expire_time = datetime.fromisoformat(expire_time)
        return expire_time > datetime.now()

    def _to_payment_record_vo(self, record: Any) -> PaymentRecordVO:
        record_dict = dict(record)
        return PaymentRecordVO(
            id=record_dict["id"],
            userId=record_dict["userId"],
            stripeSessionId=record_dict.get("stripeSessionId"),
            stripePaymentIntentId=record_dict.get("stripePaymentIntentId"),
            amount=float(record_dict["amount"]),
            currency=record_dict["currency"],
            status=record_dict["status"],
            productType=record_dict["productType"],
            description=record_dict.get("description"),
            refundTime=record_dict["refundTime"].isoformat()
            if record_dict.get("refundTime")
            else None,
            refundReason=record_dict.get("refundReason"),
            createTime=record_dict["createTime"].isoformat(),
            updateTime=record_dict["updateTime"].isoformat(),
        )

    def _ensure_stripe_ready(self, require_webhook: bool):
        """校验 Stripe 配置是否可用"""
        if not settings.stripe_api_key:
            raise BusinessException(ErrorCode.SYSTEM_ERROR, "Stripe API Key 未配置")
        if require_webhook and not settings.stripe_webhook_secret:
            raise BusinessException(
                ErrorCode.SYSTEM_ERROR, "Stripe Webhook Secret 未配置"
            )
