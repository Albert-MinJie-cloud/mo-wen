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

  <!-- 配图生成中 -->
  <div v-if="contentText && isGeneratingImages && generatedImages.length === 0" class="stream-section">
    <h3 class="stream-section-title">配图生成</h3>
    <div class="image-loading">
      <a-spin size="default" />
      <p>正在分析配图需求，搜索匹配图片...</p>
    </div>
  </div>

  <!-- 配图 -->
  <div v-if="generatedImages.length > 0" class="stream-section">
    <h3 class="stream-section-title">
      已生成配图 · {{ generatedImages.length }}
      <a-spin v-if="isGeneratingImages" size="small" style="margin-left: 8px" />
    </h3>
    <div class="stream-images">
      <div v-for="(img, i) in generatedImages" :key="i" class="stream-img-item">
        <img :src="img.url" :alt="img.description || '配图'" />
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

.image-loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  padding: 24px;
  color: var(--color-text-secondary);
  font-size: 13px;
}

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
</style>
