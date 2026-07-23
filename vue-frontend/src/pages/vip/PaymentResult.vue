<script setup lang="ts">
import { ref, onMounted, onUnmounted } from "vue";
import { useRouter, useRoute } from "vue-router";
import { useLoginUserStore } from "@/stores/loginUser";
import { isVip } from "@/utils/permission";
import { message } from "@/message";
import Button from "@/components/Button.vue";
import {
  CheckCircleFilled,
  CloseCircleFilled,
  CrownOutlined,
  LoadingOutlined,
} from "@ant-design/icons-vue";

const router = useRouter();
const route = useRoute();
const loginUserStore = useLoginUserStore();

// 通过 path 判断成功/取消（不用 route.name 避免中文名变动）
const isSuccess = route.path.startsWith("/payment/success");

// 是否正在刷新
const refreshing = ref(false);
// 是否已确认为 VIP
const vipConfirmed = ref(false);
// 重试次数
const retryCount = ref(0);
const maxRetries = 6; // 最多重试6次，每次间隔3秒 = 18秒
let retryTimer: ReturnType<typeof setInterval> | null = null;

// 刷新登录用户信息
async function refreshUserStatus() {
  refreshing.value = true;
  try {
    await loginUserStore.fetchLoginUser();
    if (isVip(loginUserStore.loginUser)) {
      vipConfirmed.value = true;
      message.success("VIP 已开通，尽情享受会员权益吧！");
      stopPolling();
      return true;
    }
  } catch {
    // 网络异常，继续重试
  } finally {
    refreshing.value = false;
  }
  return false;
}

// 开始轮询刷新（支付成功后 webhook 可能有延迟）
function startPolling() {
  if (retryTimer) return;
  retryTimer = setInterval(async () => {
    retryCount.value++;
    const ok = await refreshUserStatus();
    if (ok || retryCount.value >= maxRetries) {
      stopPolling();
    }
  }, 3000);
}

function stopPolling() {
  if (retryTimer) {
    clearInterval(retryTimer);
    retryTimer = null;
  }
}

// 前往 VIP 页面
function goToVip() {
  router.replace("/vip");
}

onMounted(async () => {
  if (isSuccess) {
    // 先刷新一次，如果不是 VIP 就开始轮询
    const ok = await refreshUserStatus();
    if (!ok) {
      startPolling();
    }
  }
});

onUnmounted(() => {
  stopPolling();
});
</script>

<template>
  <div id="paymentResultPage">
    <div class="result-container">
      <!-- 成功 -->
      <template v-if="isSuccess">
        <!-- 已确认 VIP -->
        <template v-if="vipConfirmed">
          <div class="result-icon success">
            <CheckCircleFilled />
          </div>
          <h1 class="result-title">VIP 已开通！</h1>
          <p class="result-desc">
            恭喜，你已经成功开通 VIP 会员，所有功能已解锁
          </p>
          <div class="result-crown">
            <CrownOutlined />
          </div>
        </template>

        <!-- 等待 webhook 处理 -->
        <template v-else>
          <div class="result-icon processing">
            <LoadingOutlined />
          </div>
          <h1 class="result-title">支付成功</h1>
          <p class="result-desc">
            会员正在开通中，请稍等片刻...
          </p>
          <div class="retry-info" v-if="retryCount > 0">
            正在确认开通状态（{{ retryCount }}/{{ maxRetries }}）
          </div>
          <div class="retry-info" v-if="retryCount >= maxRetries">
            开通可能稍有延迟，请稍后手动刷新
          </div>
        </template>
      </template>

      <!-- 取消 -->
      <template v-else>
        <div class="result-icon cancel">
          <CloseCircleFilled />
        </div>
        <h1 class="result-title">支付已取消</h1>
        <p class="result-desc">
          你没有完成支付，可以随时回来购买 VIP 会员
        </p>
      </template>

      <!-- 操作按钮 -->
      <div class="result-actions">
        <Button
          v-if="isSuccess"
          variant="gradient"
          size="lg"
          @click="goToVip"
        >
          <CrownOutlined />
          查看我的 VIP
        </Button>
        <Button
          v-if="isSuccess"
          variant="secondary"
          size="lg"
          :disabled="refreshing"
          @click="refreshUserStatus"
        >
          {{ refreshing ? "刷新中..." : "刷新会员状态" }}
        </Button>

        <template v-else>
          <Button variant="gradient" size="lg" @click="goToVip">
            <CrownOutlined />
            返回重新选购
          </Button>
          <Button variant="secondary" size="lg" @click="router.push('/')">
            返回首页
          </Button>
        </template>
      </div>
    </div>
  </div>
</template>

<style scoped>
#paymentResultPage {
  min-height: calc(100vh - 64px);
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--color-background);
  padding: 40px 20px;
}

.result-container {
  text-align: center;
  max-width: 420px;
}

/* 图标 */
.result-icon {
  font-size: 64px;
  margin-bottom: 20px;
  line-height: 1;
}

.result-icon.success {
  color: var(--color-success);
  filter: drop-shadow(0 0 20px rgba(34, 197, 94, 0.3));
}

.result-icon.processing {
  color: var(--color-accent-cyan);
  animation: spin 1.5s linear infinite;
}

.result-icon.cancel {
  color: var(--color-text-muted);
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* 标题 */
.result-title {
  font-family: "Outfit", "Work Sans", sans-serif;
  font-size: 28px;
  font-weight: 700;
  color: var(--color-text);
  margin: 0 0 8px;
}

.result-desc {
  font-size: 15px;
  color: var(--color-text-secondary);
  margin: 0 0 28px;
  line-height: 1.6;
}

/* 皇冠 */
.result-crown {
  font-size: 36px;
  color: #facc15;
  margin-bottom: 16px;
  filter: drop-shadow(0 0 12px rgba(250, 204, 21, 0.25));
}

/* 重试信息 */
.retry-info {
  font-size: 13px;
  color: var(--color-text-muted);
  margin-bottom: 8px;
}

/* 按钮 */
.result-actions {
  display: flex;
  flex-direction: column;
  gap: 12px;
  align-items: center;
}
</style>
