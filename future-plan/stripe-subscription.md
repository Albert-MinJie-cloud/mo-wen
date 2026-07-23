# Stripe Subscription 订阅模式

> 状态：待评估 | 优先级：中

## 背景

当前 VIP 月付/年付使用 Stripe `mode: "payment"`（一次性付款），不支持自动续费。用户在会员到期后需要手动再次购买。

## 目标

将月付和年付改为 `mode: "subscription"`，实现：

- 自动续费扣款（月付每月扣、年付每年扣）
- 扣款失败自动重试 + 暂停订阅
- 用户可通过 Stripe Customer Portal 自助管理（换卡、取消、查看账单）
- 升级/降级时按比例计费（proration）
- 永久会员保持 Payment 模式不变

## 关键改动

### 后端

- `payment_service.py`: 月付/年付改用 `mode: "subscription"` 创建 Session
- `payment_service.py`: 新增 webhook 事件处理
  - `invoice.paid` → 延长 vipExpireTime
  - `invoice.payment_failed` → 通知用户更新支付方式
  - `customer.subscription.deleted` → 用户降级为普通用户
  - `customer.subscription.updated` → 处理升级/降级
- Stripe Dashboard: 创建 Product + Price 对象（不能代码动态传价格）

### 前端

- `BuyVip.vue`: 月付/年付标注"自动续费，可随时取消"
- 新增订阅管理入口（跳转 Stripe Customer Portal）

### 数据模型

- `payment_record` 表可复用，增加 `stripeSubscriptionId` 字段

## 待定问题

- [ ] 订阅试用期？还是立即生效
- [ ] 扣款失败后宽限期几天
- [ ] 扣款失败重试次数
- [ ] 是否支持暂停订阅（pause）vs 直接取消
- [ ] 升级时剩余天数如何处理（Stripe 自带 proration，但需要和我们的 vipExpireTime 叠加逻辑对齐）

## 参考

- [Stripe Subscription 文档](https://docs.stripe.com/billing/subscriptions/overview)
- [Stripe Customer Portal](https://docs.stripe.com/customer-management)
- [Stripe Checkout + Subscription](https://docs.stripe.com/billing/subscriptions/build-subscriptions)
