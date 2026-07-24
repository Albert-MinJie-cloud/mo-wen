<script setup lang="ts">
import BasicLayout from "@/layouts/BasicLayout.vue";
import ToastContainer from "@/components/ToastContainer.vue";
import MessageContainer from "@/components/MessageContainer.vue";
import zhCN from "ant-design-vue/es/locale/zh_CN";


</script>

<template>
  <a-config-provider :locale="zhCN">
    <BasicLayout />
    <ToastContainer />
    <MessageContainer />
  </a-config-provider>
</template>

<style>
/* 引入 Google Fonts - Geometric Modern */
@import url("https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&family=Work+Sans:wght@300;400;500;600;700&display=swap");

/* 全局CSS变量 - 双主题配色方案（默认暗黑） */

/* ========== 公共变量（深浅主题共用） ========== */
:root {
  /* 品牌色 */
  --color-primary: #3b82f6;
  --color-primary-light: #60a5fa;
  --color-primary-dark: #2563eb;
  --color-accent-cyan: #06b6d4;
  --color-accent-cyan-light: #00d3f3;
  --color-accent-purple: #a855f7;

  /* 功能色 */
  --color-success: #22c55e;
  --color-warning: #eab308;
  --color-error: #ef4444;
  --color-info: #3b82f6;

  /* 圆角 */
  --radius-sm: 6px;
  --radius-md: 8px;
  --radius-lg: 12px;
  --radius-xl: 16px;
  --radius-2xl: 24px;
  --radius-full: 9999px;

  /* 过渡 */
  --transition-fast: 150ms ease-out;
  --transition-normal: 200ms ease-out;
  --transition-slow: 300ms ease-out;

  /* 渐变（品牌色不变） */
  --gradient-primary: linear-gradient(135deg, #22d3ee, #3b82f6);
}

/* ========== 暗黑主题（默认） ========== */
:root {
  /* Toast 通知主题色 */
  --toast-success-bg: rgba(34, 197, 94, 0.12);
  --toast-success-border: rgba(34, 197, 94, 0.25);
  --toast-success-text: #4ade80;
  --toast-success-icon: #22c55e;

  --toast-error-bg: rgba(239, 68, 68, 0.12);
  --toast-error-border: rgba(239, 68, 68, 0.25);
  --toast-error-text: #f87171;
  --toast-error-icon: #ef4444;

  --toast-warning-bg: rgba(234, 179, 8, 0.12);
  --toast-warning-border: rgba(234, 179, 8, 0.25);
  --toast-warning-text: #facc15;
  --toast-warning-icon: #eab308;

  --toast-info-bg: rgba(59, 130, 246, 0.12);
  --toast-info-border: rgba(59, 130, 246, 0.25);
  --toast-info-text: #60a5fa;
  --toast-info-icon: #3b82f6;

  /* 中性色 */
  --color-background: #09090b;
  --color-background-secondary: #0e0e11;
  --color-background-tertiary: #121214;
  --color-background-dark: #09090b;
  --color-text: #ffffff;
  --color-text-secondary: #a3a3a3;
  --color-text-muted: #737373;
  --color-border: rgba(255, 255, 255, 0.1);
  --color-border-light: rgba(255, 255, 255, 0.05);

  /* 填充叠加层 */
  --color-fill: rgba(255, 255, 255, 0.15);
  --color-fill-secondary: rgba(255, 255, 255, 0.08);
  --color-fill-tertiary: rgba(255, 255, 255, 0.04);

  /* 渐变 */
  --gradient-hero: linear-gradient(180deg, #09090b, #0a1122);
  --gradient-hero-dark: linear-gradient(180deg, #09090b, #0a1122);

  /* 纯色背景 */
  --bg-primary: #3b82f6;
  --bg-primary-hover: #2563eb;
  --bg-dark: #09090b;
  --bg-dark-hover: #121214;
  --bg-success: #22c55e;

  /* 阴影 */
  --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.3);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.4);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.4);
  --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.5);
  --shadow-card: 0 1px 3px rgba(0, 0, 0, 0.3);
  --shadow-card-hover: 0 8px 24px rgba(59, 130, 246, 0.1);
  --shadow-blue: 0 4px 14px rgba(59, 130, 246, 0.2);
  --shadow-cyan: 0 0 20px rgba(6, 182, 212, 0.15);

  /* 毛玻璃 */
  --glass-bg: rgba(9, 9, 11, 0.8);
  --glass-bg-accent: rgba(6, 182, 212, 0.1);
  --glass-blur: blur(12px);

  /* 按钮 hover 状态 */
  --btn-primary-hover-bg: #e5e5e5;
  --btn-secondary-hover-bg: rgba(255, 255, 255, 0.06);
  --btn-secondary-hover-border: rgba(255, 255, 255, 0.2);
}

