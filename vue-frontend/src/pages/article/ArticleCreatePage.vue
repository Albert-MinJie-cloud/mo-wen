<script setup lang="ts">
import { ref, reactive, computed } from "vue";
import { useRouter } from "vue-router";
import { message } from "@/message";
import { createArticleApiArticleCreatePost, getArticleApiArticleTaskIdGet } from "@/api/article";
import { connectSSE, closeSSE, type SSEMessage } from "@/utils/sse";
import { markdownToHtml } from "@/utils/markdown";
import { ARTICLE_STYLE_OPTIONS, IMAGE_METHOD_OPTIONS, getWordCount } from "@/utils/article";
import {
  FileTextOutlined,
  OrderedListOutlined,
  EditOutlined,
  PictureOutlined,
  ThunderboltOutlined,
  MergeCellsOutlined,
  CheckCircleFilled,
  LoadingOutlined,
  ClockCircleOutlined,
  ExclamationCircleFilled,
  ReloadOutlined,
  BulbOutlined,
  RocketOutlined,
  ArrowRightOutlined,
  InfoCircleOutlined,
} from "@ant-design/icons-vue";

const router = useRouter();

// ============ 核心状态 ============
const isCreating = ref(false);
const isCompleted = ref(false);
const taskId = ref("");
const errorMessage = ref("");

// ============ 输入状态 ============
const topic = ref("");
const style = ref<string | null>(null);
const enabledImageMethods = ref<string[]>([]);

// 热门选题
const hotTopics = [
  { emoji: "🔥", text: "2026年最值得学习的5个前端框架" },
  { emoji: "💡", text: "程序员如何通过写作提升影响力" },
  { emoji: "🚀", text: "从零到百万用户的产品增长策略" },
  { emoji: "🤖", text: "AI 时代开发者如何保持竞争力" },
  { emoji: "📈", text: "小红书运营技巧：30天涨粉10万" },
  { emoji: "🎯", text: "副业赚钱的7种实战方法" },
];

// ============ 创作进度 ============
interface AgentStep {
  key: string;
  icon: any;
  title: string;
  desc: string;
  status: "waiting" | "processing" | "done" | "error";
}

const agentSteps = reactive<AgentStep[]>([
  { key: "AGENT1", icon: FileTextOutlined, title: "标题生成", desc: "分析选题，生成吸睛标题", status: "waiting" },
  { key: "AGENT2", icon: OrderedListOutlined, title: "大纲规划", desc: "构建逻辑清晰的文章骨架", status: "waiting" },
  { key: "AGENT3", icon: EditOutlined, title: "正文撰写", desc: "逐步生成高质量正文内容", status: "waiting" },
  { key: "AGENT4", icon: PictureOutlined, title: "封面设计", desc: "匹配文章主题生成封面", status: "waiting" },
  { key: "AGENT5", icon: ThunderboltOutlined, title: "智能配图", desc: "搜索与内容匹配的配图", status: "waiting" },
]);

const outlineText = ref("");
const contentText = ref("");
const titleOptions = ref<API.TitleOption[]>([]);
const selectedTitleIndex = ref(-1);
const generatedImages = ref<any[]>([]);

// 耗时统计
const startTime = ref(0);
const elapsedSeconds = ref(0);
let timerInterval: ReturnType<typeof setInterval> | null = null;

// ============ 完成状态 ============
const article = ref<API.ArticleVO | null>(null);
const fullContentHtml = ref("");

// ============ 计算属性 ============
const eventSource = ref<EventSource | null>(null);
const canSubmit = computed(() => topic.value.trim().length > 0 && !isCreating.value);

const doneCount = computed(() => agentSteps.filter((s) => s.status === "done").length);
const totalSteps = computed(() => agentSteps.length);
const currentAgent = computed(() => agentSteps.find((s) => s.status === "processing"));

// 实时字数
const realtimeWordCount = computed(() =>
  getWordCount(outlineText.value + contentText.value)
);
const realtimeImageCount = computed(() => generatedImages.value.length);

const finalWordCount = computed(() => getWordCount(article.value?.fullContent));
const finalImageCount = computed(() => article.value?.images?.length || 0);

