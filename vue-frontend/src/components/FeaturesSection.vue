<script setup lang="ts">
import {
  FileTextOutlined,
  OrderedListOutlined,
  EditOutlined,
  PictureOutlined,
  ThunderboltOutlined,
  ClockCircleOutlined,
} from "@ant-design/icons-vue";

// 功能卡片数据
const features = [
  {
    icon: FileTextOutlined,
    title: "智能生成标题",
    description: "AI 自动分析选题，生成吸引眼球的爆款标题",
    color: "#06B6D4",
  },
  {
    icon: OrderedListOutlined,
    title: "自动生成大纲",
    description: "智能规划文章结构，确保逻辑清晰完整",
    color: "#3B82F6",
  },
  {
    icon: EditOutlined,
    title: "流式生成正文",
    description: "实时展示创作过程，体验打字机般的流畅输出",
    color: "#8B5CF6",
  },
  {
    icon: PictureOutlined,
    title: "智能配图",
    description: "自动检索高质量无版权图片，完美匹配内容",
    color: "#F59E0B",
  },
  {
    icon: ThunderboltOutlined,
    title: "快速高效",
    description: "5-10分钟完成全文创作，效率提升10倍",
    color: "#EF4444",
  },
  {
    icon: ClockCircleOutlined,
    title: "历史管理",
    description: "随时查看和管理所有创作记录，支持导出",
    color: "#06B6D4",
  },
];
</script>

<template>
  <div class="features-section">
    <div class="container">
      <div class="section-header">
        <div class="section-badge">核心能力</div>
        <h2 class="section-title">为什么创作者都在用墨文？</h2>
        <p class="section-subtitle">强大的 AI 能力，让创作变得简单高效</p>
      </div>
      <div class="features-grid">
        <div
          v-for="(feature, index) in features"
          :key="index"
          class="feature-card"
        >
          <div
            class="feature-icon-wrapper"
            :style="{ background: `${feature.color}15` }"
          >
            <component
              :is="feature.icon"
              class="feature-icon"
              :style="{ color: feature.color }"
            />
          </div>
          <div class="feature-content">
            <h3 class="feature-title">{{ feature.title }}</h3>
            <p class="feature-description">{{ feature.description }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.features-section {
  padding: 80px 20px;
  background: var(--color-background-secondary);
}

.features-section .container {
  max-width: 1100px;
  margin: 0 auto;
}

.section-header {
  text-align: center;
  margin-bottom: 48px;
}

.section-badge {
  display: inline-block;
  padding: 6px 14px;
  background: rgba(59, 130, 246, 0.1);
  border-radius: var(--radius-full);
  font-size: 13px;
  font-weight: 600;
  color: var(--color-primary-dark);
  margin-bottom: 16px;
}

.section-title {
  font-size: 32px;
  font-weight: 700;
  margin: 0 0 12px;
  color: var(--color-text);
  letter-spacing: -0.5px;
}

.section-subtitle {
  font-size: 16px;
  color: var(--color-text-secondary);
  margin: 0;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}

.feature-card {
  background: var(--color-background-tertiary);
  border-radius: var(--radius-lg);
  border: 1px solid var(--color-border);
  padding: 32px 24px;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 16px;
  transition: all var(--transition-normal);
  cursor: pointer;
}

.feature-card:hover {
  border-color: var(--color-primary-light);
  box-shadow: var(--shadow-card-hover);
  transform: translateY(-2px);
}

.feature-icon-wrapper {
  width: 56px;
  height: 56px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--radius-xl);
  flex-shrink: 0;
}

.feature-icon {
  font-size: 26px;
}

.feature-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.feature-title {
  font-size: 16px;
  font-weight: 600;
  margin: 0 0 6px;
  color: var(--color-text);
}

.feature-description {
  font-size: 14px;
  color: var(--color-text-secondary);
  margin: 0;
  line-height: 1.5;
}

@media (max-width: 992px) {
  .features-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .features-grid {
    grid-template-columns: 1fr;
  }

  .section-title {
    font-size: 24px;
  }
}
</style>
