# 墨文 (mo-wen)

AI 爆款文章创作器 - Python 后端

## 技术栈

- **框架**：FastAPI + Uvicorn
- **数据库**：MySQL + SQLAlchemy + databases
- **缓存**：Redis + aioredis
- **配置**：Pydantic Settings + python-dotenv
- **包管理**：uv

## 快速启动

```bash
# 安装依赖
uv sync

# 配置环境变量
cp .env.example .env   # 编辑 .env 填入实际配置

# 创建数据库
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS \`mo-wen\` DEFAULT CHARACTER SET utf8mb4;"

# 启动服务
uv run uvicorn app.main:app --reload
```

服务启动后访问：
- API 文档：http://localhost:8567/docs
- 健康检查：http://localhost:8567/api/health

## 项目结构

```
python-backend/
├── .env.example          # 配置文件模板
├── .python-version       # Python 版本锁定
├── pyproject.toml        # 依赖管理
├── uv.lock               # 依赖锁定文件
└── app/
    ├── main.py           # 应用入口（FastAPI 实例、中间件、异常处理）
    ├── config.py         # 配置管理（基于 pydantic-settings）
    ├── database.py       # 数据库连接（SQLAlchemy + databases 异步）
    ├── exceptions.py     # 错误码与业务异常
    ├── deps.py           # 依赖注入
    ├── routers/          # 路由层
    │   ├── health.py     # 健康检查接口
    │   └── user.py       # 用户接口
    ├── schemas/          # Pydantic 模型（请求/响应）
    │   ├── common.py     # 统一响应格式、分页请求
    │   └── user.py       # 用户相关模型
    ├── services/         # 业务逻辑层
    │   └── user_service.py
    ├── models/           # SQLAlchemy ORM 模型
    └── utils/            # 工具类
        ├── password.py   # 密码加密（MD5 + 盐值）
        └── session.py    # Redis Session 管理
```

## 环境变量

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

## 清理重建

```bash
rm -rf .venv
uv sync
```
