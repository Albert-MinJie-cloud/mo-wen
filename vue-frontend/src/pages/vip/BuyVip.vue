<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import {
  createVipPaymentSessionApiPaymentCreateVipSessionPost,
  getPaymentRecordsApiPaymentRecordsGet,
} from "@/api/payment";
import Button from "@/components/Button.vue";
import { useLoginUserStore } from "@/stores/loginUser";
import { useRouter } from "vue-router";
import { isVip } from "@/utils/permission";
import { message } from "@/message";
import {
  CrownOutlined,
  CheckOutlined,
  CloseOutlined,
  LoadingOutlined,
  ArrowRightOutlined,
} from "@ant-design/icons-vue";

const router = useRouter();
const loginUserStore = useLoginUserStore();

// 是否已登录
const isLoggedIn = computed(() => !!loginUserStore.loginUser.id);

// 支付按钮 loading 状态
const loadingTier = ref<string | null>(null);

// 支付记录
const paymentRecords = ref<API.PaymentRecordVO[]>([]);
const recordsLoading = ref(false);

// 是否已是 VIP（含过期检查）
const userIsVip = computed(() => isVip(loginUserStore.loginUser));

// VIP 是否永久
const isPermanent = computed(
  () =>
    loginUserStore.loginUser.userRole === "vip" &&
    loginUserStore.loginUser.vipExpireTime === null
);

// 档位 map
const tierMap: Record<string, number> = {
  VIP_MONTHLY: 1,
  VIP_YEARLY: 2,
  VIP_PERMANENT: 3,
};

// 当前用户 VIP 档位（从最新 SUCCEEDED 支付记录获取）
const currentTier = computed(() => {
  const succeeded = paymentRecords.value
    .filter((r) => r.status === "SUCCEEDED")
    .sort(
      (a, b) =>
        new Date(b.createTime).getTime() - new Date(a.createTime).getTime()
    );
  if (succeeded.length === 0) return 0;
  const pt = succeeded[0]?.productType;
  return tierMap[pt ?? ""] ?? 0;
});

// 当前档位名称
const currentTierName = computed(() => {
  if (currentTier.value === 0) return "";
  const succeeded = paymentRecords.value.filter(
    (r) => r.status === "SUCCEEDED"
  );
  if (succeeded.length === 0) return "";
  const desc = succeeded[0]?.description;
  return desc || "";
});

// 获取某个档位对应的按钮配置
function getButtonConfig(tierKey: string) {
  const targetTier = tierMap[tierKey] ?? 0;
  if (!userIsVip.value) {
    // 非 VIP → 立即购买
    return { text: "立即购买", disabled: false, variant: "gradient" as const };
  }
  if (isPermanent.value) {
    // 永久 → 已是最高级别
    return {
      text: "已是最高级别",
      disabled: true,
      variant: "gradient" as const,
    };
  }
  if (targetTier > currentTier.value) {
    // 高档 → 立即升级
    return { text: "立即升级", disabled: false, variant: "gradient" as const };
  }
  if (targetTier === currentTier.value) {
    // 同档 → 当前方案
    return {
      text: "当前方案",
      disabled: true,
      variant: "gradient" as const,
    };
  }
  // 低档 → 降级不可
  return {
    text: "已有更高级别",
    disabled: true,
    variant: "gradient" as const,
  };
}

// VIP 到期时间格式化
const expireTimeFormatted = computed(() => {
  const t = loginUserStore.loginUser.vipExpireTime;
  if (!t) return "永久有效";
  const d = new Date(t);
  const now = new Date();
  const diff = d.getTime() - now.getTime();
  const days = Math.ceil(diff / (1000 * 60 * 60 * 24));
  if (days <= 0) return "已过期";
  if (days <= 30) return `${d.toLocaleDateString("zh-CN")}（剩余 ${days} 天）`;
  return d.toLocaleDateString("zh-CN");
});