const elapsedDisplay = computed(() => {
  const s = elapsedSeconds.value;
  const min = Math.floor(s / 60);
  const sec = s % 60;
  return `${min.toString().padStart(2, "0")}:${sec.toString().padStart(2, "0")}`;
});

// ============ 表单方法 ============
function selectHotTopic(topicText: string) {
  topic.value = topicText;
}

function toggleImageMethod(method: string) {
  const idx = enabledImageMethods.value.indexOf(method);
  if (idx >= 0) {
    enabledImageMethods.value.splice(idx, 1);
  } else {
    enabledImageMethods.value.push(method);
  }
}

// ============ 进度方法 ============
function updateAgentStep(key: string, status: "processing" | "done" | "error") {
  const step = agentSteps.find((s) => s.key === key);
  if (step) step.status = status;
}

function startTimer() {
  startTime.value = Date.now();
  elapsedSeconds.value = 0;
  timerInterval = setInterval(() => {
    elapsedSeconds.value = Math.floor((Date.now() - startTime.value) / 1000);
  }, 1000);
}

function stopTimer() {
  if (timerInterval) {
    clearInterval(timerInterval);
    timerInterval = null;
  }
}

// ============ SSE 消息处理 ============
function handleSSEMessage(data: SSEMessage) {
  switch (data.type) {
    case "AGENT_START":
      if (data.agent) {
        const agentKeyMap: Record<string, string> = {
          Agent1: "AGENT1", Agent2: "AGENT2", Agent3: "AGENT3",
          Agent4: "AGENT4", Agent5: "AGENT5", Merge: "MERGE",
        };
        const key = agentKeyMap[data.agent] || "";
        if (key) updateAgentStep(key, "processing");
      }
      break;

    case "AGENT1_COMPLETE":
      updateAgentStep("AGENT1", "done");
      if (data.titleOptions) titleOptions.value = data.titleOptions;
      break;

    case "AGENT2_STREAMING":
      updateAgentStep("AGENT2", "processing");
      if (data.content) outlineText.value += data.content;
      break;
    case "AGENT2_COMPLETE":
      updateAgentStep("AGENT2", "done");
      break;

    case "AGENT3_STREAMING":
      updateAgentStep("AGENT3", "processing");
      if (data.content) contentText.value += data.content;
      break;
    case "AGENT3_COMPLETE":
      updateAgentStep("AGENT3", "done");
      break;

    case "AGENT4_COMPLETE":
      updateAgentStep("AGENT4", "done");
      break;

    case "IMAGE_COMPLETE":
      updateAgentStep("AGENT5", "processing");
      if (data.image) generatedImages.value.push(data.image);
      break;
    case "AGENT5_COMPLETE":
      updateAgentStep("AGENT5", "done");
      break;

    case "ALL_COMPLETE":
      stopTimer();
      onCreationComplete();
      break;

    case "ERROR":
      stopTimer();
      const active = agentSteps.find((s) => s.status === "processing");
      if (active) updateAgentStep(active.key, "error");
      errorMessage.value = data.message || "生成过程出错";
      message.error(errorMessage.value);
      break;
  }
}

// ============ 主流程 ============
async function startCreate() {
  if (!canSubmit.value) return;

  // 重置
  isCreating.value = true;
  isCompleted.value = false;
  errorMessage.value = "";
  outlineText.value = "";
  contentText.value = "";
  titleOptions.value = [];
selectedTitleIndex.value = -1;
  generatedImages.value = [];
  article.value = null;
  fullContentHtml.value = "";
  agentSteps.forEach((s) => (s.status = "waiting"));
  startTimer();

  try {
    const res = await createArticleApiArticleCreatePost(
      {},
      {
        topic: topic.value.trim(),
        style: style.value || undefined,
        enabledImageMethods:
          enabledImageMethods.value.length > 0 ? enabledImageMethods.value : undefined,
      }
    );

    if (res.data.code === 0 && res.data.data) {
      taskId.value = res.data.data;
      eventSource.value = connectSSE(taskId.value, {
        onMessage: handleSSEMessage,
        onError: () => {
          stopTimer();
          isCreating.value = false;
          message.error("连接中断，请刷新重试");
        },
        onComplete: () => {
          eventSource.value = null;
        },
      });
    } else {
      throw new Error(res.data.message || "创建任务失败");
    }
  } catch (e: any) {
    stopTimer();
    isCreating.value = false;
    errorMessage.value = e?.message || "创建任务失败，请重试";
    message.error(errorMessage.value);
  }
}

