<script setup lang="ts">
import { ref, reactive, onMounted } from "vue";
import { useRouter } from "vue-router";
import {
  listArticleApiArticleListPost,
  deleteArticleApiArticleDeletePost,
  getArticleApiArticleTaskIdGet,
} from "@/api/article";
import { message } from "@/message";
import Button from "@/components/Button.vue";
import DataList from "@/components/DataList.vue";
import { formatTime } from "@/utils/format";
import { ARTICLE_STATUS_MAP } from "@/utils/article";
import {
  PlusOutlined,
  SearchOutlined,
  FileTextOutlined,
  EyeOutlined,
  ExportOutlined,
  DeleteOutlined,
  ClockCircleOutlined,
  ReloadOutlined,
} from "@ant-design/icons-vue";

const router = useRouter();

// ============ 搜索 ============
const searchTopic = ref("");

// ============ 数据 ============
const items = ref<API.ArticleVO[]>([]);
const loading = ref(false);

const pagination = reactive({
  current: 1,
  pageSize: 10,
  total: 0,
});

// ============ 加载 ============
async function loadArticles() {
  loading.value = true;
  try {
    const res = await listArticleApiArticleListPost(
      {},
      {
        current: pagination.current,
        pageSize: pagination.pageSize,
        topic: searchTopic.value || undefined,
      }
    );
    if (res.data.code === 0 && res.data.data) {
      const result = res.data.data as any;
      items.value = result.records || [];
      pagination.total = result.total || 0;
    }
  } catch (e: any) {
    message.error(e?.message || "加载文章列表失败");
  } finally {
    loading.value = false;
  }
}

function doSearch() {
  pagination.current = 1;
  loadArticles();
}

// ============ 操作 ============
function clickItem(record: API.ArticleVO) {
  router.push(`/article/${record.taskId}`);
}

function goToCreate() {
  router.push("/create");
}

async function doExport(record: API.ArticleVO, e: Event) {
  e.stopPropagation();
  try {
    const res = await getArticleApiArticleTaskIdGet({ task_id: record.taskId });
    if (res.data.code !== 0 || !res.data.data) {
      message.error("获取文章内容失败");
      return;
    }
    const article = res.data.data;
    const title = article.mainTitle || article.topic || "文章";
    const content = article.fullContent || article.content || "";

    const blob = new Blob([content], { type: "text/markdown;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = `${title}.md`;
    link.click();
    URL.revokeObjectURL(url);
    message.success("导出成功");
  } catch {
    message.error("导出失败");
  }
}

async function doDelete(record: API.ArticleVO, e: Event) {
  e.stopPropagation();
  try {
    const res = await deleteArticleApiArticleDeletePost({}, { id: record.id });
    if (res.data.code === 0) {
      message.success("删除成功");
      loadArticles();
    } else {
      message.error(res.data.message || "删除失败");
    }
  } catch {
    message.error("删除失败");
  }
}

// ============ 分页 ============
const totalPages = ref(0);
function updateTotalPages() {
  totalPages.value = Math.ceil(pagination.total / pagination.pageSize);
}
function goPage(page: number) {
  if (page < 1 || page > totalPages.value) return;
  pagination.current = page;
  loadArticles();
  updateTotalPages();
}

function getStatusInfo(status: string) {
  return ARTICLE_STATUS_MAP[status] || { cls: "pending", text: status };
}

onMounted(() => {
  loadArticles().then(updateTotalPages);
});
</script>

<template>
  <div id="articleListPage">
    <div class="container">
      <!-- 头部 -->
      <div class="page-header">
        <div>
          <h1 class="page-title">文章列表</h1>
          <p class="page-subtitle">管理您创作的所有文章</p>
        </div>
        <Button variant="gradient" size="lg" @click="goToCreate">
          <PlusOutlined /> 创作新文章
        </Button>
      </div>

      <!-- 搜索栏 -->
      <div class="toolbar">
        <div class="search-box">
          <SearchOutlined class="search-icon" />
          <input
            v-model="searchTopic"
            placeholder="搜索选题..."
            class="search-input"
            @keyup.enter="doSearch"
          />
        </div>
        <Button variant="secondary" size="md" @click="loadArticles">
          <ReloadOutlined /> 刷新
        </Button>
        <span class="total-hint">共 {{ pagination.total }} 篇</span>
      </div>

      <!-- 列表 -->
      <DataList
        :items="items"
        :loading="loading"
        empty-text="还没有文章，快去创作第一篇吧"
        @click-item="clickItem"
      >
        <template #item="{ item }">
          <div class="article-row">
            <!-- 封面缩略图 -->
            <div class="row-cover">
              <img v-if="item.coverImage" :src="item.coverImage" alt="" />
              <FileTextOutlined v-else class="cover-placeholder" />
            </div>

            <!-- 主体信息 -->
            <div class="row-body">
              <div class="row-title">
                {{ item.mainTitle || "未命名" }}
              </div>
              <div class="row-meta">
                <span class="meta-topic">{{ item.topic }}</span>
                <span class="meta-time">
                  <ClockCircleOutlined />
                  {{ formatTime(item.createTime) }}
                </span>
              </div>
            </div>

            <!-- 状态 -->
            <div class="row-status">
              <span :class="['status-dot', getStatusInfo(item.status).cls]">
                {{ getStatusInfo(item.status).text }}
              </span>
            </div>

            <!-- 操作 -->
            <div class="row-actions">
              <span class="action-btn" title="查看" @click="router.push(`/article/${item.taskId}`)">
                <EyeOutlined />
              </span>
              <span class="action-btn" title="导出" @click="doExport(item, $event)">
                <ExportOutlined />
              </span>
              <a-popconfirm
                title="确定要删除这篇文章吗？"
                ok-text="确定"
                cancel-text="取消"
                @confirm="doDelete(item, $event)"
              >
                <span class="action-btn danger" title="删除" @click.stop>
                  <DeleteOutlined />
                </span>
              </a-popconfirm>
            </div>
          </div>
        </template>
      </DataList>

      <!-- 分页 -->
      <div v-if="totalPages > 1" class="pagination-bar">
        <button
          class="page-btn"
          :disabled="pagination.current <= 1"
          @click="goPage(pagination.current - 1)"
        >
          上一页
        </button>
        <template v-for="p in totalPages" :key="p">
          <button
            v-if="p === 1 || p === totalPages || Math.abs(p - pagination.current) <= 1"
            :class="['page-btn', { active: p === pagination.current }]"
            @click="goPage(p)"
          >
            {{ p }}
          </button>
          <span v-else-if="Math.abs(p - pagination.current) === 2" class="page-ellipsis">
            ...
          </span>
        </template>
        <button
          class="page-btn"
          :disabled="pagination.current >= totalPages"
          @click="goPage(pagination.current + 1)"
        >
          下一页
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
#articleListPage {
  width: 100%;
  min-height: calc(100vh - 64px - 48px);
  padding: 40px 20px 80px;
  background: var(--color-background);
}

.container {
  max-width: 960px;
  margin: 0 auto;
}

/* 头部 */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 24px;
}

