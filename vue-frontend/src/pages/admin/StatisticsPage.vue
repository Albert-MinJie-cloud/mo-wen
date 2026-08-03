<script setup lang="ts">
import { ref, computed, onMounted, watch } from "vue";
import { message } from "@/message";
import PageHeader from "@/components/PageHeader.vue";
import { useTheme } from "@/composables/useTheme";
import request from "@/request";
import VChart from "vue-echarts";
import * as echarts from "echarts";
import { use } from "echarts/core";
import { CanvasRenderer } from "echarts/renderers";
import { BarChart, LineChart, PieChart } from "echarts/charts";
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent,
} from "echarts/components";

use([
  CanvasRenderer,
  BarChart,
  LineChart,
  PieChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent,
]);

const AGENT_LABELS: Record<string, string> = {
  agent1_generate_titles: "Agent 1 标题",
  agent2_generate_outline: "Agent 2 大纲",
  agent3_generate_content: "Agent 3 正文",
  agent4_analyze_image_requirements: "Agent 4 图片分析",
  agent5_generate_images: "Agent 5 图片生成",
  agent6_merge_content: "Agent 6 合并",
  ai_modify_outline: "AI 修改大纲",
};

const { currentTheme } = useTheme();

const loading = ref(false);
const timeRange = ref("30d");
const granularity = ref("daily");
const stats = ref<DashboardStats | null>(null);

// ---- 图表颜色 — 跟随主题切换 ----
const chartTextColor = computed(() =>
  currentTheme.value === "dark" ? "rgba(255,255,255,0.55)" : "rgba(0,0,0,0.55)"
);
const chartBorderColor = computed(() =>
  currentTheme.value === "dark" ? "rgba(255,255,255,0.08)" : "#e4e4e7"
);
const chartTooltipBg = computed(() =>
  currentTheme.value === "dark" ? "rgba(15,23,42,0.96)" : "rgba(255,255,255,0.96)"
);
const chartTooltipTextColor = computed(() =>
  currentTheme.value === "dark" ? "#fff" : "#18181b"
);
const chartTooltipBorderColor = computed(() =>
  currentTheme.value === "dark" ? "rgba(255,255,255,0.1)" : "rgba(0,0,0,0.08)"
);
const chartPieGapColor = computed(() =>
  currentTheme.value === "dark" ? "#0f172a" : "#ffffff"
);
const chartOtherColor = computed(() =>
  currentTheme.value === "dark" ? "rgba(255,255,255,0.2)" : "rgba(0,0,0,0.12)"
);
const chartLabelColor = computed(() =>
  currentTheme.value === "dark" ? "rgba(255,255,255,0.65)" : "rgba(0,0,0,0.55)"
);

interface DashboardStats {
  creationTrend: { items: { date: string; count: number }[] };
  agentPerformance: {
    items: {
      agentName: string;
      totalCalls: number;
      successRate: number;
      avgDurationMs: number;
      minDurationMs: number;
      maxDurationMs: number;
    }[];
  };
  userAnalysis: {
    totalUsers: number;
    totalVip: number;
    vipConversionRate: number;
    trends: { date: string; newUsers: number; newVip: number }[];
  };
  quotaUsage: {
    totalQuotaConsumed: number;
    items: {
      userId: number;
      userAccount: string;
      userName: string | null;
      quotaConsumed: number;
      totalArticles: number;
    }[];
  };
}

async function fetchStats() {
  loading.value = true;
  try {
    const res = await request.post("/api/statistics/dashboard", {
      timeRange: timeRange.value,
      granularity: granularity.value,
    });
    if (res.data.code === 0 && res.data.data) {
      stats.value = res.data.data;
    } else {
      message.error(res.data.message || "获取统计数据失败");
    }
  } catch (e: any) {
    message.error(e?.message || "获取统计数据失败");
  } finally {
    loading.value = false;
  }
}

function formatMs(ms: number): string {
  if (ms < 1000) return `${ms}ms`;
  if (ms < 60000) return `${(ms / 1000).toFixed(1)}s`;
  return `${Math.floor(ms / 60000)}m ${Math.floor((ms % 60000) / 1000)}s`;
}

// 明亮色板（深浅主题通用）
const C_BLUE = "#60a5fa";
const C_GREEN = "#4ade80";
const C_YELLOW = "#fbbf24";
const C_RED = "#f87171";
const C_PURPLE = "#a78bfa";
const C_CYAN = "#22d3ee";
const C_ORANGE = "#fb923c";
const C_GOLD = "#f59e0b";

