<script setup lang="ts">
import { computed } from "vue";
import {
  ArrowUpOutlined,
  ArrowDownOutlined,
  DeleteOutlined,
  CloseOutlined,
} from "@ant-design/icons-vue";
import Button from "@/components/Button.vue";

const props = withDefaults(
  defineProps<{
    outlineSections?: any[];
    modifySuggestion?: string;
    isModifyingOutline?: boolean;
    isConfirmingOutline?: boolean;
  }>(),
  {
    outlineSections: () => [],
    modifySuggestion: "",
    isModifyingOutline: false,
    isConfirmingOutline: false,
  },
);

const emit = defineEmits<{
  (e: "addSection"): void;
  (e: "removeSection", index: number): void;
  (e: "moveSectionUp", index: number): void;
  (e: "moveSectionDown", index: number): void;
  (e: "addPoint", sectionIndex: number): void;
  (e: "removePoint", sectionIndex: number, pointIndex: number): void;
  (e: "update:modifySuggestion", value: string): void;
  (e: "aiModifyOutline"): void;
  (e: "confirmOutline"): void;
}>();

const modifySuggestionModel = computed({
  get: () => props.modifySuggestion,
  set: (v) => emit("update:modifySuggestion", v),
});
</script>

<template>
  <div class="stream-section">
    <h3 class="stream-section-title">
      编辑大纲
      <span class="section-count">· {{ outlineSections.length }} 章节</span>
    </h3>
    <div class="outline-tree">
      <div
        v-for="(section, si) in outlineSections"
        :key="si"
        class="outline-section editable"
      >
        <div class="outline-section-header">
          <span class="outline-section-num">{{ si + 1 }}</span>
          <a-input
            v-model:value="section.title"
            class="section-title-input"
            size="small"
          />
          <span class="section-actions">
            <Button
              size="sm"
              variant="secondary"
              :disabled="si === 0"
              @click="emit('moveSectionUp', si)"
            >
              <ArrowUpOutlined />
            </Button>
            <Button
              size="sm"
              variant="secondary"
              :disabled="si === outlineSections.length - 1"
              @click="emit('moveSectionDown', si)"
            >
              <ArrowDownOutlined />
            </Button>
            <Button
              size="sm"
              variant="secondary"
              :disabled="outlineSections.length <= 1"
              @click="emit('removeSection', si)"
            >
              <DeleteOutlined />
            </Button>
          </span>
        </div>
        <ul class="outline-points">
          <li
            v-for="(point, pi) in section.points"
            :key="pi"
            class="outline-point editable"
          >
            <span class="point-bullet" />
            <a-input
              v-model:value="section.points[pi]"
              class="point-input"
              size="small"
            />
            <Button
              size="sm"
              variant="secondary"
              @click="emit('removePoint', si, pi)"
            >
              <CloseOutlined />
            </Button>
          </li>
          <li class="outline-point add-point">
            <Button
              size="sm"
              variant="secondary"
              @click="emit('addPoint', si)"
            >
              + 添加要点
            </Button>
          </li>
        </ul>
      </div>
      <Button
        variant="secondary"
        size="sm"
        @click="emit('addSection')"
        style="margin-top: 8px"
      >
        + 添加章节
      </Button>
    </div>

    <div class="outline-edit-area">
      <div class="ai-modify-row">
        <a-textarea
          v-model:value="modifySuggestionModel"
          placeholder="输入修改建议，如：增加案例分析章节..."
          :rows="2"
        />
        <Button
          variant="gradient"
          size="sm"
          :disabled="!modifySuggestion.trim() || isModifyingOutline"
          @click="emit('aiModifyOutline')"
          style="margin-top: 8px"
        >
          AI 修改大纲
        </Button>
      </div>
      <Button
        variant="gradient"
        size="lg"
        :disabled="isModifyingOutline || isConfirmingOutline"
        block
        @click="emit('confirmOutline')"
        style="margin-top: 12px"
      >
        确认大纲，开始生成正文
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

.section-count {
  font-size: 12px;
  font-weight: 400;
  color: var(--color-text-muted);
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

.outline-section.editable {
  border-left-color: var(--color-primary);
  background: rgba(59, 130, 246, 0.03);
  margin-bottom: 8px;
  border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
}

.outline-section-header {
  display: flex;
  align-items: center;
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

.section-title-input {
  flex: 1;
  font-size: 14px;
  font-weight: 600;
  background: var(--color-background-tertiary) !important;
  color: var(--color-text) !important;
  border-color: var(--color-border) !important;

  &::placeholder { color: var(--color-text-muted); }
  &:focus {
    border-color: var(--color-primary) !important;
    box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.15);
  }
}

.section-actions {
  display: flex;
  gap: 2px;
  flex-shrink: 0;
}

.outline-points {
  margin: 8px 0 0 36px;
  padding: 0;
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.outline-point.editable {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 4px 0;
}

.point-bullet {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--color-text-muted);
  flex-shrink: 0;
}

.point-input {
  flex: 1;
  font-size: 13px;
  background: var(--color-background-tertiary) !important;
  color: var(--color-text) !important;
  border-color: var(--color-border) !important;

  &::placeholder { color: var(--color-text-muted); }
  &:focus {
    border-color: var(--color-primary) !important;
    box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.15);
  }
}

.outline-point.add-point {
  padding: 2px 0 2px 14px;
}

.outline-edit-area {
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid var(--color-border);
}

.ai-modify-row {
  display: flex;
  flex-direction: column;
  gap: 4px;
  margin-bottom: 8px;

  :deep(textarea) {
    background: var(--color-background-tertiary) !important;
    border-color: var(--color-border) !important;
    color: var(--color-text) !important;
    font-size: 14px;
    line-height: 1.6;
    border-radius: var(--radius-md) !important;
    resize: none;

    &::placeholder { color: var(--color-text-muted); }

    &:focus {
      border-color: var(--color-primary) !important;
      box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.15);
    }
  }
}

</style>
