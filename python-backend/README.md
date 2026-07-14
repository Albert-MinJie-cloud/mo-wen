# 墨文 (mo-wen)

AI 爆款文章创作器 - Python 后端

## 技术栈

- **框架**：FastAPI + Uvicorn
- **数据库**：MySQL + SQLAlchemy + databases
- **缓存**：Redis + aioredis
- **AI**：OpenAI SDK（兼容 DashScope）+ Google GenAI（Gemini 生图）
- **存储**：腾讯云 COS（图片上传）
- **配置**：Pydantic Settings + python-dotenv
- **包管理**：uv

## 快速启动

```bash
# 安装依赖
uv sync

# 配置环境变量
cp .env.example .env   # 编辑 .env 填入实际配置

# 创建数据库
mysql -u root -p < ../sql/create_table.sql

# （可选）安装 Mermaid CLI，用于流程图生成
npm install -g @mermaid-js/mermaid-cli

# 启动服务
uv run uvicorn app.main:app --reload
```

服务启动后访问：
- API 文档：http://localhost:8567/docs
- 健康检查：http://localhost:8567/api/health

## 项目结构

```
python-backend/
├── .env.example              # 配置文件模板
├── .python-version           # Python 版本锁定
├── pyproject.toml            # 依赖管理
├── uv.lock                   # 依赖锁定文件
├── docs/                     # 技术文档
│   ├── 项目构成.md
│   ├── 项目依赖.md
│   ├── 文章模块开发文档.md
│   ├── image_service_strategy_refactor.md
│   └── known_tech_debt.md
├── plan/                     # 设计规划
│   └── 用户交互增强.md
├── question/                 # 问题与审查记录
│   └── code_review_2026-07-14.md
└── app/
    ├── main.py               # 应用入口（FastAPI 实例、中间件、异常处理）
    ├── config.py             # 配置管理（基于 pydantic-settings）
    ├── database.py           # 数据库连接（SQLAlchemy + databases 异步）
    ├── exceptions.py         # 错误码与业务异常
    ├── deps.py               # 依赖注入
    ├── constants/            # 常量定义
    │   ├── article.py        # 文章相关常量
    │   ├── prompt.py         # Prompt 模板
    │   └── user.py           # 用户相关常量
    ├── managers/             # 管理器
    │   └── sse_manager.py    # SSE 连接管理
    ├── models/               # SQLAlchemy ORM 模型
    │   ├── article.py        # 文章表
    │   ├── enums.py          # 枚举（状态、阶段、风格、配图方式、SSE 消息）
    │   └── user.py           # 用户表
    ├── routers/              # 路由层
    │   ├── article.py        # 文章接口（创建/列表/详情/确认标题/确认大纲/AI修改大纲/SSE进度）
    │   ├── health.py         # 健康检查接口
    │   └── user.py           # 用户接口
    ├── schemas/              # Pydantic 模型（请求/响应）
    │   ├── article.py        # 文章相关模型（ArticleState、ImageRequirement 等）
    │   ├── common.py         # 统一响应格式、分页请求
    │   ├── image.py          # 图片数据模型（ImageRequest、ImageData）
    │   └── user.py           # 用户相关模型
    ├── services/             # 业务逻辑层
    │   ├── article_agent_service.py   # 5 智能体编排（标题→大纲→正文→配图需求→配图生成）
    │   ├── article_async_service.py   # 异步任务服务（SSE 进度推送）
    │   ├── article_service.py         # 文章 CRUD
    │   ├── cos_service.py             # 腾讯云 COS 上传
    │   ├── image_search_service.py    # 图片服务抽象基类
    │   ├── image_service_strategy.py  # 图片服务策略选择器
    │   ├── pexels_service.py          # Pexels 图片检索
    │   ├── nano_banana_service.py     # Gemini AI 生图
    │   ├── mermaid_service.py         # Mermaid 流程图生成
    │   ├── iconify_service.py         # Iconify 图标检索
    │   ├── emoji_pack_service.py      # 表情包搜索
    │   ├── svg_diagram_service.py     # SVG 概念示意图生成
    │   └── user_service.py            # 用户服务
    └── utils/                # 工具类
        ├── password.py       # 密码加密（MD5 + 盐值）
        └── session.py        # Redis Session 管理
```

## 智能体流水线

采用 **Human-in-the-Loop** 设计，AI 在关键节点暂停等待用户确认后再继续。

### 阶段状态机

```
PENDING → TITLE_GENERATING → TITLE_SELECTING → OUTLINE_GENERATING → OUTLINE_EDITING → CONTENT_GENERATING → COMPLETED
                                    ↑ 用户确认标题                            ↑ 用户确认大纲
```

