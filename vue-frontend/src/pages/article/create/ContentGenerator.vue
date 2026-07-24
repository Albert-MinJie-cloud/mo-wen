<script setup lang="ts">
withDefaults(
  defineProps<{
    contentText?: string;
    generatedImages?: any[];
    isGeneratingImages?: boolean;
  }>(),
  {
    contentText: "",
    generatedImages: () => [],
    isGeneratingImages: false,
  },
);
</script>

<template>
  <!-- 正文 -->
  <div v-if="contentText" class="stream-section">
    <h3 class="stream-section-title">正文内容</h3>
    <pre class="stream-block content-block">{{ contentText }}</pre>
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
</style>