async function onCreationComplete() {
  isCreating.value = false;
  isCompleted.value = true;

  try {
    const res = await getArticleApiArticleTaskIdGet({ task_id: taskId.value });
    if (res.data.code === 0 && res.data.data) {
      article.value = res.data.data;
      if (article.value.fullContent) {
        fullContentHtml.value = markdownToHtml(article.value.fullContent);
      }
    }
  } catch (e) {
    console.error("获取文章详情失败:", e);
  }
}

function resetState() {
  closeSSE(eventSource.value);
  eventSource.value = null;
  stopTimer();
  isCreating.value = false;
  isCompleted.value = false;
  topic.value = "";
  style.value = null;
  enabledImageMethods.value = [];
  taskId.value = "";
  errorMessage.value = "";
  outlineText.value = "";
  contentText.value = "";
  titleOptions.value = [];
selectedTitleIndex.value = -1;
  generatedImages.value = [];
  article.value = null;
  fullContentHtml.value = "";
  agentSteps.forEach((s) => (s.status = "waiting"));
}

function viewInList() {
  router.push("/article/list");
}
</script>

<template>
  <div id="articleCreatePage">
    <div class="three-col">
      <!-- ============ 左栏：智能体流程 ============ -->
      <aside class="left-panel">
        <div class="panel-card">
          <div class="panel-header">
            <RocketOutlined class="panel-header-icon" />
            <span>智能体流水线</span>
          </div>

          <div class="pipeline">
            <div
              v-for="(step, index) in agentSteps"
              :key="step.key"
              :class="['pipeline-node', step.status]"
            >
              <!-- 连接线 -->
              <div
                v-if="index > 0"
                :class="['pipeline-line', { active: step.status !== 'waiting' }]"
              />

              <!-- 节点 -->
              <div class="node-body">
                <div :class="['node-icon-wrap', step.status]">
                  <component :is="step.icon" class="node-icon" />
                  <CheckCircleFilled v-if="step.status === 'done'" class="node-badge" />
                  <LoadingOutlined v-if="step.status === 'processing'" class="node-badge spinning" />
                  <ExclamationCircleFilled v-if="step.status === 'error'" class="node-badge error-badge" />
                </div>
                <div class="node-text">
                  <span class="node-title">{{ step.title }}</span>
                  <span class="node-desc">{{ step.desc }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- 进度条 -->
          <div v-if="isCreating || isCompleted" class="pipeline-progress">
            <div class="progress-text">
              {{ doneCount }} / {{ totalSteps }} 完成
            </div>
            <div class="progress-track">
              <div
                class="progress-fill"
                :style="{ width: (doneCount / totalSteps) * 100 + '%' }"
              />
            </div>
          </div>
        </div>
      </aside>

      <!-- ============ 中栏：主内容区 ============ -->
      <main class="center-panel">
        <!-- 状态一：输入表单 -->
        <div v-if="!isCreating && !isCompleted" class="center-card">
          <div class="center-card-header">
            <h2 class="center-card-title">创作新文章</h2>
            <p class="center-card-subtitle">输入选题，AI 智能体将自动协作完成创作</p>
          </div>

          <div class="form-section">
            <label class="form-label">
              <FileTextOutlined /> 文章选题
            </label>
            <a-textarea
              v-model:value="topic"
              placeholder="请输入你想创作的文章主题..."
              :rows="3"
              :maxlength="500"
              show-count
              class="topic-textarea"
            />
          </div>

          <div class="form-section">
            <label class="form-label">
              <EditOutlined /> 文章风格
            </label>
            <div class="style-chips">
              <span
                v-for="opt in ARTICLE_STYLE_OPTIONS"
                :key="opt.value"
                :class="['style-chip', { active: style === opt.value }]"
                @click="style = style === opt.value ? null : opt.value"
              >
                {{ opt.label }}
              </span>
            </div>
          </div>

          <div class="form-section">
            <label class="form-label">
              <PictureOutlined /> 配图方式
              <span class="label-hint">（留空支持全部）</span>
            </label>
            <div class="image-method-chips">
              <span
                v-for="opt in IMAGE_METHOD_OPTIONS"
                :key="opt.value"
                :class="['method-chip', { active: enabledImageMethods.includes(opt.value) }]"
                :title="opt.desc"
                @click="toggleImageMethod(opt.value)"
              >
                {{ opt.label }}
              </span>
            </div>
          </div>

          <div class="form-actions">
            <a-button type="primary" size="large" :disabled="!canSubmit" @click="startCreate">
              <RocketOutlined /> 开始创作
            </a-button>
          </div>
        </div>

        <!-- 状态二：流式输出 -->
        <div v-if="isCreating && !isCompleted" class="center-card streaming-view">
          <div class="streaming-topic">
            <span class="topic-badge">正在创作</span>
            <h2 class="topic-text">{{ topic }}</h2>
          </div>

          <!-- 标题选项 -->
          <div v-if="titleOptions.length > 0" class="stream-section">
            <h3 class="stream-section-title">备选标题</h3>
            <div class="title-cards">
              <div
                v-for="(opt, i) in titleOptions"
                :key="i"
                :class="['title-card', { selected: selectedTitleIndex === i }]"
                @click="selectedTitleIndex = selectedTitleIndex === i ? -1 : i"
              >
                <span :class="['title-rank', { selected: selectedTitleIndex === i }]">
                  <CheckCircleFilled v-if="selectedTitleIndex === i" />
                  <span v-else>{{ i + 1 }}</span>
                </span>
                <div>
                  <p class="t-main">{{ opt.mainTitle }}</p>
                  <p class="t-sub">{{ opt.subTitle }}</p>
                </div>
              </div>
            </div>
          </div>

          <!-- 大纲 -->
          <div v-if="outlineText" class="stream-section">
            <h3 class="stream-section-title">文章大纲</h3>
            <pre class="stream-block">{{ outlineText }}</pre>
          </div>

          <!-- 正文 -->
          <div v-if="contentText" class="stream-section">
            <h3 class="stream-section-title">正文内容</h3>
            <pre class="stream-block content-block">{{ contentText }}</pre>
          </div>

          <!-- 配图 -->
          <div v-if="generatedImages.length > 0" class="stream-section">
            <h3 class="stream-section-title">已生成配图 · {{ generatedImages.length }}</h3>
            <div class="stream-images">
              <div v-for="(img, i) in generatedImages" :key="i" class="stream-img-item">
                <img :src="img.url" :alt="img.description || '配图'" />
              </div>
            </div>
          </div>

          <!-- 空状态 -->
          <div v-if="!titleOptions.length && !outlineText && !contentText" class="stream-waiting">
            <a-spin size="large" />
            <p>AI 智能体正在准备中...</p>
          </div>
        </div>

        <!-- 状态三：完成文章 -->
        <div v-if="isCompleted" class="center-card article-view">
          <div class="article-top-bar">
            <a-button size="small" @click="viewInList">文章列表</a-button>
            <a-button type="primary" size="small" @click="resetState">
              <ReloadOutlined /> 继续创作
            </a-button>
          </div>

          <article v-if="article">
            <div v-if="article.coverImage" class="article-cover-img">
              <img :src="article.coverImage" :alt="article.mainTitle || ''" />
            </div>

            <header class="article-header">
              <h1 class="article-title">{{ article.mainTitle }}</h1>
              <p v-if="article.subTitle" class="article-subtitle">{{ article.subTitle }}</p>
              <div class="article-tags">
                <span class="article-tag">
                  <ClockCircleOutlined /> {{ article.createTime }}
                </span>
                <span v-if="article.style" class="article-tag style-tag">
                  {{ ARTICLE_STYLE_OPTIONS.find((s) => s.value === article.style)?.label || article.style }}
                </span>
              </div>
            </header>

            <div v-if="fullContentHtml" class="article-body markdown-body" v-html="fullContentHtml" />

            <div v-if="article.images?.length" class="article-images-section">
              <h3>配图</h3>
              <div class="image-gallery">
                <div v-for="(img, i) in article.images" :key="i" class="gallery-item">
                  <img :src="img.url" :alt="img.description || '配图'" />
                  <p v-if="img.description" class="gallery-desc">{{ img.description }}</p>
                </div>
              </div>
            </div>
          </article>

          <div v-else class="article-loading">
            <a-spin />
          </div>
        </div>
      </main>

      <!-- ============ 右栏：辅助信息 ============ -->
      <aside class="right-panel">
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
          <div v-if="currentAgent" class="current-task">
            <span class="current-dot" />
            <span>正在：{{ currentAgent.title }}</span>
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
              @click="selectHotTopic(item.text)"
            >
              <span class="hot-emoji">{{ item.emoji }}</span>
              <span class="hot-text">{{ item.text }}</span>
              <ArrowRightOutlined class="hot-arrow" />
            </div>
          </div>
        </div>

        <!-- 创作中：也展示热门选题（收起） -->
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
    </div>
  </div>
</template>

<style scoped>
#articleCreatePage {
  width: 100%;
  min-height: calc(100vh - 64px - 48px);
  background: var(--color-background);
}

