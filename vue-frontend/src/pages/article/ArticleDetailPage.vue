<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import { getArticleApiArticleTaskIdGet, getExecutionLogsApiArticleExecutionLogsTaskIdGet } from "@/api/article";
import { markdownToHtml } from "@/utils/markdown";
import { message } from "@/message";
import { ARTICLE_STYLE_LABELS, ARTICLE_STATUS_MAP } from "@/utils/article";
import {
  ClockCircleOutlined,
  ArrowLeftOutlined,
  DashboardOutlined,
  CheckCircleFilled,
  CloseCircleFilled,
  SyncOutlined,
} from "@ant-design/icons-vue";

const route = useRoute();
const router = useRouter();

const article = ref<API.ArticleVO | null>(null);
const fullContentHtml = ref("");
const loading = ref(true);

const executionStats = ref<API.AgentExecutionStatsVO | null>(null);
const logsLoading = ref(false);
const logsFetched = ref(false);

const AGENT_NAME_LABELS: Record<string, string> = {
  agent1_generate_titles: "Agent 1 - 生成标题",
  agent2_generate_outline: "Agent 2 - 生成大纲",
  agent3_generate_content: "Agent 3 - 生成正文",
  agent4_analyze_image_requirements: "Agent 4 - 分析图片需求",
  agent5_generate_images: "Agent 5 - 生成图片",
  agent6_merge_content: "Agent 6 - 合并内容",
  ai_modify_outline: "AI 修改大纲",
};

function formatDuration(ms: number | null | undefined): string {
  if (ms == null) return "-";
  if (ms < 1000) return `${ms}ms`;
  if (ms < 60000) return `${(ms / 1000).toFixed(1)}s`;
  return `${Math.floor(ms / 60000)}m ${Math.floor((ms % 60000) / 1000)}s`;
}

function agentLabel(name: string): string {
  return AGENT_NAME_LABELS[name] || name;
}

async function fetchExecutionLogs(taskId: string) {
  if (logsFetched.value) return;
  logsLoading.value = true;
  try {
    const res = await getExecutionLogsApiArticleExecutionLogsTaskIdGet({ task_id: taskId });
    if (res.data.code === 0 && res.data.data) {
      executionStats.value = res.data.data;
    }
  } catch {
    // 日志加载失败不阻塞页面
  } finally {
    logsLoading.value = false;
    logsFetched.value = true;
  }
}

function onCollapseChange(keys: string[]) {
  if (keys.length > 0 && !logsFetched.value) {
    const taskId = route.params.taskId as string;
    fetchExecutionLogs(taskId);
  }
}

async function loadArticle() {
  const taskId = route.params.taskId as string;
  if (!taskId) {
    message.error("缺少文章 ID");
    return;
  }

  loading.value = true;
  try {
    const res = await getArticleApiArticleTaskIdGet({ task_id: taskId });
    if (res.data.code === 0 && res.data.data) {
      article.value = res.data.data;
      if (article.value.fullContent) {
        fullContentHtml.value = markdownToHtml(article.value.fullContent);
      }
    } else {
      message.error(res.data.message || "文章不存在");
    }
  } catch (e: any) {
    message.error(e?.message || "加载文章失败");
  } finally {
    loading.value = false;
  }
}

function goBack() {
  router.back();
}

onMounted(() => {
  loadArticle();
});
</script>

