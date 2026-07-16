<script setup lang="ts">
import { computed } from "vue";
import { CheckCircleFilled, EditOutlined } from "@ant-design/icons-vue";
import Input from "@/components/Input.vue";
import Button from "@/components/Button.vue";
import TitleConfirmArea from "./TitleConfirmArea.vue";

const props = withDefaults(
  defineProps<{
    titleOptions?: API.TitleOption[];
    selectedTitleIndex?: number;
    showTitleConfirm?: boolean;
    userDescription?: string;
    customMainTitle?: string;
    customSubTitle?: string;
    isConfirmingTitle?: boolean;
  }>(),
  {
    titleOptions: () => [],
    selectedTitleIndex: -1,
    showTitleConfirm: false,
    userDescription: "",
    customMainTitle: "",
    customSubTitle: "",
    isConfirmingTitle: false,
  },
);

const emit = defineEmits<{
  (e: "update:selectedTitleIndex", value: number): void;
  (e: "update:userDescription", value: string): void;
  (e: "update:customMainTitle", value: string): void;
  (e: "update:customSubTitle", value: string): void;
  (e: "confirmTitle"): void;
}>();

const isCustomSelected = computed(() => props.selectedTitleIndex === props.titleOptions.length);

const customMainTitleModel = computed({
  get: () => props.customMainTitle,
  set: (v) => emit("update:customMainTitle", v),
});

const customSubTitleModel = computed({
  get: () => props.customSubTitle,
  set: (v) => emit("update:customSubTitle", v),
});

function selectTitle(index: number) {
  emit("update:selectedTitleIndex", props.selectedTitleIndex === index ? -1 : index);
}

const canConfirm = computed(() => {
  if (isCustomSelected.value) {
    return props.customMainTitle.trim().length > 0;
  }
  return props.selectedTitleIndex >= 0;
});
</script>

<template>
  <div v-if="titleOptions.length > 0" class="stream-section">
    <h3 class="stream-section-title">备选标题</h3>
    <div class="title-cards">
      <!-- AI 生成的标题 -->
      <div
        v-for="(opt, i) in titleOptions"
        :key="i"
        :class="['title-card', { selected: selectedTitleIndex === i }]"
        @click="selectTitle(i)"
      >
        <span :class="['title-rank', { selected: selectedTitleIndex === i }]">
          <CheckCircleFilled v-if="selectedTitleIndex === i" />
          <span v-else>{{ i + 1 }}</span>
        </span>
        <div>
          <p class="t-main">{{ opt.mainTitle }}</p>
          <p class="t-sub">{{ opt.subTitle }}</p>
        </div>
      </div>

      <!-- 自定义标题 -->
      <div
        :class="['title-card', 'custom-title-card', { selected: isCustomSelected }]"
        @click="selectTitle(titleOptions.length)"
      >
        <span :class="['title-rank', { selected: isCustomSelected }]">
          <CheckCircleFilled v-if="isCustomSelected" />
          <EditOutlined v-else />
        </span>
        <div class="custom-title-content">
          <p class="t-main custom-title-label">自定义标题</p>
          <p class="t-sub">使用你自己想好的标题</p>
        </div>
      </div>
    </div>

    <!-- 自定义标题输入区 -->
    <div v-if="isCustomSelected" class="custom-title-inputs">
      <div class="form-section">
        <label class="form-label">主标题</label>
        <Input
          v-model:value="customMainTitleModel"
          placeholder="输入你的文章主标题..."
          size="large"
        />
      </div>
      <div class="form-section">
        <label class="form-label">副标题（可选）</label>
        <Input
          v-model:value="customSubTitleModel"
          placeholder="输入文章副标题..."
        />
      </div>
    </div>

    <TitleConfirmArea
      v-if="showTitleConfirm"
      :user-description="userDescription"
      @update:user-description="emit('update:userDescription', $event)"
    />
    <div v-if="showTitleConfirm" style="margin-top: 16px; text-align: center">
      <Button
        variant="primary"
        size="lg"
        :disabled="!canConfirm || isConfirmingTitle"
        @click="emit('confirmTitle')"
      >
        确认标题，继续生成大纲
      </Button>
    </div>
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

.title-cards {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.title-card {
  display: flex;
  gap: 14px;
  padding: 14px 16px;
  background: var(--color-background-tertiary);
  border-radius: var(--radius-md);
  border: 1.5px solid var(--color-border);
  cursor: pointer;
  transition: all var(--transition-fast);
  user-select: none;
}

.title-card:hover {
  border-color: var(--color-primary-light);
  background: rgba(59, 130, 246, 0.04);
  transform: translateX(4px);
}

.title-card.selected {
  border-color: var(--color-primary);
  background: rgba(59, 130, 246, 0.08);
  box-shadow: 0 0 0 1px rgba(59, 130, 246, 0.2), 0 2px 8px rgba(59, 130, 246, 0.1);
}

.custom-title-card {
  border-style: dashed;

  &.selected {
    border-style: solid;
  }
}

.title-rank {
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(59, 130, 246, 0.08);
  color: var(--color-text-muted);
  border-radius: var(--radius-sm);
  font-size: 13px;
  font-weight: 600;
  flex-shrink: 0;
  transition: all var(--transition-fast);
}

.title-card:hover .title-rank {
  background: rgba(59, 130, 246, 0.15);
  color: var(--color-primary);
}

.title-rank.selected {
  background: var(--color-primary);
  color: #fff;
  font-size: 14px;
}

.t-main {
  font-size: 15px;
  font-weight: 600;
  color: var(--color-text);
  margin: 0 0 4px;
  line-height: 1.4;
}

.t-sub {
  font-size: 13px;
  color: var(--color-text-secondary);
  margin: 0;
}

.custom-title-content {
  flex: 1;
}

.custom-title-label {
  color: var(--color-primary);
}

.custom-title-inputs {
  margin-top: 16px;
  padding: 16px;
  background: var(--color-background-tertiary);
  border-radius: var(--radius-md);
  border: 1px solid var(--color-border);
}

.form-section {
  margin-bottom: 16px;
}

.form-section:last-child {
  margin-bottom: 0;
}

.form-label {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 14px;
  font-weight: 600;
  color: var(--color-text);
  margin-bottom: 8px;
}

</style>