/* ============ 三栏布局 ============ */
.three-col {
  display: grid;
  grid-template-columns: 260px 1fr 280px;
  gap: 0;
  height: calc(100vh - 64px - 48px);
  overflow: hidden;
}

/* ============ 左右面板通用 ============ */
.left-panel,
.right-panel {
  padding: 24px 16px;
  overflow-y: auto;
  background: var(--color-background-secondary);
  border-right: 1px solid var(--color-border);
}

.right-panel {
  border-right: none;
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

/* ============ 左栏：智能体流水线 ============ */
.pipeline {
  display: flex;
  flex-direction: column;
  gap: 0;
}

.pipeline-node {
  display: flex;
  flex-direction: column;
}

.pipeline-line {
  width: 2px;
  height: 16px;
  margin-left: 21px;
  background: var(--color-border);
  transition: background var(--transition-normal);
}

.pipeline-line.active {
  background: var(--color-primary);
}

.node-body {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 6px 0;
}

.node-icon-wrap {
  width: 44px;
  height: 44px;
  border-radius: var(--radius-lg);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  background: var(--color-background-tertiary);
  border: 1.5px solid var(--color-border);
  position: relative;
  transition: all var(--transition-fast);
}

.node-icon {
  font-size: 18px;
  color: var(--color-text-muted);
  transition: color var(--transition-fast);
}

.node-badge {
  position: absolute;
  bottom: -3px;
  right: -3px;
  font-size: 12px;
  color: var(--color-success);
  background: var(--color-background-secondary);
  border-radius: 50%;
}

.node-badge.spinning {
  color: var(--color-primary);
  animation: spin 1s linear infinite;
}

.node-badge.error-badge {
  color: var(--color-error);
}

/* 节点状态样式 */
.pipeline-node.processing .node-icon-wrap {
  border-color: var(--color-primary);
  box-shadow: 0 0 12px rgba(59, 130, 246, 0.25);
  background: rgba(59, 130, 246, 0.1);
}

.pipeline-node.processing .node-icon {
  color: var(--color-primary);
}

.pipeline-node.done .node-icon-wrap {
  border-color: rgba(34, 197, 94, 0.4);
  background: rgba(34, 197, 94, 0.06);
}

.pipeline-node.done .node-icon {
  color: var(--color-success);
}

.pipeline-node.error .node-icon-wrap {
  border-color: rgba(239, 68, 68, 0.4);
  background: rgba(239, 68, 68, 0.06);
}

.pipeline-node.error .node-icon {
  color: var(--color-error);
}

.node-text {
  display: flex;
  flex-direction: column;
  gap: 2px;
  padding-top: 3px;
}

.node-title {
  font-size: 13px;
  font-weight: 600;
  color: var(--color-text-muted);
  transition: color var(--transition-fast);
}

.pipeline-node.processing .node-title {
  color: var(--color-text);
}

.pipeline-node.done .node-title {
  color: var(--color-text-secondary);
}

.node-desc {
  font-size: 11px;
  color: var(--color-text-muted);
  line-height: 1.4;
}

/* 流水线进度 */
.pipeline-progress {
  margin-top: 20px;
  padding-top: 16px;
  border-top: 1px solid var(--color-border);
}

.progress-text {
  font-size: 12px;
  color: var(--color-text-secondary);
  margin-bottom: 8px;
  font-weight: 500;
}

.progress-track {
  height: 4px;
  background: var(--color-border);
  border-radius: 2px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: var(--gradient-primary);
  border-radius: 2px;
  transition: width 0.5s ease;
}

/* ============ 中栏：主内容 ============ */
.center-panel {
  overflow-y: auto;
  padding: 32px 40px;
}

.center-card {
  max-width: 760px;
  margin: 0 auto;
}

.center-card-header {
  margin-bottom: 36px;
}

.center-card-title {
  font-size: 26px;
  font-weight: 700;
  color: var(--color-text);
  margin: 0 0 8px;
  letter-spacing: -0.5px;
}

.center-card-subtitle {
  font-size: 15px;
  color: var(--color-text-secondary);
  margin: 0;
}

/* 表单 */
.form-section {
  margin-bottom: 28px;
}

.form-label {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 14px;
  font-weight: 600;
  color: var(--color-text);
  margin-bottom: 10px;
}

.label-hint {
  font-weight: 400;
  font-size: 12px;
  color: var(--color-text-muted);
}

.topic-textarea :deep(textarea) {
  background: var(--color-background-tertiary) !important;
  border-color: var(--color-border) !important;
  color: var(--color-text) !important;
  font-size: 15px;
  line-height: 1.7;
  resize: none;
  border-radius: var(--radius-md) !important;
}

.topic-textarea :deep(textarea):focus {
  border-color: var(--color-primary) !important;
  box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.15) !important;
}

