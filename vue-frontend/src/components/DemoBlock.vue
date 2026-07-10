<template>
  <div class="demo-block" :class="{ 'demo-block--open': codeVisible }">
    <!-- 组件预览 -->
    <div class="demo-preview">
      <slot />
    </div>

    <!-- 工具栏 -->
    <div class="demo-toolbar">
      <button class="toolbar-btn" :title="codeVisible ? '隐藏代码' : '显示代码'" @click="codeVisible = !codeVisible">
        <CodeOutlined />
      </button>
      <button class="toolbar-btn" title="复制代码" @click="copyCode">
        <CopyOutlined v-if="!copied" />
        <CheckOutlined v-else class="copied" />
      </button>
    </div>

    <!-- 代码区域 -->
    <div v-show="codeVisible" class="demo-code">
      <pre><code ref="codeRef" class="language-html"></code></pre>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, nextTick } from "vue";
import { CodeOutlined, CopyOutlined, CheckOutlined } from "@ant-design/icons-vue";
import hljs from "highlight.js/lib/core";
import xml from "highlight.js/lib/languages/xml";
import "highlight.js/styles/github-dark.css";

hljs.registerLanguage("xml", xml);

const props = defineProps<{
  code: string;
}>();

const codeVisible = ref(false);
const copied = ref(false);
const codeRef = ref<HTMLElement>();

const highlight = () => {
  nextTick(() => {
    if (codeRef.value) {
      codeRef.value.textContent = props.code;
      hljs.highlightElement(codeRef.value);
    }
  });
};

onMounted(highlight);

watch(
  () => props.code,
  () => highlight(),
);

const copyCode = async () => {
  await navigator.clipboard.writeText(props.code);
  copied.value = true;
  setTimeout(() => {
    copied.value = false;
  }, 2000);
};
</script>

<style scoped lang="scss">
.demo-block {
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  overflow: hidden;
  margin-bottom: 24px;

  &--open {
    .demo-preview {
      border-bottom: 1px solid var(--color-border);
    }
  }
}

.demo-preview {
  padding: 32px 24px;
  background: var(--color-background-tertiary);
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 16px;
}

.demo-toolbar {
  display: flex;
  justify-content: flex-end;
  gap: 4px;
  padding: 6px 12px;
  background: var(--color-background-secondary);
  border-top: 1px solid var(--color-border);
}

.toolbar-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 30px;
  height: 30px;
  border: none;
  border-radius: var(--radius-sm);
  background: transparent;
  color: var(--color-text-muted);
  cursor: pointer;
  font-size: 15px;
  transition: all var(--transition-fast);

  &:hover {
    background: rgba(255, 255, 255, 0.08);
    color: var(--color-text);
  }

  .copied {
    color: var(--color-success);
  }
}

.demo-code {
  border-top: 1px solid var(--color-border);

  pre {
    margin: 0;
    padding: 16px;
    background: #0d0d0d;
    overflow-x: auto;
  }

  code {
    font-family: "SF Mono", "Fira Code", "Fira Mono", "Roboto Mono", monospace;
    font-size: 13px;
    line-height: 1.6;
  }
}
</style>