// 会员档位配置
const tiers = [
  {
    key: "VIP_MONTHLY",
    name: "月度会员",
    price: "9.90",
    originalPrice: "",
    period: "/月",
    duration: "30 天",
    features: [
      { text: "无限文章生成次数", included: true },
      { text: "所有配图源可用", included: true },
      { text: "AI 智能生图（Nano Banana）", included: true },
      { text: "SVG 示意图生成", included: true },
      { text: "优先处理队列", included: false },
      { text: "专属客服支持", included: false },
    ],
    highlighted: false,
    gradient: "",
  },
  {
    key: "VIP_YEARLY",
    name: "年度会员",
    price: "99.00",
    originalPrice: "118.80",
    period: "/年",
    duration: "365 天",
    features: [
      { text: "无限文章生成次数", included: true },
      { text: "所有配图源可用", included: true },
      { text: "AI 智能生图（Nano Banana）", included: true },
      { text: "SVG 示意图生成", included: true },
      { text: "优先处理队列", included: true },
      { text: "专属客服支持", included: false },
    ],
    highlighted: true,
    gradient: "linear-gradient(135deg, #22d3ee, #3b82f6)",
  },
  {
    key: "VIP_PERMANENT",
    name: "永久会员",
    price: "199.00",
    originalPrice: "",
    period: "买断",
    duration: "永久有效",
    features: [
      { text: "无限文章生成次数", included: true },
      { text: "所有配图源可用", included: true },
      { text: "AI 智能生图（Nano Banana）", included: true },
      { text: "SVG 示意图生成", included: true },
      { text: "优先处理队列", included: true },
      { text: "专属客服支持", included: true },
    ],
    highlighted: false,
    gradient: "linear-gradient(135deg, #a855f7, #6366f1)",
  },
];

// 创建支付会话并跳转 Stripe
async function handleBuy(tier: (typeof tiers)[0]) {
  if (loadingTier.value) return;

  // 检查是否登录
  if (!isLoggedIn.value) {
    message.warning("请先登录后再购买");
    router.push(`/user/login?redirect=${encodeURIComponent("/vip")}`);
    return;
  }

  loadingTier.value = tier.key;

  try {
    const res = await createVipPaymentSessionApiPaymentCreateVipSessionPost(
      {},
      { productType: tier.key }
    );
    if (res.data.code === 0 && res.data.data) {
      // 跳转到 Stripe Checkout
      window.location.href = res.data.data;
    } else {
      message.error(res.data.message || "创建支付会话失败");
    }
  } catch {
    message.error("网络异常，请稍后重试");
  } finally {
    loadingTier.value = null;
  }
}

// 支付状态标签
function statusLabel(status: string): string {
  const map: Record<string, string> = {
    PENDING: "待支付",
    SUCCEEDED: "已支付",
    FAILED: "支付失败",
    REFUNDED: "已退款",
  };
  return map[status] || status;
}

// 计算支付记录对应的 VIP 到期日
const durationDays: Record<string, number | null> = {
  VIP_MONTHLY: 30,
  VIP_YEARLY: 365,
  VIP_PERMANENT: null,
};
function getExpireDate(record: API.PaymentRecordVO): string {
  if (record.status !== "SUCCEEDED") return "-";
  const days = durationDays[record.productType];
  if (days === null || days === undefined) return "永久有效";
  const d = new Date(record.createTime);
  d.setDate(d.getDate() + days);
  return d.toLocaleDateString("zh-CN");
}

// 数字格式化为美元
function formatUSD(amount: number): string {
  return `$${amount.toFixed(2)}`;
}

// 获取支付记录
async function fetchRecords() {
  recordsLoading.value = true;
  try {
    const res = await getPaymentRecordsApiPaymentRecordsGet({});
    if (res.data.code === 0 && res.data.data) {
      paymentRecords.value = res.data.data;
    }
  } catch {
    // 静默处理
  } finally {
    recordsLoading.value = false;
  }
}

