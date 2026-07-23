<script setup lang="ts">
import { computed } from "vue";
import { FileTextOutlined, EditOutlined, PictureOutlined, RocketOutlined, LockOutlined } from "@ant-design/icons-vue";
import { ARTICLE_STYLE_OPTIONS, IMAGE_METHOD_OPTIONS } from "@/utils/article";
import { message } from "@/message";
import Button from "@/components/Button.vue";

const props = withDefaults(
  defineProps<{
    topic?: string;
    style?: string | null;
    enabledImageMethods?: string[];
    canSubmit?: boolean;
    isVip?: boolean;
  }>(),
  {
    topic: "",
    style: null,
    enabledImageMethods: () => [],
    canSubmit: false,
    isVip: false,
  },
);

const emit = defineEmits<{
  (e: "update:topic", value: string): void;
  (e: "update:style", value: string | null): void;
  (e: "toggleImageMethod", method: string): void;
  (e: "startCreate"): void;
}>();

const topicModel = computed({
  get: () => props.topic,
  set: (v) => emit("update:topic", v),
});

function onToggleStyle(optValue: string) {
  emit("update:style", props.style === optValue ? null : optValue);
}

function onToggleMethod(method: string, vipOnly: boolean) {
  if (vipOnly && !props.isVip) {
    message.warning("此配图方式仅限 VIP 会员使用");
    return;
  }
  emit("toggleImageMethod", method);
}
</script>

<template>
  <div class="center-card">
    <div class="center-card-header">
      <h2 class="center-card-title">创作新文章</h2>
      <p class="center-card-subtitle">输入选题，AI 智能体将自动协作完成创作</p>
    </div>

    <div class="form-section">
      <label class="form-label">
        <FileTextOutlined /> 文章选题
      </label>
      <a-textarea
        v-model:value="topicModel"
        placeholder="请输入你想创作的文章主题..."
        :rows="3"
        :maxlength="500"
        show-count
        class="topic-textarea"
      />
    </div>

    <div class="form-section">
      <label class="form-label">
        <EditOutlined /> 文章风格
      </label>
      <div class="style-chips">
        <span
          v-for="opt in ARTICLE_STYLE_OPTIONS"
          :key="opt.value"
          :class="['style-chip', { active: style === opt.value }]"
          @click="onToggleStyle(opt.value)"
        >
          {{ opt.label }}
        </span>
      </div>
    </div>

    <div class="form-section">
      <label class="form-label">
        <PictureOutlined /> 配图方式
        <span class="label-hint">（留空支持全部）</span>
      </label>
      <div class="image-method-chips">
        <span
          v-for="opt in IMAGE_METHOD_OPTIONS"
          :key="opt.value"
          :class="[
            'method-chip',
            {
              active: enabledImageMethods.includes(opt.value),
              'vip-only': opt.vipOnly && !isVip,
            },
          ]"
          :title="opt.vipOnly && !isVip ? `${opt.desc}（VIP专属）` : opt.desc"
          @click="onToggleMethod(opt.value, opt.vipOnly)"
        >
          <LockOutlined v-if="opt.vipOnly && !isVip" class="vip-lock" />
          {{ opt.label }}
          <span v-if="opt.vipOnly && !isVip" class="vip-tag">VIP</span>
        </span>
      </div>
    </div>

    <div class="form-actions">
      <Button variant="primary" size="lg" :disabled="!canSubmit" @click="emit('startCreate')">
        <RocketOutlined /> 开始创作
      </Button>
    </div>
  </div>
</template>

<style scoped lang="scss">
.center-card {
  max-width: 760px;
  margin: 0 auto;
}

.center-card-header {
  margin-bottom: 36px;
}

.center-card-title {
  font-size: 26px;
  font-weight: 700;
  color: var(--color-text);
  margin: 0 0 8px;
  letter-spacing: -0.5px;
}

.center-card-subtitle {
  font-size: 15px;
  color: var(--color-text-secondary);
  margin: 0;
}

.form-section {
  margin-bottom: 28px;
}

.form-label {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 14px;
  font-weight: 600;
  color: var(--color-text);
  margin-bottom: 10px;
}

.label-hint {
  font-weight: 400;
  font-size: 12px;
  color: var(--color-text-muted);
}

.topic-textarea :deep(textarea) {
  background: var(--color-background-tertiary) !important;
  border-color: var(--color-border) !important;
  color: var(--color-text) !important;
  font-size: 15px;
  line-height: 1.7;
  resize: none;
  border-radius: var(--radius-md) !important;
}

.topic-textarea :deep(textarea):focus {
  border-color: var(--color-primary) !important;
  box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.15) !important;
}

.style-chips,
.image-method-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.style-chip,
.method-chip {
  padding: 6px 14px;
  border-radius: var(--radius-full);
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all var(--transition-fast);
  background: var(--color-background-tertiary);
  border: 1px solid var(--color-border);
  color: var(--color-text-secondary);
}

.style-chip:hover,
.method-chip:hover {
  border-color: var(--color-primary-light);
  color: var(--color-text);
}

.style-chip.active,
.method-chip.active {
  background: rgba(59, 130, 246, 0.12);
  border-color: var(--color-primary);
  color: var(--color-primary);
}

.method-chip.vip-only {
  opacity: 0.5;
  cursor: not-allowed;
}

.method-chip.vip-only:hover {
  border-color: var(--color-border);
  color: var(--color-text-secondary);
}

.vip-lock {
  font-size: 11px;
  margin-right: 2px;
}

.vip-tag {
  font-size: 10px;
  font-weight: 700;
  color: var(--color-accent-purple);
  margin-left: 4px;
  padding: 1px 5px;
  border-radius: var(--radius-sm);
  background: rgba(168, 85, 247, 0.12);
}

.form-actions {
  padding-top: 8px;
  text-align: center;
}
</style>
