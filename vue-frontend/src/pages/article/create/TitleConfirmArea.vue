<script setup lang="ts">
import { computed } from "vue";

const props = withDefaults(
  defineProps<{
    userDescription?: string;
  }>(),
  {
    userDescription: "",
  },
);

const emit = defineEmits<{
  (e: "update:userDescription", value: string): void;
}>();

const userDescriptionModel = computed({
  get: () => props.userDescription,
  set: (v) => emit("update:userDescription", v),
});
</script>

<template>
  <div class="title-confirm-area">
    <div class="form-section">
      <label class="form-label">补充描述（可选）</label>
      <div class="desc-textarea">
        <a-textarea
          v-model:value="userDescriptionModel"
          placeholder="对文章内容的额外要求或说明..."
          :rows="2"
        />
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
.title-confirm-area {
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid var(--color-border);
}

.form-section {
  margin-bottom: 16px;
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

.desc-textarea :deep(textarea) {
  background: var(--color-background-tertiary) !important;
  border-color: var(--color-border) !important;
  color: var(--color-text) !important;
  font-size: 15px;
  line-height: 1.7;
  resize: none;
  border-radius: var(--radius-md) !important;

  &::placeholder {
    color: var(--color-text-secondary);
    opacity: 0.6;
  }
}

.desc-textarea :deep(textarea):hover {
  border-color: rgba(255, 255, 255, 0.15) !important;
}

.desc-textarea :deep(textarea):focus {
  border-color: var(--color-primary) !important;
  box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.15);
}
</style>
