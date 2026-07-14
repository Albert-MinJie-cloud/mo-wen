<script setup lang="ts" generic="T extends Record<string, any>">
import { computed } from "vue";

const props = withDefaults(
  defineProps<{
    items: T[];
    loading?: boolean;
    emptyText?: string;
  }>(),
  {
    loading: false,
    emptyText: "暂无数据",
  }
);

const emit = defineEmits<{
  (e: "clickItem", item: T): void;
}>();

const hasItems = computed(() => props.items.length > 0);
</script>

<template>
  <div :class="['data-list', { 'is-empty': !hasItems, 'is-loading': loading }]">
    <!-- Loading -->
    <div v-if="loading" class="data-list-loading">
      <a-spin size="default" />
      <span>加载中...</span>
    </div>

    <!-- 列表 -->
    <div v-else-if="hasItems" class="data-list-body">
      <div
        v-for="(item, index) in items"
        :key="(item.id as any) ?? index"
        class="data-list-item"
        @click="emit('clickItem', item)"
      >
        <slot name="item" :item="item" :index="index" />
      </div>
    </div>

    <!-- 空状态 -->
    <div v-else class="data-list-empty">
      <div class="empty-icon">
        <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round">
          <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
          <polyline points="14 2 14 8 20 8"/>
        </svg>
      </div>
      <p>{{ emptyText }}</p>
    </div>
  </div>
</template>

<style scoped>
.data-list {
  min-height: 200px;
}

.data-list-loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 12px;
  padding: 80px 0;
  color: var(--color-text-muted);
  font-size: 14px;
}

/* 列表项 */
.data-list-body {
  display: flex;
  flex-direction: column;
  gap: 1px;
  background: var(--color-border);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  overflow: hidden;
}

.data-list-item {
  background: var(--color-background-tertiary);
  padding: 0;
  cursor: pointer;
  transition: background var(--transition-fast);
}

.data-list-item:hover {
  background: rgba(59, 130, 246, 0.04);
}

/* 空状态 */
.data-list-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 16px;
  padding: 80px 0;
  color: var(--color-text-muted);
  font-size: 14px;
}

.empty-icon {
  opacity: 0.25;
}
</style>
