<template>
  <Teleport to="body">
    <div class="message-container">
      <TransitionGroup name="msg">
        <div
          v-for="msg in messages"
          :key="msg.id"
          :class="['message-item', `message-item--${msg.type}`]"
        >
          <CheckCircleFilled v-if="msg.type === 'success'" class="msg-icon" />
          <CloseCircleFilled v-else-if="msg.type === 'error'" class="msg-icon" />
          <WarningFilled v-else-if="msg.type === 'warning'" class="msg-icon" />
          <InfoCircleFilled v-else class="msg-icon" />
          <span>{{ msg.content }}</span>
        </div>
      </TransitionGroup>
    </div>
  </Teleport>
</template>

<script setup lang="ts">
import { useMessage } from "@/composables/useMessage";
import {
  CheckCircleFilled,
  CloseCircleFilled,
  WarningFilled,
  InfoCircleFilled,
} from "@ant-design/icons-vue";

const { messages } = useMessage();
</script>

<style scoped lang="scss">
.message-container {
  position: fixed;
  top: 24px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 10000;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  pointer-events: none;
}

.message-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 20px;
  border-radius: var(--radius-md);
  font-size: 14px;
  font-weight: 500;
  pointer-events: auto;
  backdrop-filter: blur(12px);
  box-shadow: var(--shadow-lg);

  &--success {
    background: var(--toast-success-bg);
    border: 1px solid var(--toast-success-border);
    color: var(--toast-success-text);

    .msg-icon { color: var(--toast-success-icon); }
  }

  &--error {
    background: var(--toast-error-bg);
    border: 1px solid var(--toast-error-border);
    color: var(--toast-error-text);

    .msg-icon { color: var(--toast-error-icon); }
  }

  &--warning {
    background: var(--toast-warning-bg);
    border: 1px solid var(--toast-warning-border);
    color: var(--toast-warning-text);

    .msg-icon { color: var(--toast-warning-icon); }
  }

  &--info {
    background: var(--toast-info-bg);
    border: 1px solid var(--toast-info-border);
    color: var(--toast-info-text);

    .msg-icon { color: var(--toast-info-icon); }
  }
}

.msg-icon {
  font-size: 16px;
  flex-shrink: 0;
}

/* Transition */
.msg-enter-active {
  transition: all 300ms ease-out;
}

.msg-leave-active {
  transition: all 200ms ease-in;
}

.msg-enter-from {
  opacity: 0;
  transform: translateY(-16px);
}

.msg-leave-to {
  opacity: 0;
  transform: translateY(-16px);
}
</style>
