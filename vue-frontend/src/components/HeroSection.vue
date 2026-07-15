<script setup lang="ts">
import { useRouter } from "vue-router";
import Button from "@/components/Button.vue";
import { ThunderboltOutlined } from "@ant-design/icons-vue";

const router = useRouter();

const goToCreate = () => {
  router.push("/create");
};
</script>

<template>
  <div class="hero-section">
    <div class="hero-bg"></div>
    <div class="container">
      <div class="hero-badge">
        <ThunderboltOutlined />
        <span>新一代 AI 爆文写作引擎已上线</span>
      </div>
      <div class="hero-titles">
        <h1 class="hero-title-white">重塑爆款逻辑，</h1>
        <h1 class="hero-title-blue">让灵感引爆全网。</h1>
      </div>

      <div class="hero-subtitles">
        <p class="hero-subtitle">
          墨文 (Mo-Wen) 深度解析小红书、公众号、头条等平台爆款基因。
        </p>
        <p class="hero-subtitle">
          只需输入核心观点，AI 即刻生成自带流量密码的高质量新媒体文章。
        </p>
      </div>

      <!-- CTA 按钮 -->
      <div class="cta-actions">
        <Button variant="primary" size="lg" @click="goToCreate">
          立即创作爆款
        </Button>
        <Button variant="secondary" size="lg"> 查看案例 </Button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.hero-section {
  position: relative;
  padding: 160px 0px;
  text-align: center;
  overflow: hidden;
}

.hero-bg {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 0;
}

.hero-bg::after {
  content: "";
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 600px;
  height: 400px;
  background: rgba(59, 130, 246, 0.15);
  filter: blur(120px);
  border-radius: 50%;
  pointer-events: none;
}

.container {
  position: relative;
  z-index: 1;
  max-width: 900px;
  margin: 0 auto;
}

.hero-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 4px 8px;
  background: var(--color-border);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-full);
  font-size: 14px;
  font-weight: 500;
  margin-bottom: 24px;
  color: var(--color-accent-cyan-light);
}

.hero-titles {
  margin-bottom: 40px;
}

.hero-title-white {
  font-size: 90px;
  font-weight: 700;
  color: var(--color-text);
  margin: 0;
  line-height: 1.25;
}

.hero-title-blue {
  font-size: 90px;
  font-weight: 700;
  background: var(--gradient-primary);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin: 0;
  line-height: 1.25;
}

.hero-subtitle {
  font-size: 20px;
  margin: 0;
  color: var(--color-text-secondary);
  font-weight: 400;
}

.cta-actions {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16px;
  margin-top: 40px;
  margin-bottom: 32px;
}

@media (max-width: 768px) {
  .hero-section {
    padding: 60px 20px 80px;
  }

  .hero-title-white,
  .hero-title-blue {
    font-size: 36px;
  }

  .hero-subtitle {
    font-size: 16px;
  }

  .cta-actions {
    flex-direction: column;
    width: 100%;
  }

  .cta-actions :deep(.btn) {
    width: 100%;
    justify-content: center;
  }
}
</style>
