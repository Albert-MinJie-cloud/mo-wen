<template>
  <div class="page-header">
    <div class="header-container">
      <div class="header-content">
        <h1 class="page-title">{{ title }}</h1>
        <p v-if="subtitle" class="page-subtitle">{{ subtitle }}</p>
      </div>
      <div v-if="$slots.extra" class="header-extra">
        <slot name="extra" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  title: string;
  subtitle?: string;
}>();
</script>

<style scoped lang="scss">
.page-header {
  margin-bottom: 24px;
}

.header-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 32px 20px;
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
}

.header-content {
  color: var(--color-text);
}

.page-title {
  font-size: 28px;
  font-weight: 700;
  margin: 0 0 6px;
  letter-spacing: -0.5px;
  color: var(--color-text);
}

.page-subtitle {
  font-size: 14px;
  color: var(--color-text-secondary);
  margin: 0;
}

.header-extra {
  flex-shrink: 0;
}

@media (max-width: 768px) {
  .header-container {
    padding: 24px 20px;
  }

  .page-title {
    font-size: 22px;
  }
}
</style>