onMounted(() => {
  fetchRecords();
});
</script>

<template>
  <div id="buyVipPage">
    <!-- Hero 头部 -->
    <section class="vip-hero">
      <div class="hero-bg"></div>
      <div class="hero-content">
        <div class="hero-icon">
          <CrownOutlined />
        </div>
        <h1 class="hero-title">解锁 VIP 会员</h1>
        <p class="hero-subtitle">
          无限创作，智能配图，让你的每一篇文章都成为爆款
        </p>
      </div>
    </section>

    <!-- 当前 VIP 状态卡片 -->
    <section v-if="userIsVip" class="status-section">
      <div class="status-card">
        <div class="status-left">
          <CrownOutlined class="status-crown" />
          <div class="status-info">
            <div class="status-label">当前会员状态</div>
            <div class="status-tier">
              {{ isPermanent ? "永久会员" : currentTierName || "VIP 会员" }}
            </div>
            <div class="status-expire">
              到期时间：{{ expireTimeFormatted }}
            </div>
          </div>
        </div>
        <div class="status-right">
          <div class="status-quota">
            <span class="quota-value">{{ loginUserStore.loginUser.quota ?? "无限" }}</span>
            <span class="quota-label">剩余配额</span>
          </div>
        </div>
      </div>
    </section>

    <!-- 定价卡片 -->
    <section class="pricing-section">
      <h2 class="section-title">选择适合你的方案</h2>
      <p class="section-subtitle">
        升级 VIP 解锁全部功能，支持随时退款
      </p>

      <div class="pricing-grid">
        <div
          v-for="tier in tiers"
          :key="tier.key"
          :class="['pricing-card', { highlighted: tier.highlighted }]"
          :style="tier.highlighted ? { '--card-gradient': tier.gradient } : {}"
        >
          <!-- 推荐标签 -->
          <div v-if="tier.highlighted" class="recommend-badge">
            <CrownOutlined />
            最受欢迎
          </div>

          <!-- 头部 -->
          <div class="card-header">
            <h3 class="card-name">{{ tier.name }}</h3>
            <p class="card-duration">{{ tier.duration }}</p>
          </div>

          <!-- 价格 -->
          <div class="card-price">
            <span class="price-currency">$</span>
            <span class="price-value">{{ tier.price }}</span>
            <span class="price-period">{{ tier.period }}</span>
          </div>
          <div v-if="tier.originalPrice" class="card-original-price">
            原价 ${{ tier.originalPrice }}
          </div>

          <!-- 特性列表 -->
          <ul class="card-features">
            <li
              v-for="(feat, i) in tier.features"
              :key="i"
              :class="['feature-item', { excluded: !feat.included }]"
            >
              <CheckOutlined v-if="feat.included" class="feature-check" />
              <CloseOutlined v-else class="feature-cross" />
              <span>{{ feat.text }}</span>
            </li>
          </ul>

          <!-- 购买按钮 -->
          <div class="card-action">
            <template v-if="getButtonConfig(tier.key).disabled">
              <div
                :class="[
                  'tier-status-hint',
                  { 'tier-current': getButtonConfig(tier.key).text === '当前方案' },
                ]"
              >
                <CheckOutlined v-if="getButtonConfig(tier.key).text === '当前方案'" />
                <CrownOutlined v-else />
                {{ getButtonConfig(tier.key).text }}
              </div>
            </template>
            <Button
              v-else
              :variant="tier.highlighted ? 'gradient' : 'secondary'"
              size="lg"
              block
              :disabled="loadingTier === tier.key"
              @click="handleBuy(tier)"
            >
              <LoadingOutlined v-if="loadingTier === tier.key" />
              <CrownOutlined v-else />
              {{ loadingTier === tier.key ? "正在跳转..." : getButtonConfig(tier.key).text }}
            </Button>
          </div>
        </div>
      </div>
    </section>

    <!-- 支付记录 -->
    <section v-if="paymentRecords.length > 0" class="records-section">
      <h2 class="section-title">支付记录</h2>
      <div class="records-table-wrap">
        <a-table
          :dataSource="paymentRecords"
          :pagination="false"
          :loading="recordsLoading"
          size="small"
          rowKey="id"
        >
          <a-table-column title="产品" dataIndex="description" key="description">
            <template #default="{ record }">
              <span class="record-product">{{ record.description }}</span>
            </template>
          </a-table-column>
          <a-table-column title="金额" dataIndex="amount" key="amount">
            <template #default="{ record }">
              {{ formatUSD(record.amount) }}
            </template>
          </a-table-column>
          <a-table-column title="状态" dataIndex="status" key="status">
            <template #default="{ record }">
              <span :class="['record-status', `status-${record.status.toLowerCase()}`]">
                {{ statusLabel(record.status) }}
              </span>
            </template>
          </a-table-column>
          <a-table-column title="有效期" key="expireDate">
            <template #default="{ record }">
              <span class="record-expire">{{ getExpireDate(record) }}</span>
            </template>
          </a-table-column>
          <a-table-column title="时间" dataIndex="createTime" key="createTime">
            <template #default="{ record }">
              {{ new Date(record.createTime).toLocaleString("zh-CN") }}
            </template>
          </a-table-column>
        </a-table>
      </div>
    </section>

    <!-- 空支付记录提示 -->
    <section v-else class="records-section">
      <div class="empty-records">
        <p class="empty-text">还没有支付记录</p>
        <p class="empty-hint">选择上方方案，开始你的 VIP 之旅</p>
      </div>
    </section>

    <!-- 底部保障 -->
    <section class="assurance-section">
      <div class="assurance-items">
        <div class="assurance-item">
          <div class="assurance-icon">🔒</div>
          <div class="assurance-label">Stripe 安全支付</div>
        </div>
        <div class="assurance-item">
          <div class="assurance-icon">↩️</div>
          <div class="assurance-label">支持随时退款</div>
        </div>
        <div class="assurance-item">
          <div class="assurance-icon">⚡</div>
          <div class="assurance-label">即时开通生效</div>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