/* ========== 浅色主题 ========== */
:root[data-theme="light"] {
  /* Toast 通知主题色 */
  --toast-success-bg: #f0fdf4;
  --toast-success-border: #bbf7d0;
  --toast-success-text: #15803d;
  --toast-success-icon: #22c55e;

  --toast-error-bg: #fef2f2;
  --toast-error-border: #fecaca;
  --toast-error-text: #b91c1c;
  --toast-error-icon: #ef4444;

  --toast-warning-bg: #fefce8;
  --toast-warning-border: #fef08a;
  --toast-warning-text: #a16207;
  --toast-warning-icon: #eab308;

  --toast-info-bg: #eff6ff;
  --toast-info-border: #bfdbfe;
  --toast-info-text: #1d4ed8;
  --toast-info-icon: #3b82f6;

  /* 中性色 — zinc 色系 */
  --color-background: #ffffff;
  --color-background-secondary: #ffffff;
  --color-background-tertiary: #f4f4f5;
  --color-background-dark: #ffffff;
  --color-text: #09090b;
  --color-text-secondary: #52525b;
  --color-text-muted: #71717a;
  --color-border: #d4d4d8;
  --color-border-light: #e4e4e7;

  /* 填充叠加层 */
  --color-fill: rgba(0, 0, 0, 0.06);
  --color-fill-secondary: rgba(0, 0, 0, 0.04);
  --color-fill-tertiary: rgba(0, 0, 0, 0.02);

  /* 渐变 */
  --gradient-hero: linear-gradient(180deg, #ffffff 0%, #f0f5ff 100%);
  --gradient-hero-dark: linear-gradient(180deg, #ffffff 0%, #f0f5ff 100%);

  /* 纯色背景 */
  --bg-primary: #3b82f6;
  --bg-primary-hover: #2563eb;
  --bg-dark: #f4f4f5;
  --bg-dark-hover: #e4e4e7;
  --bg-success: #22c55e;

  /* 阴影 — 加重使其可见 */
  --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.07);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.07);
  --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.08);
  --shadow-card: 0 1px 3px 0 rgba(0, 0, 0, 0.06), 0 1px 2px -1px rgba(0, 0, 0, 0.06);
  --shadow-card-hover: 0 10px 15px -3px rgba(0, 0, 0, 0.08), 0 4px 6px -4px rgba(0, 0, 0, 0.04);
  --shadow-blue: 0 4px 14px rgba(59, 130, 246, 0.2);
  --shadow-cyan: 0 0 20px rgba(6, 182, 212, 0.12);

  /* 毛玻璃 — 白色半透明 + 边框补偿 */
  --glass-bg: rgba(255, 255, 255, 0.72);
  --glass-bg-accent: rgba(6, 182, 212, 0.04);
  --glass-blur: blur(16px);

  /* 按钮 hover 状态 */
  --btn-primary-hover-bg: #27272a;
  --btn-secondary-hover-bg: rgba(0, 0, 0, 0.04);
  --btn-secondary-hover-border: rgba(0, 0, 0, 0.1);
}

/* 全局样式优化 */
* {
  box-sizing: border-box;
}

body {
  margin: 0;
  padding: 0;
  font-family: "Work Sans", -apple-system, BlinkMacSystemFont, "Segoe UI",
    "Roboto", "Oxygen", "Ubuntu", "Helvetica Neue", sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  overflow-x: hidden;
  background-color: var(--color-background);
  color: var(--color-text);
  line-height: 1.6;
}

html {
  overflow-x: hidden;
}

h1,
h2,
h3,
h4,
h5,
h6 {
  font-family: "Outfit", sans-serif;
}

/* 全局链接样式 */
a {
  color: var(--color-text);
  text-decoration: none;
  transition: color var(--transition-fast);
}

a:hover {
  color: var(--color-primary);
}

/* 全局按钮增强 */
.ant-btn {
  transition: all var(--transition-normal);
  font-weight: 500;
  border-radius: var(--radius-md);
}

.ant-btn-primary {
  background: var(--bg-primary);
  border-color: var(--bg-primary);
  box-shadow: var(--shadow-blue);
}

.ant-btn-primary:not(:disabled):hover {
  background: var(--bg-primary-hover);
  border-color: var(--bg-primary-hover);
  box-shadow: 0 6px 20px rgba(59, 130, 246, 0.35);
}

/* 全局卡片增强 */
.ant-card {
  border-radius: var(--radius-lg);
  border: 1px solid var(--color-border);
  transition: all var(--transition-normal);
}

/* 可点击元素统一cursor */
.clickable,
[role="button"],
button,
.ant-btn,
.ant-card.hoverable {
  cursor: pointer;
}

/* 选中状态 */
::selection {
  background: rgba(59, 130, 246, 0.2);
  color: var(--color-text);
}

/* Ant Design 菜单覆盖 */
.ant-menu-horizontal > .ant-menu-item:hover::after,
.ant-menu-horizontal > .ant-menu-item-active::after,
.ant-menu-horizontal > .ant-menu-item-selected::after {
  border-bottom-color: var(--color-primary) !important;
}

.ant-menu-horizontal > .ant-menu-item:hover,
.ant-menu-horizontal > .ant-menu-item-active {
  color: var(--color-text) !important;
}

/* Ant Design 按钮 disabled 状态 */
.ant-btn:disabled {
  background: var(--color-border) !important;
  color: var(--color-text-muted) !important;
  border-color: var(--color-border) !important;
  box-shadow: none !important;
}

.ant-btn-primary:disabled {
  background: var(--color-border) !important;
  color: var(--color-text-muted) !important;
}

/* Steps 组件样式覆盖 */
.ant-steps .ant-steps-item-process .ant-steps-item-icon {
  background: var(--color-primary);
  border-color: var(--color-primary);
}

.ant-steps .ant-steps-item-finish .ant-steps-item-icon {
  border-color: var(--color-primary);
}

.ant-steps .ant-steps-item-finish .ant-steps-item-icon > .ant-steps-icon {
  color: var(--color-primary);
}

.ant-steps
  .ant-steps-item-finish
  > .ant-steps-item-container
  > .ant-steps-item-tail::after {
  background-color: var(--color-primary);
}

/* 文本域 */
.ant-input-textarea-show-count::after {
  color: var(--color-text-muted);
}

/* Progress 组件 */
.ant-progress-bg {
  background: var(--gradient-primary);
}

/* Spin 组件 */
.ant-spin-dot-item {
  background-color: var(--color-primary);
}
</style>
