<script setup lang="ts">
import { computed } from "vue";
import {
  ClockCircleOutlined,
  InfoCircleOutlined,
  CheckCircleFilled,
  BulbOutlined,
  ArrowRightOutlined,
  CrownOutlined,
} from "@ant-design/icons-vue";
import { isVip } from "@/utils/permission";

const props = withDefaults(
  defineProps<{
    isCreating?: boolean;
    isCompleted?: boolean;
    article?: API.ArticleVO | null;
    loginUser?: API.LoginUserVO | null;
    doneCount?: number;
    totalSteps?: number;
    elapsedDisplay?: string;
    currentAgentTitle?: string;
    realtimeWordCount?: number;
    realtimeImageCount?: number;
    finalWordCount?: number;
    finalImageCount?: number;
  }>(),
  {
    isCreating: false,
    isCompleted: false,
    article: null,
    loginUser: null,
    doneCount: 0,
    totalSteps: 0,
    elapsedDisplay: "00:00",
    currentAgentTitle: undefined,
    realtimeWordCount: 0,
    realtimeImageCount: 0,
    finalWordCount: 0,
    finalImageCount: 0,
  },
);

const emit = defineEmits<{
  (e: "selectHotTopic", topicText: string): void;
}>();

const userIsVip = computed(() => isVip(props.loginUser ?? undefined));
const quota = computed(() => props.loginUser?.quota ?? 0);

// 热门选题
const hotTopics = [
  { emoji: "🔥", text: "2026年最值得学习的5个前端框架" },
  { emoji: "💡", text: "程序员如何通过写作提升影响力" },
  { emoji: "🚀", text: "从零到百万用户的产品增长策略" },
  { emoji: "🤖", text: "AI 时代开发者如何保持竞争力" },
  { emoji: "📈", text: "小红书运营技巧：30天涨粉10万" },
  { emoji: "🎯", text: "副业赚钱的7种实战方法" },
];
</script>

<template>
  <aside class="right-panel">
    <!-- 会员状态 & 配额 -->
    <div v-if="loginUser?.id" class="panel-card quota-card">
      <div class="panel-header">
        <CrownOutlined class="panel-header-icon" :class="{ vip: userIsVip }" />
        <span>会员状态</span>
      </div>
      <div class="quota-info">
        <div class="quota-row">
          <span class="quota-label-text">当前身份</span>
          <span :class="['quota-badge', userIsVip ? 'vip' : 'free']">
            {{ userIsVip ? 'VIP 会员' : '免费用户' }}
          </span>
        </div>
        <div class="quota-row">
          <span class="quota-label-text">剩余配额</span>
          <span class="quota-value-text">
            {{ userIsVip ? '无限' : quota }}
          </span>
        </div>
      </div>
      <div v-if="!userIsVip" class="quota-upgrade">
        <RouterLink to="/vip" class="upgrade-link">
          <CrownOutlined />
          升级 VIP 享无限配额
        </RouterLink>
      </div>
    </div>

    <!-- 创作中：实时进度 -->
    <div v-if="isCreating" class="panel-card">
      <div class="panel-header">
        <ClockCircleOutlined class="panel-header-icon" />
        <span>创作进度</span>
      </div>
      <div class="stats-grid">
        <div class="stat-item">
          <span class="stat-value accent">{{ doneCount }}</span>
          <span class="stat-label">已完成</span>
        </div>
        <div class="stat-item">
          <span class="stat-value">{{ totalSteps - doneCount }}</span>
          <span class="stat-label">剩余</span>
        </div>
        <div class="stat-item">
          <span class="stat-value">{{ elapsedDisplay }}</span>
          <span class="stat-label">耗时</span>
        </div>
      </div>
      <div v-if="currentAgentTitle" class="current-task">
        <span class="current-dot" />
        <span>正在：{{ currentAgentTitle }}</span>
      </div>
    </div>

    <!-- 文章信息统计（创作中 & 完成后） -->
    <div v-if="isCreating || (isCompleted && article)" class="panel-card">
      <div class="panel-header">
        <InfoCircleOutlined class="panel-header-icon" />
        <span>文章信息</span>
      </div>
      <div class="stats-grid">
        <div class="stat-item">
          <span class="stat-value accent">
            {{ isCreating ? realtimeWordCount : finalWordCount }}
          </span>
          <span class="stat-label">总字数</span>
        </div>
        <div class="stat-item">
          <span class="stat-value">
            {{ isCreating ? realtimeImageCount : finalImageCount }}
          </span>
          <span class="stat-label">配图数</span>
        </div>
      </div>
    </div>

    <!-- 完成：耗时统计 -->
    <div v-if="isCompleted && article" class="panel-card">
      <div class="panel-header">
        <CheckCircleFilled class="panel-header-icon success" />
        <span>创作完成</span>
      </div>
      <div class="stats-grid">
        <div class="stat-item">
          <span class="stat-value accent">{{ elapsedDisplay }}</span>
          <span class="stat-label">总耗时</span>
        </div>
        <div class="stat-item">
          <span class="stat-value">{{ article.fullContent?.length || 0 }}</span>
          <span class="stat-label">总字符</span>
        </div>
        <div class="stat-item">
          <span class="stat-value">{{ article.images?.length || 0 }}</span>
          <span class="stat-label">配图数</span>
        </div>
      </div>
    </div>

    <!-- 热门选题（非创作中显示） -->
    <div v-if="!isCreating && !isCompleted" class="panel-card">
      <div class="panel-header">
        <BulbOutlined class="panel-header-icon" />
        <span>热门选题</span>
      </div>
      <div class="hot-topics">
        <div
          v-for="(item, i) in hotTopics"
          :key="i"
          class="hot-topic-item"
          @click="emit('selectHotTopic', item.text)"
        >
          <span class="hot-emoji">{{ item.emoji }}</span>
          <span class="hot-text">{{ item.text }}</span>
          <ArrowRightOutlined class="hot-arrow" />
        </div>
      </div>
    </div>

    <!-- 创作中：创作小贴士 -->
    <div v-if="isCreating" class="panel-card">
      <div class="panel-header">
        <BulbOutlined class="panel-header-icon" />
        <span>创作小贴士</span>
      </div>
      <div class="tips-list">
        <div class="tip-item">
          <span class="tip-dot" />
          <span>选题越具体，生成效果越好</span>
        </div>
        <div class="tip-item">
          <span class="tip-dot" />
          <span>选择合适的风格让文章更精准</span>
        </div>
        <div class="tip-item">
          <span class="tip-dot" />
          <span>配图方式越多，文章越丰富</span>
        </div>
        <div class="tip-item">
          <span class="tip-dot" />
          <span>完成后可复制全文到编辑器</span>
        </div>
      </div>
    </div>
  </aside>
