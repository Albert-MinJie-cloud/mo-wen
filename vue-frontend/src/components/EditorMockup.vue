<template>
  <section class="mockup-section">
    <div class="container">
      <div class="mockup-card">
        <!-- Editor Header -->
        <div class="mockup-header">
          <div class="traffic-lights">
            <div class="light light-red"></div>
            <div class="light light-yellow"></div>
            <div class="light light-green"></div>
          </div>
          <div class="header-title">mowen-editor.app</div>
        </div>

        <!-- Editor Body -->
        <div class="mockup-body">
          <!-- Sidebar -->
          <div class="mockup-sidebar">
            <div class="sidebar-section">
              <div class="sidebar-label">创作配置</div>

              <div class="config-group">
                <label class="config-label">目标平台</label>
                <div class="config-select">
                  小红书
                  <RightOutlined class="select-arrow" />
                </div>
              </div>

              <div class="config-group">
                <label class="config-label">爆款风格</label>
                <div class="config-option">
                  强烈共鸣 / 痛点挖掘
                </div>
              </div>

              <div class="config-group">
                <label class="config-label">字数限制</label>
                <div class="config-option">500 - 800 字</div>
              </div>
            </div>

            <div class="sidebar-footer">
              <button class="generate-btn">
                <ThunderboltOutlined />
                生成爆款文案
              </button>
            </div>
          </div>

          <!-- Main Canvas -->
          <div class="mockup-canvas">
            <div class="canvas-content">
              <h3 class="article-title">
                那些年薪百万的年轻人，都有这3个反直觉的习惯...
              </h3>
              <div class="article-body">
                <p class="article-paragraph">
                  <span class="bullet"></span>
                  <span>
                    在这个充满焦虑的时代，我们总是习惯于向外寻找答案。但真正的高手，往往都是在向内探索。
                  </span>
                </p>
                <p class="article-paragraph">
                  <span class="bullet"></span>
                  <span>
                    今天分享的这三个习惯，可能会颠覆你以往的认知，但这正是拉开人与人差距的核心秘密。尤其是第三个，99%的人都在做错。
                  </span>
                </p>

                <!-- AI Suggestion Card -->
                <div class="ai-card">
                  <div class="ai-card-border"></div>
                  <p class="ai-card-title">
                    <ThunderboltOutlined />
                    AI 留存率优化建议
                  </p>
                  <p class="ai-card-text">
                    此处建议插入一个真实的个人职场困境案例（如：25岁遭遇职业瓶颈）。根据数据大盘分析，这能将前3秒的读者流失率降低
                    30%，大幅提升完播和互动率。
                  </p>
                  <div class="ai-card-actions">
                    <button class="ai-btn-primary">采纳并生成案例</button>
                    <button class="ai-btn-secondary">忽略</button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { RightOutlined, ThunderboltOutlined } from "@ant-design/icons-vue";
</script>

<style scoped lang="scss">
.mockup-section {
  padding: 0 20px 80px;
  position: relative;
  z-index: 10;

  .container {
    max-width: 1100px;
    margin: 0 auto;
  }
}

.mockup-card {
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  background: #121214;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
  overflow: hidden;
}

/* Header */
.mockup-header {
  height: 48px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  display: flex;
  align-items: center;
  padding: 0 16px;
  gap: 12px;
  background: #09090b;
}

.traffic-lights {
  display: flex;
  gap: 6px;
}

.light {
  width: 12px;
  height: 12px;
  border-radius: 50%;

  &-red {
    background: rgba(239, 68, 68, 0.8);
  }

  &-yellow {
    background: rgba(234, 179, 8, 0.8);
  }

  &-green {
    background: rgba(34, 197, 94, 0.8);
  }
}

.header-title {
  flex: 1;
  text-align: center;
  font-size: 12px;
  font-weight: 500;
  color: #737373;
  margin-right: 44px; // offset to center
}

/* Body */
.mockup-body {
  display: flex;
  height: 480px;
}

/* Sidebar */
.mockup-sidebar {
  width: 256px;
  border-right: 1px solid rgba(255, 255, 255, 0.05);
  background: #0e0e11;
  padding: 20px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  flex-shrink: 0;
}

.sidebar-section {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.sidebar-label {
  font-size: 12px;
  font-weight: 600;
  color: #737373;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.config-group {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.config-label {
  font-size: 12px;
  color: #a3a3a3;
  padding-left: 4px;
}

.config-select {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 12px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
  font-size: 14px;
  color: #fff;
  border: 1px solid rgba(255, 255, 255, 0.1);

  .select-arrow {
    font-size: 12px;
    color: #737373;
  }
}

.config-option {
  padding: 8px 12px;
  border-radius: 8px;
  font-size: 14px;
  color: #d4d4d4;
  border: 1px solid transparent;
  cursor: default;
}

.sidebar-footer {
  margin-top: auto;
}

.generate-btn {
  width: 100%;
  padding: 10px 0;
  background: linear-gradient(135deg, #06b6d4, #3b82f6);
  color: #fff;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  border: none;
  cursor: pointer;

  &:hover {
    opacity: 0.9;
  }
}

/* Canvas */
.mockup-canvas {
  flex: 1;
  padding: 32px 40px;
  background: #121214;
  overflow-y: auto;
}

.canvas-content {
  max-width: 600px;
  margin: 0 auto;
}

.article-title {
  font-size: 26px;
  font-weight: 700;
  color: #fff;
  margin: 0 0 24px;
  line-height: 1.4;
  letter-spacing: -0.5px;
}

.article-body {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.article-paragraph {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  margin: 0;
  font-size: 15px;
  color: #a3a3a3;
  line-height: 1.7;
}

.bullet {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #06b6d4;
  flex-shrink: 0;
  margin-top: 9px;
  box-shadow: 0 0 8px rgba(6, 182, 212, 0.8);
}

/* AI Card */
.ai-card {
  margin-top: 24px;
  padding: 16px;
  background: rgba(59, 130, 246, 0.1);
  border: 1px solid rgba(59, 130, 246, 0.2);
  border-radius: 12px;
  position: relative;
  overflow: hidden;

  .ai-card-border {
    position: absolute;
    top: 0;
    left: 0;
    width: 4px;
    height: 100%;
    background: #3b82f6;
  }
}

.ai-card-title {
  font-size: 14px;
  font-weight: 500;
  color: #60a5fa;
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 0 0 8px;
}

.ai-card-text {
  font-size: 14px;
  color: #d4d4d4;
  margin: 0 0 12px;
  line-height: 1.6;
}

.ai-card-actions {
  display: flex;
  gap: 8px;
}

.ai-btn-primary {
  font-size: 12px;
  background: rgba(59, 130, 246, 0.2);
  color: #93c5fd;
  padding: 6px 12px;
  border-radius: 6px;
  border: none;
  cursor: pointer;

  &:hover {
    background: rgba(59, 130, 246, 0.3);
  }
}

.ai-btn-secondary {
  font-size: 12px;
  background: rgba(255, 255, 255, 0.05);
  color: #a3a3a3;
  padding: 6px 12px;
  border-radius: 6px;
  border: none;
  cursor: pointer;

  &:hover {
    background: rgba(255, 255, 255, 0.1);
  }
}

/* Responsive */
@media (max-width: 768px) {
  .mockup-body {
    flex-direction: column;
    height: auto;
  }

  .mockup-sidebar {
    width: 100%;
    border-right: none;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    flex-shrink: 1;
  }

  .mockup-canvas {
    padding: 24px 20px;
  }

  .article-title {
    font-size: 20px;
  }
}
</style>