- **TITLE_SELECTING** 和 **OUTLINE_EDITING** 为两个用户介入点
- `status` 字段追踪粗粒度生命周期（PENDING → PROCESSING → COMPLETED/FAILED）
- `phase` 字段追踪细粒度阶段（ArticlePhaseEnum）

### 三阶段异步执行

| 阶段 | 触发方式 | 执行内容 | SSE 结束事件 |
|------|---------|---------|-------------|
| 阶段1 | `POST /article/create` | Agent 1 生成多组标题方案 | `TITLES_GENERATED` |
| 阶段2 | `POST /article/confirm-title` | Agent 2 流式生成大纲 | `OUTLINE_GENERATED` |
| 阶段3 | `POST /article/confirm-outline` | Agent 3+4+5 正文、配图、合成 | `ALL_COMPLETE` |

每个阶段通过独立的 SSE 连接推送进度。

### API 接口

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/article/create` | 创建文章任务（触发阶段1） |
| POST | `/api/article/confirm-title` | 确认标题（触发阶段2） |
| POST | `/api/article/confirm-outline` | 确认大纲（触发阶段3） |
| POST | `/api/article/ai-modify-outline` | AI 修改大纲 |
| GET | `/api/article/progress/{task_id}` | SSE 进度推送 |
| GET | `/api/article/{task_id}` | 获取文章详情 |
| POST | `/api/article/list` | 分页查询文章列表 |
| POST | `/api/article/delete` | 删除文章（软删除） |

全部接口需要登录态。

### SSE 消息类型

| 类型 | 说明 |
|------|------|
| `TITLES_GENERATED` | 标题方案生成完成，携带 titleOptions（等待用户选择） |
| `AGENT2_STREAMING` | 大纲流式输出 |
| `OUTLINE_GENERATED` | 大纲生成完成，携带 outline（等待用户编辑） |
| `AGENT3_STREAMING` | 正文流式输出 |
| `AGENT3_COMPLETE` | 正文生成完成 |
| `AGENT4_COMPLETE` | 配图需求分析完成 |
| `IMAGE_COMPLETE` | 单张配图完成 |
| `AGENT5_COMPLETE` | 配图生成完成 |
| `MERGE_COMPLETE` | 图文合成完成 |
| `ALL_COMPLETE` | 全部完成 |
| `ERROR` | 错误 |

### 配图支持

6 种来源，通过策略模式统一管理：

| 来源 | 说明 |
|------|------|
| PEXELS | 真实场景照片（图库检索） |
| NANO_BANANA | Gemini AI 创意生图 |
| MERMAID | 流程图/架构图（需要 mmdc CLI） |
| ICONIFY | 开源图标库（SVG） |
| EMOJI_PACK | 表情包（Bing 搜索） |
| SVG_DIAGRAM | LLM 生成概念示意图 |

## 环境变量

### 基础配置
| 变量 | 说明 | 默认值 |
|------|------|--------|
| SERVER_HOST | 服务地址 | 0.0.0.0 |
| SERVER_PORT | 服务端口 | 8567 |
| DB_HOST | 数据库地址 | localhost |
| DB_PORT | 数据库端口 | 3306 |
| DB_NAME | 数据库名称 | mo-wen |
| DB_USER | 数据库用户 | root |
| DB_PASSWORD | 数据库密码 | - |
| REDIS_HOST | Redis 地址 | localhost |
| REDIS_PORT | Redis 端口 | 6379 |
| REDIS_DB | Redis 数据库编号 | 0 |
| REDIS_PASSWORD | Redis 密码 | - |
| SESSION_SECRET_KEY | Session 密钥 | - |
| SESSION_MAX_AGE | Session 有效期（秒） | 2592000 |
| PASSWORD_SALT | 密码加密盐值 | - |

### AI 配置
| 变量 | 说明 | 默认值 |
|------|------|--------|
| DASHSCOPE_API_KEY | DashScope API Key（LLM 调用） | - |
| DASHSCOPE_MODEL | DashScope 模型 | qwen-plus |

### 图片服务
| 变量 | 说明 | 默认值 |
|------|------|--------|
| PEXELS_API_KEY | Pexels API Key | - |
| NANO_BANANA_API_KEY | Gemini API Key | - |
| NANO_BANANA_MODEL | Gemini 生图模型 | gemini-2.5-flash-image |
| NANO_BANANA_ASPECT_RATIO | 生图宽高比 | 16:9 |
| TENcent_COS_SECRET_ID | 腾讯云 COS SecretId | - |
| TENcent_COS_SECRET_KEY | 腾讯云 COS SecretKey | - |
| TENcent_COS_REGION | COS 区域 | ap-beijing |
| TENcent_COS_BUCKET | COS Bucket 名称 | - |

## 清理重建

```bash
rm -rf .venv
uv sync
```
