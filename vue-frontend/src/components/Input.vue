<template>
  <a-input
    v-if="!isPassword"
    v-bind="$attrs"
    :class="['custom-input', $attrs.class]"
    :size="size"
  >
    <template v-for="(_, name) in $slots" #[name]="slotProps">
      <slot :name="name" v-bind="slotProps || {}" />
    </template>
  </a-input>
  <a-input-password
    v-else
    v-bind="$attrs"
    :class="['custom-input', $attrs.class]"
    :size="size"
  >
    <template v-for="(_, name) in $slots" #[name]="slotProps">
      <slot :name="name" v-bind="slotProps || {}" />
    </template>
  </a-input-password>
</template>

<script setup lang="ts">
withDefaults(
  defineProps<{
    isPassword?: boolean;
    size?: "large" | "middle" | "small";
  }>(),
  {
    isPassword: false,
    size: "large",
  },
);
</script>

<style scoped lang="scss">
.custom-input {
  height: 44px;
  border-radius: var(--radius-md);
  border-color: var(--color-border);
  background: rgba(255, 255, 255, 0.04) !important;
  transition: all var(--transition-fast);

  :deep(.ant-input) {
    background: transparent !important;
    color: var(--color-text);
    font-size: 14px;

    &::placeholder {
      color: var(--color-text-muted);
    }
  }

  :deep(.ant-input-affix-wrapper) {
    background: transparent !important;
  }

  :deep(.ant-input-prefix) {
    margin-right: 10px;
  }

  :deep(.ant-input-password-icon) {
    color: var(--color-text-muted) !important;

    &:hover {
      color: var(--color-text-secondary) !important;
    }
  }

  :deep(.ant-input-suffix) {
    color: var(--color-text-muted);
  }

  &:hover {
    border-color: rgba(255, 255, 255, 0.15);
    background: rgba(255, 255, 255, 0.06) !important;
  }

  &:focus,
  &:focus-within {
    border-color: var(--color-primary);
    background: rgba(255, 255, 255, 0.06) !important;
    box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.15);
  }
}
</style>
