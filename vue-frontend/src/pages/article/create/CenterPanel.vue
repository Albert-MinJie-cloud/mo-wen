<script setup lang="ts">
import TopicForm from "./TopicForm.vue";
import TitleSelector from "./TitleSelector.vue";
import OutlineStream from "./OutlineStream.vue";
import OutlineEditor from "./OutlineEditor.vue";
import ContentGenerator from "./ContentGenerator.vue";
import ArticleResult from "./ArticleResult.vue";

const props = withDefaults(
  defineProps<{
    // 表单状态
    topic?: string;
    style?: string | null;
    enabledImageMethods?: string[];
    canSubmit?: boolean;
    // 流式状态
    isCreating?: boolean;
    isCompleted?: boolean;
    titleOptions?: API.TitleOption[];
    selectedTitleIndex?: number;
    showTitleConfirm?: boolean;
    userDescription?: string;
    customMainTitle?: string;
    customSubTitle?: string;
    outlineText?: string;
    outlineSections?: any[];
    showOutlineEdit?: boolean;
    modifySuggestion?: string;
    isModifyingOutline?: boolean;
    isConfirmingTitle?: boolean;
    isConfirmingOutline?: boolean;
    contentText?: string;
    generatedImages?: any[];
    // 完成状态
    article?: API.ArticleVO | null;
    fullContentHtml?: string;
  }>(),
  {
    topic: "",
    style: null,
    enabledImageMethods: () => [],
    canSubmit: false,
    isCreating: false,
    isCompleted: false,
    titleOptions: () => [],
    selectedTitleIndex: -1,
    showTitleConfirm: false,
    userDescription: "",
    customMainTitle: "",
    customSubTitle: "",
    outlineText: "",
    outlineSections: () => [],
    showOutlineEdit: false,
    modifySuggestion: "",
    isModifyingOutline: false,
    isConfirmingTitle: false,
    isConfirmingOutline: false,
    contentText: "",
    generatedImages: () => [],
    article: null,
    fullContentHtml: "",
  },
);

const emit = defineEmits<{
  // 表单操作
  (e: "update:topic", value: string): void;
  (e: "update:style", value: string | null): void;
  (e: "toggleImageMethod", method: string): void;
  (e: "startCreate"): void;
  // 阶段交互
  (e: "update:selectedTitleIndex", value: number): void;
  (e: "update:userDescription", value: string): void;
  (e: "update:customMainTitle", value: string): void;
  (e: "update:customSubTitle", value: string): void;
  (e: "confirmTitle"): void;
  // 大纲编辑
  (e: "update:modifySuggestion", value: string): void;
  (e: "addSection"): void;
  (e: "removeSection", index: number): void;
  (e: "moveSectionUp", index: number): void;
  (e: "moveSectionDown", index: number): void;
  (e: "addPoint", sectionIndex: number): void;
  (e: "removePoint", sectionIndex: number, pointIndex: number): void;
  (e: "aiModifyOutline"): void;
  (e: "confirmOutline"): void;
  // 完成后操作
  (e: "resetState"): void;
  (e: "viewInList"): void;
}>();
</script>

<template>
  <main class="center-panel">
    <!-- 状态一：输入表单 -->
    <TopicForm
      v-if="!isCreating && !isCompleted"
      :topic="topic"
      @update:topic="emit('update:topic', $event)"
      :style="style"
      @update:style="emit('update:style', $event)"
      :enabled-image-methods="enabledImageMethods"
      @toggle-image-method="emit('toggleImageMethod', $event)"
      :can-submit="canSubmit"
      @start-create="emit('startCreate')"
    />

    <!-- 状态二：流式输出 -->
    <div v-if="isCreating && !isCompleted" class="center-card streaming-view">
      <div class="streaming-topic">
        <span class="topic-badge">正在创作</span>
        <h2 class="topic-text">{{ topic }}</h2>
      </div>

      <!-- 标题选择 -->
      <TitleSelector
        v-if="titleOptions.length > 0 && !showOutlineEdit"
        :title-options="titleOptions"
        :selected-title-index="selectedTitleIndex"
        @update:selected-title-index="emit('update:selectedTitleIndex', $event)"
        :show-title-confirm="showTitleConfirm"
        :user-description="userDescription"
        @update:user-description="emit('update:userDescription', $event)"
        :custom-main-title="customMainTitle"
        @update:custom-main-title="emit('update:customMainTitle', $event)"
        :custom-sub-title="customSubTitle"
        @update:custom-sub-title="emit('update:customSubTitle', $event)"
        :is-confirming-title="isConfirmingTitle"
        @confirm-title="emit('confirmTitle')"
      />

      <!-- 大纲只读流式 -->
      <OutlineStream
        v-if="(outlineText || outlineSections.length) && !showOutlineEdit"
        :outline-text="outlineText"
        :outline-sections="outlineSections"
      />

      <!-- 大纲编辑模式 -->
      <OutlineEditor
        v-if="showOutlineEdit"
        :outline-sections="outlineSections"
        :modify-suggestion="modifySuggestion"
        @update:modify-suggestion="emit('update:modifySuggestion', $event)"
        :is-modifying-outline="isModifyingOutline"
        :is-confirming-outline="isConfirmingOutline"
        @add-section="emit('addSection')"
        @remove-section="emit('removeSection', $event)"
        @move-section-up="emit('moveSectionUp', $event)"
        @move-section-down="emit('moveSectionDown', $event)"
        @add-point="emit('addPoint', $event)"
        @remove-point="(si, pi) => emit('removePoint', si, pi)"
        @ai-modify-outline="emit('aiModifyOutline')"
        @confirm-outline="emit('confirmOutline')"
      />

      <!-- 正文 & 配图流式 -->
      <ContentGenerator
        :content-text="contentText"
        :generated-images="generatedImages"
      />

      <!-- 空状态 -->
      <div
        v-if="!titleOptions.length && !outlineText && !contentText && !showTitleConfirm && !showOutlineEdit"
        class="stream-waiting"
      >
        <a-spin size="large" />
        <p>AI 智能体正在准备中...</p>
      </div>
    </div>

    <!-- 状态三：完成文章 -->
    <ArticleResult
      v-if="isCompleted"
      :article="article"
      :full-content-html="fullContentHtml"
      @reset-state="emit('resetState')"
      @view-in-list="emit('viewInList')"
    />
  </main>
</template>

<style scoped lang="scss">
.center-panel {
  overflow-y: auto;
  padding: 32px 40px;
}

.center-card {
  max-width: 760px;
  margin: 0 auto;
}

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

.stream-waiting {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  padding: 80px 20px;
  color: var(--color-text-muted);
  font-size: 15px;
}
</style>
