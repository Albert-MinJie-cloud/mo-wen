# 墨文 (mo-wen)

AI 爆款文章创作器 — 输入选题，自动生成结构完整、配图丰富的长文。

## 技术栈

| 层级 | 技术 |
|------|------|
| 后端框架 | FastAPI (Python 3.10+) |
| 前端框架 | Vue 3 + Vite + TypeScript |
| 数据库 | MySQL |
| 缓存/会话 | Redis |
| 支付 | Stripe |
| 对象存储 | 腾讯云 COS |
| AI 模型 | OpenAI 兼容 API / Google Gemini |
| 包管理 | uv (Python) / npm (Node) |

## 目录结构

```
mo-wen/
├── python-backend/          # FastAPI 后端
│   ├── app/
│   │   ├── agent/           # AI Agent 上下文与流处理器
│   │   ├── constants/       # Prompt 模板、常量
│   │   ├── managers/        # SSE 管理器
│   │   ├── models/          # ORM 模型、枚举
│   │   ├── routers/         # API 路由
│   │   ├── schemas/         # Pydantic 请求/响应模型
│   │   ├── services/        # 业务逻辑 + AI Agent
│   │   ├── utils/           # 工具函数
│   │   ├── config.py        # 配置（.env 读取）
│   │   ├── database.py      # 数据库连接
│   │   ├── deps.py          # 依赖注入（认证链）
│   │   ├── exceptions.py    # 异常体系
│   │   └── main.py          # 应用入口
│   ├── pyproject.toml
│   └── uv.lock
├── vue-frontend/            # Vue 3 前端
│   └── src/
│       ├── api/             # 自动生成的 API 客户端（OpenAPI→TS）
│       ├── components/      # 通用组件
│       ├── composables/     # 组合式函数
│       ├── constants/       # 常量
│       ├── layouts/         # 布局组件
│       ├── pages/           # 页面组件
│       ├── router/          # 路由配置 + 权限守卫
│       ├── stores/          # Pinia 状态管理
│       ├── utils/           # 工具函数（SSE、Markdown 等）
│       ├── access.ts        # 首次加载用户信息
│       └── request.ts       # Axios 实例
└── sql/                     # 数据库迁移脚本
```

## 后端技术架构

### 请求处理链路

```
Route Handler → Service（new 创建）→ raw SQL（databases 库）
                     ↑
              Database（Depends 注入）
```

- SQLAlchemy 仅用于 ORM 模型定义，查询使用 `databases.Database` 异步执行原始 SQL
- Service 在路由处理函数中直接 `new`，不走 FastAPI DI 容器

### 认证体系

```
Cookie(session_id) → get_session_id → get_current_user → require_login → require_admin
```

- 无 JWT，Cookie + Redis 存储会话
- 登录成功在 Redis 写入 `session:{uuid}` → `LoginUserVO` JSON
- 支持可选登录和强制登录两级

### 错误处理

- 所有错误统一返回 HTTP 200，通过 `code` 字段区分
- `BusinessException` + `ErrorCode` 枚举
- `throw_if(condition, ErrorCode, msg)` 守卫式断言
- 响应格式: `{ code: int, data: T | null, message: string }`

### 文章生成流水线（5 Agent）

```
Phase 1: 标题生成    → Agent 1（选题分析 + 标题方案）
         用户确认标题 → POST /confirm-title
Phase 2: 大纲生成    → Agent 2（流式输出大纲结构）
         用户确认大纲 → POST /confirm-outline
Phase 3: 正文+配图  → Agent 3（流式输出正文）
                    → Agent 4（分析配图需求）
                    → Agent 5（多源配图生成）
                    → Merge（图文合成）
```

关键技术点：
- **异步编排**: `asyncio.create_task()` 启动每阶段，不阻塞请求
- **SSE 推送**: `SseEmitterManager` 维护 `asyncio.Queue` 字典，按 taskId 隔离
- **流式输出**: Agent 2/3 调用 OpenAI 兼容 API `stream=True`，逐 chunk 通过 SSE 推送
- **进度通信**: 前端 `EventSource` 或 `fetch + ReadableStream` 监听 `/api/article/progress/{taskId}`
- **图片策略**: `ImageServiceStrategy` 插件化，7 个源（Pexels/Gemini/Mermaid/Iconify/Emoji/SVG/Picsum），Failover 兜底

### 支付流程

```
创建会话 → Stripe Checkout → 用户支付 → Webhook 验签 → 更新用户 VIP 状态
```

VIP 档位: 月付 ¥9.90 / 年付 ¥99.00 / 永久 ¥199.00

## 前端技术架构

### 路由与权限

```
createWebHistory → access.ts（首次获取用户）→ 路由守卫（/admin/* 拦截）
```

- `api/` 目录代码由 OpenAPI 规范自动生成（`npm run openapi2ts`）
- Axios 实例配置 `withCredentials: true`，自动携带 Cookie

### 状态管理策略

- **Pinia**: 仅存储跨页面共享的登录用户状态
- **页面级状态**: 使用 Vue 3 `ref`/`reactive`，保持组件自治
- 无全局 store 膨胀

### 文章创作页（三栏布局）

```
┌──────────┬──────────────────────┬──────────┐
│ LeftPanel│    CenterPanel       │RightPanel│
│          │                      │          │
│ Pipeline │ TopicForm → Title    │  Stats   │
│ Status   │ Selector → Outline   │  Tips    │
│ Steps    │ Editor → Content     │  Hot     │
│          │ Generator → Result   │  Topics  │
│          │                      │          │
└──────────┴──────────────────────┴──────────┘
  260px         1fr                280px
```