// ======== 创作趋势 柱状图 ========
const creationTrendOption = computed(() => {
  const items = stats.value?.creationTrend?.items || [];
  return {
    tooltip: {
      trigger: "axis",
      backgroundColor: chartTooltipBg.value,
      borderColor: chartTooltipBorderColor.value,
      textStyle: { color: chartTooltipTextColor.value, fontSize: 12 },
    },
    grid: { left: 50, right: 20, top: 20, bottom: 30 },
    xAxis: {
      type: "category",
      data: items.map((i) => i.date),
      axisLabel: { rotate: items.length > 10 ? 45 : 0, fontSize: 11, color: chartTextColor.value },
      axisLine: { lineStyle: { color: chartBorderColor.value } },
      axisTick: { lineStyle: { color: chartBorderColor.value } },
    },
    yAxis: {
      type: "value", minInterval: 1,
      axisLabel: { color: chartTextColor.value },
      splitLine: { lineStyle: { color: chartBorderColor.value } },
    },
    series: [
      {
        name: "文章数",
        type: "bar",
        data: items.map((i) => i.count),
        barMaxWidth: 32,
        itemStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: C_BLUE },
            { offset: 1, color: "rgba(96,165,250,0.3)" },
          ]),
          borderRadius: [4, 4, 0, 0],
        },
      },
    ],
  };
});

const totalArticleCount = computed(() =>
  (stats.value?.creationTrend?.items || []).reduce((sum, i) => sum + i.count, 0)
);

const avgTotalTime = computed(() => {
  const items = stats.value?.agentPerformance?.items || [];
  if (items.length === 0) return 0;
  return items.reduce((sum, i) => sum + i.avgDurationMs, 0) / items.length;
});

// ======== 智能体性能 横向柱状图 ========
const PIE_COLORS = [C_BLUE, C_GREEN, C_YELLOW, C_PURPLE, C_CYAN, C_ORANGE, C_GOLD, C_RED, "#818cf8", "#34d399"];

const agentPerformanceOption = computed(() => {
  const items = stats.value?.agentPerformance?.items || [];
  const names = items.map((i) => AGENT_LABELS[i.agentName] || i.agentName);
  return {
    tooltip: {
      trigger: "axis",
      axisPointer: { type: "shadow" },
      backgroundColor: chartTooltipBg.value,
      borderColor: chartTooltipBorderColor.value,
      textStyle: { color: chartTooltipTextColor.value, fontSize: 12 },
      formatter: (params: any) => {
        const p = params[0];
        if (!p || p.dataIndex == null) return "";
        const it = items[p.dataIndex];
        if (!it) return "";
        return `${p.name}<br/>
          调用次数: ${it.totalCalls}<br/>
          成功率: ${it.successRate}%<br/>
          平均耗时: ${formatMs(it.avgDurationMs)}<br/>
          最快: ${formatMs(it.minDurationMs)} / 最慢: ${formatMs(it.maxDurationMs)}`;
      },
    },
    grid: { left: 120, right: 70, top: 10, bottom: 20 },
    xAxis: {
      type: "value",
      name: "平均耗时",
      nameTextStyle: { fontSize: 11, color: chartTextColor.value },
      axisLabel: { formatter: (v: number) => formatMs(v), color: chartTextColor.value },
      splitLine: { lineStyle: { color: chartBorderColor.value } },
    },
    yAxis: {
      type: "category",
      data: names,
      axisLabel: { fontSize: 11, color: chartTextColor.value },
      axisLine: { lineStyle: { color: chartBorderColor.value } },
    },
    series: [
      {
        name: "平均耗时",
        type: "bar",
        data: items.map((i, idx) => ({
          value: i.avgDurationMs,
          itemStyle: {
            color: PIE_COLORS[idx % PIE_COLORS.length],
            borderRadius: [0, 4, 4, 0],
          },
        })),
        barMaxWidth: 24,
        label: {
          show: true,
          position: "right",
          fontSize: 11,
          color: chartLabelColor.value,
          formatter: (p: any) => formatMs(p.value),
        },
      },
    ],
  };
});

// ======== 用户分析 饼状图 ========
const userAnalysisOption = computed(() => {
  const ua = stats.value?.userAnalysis;
  const normalUsers = (ua?.totalUsers || 0) - (ua?.totalVip || 0);
  return {
    tooltip: {
      trigger: "item",
      backgroundColor: chartTooltipBg.value,
      borderColor: chartTooltipBorderColor.value,
      textStyle: { color: chartTooltipTextColor.value, fontSize: 12 },
      formatter: "{b}: {c} ({d}%)",
    },
    legend: {
      orient: "vertical",
      right: 10,
      top: "center",
      textStyle: { color: chartTextColor.value, fontSize: 12 },
    },
    series: [
      {
        name: "用户分布",
        type: "pie",
        radius: ["50%", "75%"],
        center: ["45%", "50%"],
        avoidLabelOverlap: false,
        itemStyle: { borderRadius: 4, borderColor: chartPieGapColor.value, borderWidth: 3 },
        label: { show: false },
        emphasis: {
          label: { show: true, fontSize: 14, fontWeight: "bold" },
        },
        data: [
          { value: normalUsers, name: "普通用户", itemStyle: { color: C_BLUE } },
          { value: ua?.totalVip || 0, name: "VIP 用户", itemStyle: { color: C_GOLD } },
        ],
      },
    ],
  };
});

