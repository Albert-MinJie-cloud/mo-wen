<template>
  <component
    :is="to ? 'RouterLink' : 'button'"
    :to="to"
    :type="to ? undefined : nativeType"
    :class="['btn', `btn--${variant}`, `btn--${size}`, { 'btn--block': block }]"
    :disabled="disabled"
    v-bind="$attrs"
  >
    <slot />
  </component>
</template>

<script setup lang="ts">
withDefaults(
  defineProps<{
    /** 按钮变体：primary 白底黑字, secondary 透明底白字, gradient 渐变蓝底 */
    variant?: "primary" | "secondary" | "gradient";
    /** 按钮大小 */
    size?: "sm" | "md" | "lg";
    /** 是否为原生 submit 按钮 */
    nativeType?: "button" | "submit" | "reset";
    /** RouterLink 跳转路径 */
    to?: string;
    /** 是否禁用 */
    disabled?: boolean;
    /** 是否撑满容器宽度 */
    block?: boolean;
  }>(),
  {
    variant: "primary",
    size: "md",
    nativeType: "button",
  },
);
</script>

<style scoped lang="scss">
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  border: none;
  cursor: pointer;
  font-weight: 600;
  text-decoration: none;
  white-space: nowrap;
  transition: all 200ms ease-out;
  font-family: inherit;

  &--block {
    width: 100%;
  }

  &:disabled {
    opacity: 0.4;
    cursor: not-allowed;
  }
}

/* Size */
.btn--sm {
  height: 36px;
  padding: 0 16px;
  font-size: 13px;
  border-radius: 50px;
}

.btn--md {
  height: 42px;
  padding: 0 24px;
  font-size: 14px;
  border-radius: 50px;
}

.btn--lg {
  height: 52px;
  padding: 0 32px;
  font-size: 16px;
  border-radius: 50px;
}

/* Variant: primary - 白底黑字 */
.btn--primary {
  background: #fff;
  color: #000;

  &:hover:not(:disabled) {
    background: #e5e5e5;
  }
}

/* Variant: secondary - 透明底白字 */
.btn--secondary {
  background: transparent;
  color: #fff;
  border: 1px solid rgba(255, 255, 255, 0.2);

  &:hover:not(:disabled) {
    background: rgba(255, 255, 255, 0.05);
    border-color: rgba(255, 255, 255, 0.3);
  }
}

/* Variant: gradient - 渐变蓝底白字 */
.btn--gradient {
  background: linear-gradient(135deg, #22d3ee, #3b82f6);
  color: #fff;
  box-shadow: 0 4px 14px rgba(59, 130, 246, 0.2);

  &:hover:not(:disabled) {
    opacity: 0.92;
  }
}
</style>
