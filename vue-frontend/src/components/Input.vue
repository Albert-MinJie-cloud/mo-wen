<template>
  <a-input
    v-if="!isPassword"
    v-bind="$attrs"
    class="mo-input"
    :size="size"
  >
    <template v-for="(_, name) in $slots" #[name]="slotProps">
      <slot :name="name" v-bind="slotProps || {}" />
    </template>
  </a-input>
  <a-input-password
    v-else
    v-bind="$attrs"
    class="mo-input"
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

<style lang="scss">
/* mo-input 命名空间，非 scoped，避免 Vue scoped CSS 穿透限制 */
.mo-input {
  height: 44px;
  border-radius: var(--radius-md);
  border-color: var(--color-border);
  background: rgba(255, 255, 255, 0.04) !important;
  color: var(--color-text) !important;
  font-size: 14px;
  transition: all var(--transition-fast);

  &::placeholder {
    color: var(--color-text-secondary);
    opacity: 0.6;
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

  .ant-input-prefix {
    margin-right: 10px;
  }

  .ant-input-password-icon {
    color: var(--color-text-muted) !important;

    &:hover {
      color: var(--color-text-secondary) !important;
    }
  }

  .ant-input-suffix {
    color: var(--color-text-muted);
  }
}

/* 有 prefix/suffix 时，ant-design 根元素变成 span 包装器，需要穿透到内部 input */
.mo-input.ant-input-affix-wrapper,
.mo-input.ant-input-password {
  > .ant-input {
    background: transparent !important;
    color: var(--color-text) !important;

    &::placeholder {
      color: var(--color-text-secondary);
      opacity: 0.6;
    }
  }
}
</style>
