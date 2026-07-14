<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { useLoginUserStore } from "@/stores/loginUser";
import EditorMockup from "@/components/EditorMockup.vue";
import Button from "@/components/Button.vue";
// import { listArticle } from "@/api/articleController";
import { formatTime } from "@/utils/format";
import { ARTICLE_STATUS_MAP } from "@/utils/article";
import {
  FileTextOutlined,
  OrderedListOutlined,
  EditOutlined,
  PictureOutlined,
  ThunderboltOutlined,
  ClockCircleOutlined,
  RightOutlined,
} from "@ant-design/icons-vue";

const router = useRouter();
const loginUserStore = useLoginUserStore();

// 最近文章
const recentArticles = ref<API.ArticleVO[]>([]);
const loadingArticles = ref(false);

const goToCreate = () => {
  router.push("/create");
};

const goToList = () => {
  router.push("/article/list");
};

const viewArticle = (article: API.ArticleVO) => {
  router.push(`/article/${article.taskId}`);
};

// 加载最近文章
const loadRecentArticles = async () => {
  if (!loginUserStore.loginUser.id) return;

  loadingArticles.value = true;
  try {
    const res = await listArticle({ pageNum: 1, pageSize: 6 });
    recentArticles.value = res.data.data?.records || [];
  } catch (error) {
    console.error("加载文章失败:", error);
  } finally {
    loadingArticles.value = false;
  }
};

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

onMounted(() => {
  loadRecentArticles();
});
</script>

<template>
  <div id="homePage">
    <!-- Hero Section -->
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

        <!-- <p class="hero-tips">
          工作总结、心得体会、演讲稿、分析报告... 一键生成
        </p> -->
      </div>
    </div>

    <!-- Mockup Section -->
    <EditorMockup />

    <!-- Features Section -->
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

    <!-- Recent Articles Section -->
    <div
      v-if="loginUserStore.loginUser.id && recentArticles.length > 0"
      class="articles-section"
    >
      <div class="container">
        <div class="section-header-row">
          <div>
            <h2 class="section-title-sm">最近创作</h2>
            <p class="section-subtitle-sm">查看您最近创作的文章</p>
          </div>
          <a-button type="link" @click="goToList" class="view-all-btn">
            查看全部
            <RightOutlined />
          </a-button>
        </div>

        <a-spin :spinning="loadingArticles">
          <div class="articles-grid">
            <div
              v-for="article in recentArticles"
              :key="article.id"
              class="article-card"
              @click="viewArticle(article)"
            >
              <div class="article-cover">
                <img
                  v-if="article.coverImage"
                  :src="article.coverImage"
                  :alt="article.mainTitle"
                />
                <div v-else class="cover-placeholder">
                  <FileTextOutlined />
                </div>
              </div>
              <div class="article-info">
                <h4 class="article-title">
                  {{ article.mainTitle || article.topic }}
                </h4>
                <div class="article-meta">
                  <span class="article-time">
                    <ClockCircleOutlined />
                    {{ formatTime(article.createTime, "MM-DD HH:mm") }}
                  </span>
                  <span
                    :class="[
                      'article-status',
                      `status-${article.status?.toLowerCase()}`,
                    ]"
                  >
                    {{ ARTICLE_STATUS_MAP[article.status]?.text || article.status }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </a-spin>
      </div>
    </div>
  </div>
</template>

<style scoped>
#homePage {
  width: 100%;
  margin: 0;
  padding: 0;
  min-height: 100vh;
  background: var(--color-background);
}

/* Hero Section */
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

.hero-tips {
  font-size: 14px;
  color: var(--color-text-muted);
  margin: 0;
}

/* Features Section */
.features-section {
  padding: 80px 20px;
  background: var(--color-background-secondary);
}

.features-section .container {
  max-width: 1100px;
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

/* Articles Section */
.articles-section {
  padding: 60px 20px 80px;
  background: var(--color-background);
}

.articles-section .container {
  max-width: 1100px;
}

.section-header-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 32px;
}

.section-title-sm {
  font-size: 24px;
  font-weight: 700;
  margin: 0 0 4px;
  color: var(--color-text);
}

.section-subtitle-sm {
  font-size: 14px;
  color: var(--color-text-secondary);
  margin: 0;
}

.view-all-btn {
  display: flex;
  align-items: center;
  gap: 4px;
  color: var(--color-primary);
  font-weight: 500;
  padding: 0;
}

.view-all-btn:hover {
  color: var(--color-primary-dark);
}

.articles-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}

.article-card {
  background: var(--color-background-tertiary);
  border-radius: var(--radius-lg);
  border: 1px solid var(--color-border);
  overflow: hidden;
  transition: all var(--transition-normal);
  cursor: pointer;
}

.article-card:hover {
  border-color: var(--color-primary-light);
  box-shadow: var(--shadow-card-hover);
  transform: translateY(-2px);
}

.article-cover {
  height: 140px;
  background: var(--color-background-tertiary);
  overflow: hidden;
}

.article-cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.cover-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 32px;
  color: var(--color-text-muted);
}

.article-info {
  padding: 16px;
}

.article-title {
  font-size: 15px;
  font-weight: 600;
  margin: 0 0 12px;
  color: var(--color-text);
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.article-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.article-time {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  color: var(--color-text-muted);
}

.article-status {
  font-size: 12px;
  padding: 2px 8px;
  border-radius: var(--radius-sm);
  font-weight: 500;
}

.article-status.status-completed {
  background: rgba(59, 130, 246, 0.1);
  color: var(--color-primary-dark);
}

.article-status.status-processing {
  background: rgba(59, 130, 246, 0.1);
  color: #2563eb;
}

.article-status.status-pending {
  background: var(--color-background-tertiary);
  color: var(--color-text-muted);
}

/* Responsive */
@media (max-width: 992px) {
  .features-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .articles-grid {
    grid-template-columns: repeat(2, 1fr);
  }
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

  .features-grid {
    grid-template-columns: 1fr;
  }

  .articles-grid {
    grid-template-columns: 1fr;
  }

  .section-title {
    font-size: 24px;
  }

  .section-header-row {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }
}
</style>