.page-title {
  font-size: 24px;
  font-weight: 700;
  color: var(--color-text);
  margin: 0 0 4px;
  letter-spacing: -0.5px;
}

.page-subtitle {
  font-size: 14px;
  color: var(--color-text-secondary);
  margin: 0;
}

/* 工具栏 */
.toolbar {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 20px;
}

.search-box {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 0 14px;
  background: var(--color-background-tertiary);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  flex: 1;
  max-width: 320px;
  transition: border-color var(--transition-fast);
}

.search-box:focus-within {
  border-color: var(--color-primary);
}

.search-icon {
  color: var(--color-text-muted);
  font-size: 14px;
  flex-shrink: 0;
}

.search-input {
  flex: 1;
  background: none;
  border: none;
  outline: none;
  color: var(--color-text);
  font-size: 14px;
  padding: 8px 0;
}

.search-input::placeholder {
  color: var(--color-text-muted);
}

.total-hint {
  margin-left: auto;
  font-size: 13px;
  color: var(--color-text-muted);
}

/* 行样式 */
.article-row {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px 20px;
}

.row-cover {
  width: 56px;
  height: 42px;
  border-radius: 6px;
  overflow: hidden;
  flex-shrink: 0;
  background: var(--color-background-secondary);
  display: flex;
  align-items: center;
  justify-content: center;
}

.row-cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.cover-placeholder {
  font-size: 18px;
  color: var(--color-text-muted);
  opacity: 0.4;
}

.row-body {
  flex: 1;
  min-width: 0;
}

.row-title {
  font-size: 15px;
  font-weight: 600;
  color: var(--color-text);
  line-height: 1.4;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.row-meta {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-top: 4px;
}

.meta-topic {
  font-size: 13px;
  color: var(--color-text-secondary);
}

.meta-time {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  color: var(--color-text-muted);
}

/* 状态 */
.row-status {
  flex-shrink: 0;
}

.status-dot {
  font-size: 12px;
  font-weight: 500;
  padding: 2px 10px;
  border-radius: var(--radius-full);
  white-space: nowrap;
}

.status-dot.completed {
  background: rgba(34, 197, 94, 0.1);
  color: #4ade80;
}

.status-dot.processing {
  background: rgba(59, 130, 246, 0.12);
  color: #60a5fa;
}

.status-dot.pending {
  background: rgba(255, 255, 255, 0.05);
  color: var(--color-text-muted);
}

.status-dot.failed {
  background: rgba(239, 68, 68, 0.1);
  color: #f87171;
}

/* 操作 */
.row-actions {
  display: flex;
  align-items: center;
  gap: 4px;
  flex-shrink: 0;
  opacity: 0;
  transition: opacity var(--transition-fast);
}

.data-list-item:hover .row-actions {
  opacity: 1;
}

.action-btn {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--radius-sm);
  color: var(--color-text-secondary);
  cursor: pointer;
  transition: all var(--transition-fast);
  font-size: 14px;
}

.action-btn:hover {
  background: rgba(59, 130, 246, 0.1);
  color: var(--color-primary);
}

.action-btn.danger:hover {
  background: rgba(239, 68, 68, 0.1);
  color: #f87171;
}

/* 分页 */
.pagination-bar {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
  margin-top: 24px;
}

.page-btn {
  padding: 6px 14px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  background: var(--color-background-tertiary);
  color: var(--color-text-secondary);
  font-size: 13px;
  cursor: pointer;
  transition: all var(--transition-fast);
}

.page-btn:hover:not(:disabled) {
  border-color: var(--color-primary);
  color: var(--color-text);
}

.page-btn.active {
  background: rgba(59, 130, 246, 0.12);
  border-color: var(--color-primary);
  color: var(--color-primary);
}

.page-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.page-ellipsis {
  padding: 6px 4px;
  color: var(--color-text-muted);
  font-size: 13px;
}
</style>