// ======== 配额使用 饼状图 ========
const quotaUsageOption = computed(() => {
  const items = stats.value?.quotaUsage?.items || [];
  const top5 = items.slice(0, 5);
  const othersCount = items.slice(5).reduce((sum, i) => sum + i.quotaConsumed, 0);
  const data = top5.map((i, idx) => ({
    value: i.quotaConsumed,
    name: i.userName || i.userAccount,
    itemStyle: { color: PIE_COLORS[idx % PIE_COLORS.length] },
  }));
  if (othersCount > 0) {
    data.push({ value: othersCount, name: "其他用户", itemStyle: { color: chartOtherColor.value } });
  }
  return {
    tooltip: {
      trigger: "item",
      backgroundColor: chartTooltipBg.value,
      borderColor: chartTooltipBorderColor.value,
      textStyle: { color: chartTooltipTextColor.value, fontSize: 12 },
      formatter: "{b}: {c} 次 ({d}%)",
    },
    legend: {
      orient: "vertical",
      right: 10,
      top: "center",
      textStyle: { color: chartTextColor.value, fontSize: 11 },
    },
    series: [
      {
        name: "配额使用",
        type: "pie",
        radius: ["45%", "72%"],
        center: ["42%", "50%"],
        avoidLabelOverlap: false,
        itemStyle: { borderRadius: 3, borderColor: chartPieGapColor.value, borderWidth: 2 },
        label: { show: false },
        emphasis: {
          label: { show: true, fontSize: 13, fontWeight: "bold" },
        },
        data,
      },
    ],
  };
});

watch([timeRange, granularity], () => fetchStats());
onMounted(() => fetchStats());
</script>

<template>
  <div id="statisticsPage">
    <PageHeader title="数据统计" subtitle="AI 文章创作数据分析" />

    <div class="container">
      <a-card :bordered="false" class="content-card">
        <!-- 筛选栏 -->
        <div class="filter-bar">
          <a-radio-group v-model:value="timeRange" button-style="solid" size="small">
            <a-radio-button value="7d">7 天</a-radio-button>
            <a-radio-button value="30d">30 天</a-radio-button>
            <a-radio-button value="90d">90 天</a-radio-button>
          </a-radio-group>
          <a-select
            v-model:value="granularity"
            style="width: 120px"
            size="small"
            popup-class-name="statistics-dropdown"
          >
            <a-select-option value="daily">按天</a-select-option>
            <a-select-option value="weekly">按周</a-select-option>
            <a-select-option value="monthly">按月</a-select-option>
          </a-select>
        </div>

        <a-divider style="margin: 16px 0" />

        <a-spin :spinning="loading">
          <template v-if="stats">
            <!-- 图表区域 2x2 Grid -->
            <div class="charts-grid">
              <!-- 创作趋势 -->
              <a-card title="创作趋势" :bordered="true" class="chart-card">
                <div v-if="stats.creationTrend.items.length > 0" class="chart-box">
                  <VChart :option="creationTrendOption" autoresize />
                </div>
                <div v-else class="empty-chart">暂无数据</div>
              </a-card>

              <!-- 智能体性能 -->
              <a-card title="智能体性能" :bordered="true" class="chart-card">
                <template v-if="stats.agentPerformance.items.length > 0" #extra>
                  <span class="inline-stats">
                    <span class="stat-tag">总创作 <strong>{{ totalArticleCount }}</strong> 篇</span>
                    <span class="stat-tag">平均耗时 <strong>{{ formatMs(avgTotalTime) }}</strong></span>
                  </span>
                </template>
                <div v-if="stats.agentPerformance.items.length > 0">
                  <div class="chart-box">
                    <VChart :option="agentPerformanceOption" autoresize />
                  </div>
                </div>
                <div v-else class="empty-chart">暂无数据</div>
              </a-card>

              <!-- 用户分析 -->
              <a-card title="用户分析" :bordered="true" class="chart-card">
                <template v-if="stats.userAnalysis.totalUsers > 0">
                  <!-- 摘要卡片 -->
                  <div class="summary-cards">
                    <div class="summary-item">
                      <span class="summary-value">{{ stats.userAnalysis.totalUsers }}</span>
                      <span class="summary-label">总用户</span>
                    </div>
                    <div class="summary-item">
                      <span class="summary-value">{{ stats.userAnalysis.totalVip }}</span>
                      <span class="summary-label">VIP 用户</span>
                    </div>
                    <div class="summary-item">
                      <span class="summary-value">{{ stats.userAnalysis.vipConversionRate }}%</span>
                      <span class="summary-label">转化率</span>
                    </div>
                  </div>
                  <div class="chart-box">
                    <VChart :option="userAnalysisOption" autoresize />
                  </div>
                </template>
                <div v-else class="empty-chart">暂无数据</div>
              </a-card>

              <!-- 配额使用 -->
              <a-card title="配额使用" :bordered="true" class="chart-card">
                <div v-if="stats.quotaUsage.items.length > 0">
                  <div class="quota-total">
                    统计周期内共消耗 <strong>{{ stats.quotaUsage.totalQuotaConsumed }}</strong> 次配额
                  </div>
                  <div class="chart-box">
                    <VChart :option="quotaUsageOption" autoresize />
                  </div>
                </div>
                <div v-else class="empty-chart">暂无数据</div>
              </a-card>
            </div>
          </template>
        </a-spin>
      </a-card>
    </div>
  </div>