#buyVipPage {
  min-height: calc(100vh - 64px);
  background: var(--color-background);
  padding-bottom: 80px;
}

/* ===== Hero 头部 ===== */
.vip-hero {
  position: relative;
  padding: 72px 20px 56px;
  text-align: center;
  overflow: hidden;
}

.hero-bg {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background:
    radial-gradient(ellipse 60% 60% at 50% 0%, rgba(6, 182, 212, 0.12), transparent),
    radial-gradient(ellipse 40% 40% at 80% 50%, rgba(59, 130, 246, 0.08), transparent),
    radial-gradient(ellipse 40% 40% at 20% 50%, rgba(168, 85, 247, 0.06), transparent);
}

.hero-content {
  position: relative;
  z-index: 1;
}

.hero-icon {
  font-size: 48px;
  color: #facc15;
  margin-bottom: 20px;
  filter: drop-shadow(0 0 20px rgba(250, 204, 21, 0.3));
}

.hero-title {
  font-family: "Outfit", "Work Sans", sans-serif;
  font-size: 40px;
  font-weight: 700;
  color: var(--color-text);
  margin: 0 0 12px;
  letter-spacing: -1px;
}

.hero-subtitle {
  font-size: 17px;
  color: var(--color-text-secondary);
  margin: 0;
  max-width: 480px;
  margin-inline: auto;
  line-height: 1.7;
}

/* ===== VIP 状态卡片 ===== */
.status-section {
  max-width: 800px;
  margin: 0 auto 48px;
  padding: 0 20px;
}