<template>
  <div id="articleDetailPage">
    <div class="container">
      <!-- 顶部导航 -->
      <div class="top-bar">
        <a-button @click="goBack">
          <ArrowLeftOutlined /> 返回
        </a-button>
      </div>

      <a-spin :spinning="loading">
        <article v-if="article" class="article-display">
          <!-- 封面 -->
          <div v-if="article.coverImage" class="article-cover">
            <img :src="article.coverImage" :alt="article.mainTitle || ''" />
          </div>

          <!-- 标题 -->
          <header class="article-header">
            <h1 class="article-title">{{ article.mainTitle }}</h1>
            <p v-if="article.subTitle" class="article-subtitle">{{ article.subTitle }}</p>
            <div class="article-meta">
              <span class="meta-item">
                <ClockCircleOutlined />
                {{ article.createTime }}
              </span>
              <span v-if="article.style" class="meta-tag">
                {{ ARTICLE_STYLE_LABELS[article.style] || article.style }}
              </span>
              <a-tag :color="article.status === 'COMPLETED' ? 'success' : 'processing'">
                {{ ARTICLE_STATUS_MAP[article.status]?.text || article.status }}
              </a-tag>
            </div>
          </header>

          <!-- 正文 -->
          <div
            v-if="fullContentHtml"
            class="article-body markdown-body"
            v-html="fullContentHtml"
          />

          <!-- 智能体执行日志 -->
          <div class="execution-logs">
            <a-collapse
              :bordered="false"
              @change="onCollapseChange"
            >
              <a-collapse-panel key="logs">
                <template #header>
                  <span class="logs-header">
                    <DashboardOutlined />
                    智能体执行日志
                    <span v-if="executionStats" class="logs-summary">
                      {{ executionStats.agentCount }} 个智能体
                      &middot;
                      总耗时 {{ formatDuration(executionStats.totalDurationMs) }}
                      <a-tag
                        :color="executionStats.overallStatus === 'SUCCESS' ? 'success' : executionStats.overallStatus === 'FAILED' ? 'error' : 'processing'"
                        class="logs-status-tag"
                      >
                        {{ executionStats.overallStatus === 'SUCCESS' ? '成功' : executionStats.overallStatus === 'FAILED' ? '失败' : '运行中' }}
                      </a-tag>
                    </span>
                  </span>
                </template>
                <a-spin :spinning="logsLoading">
                  <div v-if="executionStats && executionStats.logs?.length" class="logs-list">
                    <div
                      v-for="log_item in executionStats.logs"
                      :key="log_item.id"
                      class="log-item"
                    >
                      <div class="log-item-left">
                        <CheckCircleFilled
                          v-if="log_item.status === 'SUCCESS'"
                          class="log-status-icon success"
                        />
                        <CloseCircleFilled
                          v-else-if="log_item.status === 'FAILED'"
                          class="log-status-icon failed"
                        />
                        <SyncOutlined
                          v-else
                          spin
                          class="log-status-icon running"
                        />
                        <span class="log-agent-name">{{ agentLabel(log_item.agentName) }}</span>
                      </div>
                      <div class="log-item-right">
                        <span class="log-duration">{{ formatDuration(log_item.durationMs) }}</span>
                        <a-tag
                          :color="log_item.status === 'SUCCESS' ? 'success' : log_item.status === 'FAILED' ? 'error' : 'processing'"
                        >
                          {{ log_item.status === 'SUCCESS' ? '成功' : log_item.status === 'FAILED' ? '失败' : '运行中' }}
                        </a-tag>
                      </div>
                    </div>
                  </div>
                  <div v-else-if="!logsLoading" class="logs-empty">
                    暂无执行日志
                  </div>
                </a-spin>
              </a-collapse-panel>
            </a-collapse>
          </div>

        </article>
      </a-spin>
    </div>
  </div>
</template>

<style scoped>
#articleDetailPage {
  width: 100%;
  min-height: calc(100vh - 64px - 48px);
  padding: 32px 20px 80px;
  background: var(--color-background);
}

.container {
  max-width: 800px;
  margin: 0 auto;
}

.top-bar {
  margin-bottom: 24px;
}

/* 文章展示 */
.article-display {
  background: var(--color-background-tertiary);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  overflow: hidden;
}

.article-cover {
  width: 100%;
  aspect-ratio: 16 / 9;
  overflow: hidden;
  background: var(--color-background-secondary);
}

.article-cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.article-header {
  padding: 36px 48px 28px;
  border-bottom: 1px solid var(--color-border);
}

.article-title {
  font-size: 28px;
  font-weight: 700;
  color: var(--color-text);
  margin: 0 0 10px;
  line-height: 1.35;
  letter-spacing: -0.5px;
}

.article-subtitle {
  font-size: 16px;
  color: var(--color-text-secondary);
  margin: 0 0 16px;
}

.article-meta {
  display: flex;
  align-items: center;
  gap: 12px;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 13px;
  color: var(--color-text-muted);
}

.meta-tag {
  font-size: 12px;
  padding: 2px 10px;
  background: rgba(59, 130, 246, 0.1);
  color: var(--color-primary);
  border-radius: var(--radius-full);
}

.article-body {
  padding: 36px 48px;
}

