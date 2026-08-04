<script setup lang="ts">
import { computed } from "vue";

const props = withDefaults(
  defineProps<{
    contentText?: string;
    generatedImages?: any[];
    isGeneratingImages?: boolean;
    currentAgentKey?: string;
  }>(),
  {
    contentText: "",
    generatedImages: () => [],
    isGeneratingImages: false,
    currentAgentKey: "",
  },
);

const phaseText = computed(() => {
  switch (props.currentAgentKey) {
    case "AGENT4":
      return "正在分析配图需求";
    case "AGENT5":
      return "正在生成配图";
    case "MERGE":
      return "正在图文合成";
    default:
      return "正在处理...";
  }
});
</script>

<template>
  <!-- 正文 -->
  <div v-if="contentText" class="stream-section">
    <h3 class="stream-section-title">正文内容</h3>
    <pre class="stream-block content-block">{{ contentText }}</pre>
  </div>

  <!-- 配图进度 -->
  <div v-if="contentText && isGeneratingImages" class="stream-section image-progress-section">
    <h3 class="stream-section-title">
      <a-spin size="small" />
      <span class="image-status-text">
        {{ phaseText }}
        <template v-if="generatedImages.length">（已生成 {{ generatedImages.length }} 张）</template>
        ...
      </span>
    </h3>

    <!-- 已生成图片预览 -->
    <div v-if="generatedImages.length" class="image-preview-grid">
      <div
        v-for="(img, i) in generatedImages"
        :key="i"
        class="image-preview-item"
      >
        <img :src="img.url" :alt="img.description" />
        <span class="image-index">{{ i + 1 }}</span>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
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
  display: flex;
  align-items: center;
  gap: 8px;
}

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

.image-progress-section {
  padding: 16px;
  background: var(--color-background-tertiary);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);

  .stream-section-title {
    margin-bottom: 12px;
    padding-bottom: 8px;
  }
}

.image-status-text {
  color: var(--color-primary);
  font-size: 13px;
}

.image-preview-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 8px;
}

.image-preview-item {
  position: relative;
  aspect-ratio: 16 / 9;
  border-radius: var(--radius-sm);
  overflow: hidden;
  background: var(--color-background);

  img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }

  .image-index {
    position: absolute;
    top: 4px;
    left: 4px;
    width: 20px;
    height: 20px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(0, 0, 0, 0.6);
    color: #fff;
    font-size: 11px;
    font-weight: 600;
    border-radius: var(--radius-sm);
  }
}
</style>