.status-card {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: linear-gradient(135deg, rgba(6, 182, 212, 0.1), rgba(59, 130, 246, 0.08));
  border: 1px solid rgba(6, 182, 212, 0.2);
  border-radius: var(--radius-xl);
  padding: 24px 28px;
}

.status-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.status-crown {
  font-size: 32px;
  color: #facc15;
}

.status-label {
  font-size: 13px;
  color: var(--color-text-muted);
  margin-bottom: 4px;
}

.status-tier {
  font-size: 20px;
  font-weight: 700;
  color: var(--color-text);
  margin-bottom: 2px;
}

.status-expire {
  font-size: 13px;
  color: var(--color-text-secondary);
}

.status-right {
  text-align: center;
}

.quota-value {
  display: block;
  font-size: 28px;
  font-weight: 700;
  color: var(--color-accent-cyan);
  line-height: 1;
}

.quota-label {
  font-size: 12px;
  color: var(--color-text-muted);
  margin-top: 4px;
}

/* ===== 定价区 ===== */
.pricing-section {
  max-width: 1100px;
  margin: 0 auto;
  padding: 0 20px;
}

.section-title {
  font-family: "Outfit", "Work Sans", sans-serif;
  font-size: 28px;
  font-weight: 700;
  color: var(--color-text);
  text-align: center;
  margin: 0 0 8px;
}

.section-subtitle {
  font-size: 15px;
  color: var(--color-text-secondary);
  text-align: center;
  margin: 0 0 40px;
}

.pricing-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}

/* ===== 定价卡片 ===== */
.pricing-card {
  position: relative;
  background: var(--color-background-tertiary);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xl);
  padding: 32px 24px 28px;
  display: flex;
  flex-direction: column;
  transition: all var(--transition-normal);
}

.pricing-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-xl);
}

.pricing-card.highlighted {
  border-color: transparent;
  background: var(--color-background-tertiary);
  position: relative;
}

.pricing-card.highlighted::before {
  content: "";
  position: absolute;
  inset: -1px;
  border-radius: var(--radius-xl);
  background: var(--card-gradient, var(--gradient-primary));
  z-index: -1;
}

.pricing-card.highlighted::after {
  content: "";
  position: absolute;
  inset: 0;
  border-radius: var(--radius-xl);
  background: var(--color-background-tertiary);
  z-index: -1;
}

.recommend-badge {
  position: absolute;
  top: -12px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  align-items: center;
  gap: 6px;
  background: var(--gradient-primary);
  color: #fff;
  font-size: 12px;
  font-weight: 600;
  padding: 5px 16px;
  border-radius: var(--radius-full);
  white-space: nowrap;
}

.card-header {
  text-align: center;
  margin-bottom: 20px;
}

.card-name {
  font-family: "Outfit", "Work Sans", sans-serif;
  font-size: 20px;
  font-weight: 700;
  color: var(--color-text);
  margin: 0 0 4px;
}

.card-duration {
  font-size: 13px;
  color: var(--color-text-muted);
  margin: 0;
}

.card-price {
  text-align: center;
  margin-bottom: 4px;
}

.price-currency {
  font-size: 20px;
  font-weight: 600;
  color: var(--color-text-secondary);
  vertical-align: super;
}

.price-value {
  font-family: "Outfit", "Work Sans", sans-serif;
  font-size: 42px;
  font-weight: 800;
  color: var(--color-text);
  line-height: 1;
}

.price-period {
  font-size: 14px;
  color: var(--color-text-muted);
  margin-left: 4px;
}

.card-original-price {
  text-align: center;
  font-size: 13px;
  color: var(--color-text-muted);
  text-decoration: line-through;
  margin-bottom: 16px;
  min-height: 20px;
}

.card-features {
  list-style: none;
  padding: 0;
  margin: 0 0 28px;
  flex: 1;
}

.feature-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 9px 0;
  font-size: 14px;
  color: var(--color-text-secondary);
  border-bottom: 1px solid var(--color-border-light);
}