### SSE 通信方案

| 方案 | 文件 | 适用场景 |
|------|------|---------|
| `EventSource` | `utils/sse.ts` | 简单场景 |
| `fetch + ReadableStream` | `utils/sseFetch.ts` | 需要 AbortController 精确控制生命周期 |

### 自定义通知

- Toast（右上角）和 Message（顶部居中）通过 composables + `<Teleport>` 实现
- 不使用 ant-design 内置的 message/notification 组件，便于全局样式控制

### 组件体系

- 14 个通用组件（`GlobalHeader`, `GlobalFooter`, `PageHeader`, `Logo`, 基础表单控件等）
- 所有组件使用 `<script setup lang="ts">` 语法
- SCSS 样式，CSS 变量做主题切换

## 技术特点

**后端**
- 全异步（async/await + asyncio + databases）
- 统一错误码 + 统一响应格式
- 策略模式插件化图片来源
- SSE 流式进度推送，asyncio.Queue 解耦

**前端**
- OpenAPI 自动生成 TS 类型与 API 函数
- 三栏 CSS Grid 创作工作台
- fetch + ReadableStream SSE 支持 AbortController 精确控制
- Pinia 轻量化，页面状态自治
- 深浅主题切换（CSS 变量）

**工程化**
- uv + npm 双包管理
- Conventional Commits 规范
- SQL 迁移脚本独立管理
- 无 Docker/CI/测试框架，轻量开发

## 系统架构图

```mermaid
flowchart TD
    %% ========== 样式 ==========
    classDef client fill:#e3f2fd,stroke:#1976d2,color:#0d47a1
    classDef access fill:#e8f5e9,stroke:#388e3c,color:#1b5e20
    classDef api    fill:#fff8e1,stroke:#f9a825,color:#e65100
    classDef biz    fill:#fff3e0,stroke:#fb8c00,color:#bf360c
    classDef agent  fill:#fce4ec,stroke:#d81b60,color:#880e4f
    classDef data   fill:#ede7f6,stroke:#5e35b1,color:#311b92
    classDef ext    fill:#eceff1,stroke:#546e7a,color:#263238

    %% ========== 客户端层 ==========
    subgraph L1["🖥 客户端"]
        B["浏览器 Vue3 + Vite + TS · Ant Design Vue 4"]
    end

    %% ========== 接入层 ==========
    subgraph L2["🌐 接入层"]
        direction LR
        V["Vite Dev Server  :5173"]
        N["Nginx  生产反向代理"]
    end

    %% ========== 接口层 ==========
    subgraph L3["📡 接口层 — FastAPI"]
        direction LR
        R1["/api/user 用户"]
        R2["/api/article 文章·SSE"]
        R3["/api/payment 支付"]
        R4["/api/webhook 回调"]
        R5["/api/statistics 统计"]
        R6["/api/topic 选题"]
        R7["/api/health 健康"]
    end

    %% ========== 业务层 ==========
    subgraph L4["⚙ 业务层 — Services"]
        direction LR
        S1["UserService 用户鉴权"]
        S2["ArticleService CRUD"]
        S3["ArticleAsyncService 异步编排·SSE"]
        S4["PaymentService Stripe"]
        S5["AgentLogService 日志"]
        S6["CosService COS上传"]
        S7["ImageServiceStrategy 图片策略"]
    end

    %% ========== 智能体层 ==========
    subgraph L5["🤖 智能体层 — 5-Agent Pipeline"]
        direction LR
        AG1["Agent1 标题方案"]
        AG2["Agent2 大纲生成"]
        AG3["Agent3 正文撰写"]
        AG4["Agent4 配图分析"]
        AG5["Agent5 配图生成"]
        MG["Merge 图文合成"]
    end

    %% ========== 数据层 & 外部服务（并行） ==========
    subgraph L6["🗄 数据层"]
        direction TB
        DB["MySQL 持久化 · 软删除"]
        RD["Redis 会话缓存"]
        COS["腾讯云 COS 图片存储"]
    end

    subgraph L7["🔗 外部服务"]
        direction TB
        E1["OpenAI API LLM流式"]
        E2["Gemini NanoBanana"]
        E3["Stripe 支付网关"]
        E4["Pexels 图片搜索"]
        E5["Mermaid CLI 图表"]
        E6["Iconify·EmojiPack"]
    end

    %% ========== 分层样式 ==========
    class L1,B client
    class L2,V,N access
    class L3,R1,R2,R3,R4,R5,R6,R7 api
    class L4,S1,S2,S3,S4,S5,S6,S7 biz
    class L5,AG1,AG2,AG3,AG4,AG5,MG agent
    class L6,DB,RD,COS data
    class L7,E1,E2,E3,E4,E5,E6 ext

    %% ========== 流向 ==========
    B --> V & N
    V & N --> R1 & R2 & R3 & R4 & R5 & R6 & R7

    R1 --> S1
    R2 --> S2 & S3 & S5
    R3 & R4 --> S4
    R5 --> S5
    R6 --> S2

    S2 --> S3 --> AG1 --> AG2 --> AG3 --> AG4 --> AG5 --> MG

    S2 & S3 --> S6
    AG5 --> S7 --> S6 --> COS

    S1 --> DB & RD
    S2 & S4 & S5 --> DB
    S4 --> E3

    AG1 & AG2 & AG3 --> E1
    AG4 & AG5 --> E2 & E4
    AG5 --> E5 & E6
```