.style-chips,
.image-method-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.style-chip,
.method-chip {
  padding: 6px 14px;
  border-radius: var(--radius-full);
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all var(--transition-fast);
  background: var(--color-background-tertiary);
  border: 1px solid var(--color-border);
  color: var(--color-text-secondary);
}

.style-chip:hover,
.method-chip:hover {
  border-color: var(--color-primary-light);
  color: var(--color-text);
}

.style-chip.active,
.method-chip.active {
  background: rgba(59, 130, 246, 0.12);
  border-color: var(--color-primary);
  color: var(--color-primary);
}

.form-actions {
  padding-top: 8px;
}

/* ============ 流式输出视图 ============ */
.streaming-view {
  padding-bottom: 80px;
}

.streaming-topic {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  margin-bottom: 32px;
  padding: 16px 20px;
  background: var(--color-background-tertiary);
  border-radius: var(--radius-md);
  border: 1px solid var(--color-border);
}

.topic-badge {
  flex-shrink: 0;
  font-size: 11px;
  font-weight: 600;
  padding: 2px 10px;
  border-radius: var(--radius-full);
  background: rgba(59, 130, 246, 0.15);
  color: var(--color-primary);
  white-space: nowrap;
  margin-top: 2px;
}

.topic-text {
  font-size: 16px;
  font-weight: 600;
  color: var(--color-text);
  margin: 0;
  line-height: 1.5;
}

