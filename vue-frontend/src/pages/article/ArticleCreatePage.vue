<script setup lang="ts">
import { ref, reactive, computed } from "vue";
import { useRouter } from "vue-router";
import { message } from "@/message";
import {
  createArticleApiArticleCreatePost,
  getArticleApiArticleTaskIdGet,
  confirmTitleApiArticleConfirmTitlePost,
  confirmOutlineApiArticleConfirmOutlinePost,
  aiModifyOutlineApiArticleAiModifyOutlinePost,
} from "@/api/article";
import { connectSSE, closeSSE, type SSEMessage } from "@/utils/sse";
import { markdownToHtml } from "@/utils/markdown";
import { getWordCount } from "@/utils/article";
import LeftPanel from "./create/LeftPanel.vue";
import type { AgentStep } from "./create/LeftPanel.vue";
import CenterPanel from "./create/CenterPanel.vue";
import RightPanel from "./create/RightPanel.vue";
import {
  FileTextOutlined,
  OrderedListOutlined,
  EditOutlined,
  PictureOutlined,
  ThunderboltOutlined,
  MergeCellsOutlined,
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

// ============ 阶段交互状态 ============
const currentPhase = ref<1 | 2 | 3>(1);
const userDescription = ref("");
const showTitleConfirm = ref(false);
const showOutlineEdit = ref(false);
const modifySuggestion = ref("");
const isModifyingOutline = ref(false);
const isConfirmingTitle = ref(false);
const isConfirmingOutline = ref(false);

// ============ 创作进度 ============
const agentSteps = reactive<AgentStep[]>([
  { key: "AGENT1", icon: FileTextOutlined, title: "标题生成", desc: "分析选题，生成吸睛标题", status: "waiting" },
  { key: "AGENT2", icon: OrderedListOutlined, title: "大纲规划", desc: "构建逻辑清晰的文章骨架", status: "waiting" },
  { key: "AGENT3", icon: EditOutlined, title: "正文撰写", desc: "逐步生成高质量正文内容", status: "waiting" },
  { key: "AGENT4", icon: PictureOutlined, title: "配图分析", desc: "分析内容，确定配图位置与来源", status: "waiting" },
  { key: "AGENT5", icon: ThunderboltOutlined, title: "生成配图", desc: "搜索与内容匹配的配图", status: "waiting" },
  { key: "MERGE", icon: MergeCellsOutlined, title: "图文合成", desc: "将配图嵌入文章正文", status: "waiting" },
]);

const outlineText = ref("");
const outlineSections = ref<any[]>([]);
const contentText = ref("");
const titleOptions = ref<API.TitleOption[]>([]);
const selectedTitleIndex = ref(-1);
const customMainTitle = ref("");
const customSubTitle = ref("");
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

const currentAgentTitle = computed(() => currentAgent.value?.title);

const isGeneratingImages = computed(() => {
  const key = currentAgent.value?.key;
  return key === "AGENT4" || key === "AGENT5" || key === "MERGE";
});

const loadingMessage = computed(() => {
  if (currentPhase.value === 1) return "正在分析选题，生成标题方案...";
  if (currentPhase.value === 2) return "正在分析文章结构，生成大纲...";
  return "正在撰写正文内容，匹配配图...";
});

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
    case "AGENT1_COMPLETE":
      break;

    case "TITLES_GENERATED":
      updateAgentStep("AGENT1", "done");
      if (data.titleOptions) titleOptions.value = data.titleOptions;
      closeSSE(eventSource.value);
      eventSource.value = null;
      showTitleConfirm.value = true;
      currentPhase.value = 1;
      break;

    case "AGENT2_STREAMING":
      updateAgentStep("AGENT2", "processing");
      if (data.content) outlineText.value += data.content;
      break;

    case "AGENT2_COMPLETE":
      break;

    case "OUTLINE_GENERATED":
      updateAgentStep("AGENT2", "done");
      if (data.outline) outlineSections.value = data.outline;
      closeSSE(eventSource.value);
      eventSource.value = null;
      showOutlineEdit.value = true;
      currentPhase.value = 2;
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
      updateAgentStep("MERGE", "processing");
      break;

    case "MERGE_COMPLETE":
      updateAgentStep("MERGE", "done");
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

// ============ 阶段交互 ============
async function confirmTitle() {
  const isCustom = selectedTitleIndex.value === titleOptions.value.length;
  if (!isCustom && selectedTitleIndex.value < 0) {
    message.warning("请先选择一个标题");
    return;
  }
  if (isCustom && !customMainTitle.value.trim()) {
    message.warning("请输入自定义标题");
    return;
  }

  const selectedMainTitle = isCustom
    ? customMainTitle.value.trim()
    : titleOptions.value[selectedTitleIndex.value].mainTitle;
  const selectedSubTitle = isCustom
    ? customSubTitle.value.trim()
    : titleOptions.value[selectedTitleIndex.value].subTitle;
  isConfirmingTitle.value = true;
  try {
    await confirmTitleApiArticleConfirmTitlePost(
      {},
      {
        taskId: taskId.value,
        selectedMainTitle: selectedMainTitle,
        selectedSubTitle: selectedSubTitle,
        userDescription: userDescription.value || undefined,
      }
    );
    titleOptions.value = [];
    outlineText.value = "";
    outlineSections.value = [];
    showTitleConfirm.value = false;
    currentPhase.value = 2;
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
  } catch (e: any) {
    message.error(e?.message || "确认标题失败");
  } finally {
    isConfirmingTitle.value = false;
  }
}

async function confirmOutline() {
  isConfirmingOutline.value = true;
  try {
    await confirmOutlineApiArticleConfirmOutlinePost(
      {},
      {
        taskId: taskId.value,
        outline: outlineSections.value,
      }
    );
    outlineText.value = "";
    outlineSections.value = [];
    contentText.value = "";
    generatedImages.value = [];
    showOutlineEdit.value = false;
    currentPhase.value = 3;
    updateAgentStep("AGENT1", "done");
    updateAgentStep("AGENT2", "done");
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
  } catch (e: any) {
    message.error(e?.message || "确认大纲失败");
  } finally {
    isConfirmingOutline.value = false;
  }
}

async function aiModifyOutline() {
  if (!modifySuggestion.value.trim()) {
    message.warning("请输入修改建议");
    return;
  }
  isModifyingOutline.value = true;
  try {
    const res = await aiModifyOutlineApiArticleAiModifyOutlinePost(
      {},
      {
        taskId: taskId.value,
        modifySuggestion: modifySuggestion.value.trim(),
      }
    );
    if (res.data.code === 0 && res.data.data) {
      outlineSections.value = res.data.data;
      modifySuggestion.value = "";
      message.success("大纲已修改");
    }
  } catch (e: any) {
    message.error(e?.message || "AI 修改失败");
  } finally {
    isModifyingOutline.value = false;
  }
}

// ============ 大纲编辑 ============
function addSection() {
  const newSection: API.OutlineSection = {
    section: outlineSections.value.length + 1,
    title: "",
    points: [],
  };
  outlineSections.value.push(newSection);
}

function removeSection(index: number) {
  outlineSections.value.splice(index, 1);
  outlineSections.value.forEach((s, i) => (s.section = i + 1));
}

function moveSectionUp(index: number) {
  if (index === 0) return;
  const temp = outlineSections.value[index];
  outlineSections.value[index] = outlineSections.value[index - 1];
  outlineSections.value[index - 1] = temp;
  outlineSections.value.forEach((s, i) => (s.section = i + 1));
}

function moveSectionDown(index: number) {
  if (index === outlineSections.value.length - 1) return;
  const temp = outlineSections.value[index];
  outlineSections.value[index] = outlineSections.value[index + 1];
  outlineSections.value[index + 1] = temp;
  outlineSections.value.forEach((s, i) => (s.section = i + 1));
}

function addPoint(sectionIndex: number) {
  outlineSections.value[sectionIndex].points.push("");
}

function removePoint(sectionIndex: number, pointIndex: number) {
  outlineSections.value[sectionIndex].points.splice(pointIndex, 1);
}

// ============ 主流程 ============
async function startCreate() {
  if (!canSubmit.value) return;

  isCreating.value = true;
  isCompleted.value = false;
  errorMessage.value = "";
  outlineText.value = "";
  outlineSections.value = [];
  contentText.value = "";
  titleOptions.value = [];
  selectedTitleIndex.value = -1;
  customMainTitle.value = "";
  customSubTitle.value = "";
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
  outlineSections.value = [];
  contentText.value = "";
  titleOptions.value = [];
  selectedTitleIndex.value = -1;
  customMainTitle.value = "";
  customSubTitle.value = "";
  generatedImages.value = [];
  article.value = null;
  fullContentHtml.value = "";
  agentSteps.forEach((s) => (s.status = "waiting"));
  currentPhase.value = 1;
  userDescription.value = "";
  showTitleConfirm.value = false;
  showOutlineEdit.value = false;
  modifySuggestion.value = "";
  isModifyingOutline.value = false;
  isConfirmingTitle.value = false;
  isConfirmingOutline.value = false;
}

function viewInList() {
  router.push("/article/list");
}
</script>

<template>
  <div id="articleCreatePage">
    <div class="three-col">
      <LeftPanel
        :agent-steps="agentSteps"
        :is-creating="isCreating"
        :is-completed="isCompleted"
        :done-count="doneCount"
        :total-steps="totalSteps"
      />

      <CenterPanel
        :topic="topic"
        @update:topic="topic = $event"
        :style="style"
        @update:style="style = $event"
        :enabled-image-methods="enabledImageMethods"
        @toggle-image-method="toggleImageMethod"
        :can-submit="canSubmit"
        @start-create="startCreate"
        :is-creating="isCreating"
        :is-completed="isCompleted"
        :title-options="titleOptions"
        :selected-title-index="selectedTitleIndex"
        @update:selected-title-index="selectedTitleIndex = $event"
        :show-title-confirm="showTitleConfirm"
        :user-description="userDescription"
        @update:user-description="userDescription = $event"
        :custom-main-title="customMainTitle"
        @update:custom-main-title="customMainTitle = $event"
        :custom-sub-title="customSubTitle"
        @update:custom-sub-title="customSubTitle = $event"
        @confirm-title="confirmTitle"
        :outline-text="outlineText"
        :outline-sections="outlineSections"
        :show-outline-edit="showOutlineEdit"
        :modify-suggestion="modifySuggestion"
        @update:modify-suggestion="modifySuggestion = $event"
        :is-modifying-outline="isModifyingOutline"
        :is-confirming-title="isConfirmingTitle"
        :is-confirming-outline="isConfirmingOutline"
        :loading-message="loadingMessage"
        :is-generating-images="isGeneratingImages"
        @ai-modify-outline="aiModifyOutline"
        @add-section="addSection"
        @remove-section="removeSection"
        @move-section-up="moveSectionUp"
        @move-section-down="moveSectionDown"
        @add-point="addPoint"
        @remove-point="removePoint"
        @confirm-outline="confirmOutline"
        :content-text="contentText"
        :generated-images="generatedImages"
        :article="article"
        :full-content-html="fullContentHtml"
        @reset-state="resetState"
        @view-in-list="viewInList"
      />

      <RightPanel
        :is-creating="isCreating"
        :is-completed="isCompleted"
        :article="article"
        :done-count="doneCount"
        :total-steps="totalSteps"
        :elapsed-display="elapsedDisplay"
        :current-agent-title="currentAgentTitle"
        :realtime-word-count="realtimeWordCount"
        :realtime-image-count="realtimeImageCount"
        :final-word-count="finalWordCount"
        :final-image-count="finalImageCount"
        @select-hot-topic="selectHotTopic"
      />
    </div>
  </div>
</template>

<style scoped lang="scss">
#articleCreatePage {
  width: 100%;
  min-height: calc(100vh - 64px - 48px);
  background: var(--color-background);
}

/* 三栏布局 */
.three-col {
  display: grid;
  grid-template-columns: 260px 1fr 280px;
  gap: 0;
  height: calc(100vh - 64px - 48px);
  overflow: hidden;
}

/* 响应式 */
@media (max-width: 1200px) {
  .three-col {
    grid-template-columns: 220px 1fr 240px;
  }
}

@media (max-width: 900px) {
  .three-col {
    grid-template-columns: 1fr;
    height: auto;
  }

  .three-col :deep(.left-panel),
  .three-col :deep(.right-panel) {
    display: none;
  }
}
</style>