</template>

<style scoped lang="scss">
.right-panel {
  padding: 24px 16px;
  overflow-y: auto;
  background: var(--color-background-secondary);
  border-left: 1px solid var(--color-border);
}

.panel-card {
  margin-bottom: 20px;
}

.panel-card:last-child {
  margin-bottom: 0;
}

.panel-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  font-weight: 600;
  color: var(--color-text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 1px solid var(--color-border);
}

.panel-header-icon {
  font-size: 14px;
  color: var(--color-primary);
}

.panel-header-icon.success {
  color: var(--color-success);
}

.panel-header-icon.vip {
  color: #facc15;
}

/* 会员状态 & 配额 */
.quota-card {
  background: var(--color-background-tertiary);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: 16px;
  margin-bottom: 20px;
}

.quota-card .panel-header {
  margin-bottom: 12px;
  padding-bottom: 10px;
}

.quota-info {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.quota-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.quota-label-text {
  font-size: 13px;
  color: var(--color-text-muted);
}

.quota-badge {
  font-size: 12px;
  font-weight: 600;
  padding: 2px 10px;
  border-radius: var(--radius-full);
}

.quota-badge.vip {
  color: #facc15;
  background: rgba(250, 204, 21, 0.1);
}

.quota-badge.free {
  color: var(--color-text-muted);
  background: rgba(115, 115, 115, 0.1);
}

.quota-value-text {
  font-family: "Outfit", sans-serif;
  font-size: 16px;
  font-weight: 700;
  color: var(--color-text);
}

.quota-upgrade {
  margin-top: 14px;
  padding-top: 12px;
  border-top: 1px solid var(--color-border);
}

.upgrade-link {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  font-size: 13px;
  font-weight: 600;
  color: var(--color-primary);
  text-decoration: none;
  padding: 8px;
  border-radius: var(--radius-md);
  background: rgba(59, 130, 246, 0.08);
  transition: all var(--transition-fast);
}

.upgrade-link:hover {
  background: rgba(59, 130, 246, 0.15);
  color: var(--color-primary-light);
}

/* 统计 */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 8px;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 12px 8px;
  background: var(--color-background-tertiary);
  border-radius: var(--radius-md);
  border: 1px solid var(--color-border);
}

.stat-value {
  font-size: 20px;
  font-weight: 700;
  color: var(--color-text);
  font-family: "Outfit", sans-serif;
}

.stat-value.accent {
  background: var(--gradient-primary);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.stat-label {
  font-size: 11px;
  color: var(--color-text-muted);
  margin-top: 2px;
}

.current-task {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: 14px;
  padding: 10px 12px;
  background: var(--color-background-tertiary);
  border-radius: var(--radius-md);
  font-size: 13px;
  color: var(--color-text-secondary);
}

.current-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--color-primary);
  animation: pulse 1.5s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.4; }
}

/* 热门选题 */
.hot-topics {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.hot-topic-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 10px;
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all var(--transition-fast);
  color: var(--color-text-secondary);
}

.hot-topic-item:hover {
  background: var(--color-background-tertiary);
  color: var(--color-text);
}

.hot-emoji {
  font-size: 14px;
  flex-shrink: 0;
}

.hot-text {
  font-size: 13px;
  line-height: 1.4;
  flex: 1;
}

.hot-arrow {
  font-size: 11px;
  opacity: 0;
  color: var(--color-primary);
  transition: all var(--transition-fast);
  flex-shrink: 0;
}

.hot-topic-item:hover .hot-arrow {
  opacity: 1;
}

/* 创作小贴士 */
.tips-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.tip-item {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  font-size: 12px;
  color: var(--color-text-secondary);
  line-height: 1.5;
}

.tip-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--color-primary);
  margin-top: 6px;
  flex-shrink: 0;
  opacity: 0.5;
}
</style>
