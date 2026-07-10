<template>
  <Teleport to="body">
    <div class="toast-container">
      <TransitionGroup name="toast">
        <div
          v-for="toast in toasts"
          :key="toast.id"
          :class="['toast-item', `toast-item--${toast.type}`]"
          @click="remove(toast.id)"
        >
          <CheckCircleFilled v-if="toast.type === 'success'" class="toast-icon" />
          <CloseCircleFilled v-else-if="toast.type === 'error'" class="toast-icon" />
          <WarningFilled v-else-if="toast.type === 'warning'" class="toast-icon" />
          <InfoCircleFilled v-else class="toast-icon" />
          <span class="toast-message">{{ toast.message }}</span>
        </div>
      </TransitionGroup>
    </div>
  </Teleport>
</template>

<script setup lang="ts">
import { useToast } from "@/composables/useToast";
import {
  CheckCircleFilled,
  CloseCircleFilled,
  WarningFilled,
  InfoCircleFilled,
} from "@ant-design/icons-vue";

const { toasts, remove } = useToast();
</script>

<style scoped lang="scss">
.toast-container {
  position: fixed;
  top: 80px;
  right: 24px;
  z-index: 9999;
  display: flex;
  flex-direction: column;
  gap: 10px;
  pointer-events: none;
}

.toast-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 20px;
  border-radius: var(--radius-lg);
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  pointer-events: auto;
  backdrop-filter: blur(12px);
  transition: all 200ms ease;
  min-width: 280px;
  max-width: 420px;

  &:hover {
    transform: translateX(-4px);
  }

  &--success {
    background: var(--toast-success-bg);
    border: 1px solid var(--toast-success-border);
    color: var(--toast-success-text);

    .toast-icon {
      color: var(--toast-success-icon);
    }
  }

  &--error {
    background: var(--toast-error-bg);
    border: 1px solid var(--toast-error-border);
    color: var(--toast-error-text);

    .toast-icon {
      color: var(--toast-error-icon);
    }
  }

  &--warning {
    background: var(--toast-warning-bg);
    border: 1px solid var(--toast-warning-border);
    color: var(--toast-warning-text);

    .toast-icon {
      color: var(--toast-warning-icon);
    }
  }

  &--info {
    background: var(--toast-info-bg);
    border: 1px solid var(--toast-info-border);
    color: var(--toast-info-text);

    .toast-icon {
      color: var(--toast-info-icon);
    }
  }
}

.toast-icon {
  font-size: 18px;
  flex-shrink: 0;
}

.toast-message {
  line-height: 1.4;
}

/* Transition */
.toast-enter-active {
  transition: all 300ms ease-out;
}

.toast-leave-active {
  transition: all 200ms ease-in;
}

.toast-enter-from {
  opacity: 0;
  transform: translateX(40px);
}

.toast-leave-to {
  opacity: 0;
  transform: translateX(40px);
}
</style>