.stream-section {
  margin-bottom: 28px;
}

.stream-section-title {
  font-size: 14px;
  font-weight: 600;
  color: var(--color-text);
  margin: 0 0 12px;
  padding-bottom: 8px;
  border-bottom: 1px solid var(--color-border);
}

/* 标题卡片 */
.title-cards {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.title-card {
  display: flex;
  gap: 14px;
  padding: 14px 16px;
  background: var(--color-background-tertiary);
  border-radius: var(--radius-md);
  border: 1.5px solid var(--color-border);
  cursor: pointer;
  transition: all var(--transition-fast);
  user-select: none;
}

.title-card:hover {
  border-color: var(--color-primary-light);
  background: rgba(59, 130, 246, 0.04);
  transform: translateX(4px);
}

.title-card.selected {
  border-color: var(--color-primary);
  background: rgba(59, 130, 246, 0.08);
  box-shadow: 0 0 0 1px rgba(59, 130, 246, 0.2), 0 2px 8px rgba(59, 130, 246, 0.1);
}

.title-rank {
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(59, 130, 246, 0.08);
  color: var(--color-text-muted);
  border-radius: var(--radius-sm);
  font-size: 13px;
  font-weight: 600;
  flex-shrink: 0;
  transition: all var(--transition-fast);
}

.title-card:hover .title-rank {
  background: rgba(59, 130, 246, 0.15);
  color: var(--color-primary);
}

.title-rank.selected {
  background: var(--color-primary);
  color: #fff;
  font-size: 14px;
}

.t-main {
  font-size: 15px;
  font-weight: 600;
  color: var(--color-text);
  margin: 0 0 4px;
  line-height: 1.4;
}

.t-sub {
  font-size: 13px;
  color: var(--color-text-secondary);
  margin: 0;
}

/* 流式文本块 */
.stream-block {
  background: var(--color-background-tertiary);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  padding: 16px 18px;
  font-family: "Work Sans", ui-monospace, monospace;
  font-size: 13px;
  color: var(--color-text-secondary);
  white-space: pre-wrap;
  word-break: break-word;
  line-height: 1.7;
  margin: 0;
  max-height: 360px;
  overflow-y: auto;
}

.content-block {
  max-height: 500px;
}

/* 流式图片 */
.stream-images {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
}

.stream-img-item {
  border-radius: var(--radius-md);
  overflow: hidden;
  aspect-ratio: 4 / 3;
  background: var(--color-background-tertiary);
}

.stream-img-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.stream-waiting {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  padding: 80px 20px;
  color: var(--color-text-muted);
  font-size: 15px;
}

/* ============ 完成文章视图 ============ */
.article-view {
  padding-bottom: 80px;
}

.article-top-bar {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
  margin-bottom: 24px;
}

.article-cover-img {
  width: 100%;
  aspect-ratio: 16 / 9;
  overflow: hidden;
  border-radius: var(--radius-lg);
  margin-bottom: 32px;
  background: var(--color-background-tertiary);
}

.article-cover-img img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.article-header {
  margin-bottom: 32px;
  padding-bottom: 24px;
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
  line-height: 1.5;
}

.article-tags {
  display: flex;
  gap: 12px;
}

.article-tag {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  color: var(--color-text-muted);
}

.style-tag {
  padding: 2px 10px;
  background: rgba(59, 130, 246, 0.1);
  color: var(--color-primary);
  border-radius: var(--radius-full);
}

.article-body {
  margin-bottom: 32px;
}

.article-images-section h3 {
  font-size: 16px;
  font-weight: 600;
  color: var(--color-text);
  margin: 0 0 14px;
}

.image-gallery {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 14px;
}

.gallery-item {
  background: var(--color-background-tertiary);
  border-radius: var(--radius-md);
  overflow: hidden;
}

.gallery-item img {
  width: 100%;
  aspect-ratio: 4 / 3;
  object-fit: cover;
  display: block;
}

.gallery-desc {
  padding: 10px 14px;
  font-size: 12px;
  color: var(--color-text-secondary);
  margin: 0;
}

.article-loading {
  display: flex;
  justify-content: center;
  padding: 80px 0;
}

/* ============ Markdown 正文 ============ */
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
  background: var(--color-background-tertiary);
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 14px;
  color: var(--color-accent-cyan-light);
}

.markdown-body :deep(pre) {
  background: var(--color-background-tertiary);
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
  max-width: 100%;
  border-radius: var(--radius-md);
  margin: 16px 0;
}

.markdown-body :deep(table) { width: 100%; border-collapse: collapse; margin: 16px 0; }

.markdown-body :deep(th),
.markdown-body :deep(td) { border: 1px solid var(--color-border); padding: 10px 14px; text-align: left; }

.markdown-body :deep(th) { background: var(--color-background-tertiary); font-weight: 600; }

.markdown-body :deep(hr) { border: none; border-top: 1px solid var(--color-border); margin: 32px 0; }

/* ============ 右栏：统计 ============ */
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

/* 动画 */
@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* ============ 响应式 ============ */
@media (max-width: 1200px) {
  .three-col {
    grid-template-columns: 220px 1fr 240px;
  }

  .center-panel {
    padding: 24px 28px;
  }
}

@media (max-width: 900px) {
  .three-col {
    grid-template-columns: 1fr;
    height: auto;
  }

  .left-panel,
  .right-panel {
    display: none;
  }

  .center-panel {
    padding: 20px 16px;
  }
}
</style>
