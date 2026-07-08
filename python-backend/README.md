# 墨文 (mo-wen)

AI 爆款文章创作器 - Python 后端

## 技术栈

- **框架**：FastAPI + Uvicorn
- **数据库**：MySQL + SQLAlchemy + databases
- **缓存**：Redis + aioredis
- **配置**：Pydantic Settings + python-dotenv

## 快速启动

```bash
uv sync

cp .env.example .env   # 编辑 .env 填入实际配置

uv run uvicorn app.main:app --reload
```

## 如果你之前手动装过包、环境错乱

清理重建虚拟环境：

```bash
# 删除旧虚拟环境
rm -rf .venv

# 重新安装所有依赖
uv sync
```
