<script setup lang="ts">
import { ClockCircleOutlined, ReloadOutlined } from "@ant-design/icons-vue";
import { ARTICLE_STYLE_OPTIONS } from "@/utils/article";
import Button from "@/components/Button.vue";

withDefaults(
  defineProps<{
    article?: API.ArticleVO | null;
    fullContentHtml?: string;
  }>(),
  {
    article: null,
    fullContentHtml: "",
  },
);

const emit = defineEmits<{
  (e: "resetState"): void;
  (e: "viewInList"): void;
}>();
</script>

<template>
  <div class="center-card article-view">
    <div class="article-top-bar">
      <Button variant="secondary" size="sm" @click="emit('viewInList')">文章列表</Button>
      <Button variant="gradient" size="sm" @click="emit('resetState')">
        <ReloadOutlined /> 继续创作
      </Button>
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
</template>

<style scoped lang="scss">
.center-card {
  max-width: 760px;
  margin: 0 auto;
}

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
</style>