</template>

<style scoped lang="scss">
#statisticsPage {
  background: var(--color-background);
  min-height: 100vh;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px 60px;
}

.content-card {
  border-radius: var(--radius-lg);
  border: 1px solid var(--color-border);
  box-shadow: none;
  background: var(--color-background-secondary);
  overflow: hidden;

  :deep(.ant-card-body) {
    background: var(--color-background-secondary);
  }
}

.filter-bar {
  display: flex;
  align-items: center;
  gap: 16px;

  :deep(.ant-radio-button-wrapper) {
    color: var(--color-text-muted);
    background: var(--color-fill-tertiary);
    border-color: var(--color-border);
    &:hover { color: var(--color-text); }
    &:not(:first-child)::before {
      background-color: var(--color-border);
    }
  }
  :deep(.ant-radio-button-wrapper-checked) {
    color: #fff;
    background: var(--color-primary);
    border-color: var(--color-primary);
    box-shadow: none;
    &:hover { color: #fff; }
  }

  :deep(.ant-select) {
    .ant-select-selector {
      background: var(--color-fill-tertiary);
      border-color: var(--color-border);
      color: var(--color-text);
    }
    .ant-select-arrow { color: var(--color-text-muted); }
  }
  :deep(.ant-select-focused .ant-select-selector) {
    border-color: var(--color-primary) !important;
    box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2);
  }
}

.charts-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.chart-card {
  border-radius: var(--radius-md);
  background: var(--color-background);
  border: 1px solid var(--color-border);

  :deep(.ant-card-head) {
    background: var(--color-background);
    border-bottom: 1px solid var(--color-border);
  }

  :deep(.ant-card-head-title) {
    color: var(--color-text);
  }

  :deep(.ant-card-body) {
    background: var(--color-background);
  }
}

.chart-box {
  height: 280px;
}

.empty-chart {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 180px;
  color: var(--color-text-muted);
  font-size: 14px;
}

.inline-stats {
  display: inline-flex;
  gap: 8px;
}

.stat-tag {
  font-size: 12px;
  color: var(--color-text-muted);
  background: var(--color-fill-secondary);
  border: 1px solid var(--color-border-light);
  border-radius: var(--radius-full);
  padding: 3px 12px;
  strong {
    color: var(--color-text);
    font-weight: 600;
  }
}

.summary-cards {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 12px;
  margin-bottom: 8px;
}

.summary-item {
  text-align: center;
  padding: 16px 12px;
  background: var(--color-background-secondary);
  border-radius: var(--radius-md);
}

.summary-value {
  display: block;
  font-size: 22px;
  font-weight: 700;
  color: var(--color-primary);
}

.summary-label {
  display: block;
  font-size: 12px;
  color: var(--color-text-muted);
  margin-top: 2px;
}

.quota-total {
  margin-bottom: 12px;
  font-size: 14px;
  color: var(--color-text);
  text-align: center;
  strong {
    color: var(--color-primary-light);
    font-size: 18px;
  }
}

:deep(.ant-divider) {
  border-color: var(--color-border);
}

@media (max-width: 768px) {
  .charts-grid {
    grid-template-columns: 1fr;
  }
}
</style>

<style lang="scss">
// Select 下拉面板（渲染在 body，无法用 scoped）
.statistics-dropdown {
  background: var(--color-background-secondary);
  box-shadow: var(--shadow-lg);

  .ant-select-item {
    color: var(--color-text-secondary);
  }
  .ant-select-item-option-active {
    background: rgba(59, 130, 246, 0.08);
  }
  .ant-select-item-option-selected {
    background: rgba(59, 130, 246, 0.12);
    color: var(--color-primary);
    font-weight: 600;
  }
}
</style>
