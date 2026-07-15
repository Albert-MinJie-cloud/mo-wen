<script lang="ts">
export interface AgentStep {
  key: string;
  icon: any;
  title: string;
  desc: string;
  status: "waiting" | "processing" | "done" | "error";
}
</script>

<script setup lang="ts">
import {
  FileTextOutlined,
  OrderedListOutlined,
  EditOutlined,
  PictureOutlined,
  ThunderboltOutlined,
  MergeCellsOutlined,
  CheckCircleFilled,
  LoadingOutlined,
  ExclamationCircleFilled,
  RocketOutlined,
} from "@ant-design/icons-vue";

withDefaults(
  defineProps<{
    agentSteps: AgentStep[];
    isCreating?: boolean;
    isCompleted?: boolean;
    doneCount?: number;
    totalSteps?: number;
  }>(),
  {
    isCreating: false,
    isCompleted: false,
    doneCount: 0,
    totalSteps: 0,
  },
);
</script>

<template>
  <aside class="left-panel">
    <div class="panel-card">
      <div class="panel-header">
        <RocketOutlined class="panel-header-icon" />
        <span>智能体流水线</span>
      </div>

      <div class="pipeline">
        <div
          v-for="(step, index) in agentSteps"
          :key="step.key"
          :class="['pipeline-node', step.status]"
        >
          <!-- 连接线 -->
          <div
            v-if="index > 0"
            :class="['pipeline-line', { active: step.status !== 'waiting' }]"
          />

          <!-- 节点 -->
          <div class="node-body">
            <div :class="['node-icon-wrap', step.status]">
              <component :is="step.icon" class="node-icon" />
              <CheckCircleFilled v-if="step.status === 'done'" class="node-badge" />
              <LoadingOutlined v-if="step.status === 'processing'" class="node-badge spinning" />
              <ExclamationCircleFilled v-if="step.status === 'error'" class="node-badge error-badge" />
            </div>
            <div class="node-text">
              <span class="node-title">{{ step.title }}</span>
              <span class="node-desc">{{ step.desc }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 进度条 -->
      <div v-if="isCreating || isCompleted" class="pipeline-progress">
        <div class="progress-text">
          {{ doneCount }} / {{ totalSteps }} 完成
        </div>
        <div class="progress-track">
          <div
            class="progress-fill"
            :style="{ width: totalSteps > 0 ? (doneCount / totalSteps) * 100 + '%' : '0%' }"
          />
        </div>
      </div>
    </div>
  </aside>
</template>

<style scoped lang="scss">
.left-panel {
  padding: 24px 16px;
  overflow-y: auto;
  background: var(--color-background-secondary);
  border-right: 1px solid var(--color-border);
}

.panel-card {
  margin-bottom: 20px;
}

.panel-card:last-child {
  margin-bottom: 0;
}

.panel-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  font-weight: 600;
  color: var(--color-text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 1px solid var(--color-border);
}

.panel-header-icon {
  font-size: 14px;
  color: var(--color-primary);
}

/* 流水线 */
.pipeline {
  display: flex;
  flex-direction: column;
  gap: 0;
}

.pipeline-node {
  display: flex;
  flex-direction: column;
}

.pipeline-line {
  width: 2px;
  height: 16px;
  margin-left: 21px;
  background: var(--color-border);
  transition: background var(--transition-normal);
}

.pipeline-line.active {
  background: var(--color-primary);
}

.node-body {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 6px 0;
}

.node-icon-wrap {
  width: 44px;
  height: 44px;
  border-radius: var(--radius-lg);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  background: var(--color-background-tertiary);
  border: 1.5px solid var(--color-border);
  position: relative;
  transition: all var(--transition-fast);
}

.node-icon {
  font-size: 18px;
  color: var(--color-text-muted);
  transition: color var(--transition-fast);
}

.node-badge {
  position: absolute;
  bottom: -3px;
  right: -3px;
  font-size: 12px;
  color: var(--color-success);
  background: var(--color-background-secondary);
  border-radius: 50%;
}

.node-badge.spinning {
  color: var(--color-primary);
  animation: spin 1s linear infinite;
}

.node-badge.error-badge {
  color: var(--color-error);
}

/* 节点状态样式 */
.pipeline-node.processing .node-icon-wrap {
  border-color: var(--color-primary);
  box-shadow: 0 0 12px rgba(59, 130, 246, 0.25);
  background: rgba(59, 130, 246, 0.1);
}

.pipeline-node.processing .node-icon {
  color: var(--color-primary);
}

.pipeline-node.done .node-icon-wrap {
  border-color: rgba(34, 197, 94, 0.4);
  background: rgba(34, 197, 94, 0.06);
}

.pipeline-node.done .node-icon {
  color: var(--color-success);
}

.pipeline-node.error .node-icon-wrap {
  border-color: rgba(239, 68, 68, 0.4);
  background: rgba(239, 68, 68, 0.06);
}

.pipeline-node.error .node-icon {
  color: var(--color-error);
}

.node-text {
  display: flex;
  flex-direction: column;
  gap: 2px;
  padding-top: 3px;
}

.node-title {
  font-size: 13px;
  font-weight: 600;
  color: var(--color-text-muted);
  transition: color var(--transition-fast);
}

.pipeline-node.processing .node-title {
  color: var(--color-text);
}

.pipeline-node.done .node-title {
  color: var(--color-text-secondary);
}

.node-desc {
  font-size: 11px;
  color: var(--color-text-muted);
  line-height: 1.4;
}

/* 流水线进度 */
.pipeline-progress {
  margin-top: 20px;
  padding-top: 16px;
  border-top: 1px solid var(--color-border);
}

.progress-text {
  font-size: 12px;
  color: var(--color-text-secondary);
  margin-bottom: 8px;
  font-weight: 500;
}

.progress-track {
  height: 4px;
  background: var(--color-border);
  border-radius: 2px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: var(--gradient-primary);
  border-radius: 2px;
  transition: width 0.5s ease;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}
</style>
