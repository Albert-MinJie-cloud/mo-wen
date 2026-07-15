<script setup lang="ts">
withDefaults(
  defineProps<{
    outlineText?: string;
    outlineSections?: any[];
  }>(),
  {
    outlineText: "",
    outlineSections: () => [],
  },
);
</script>

<template>
  <div v-if="outlineText || outlineSections.length" class="stream-section">
    <h3 class="stream-section-title">文章大纲</h3>
    <!-- 结构化渲染 -->
    <div v-if="outlineSections.length" class="outline-tree">
      <div
        v-for="(section, si) in outlineSections"
        :key="si"
        class="outline-section"
      >
        <div class="outline-section-header">
          <span class="outline-section-num">{{ section.section }}</span>
          <span class="outline-section-title">{{ section.title }}</span>
        </div>
        <ul class="outline-points">
          <li
            v-for="(point, pi) in section.points"
            :key="pi"
            class="outline-point"
          >
            {{ point }}
          </li>
        </ul>
      </div>
    </div>
    <!-- 流式原始输出 -->
    <pre v-else class="stream-block">{{ outlineText }}</pre>
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
}

.outline-tree {
  display: flex;
  flex-direction: column;
  gap: 0;
}

.outline-section {
  padding: 12px 16px;
  border-left: 2px solid var(--color-border);
  transition: border-color var(--transition-fast);
}

.outline-section:hover {
  border-left-color: var(--color-primary-light);
}

.outline-section-header {
  display: flex;
  align-items: flex-start;
  gap: 12px;
}

.outline-section-num {
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(59, 130, 246, 0.12);
  color: var(--color-primary);
  border-radius: var(--radius-sm);
  font-size: 13px;
  font-weight: 700;
  flex-shrink: 0;
  font-family: "Outfit", sans-serif;
}

.outline-section-title {
  font-size: 15px;
  font-weight: 600;
  color: var(--color-text);
  line-height: 1.4;
  padding-top: 1px;
}

.outline-points {
  margin: 8px 0 0 36px;
  padding: 0;
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.outline-point {
  font-size: 13px;
  color: var(--color-text-secondary);
  line-height: 1.6;
  padding: 2px 0;

  &::before {
    content: "•";
    color: var(--color-text-muted);
    margin-right: 8px;
  }
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
</style>