/* Markdown */
.markdown-body {
  color: var(--color-text);
  font-size: 16px;
  line-height: 1.85;
}

.markdown-body :deep(h1),
.markdown-body :deep(h2),
.markdown-body :deep(h3) {
  color: var(--color-text);
  font-weight: 600;
  margin: 28px 0 14px;
}

.markdown-body :deep(h2) {
  font-size: 22px;
  padding-bottom: 8px;
  border-bottom: 1px solid var(--color-border);
}

.markdown-body :deep(h3) { font-size: 18px; }
.markdown-body :deep(p) { margin: 0 0 16px; }
.markdown-body :deep(strong) { color: var(--color-text); }

.markdown-body :deep(blockquote) {
  border-left: 3px solid var(--color-primary);
  padding: 4px 16px;
  margin: 16px 0;
  color: var(--color-text-secondary);
  background: rgba(59, 130, 246, 0.05);
  border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
}

.markdown-body :deep(code) {
  background: var(--color-background-secondary);
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 14px;
  color: var(--color-accent-cyan-light);
}

.markdown-body :deep(pre) {
  background: var(--color-background-secondary);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  padding: 16px;
  overflow-x: auto;
}

.markdown-body :deep(pre code) {
  background: none;
  padding: 0;
  color: var(--color-text-secondary);
}

.markdown-body :deep(ul),
.markdown-body :deep(ol) { padding-left: 24px; margin: 8px 0 16px; }
.markdown-body :deep(li) { margin-bottom: 6px; }

.markdown-body :deep(img) {
  max-width: 50%;
  border-radius: var(--radius-md);
  margin: 16px auto;
  display: block;
}

.markdown-body :deep(table) { width: 100%; border-collapse: collapse; margin: 16px 0; }
.markdown-body :deep(th),
.markdown-body :deep(td) { border: 1px solid var(--color-border); padding: 10px 14px; text-align: left; }
.markdown-body :deep(th) { background: var(--color-background-secondary); font-weight: 600; }
.markdown-body :deep(hr) { border: none; border-top: 1px solid var(--color-border); margin: 32px 0; }

/* 智能体执行日志 */
.execution-logs {
  border-top: 1px solid var(--color-border);
}

.execution-logs :deep(.ant-collapse) {
  background: transparent;
}

.execution-logs :deep(.ant-collapse > .ant-collapse-item > .ant-collapse-header) {
  padding: 16px 48px;
  font-size: 15px;
  font-weight: 500;
  color: var(--color-text);
}

.logs-header {
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

.logs-summary {
  font-size: 13px;
  font-weight: 400;
  color: var(--color-text-muted);
  margin-left: 4px;
}

.logs-status-tag {
  margin-left: 4px;
}

.execution-logs :deep(.ant-collapse-content-box) {
  padding: 0 48px 24px;
}

.logs-list {
  display: flex;
  flex-direction: column;
  gap: 0;
}

.log-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 0;
  border-bottom: 1px solid rgba(128, 128, 128, 0.12);
}

.log-item:last-child {
  border-bottom: none;
}

.log-item-left {
  display: flex;
  align-items: center;
  gap: 10px;
}

.log-item-right {
  display: flex;
  align-items: center;
  gap: 10px;
}

.log-status-icon {
  font-size: 16px;
}

.log-status-icon.success {
  color: #52c41a;
}

.log-status-icon.failed {
  color: #ff4d4f;
}

.log-status-icon.running {
  color: #1677ff;
}

.log-agent-name {
  font-size: 14px;
  color: var(--color-text);
}

.log-duration {
  font-size: 13px;
  color: var(--color-text-muted);
  font-variant-numeric: tabular-nums;
  min-width: 60px;
  text-align: right;
}

.logs-empty {
  text-align: center;
  padding: 24px 0;
  color: var(--color-text-muted);
  font-size: 14px;
}

@media (max-width: 768px) {
  .article-header {
    padding: 24px;
  }
  .article-body {
    padding: 24px;
  }
  .article-title {
    font-size: 22px;
  }
  .execution-logs :deep(.ant-collapse > .ant-collapse-item > .ant-collapse-header) {
    padding: 14px 24px;
  }
  .execution-logs :deep(.ant-collapse-content-box) {
    padding: 0 24px 20px;
  }
}
</style>