.feature-item:last-child {
  border-bottom: none;
}

.feature-check {
  color: var(--color-success);
  font-size: 15px;
  flex-shrink: 0;
}

.feature-cross {
  color: var(--color-text-muted);
  font-size: 13px;
  flex-shrink: 0;
}

.feature-item.excluded {
  color: var(--color-text-muted);
}

.card-action {
  text-align: center;
}

.tier-status-hint {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  height: 52px;
  font-size: 15px;
  font-weight: 600;
  border-radius: 50px;
  color: var(--color-text-muted);
  border: 1px solid rgba(115, 115, 115, 0.2);
  background: rgba(115, 115, 115, 0.05);
}

.tier-status-hint.tier-current {
  color: var(--color-success);
  border: 1px solid rgba(34, 197, 94, 0.2);
  background: rgba(34, 197, 94, 0.05);
}

/* ===== 支付记录 ===== */
.records-section {
  max-width: 800px;
  margin: 56px auto 0;
  padding: 0 20px;
}

.records-table-wrap {
  margin-top: 24px;
  background: var(--color-background-tertiary);
  border-radius: var(--radius-lg);
  border: 1px solid var(--color-border);
  overflow: hidden;
}

.records-table-wrap :deep(.ant-table) {
  background: transparent;
}

.records-table-wrap :deep(.ant-table-thead > tr > th) {
  background: rgba(255, 255, 255, 0.03);
  color: var(--color-text-secondary);
  font-size: 13px;
  border-bottom: 1px solid var(--color-border);
}

.records-table-wrap :deep(.ant-table-tbody > tr > td) {
  border-bottom: 1px solid var(--color-border-light);
  color: var(--color-text);
}

.records-table-wrap :deep(.ant-table-tbody > tr:hover > td) {
  background: rgba(255, 255, 255, 0.02);
}

.records-table-wrap :deep(.ant-empty-description) {
  color: var(--color-text-muted);
}

.record-product {
  font-weight: 500;
}

.record-expire {
  font-size: 13px;
  color: var(--color-text-secondary);
}

.record-status {
  font-size: 12px;
  font-weight: 600;
  padding: 2px 10px;
  border-radius: var(--radius-full);
}

.record-status.status-succeeded {
  color: #4ade80;
  background: rgba(34, 197, 94, 0.1);
}

.record-status.status-pending {
  color: #facc15;
  background: rgba(234, 179, 8, 0.1);
}

.record-status.status-failed {
  color: #f87171;
  background: rgba(239, 68, 68, 0.1);
}

.record-status.status-refunded {
  color: var(--color-text-muted);
  background: rgba(115, 115, 115, 0.1);
}

/* ===== 空支付记录 ===== */
.empty-records {
  text-align: center;
  padding: 40px 20px;
}

.empty-text {
  font-size: 15px;
  color: var(--color-text-secondary);
  margin: 0 0 6px;
}

.empty-hint {
  font-size: 13px;
  color: var(--color-text-muted);
  margin: 0;
}

/* ===== 底部保障 ===== */
.assurance-section {
  max-width: 600px;
  margin: 56px auto 0;
  padding: 0 20px;
}

.assurance-items {
  display: flex;
  justify-content: center;
  gap: 40px;
}

.assurance-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: var(--color-text-muted);
}

.assurance-icon {
  font-size: 16px;
}

/* ===== 响应式 ===== */
@media (max-width: 900px) {
  .pricing-grid {
    grid-template-columns: 1fr;
    max-width: 400px;
    margin-inline: auto;
  }

  .hero-title {
    font-size: 30px;
  }

  .status-card {
    flex-direction: column;
    gap: 16px;
    text-align: center;
  }

  .status-left {
    flex-direction: column;
  }

  .assurance-items {
    flex-direction: column;
    align-items: center;
    gap: 16px;
  }
}
</style>
