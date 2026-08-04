# 墨文部署方案：前端 Cloudflare Pages + 后端腾讯云 CVM

## 一、整体架构

```
用户浏览器
    │
    ├── mo-wen.com (前端 SPA) ──► Cloudflare Pages (CDN 全球加速)
    │
    └── api.mo-wen.com (API) ──► 腾讯云 CVM (Nginx → FastAPI :8567)
                                      │
                                      ├── MySQL (腾讯云 CDB 或自建)
                                      ├── Redis (腾讯云 Redis 或自建)
                                      └── 腾讯云 COS (图片存储)
```

## 二、前端部署：Cloudflare Pages

### 2.1 构建配置

| 配置项 | 值 |
|--------|-----|
| 框架预设 | Vite (自动识别) |
| 构建命令 | `npm run build` |
| 输出目录 | `dist` |
| Node 版本 | `>=22.18.0` |

### 2.2 环境变量 (Cloudflare Pages 后台设置)

| 变量名 | 说明 |
|--------|------|
| `VITE_API_BASE_URL` | API 基础地址，生产环境设为 `https://api.mo-wen.com` |

### 2.3 前端代码改造

当前开发环境通过 `vite.config.ts` 中 proxy 转发 `/api`，生产环境需要直接请求 API 域名。

**方案**：在 `request.ts` 中通过环境变量切换 baseURL：

```ts
// src/request.ts
const baseURL = import.meta.env.VITE_API_BASE_URL || "";
// axios 的 baseURL，开发环境为空（走 vite proxy），生产为 https://api.mo-wen.com
```

### 2.4 路由 SPA 回退

Cloudflare Pages 默认会自动处理 SPA 路由回退，但需确认 `_redirects` 文件（放在 `public/` 下）：

```
/*    /index.html   200
```

### 2.5 自定义域名 + SSL

1. 域名 DNS 添加 CNAME 记录指向 Cloudflare Pages
2. Cloudflare 自动签发 SSL 证书

## 三、后端部署：腾讯云 CVM

### 3.1 服务器配置建议

| 配置项 | 建议值 |
|--------|--------|
| 实例规格 | 轻量应用服务器 2C4G 起步 |
| 操作系统 | Ubuntu 22.04 LTS |
| 带宽 | 3-5 Mbps |
| 系统盘 | 40GB SSD |

### 3.2 环境安装

```bash
# 基础工具
sudo apt update && sudo apt install -y python3.10 python3.10-venv nginx git curl

# 安装 uv (Python 包管理器)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 安装 Node (仅用于前端构建验证，非必须)
# curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
# sudo apt install -y nodejs

# MySQL 客户端（如使用自建 MySQL）
sudo apt install -y mysql-client

# Redis 客户端
sudo apt install -y redis-tools
```

### 3.3 项目部署

```bash
# 创建部署目录
sudo mkdir -p /opt/mo-wen
sudo chown $USER:$USER /opt/mo-wen

# 拉取代码
cd /opt/mo-wen
git clone https://github.com/Albert-MinJie-cloud/mo-wen.git python-backend

# 安装依赖
cd python-backend
uv sync

# 配置环境变量
cp .env.example .env  # 然后编辑 .env
```

### 3.4 环境变量 (.env)

```bash
# 服务器配置
SERVER_PORT=8567
SERVER_HOST=127.0.0.1

# 数据库配置 (使用腾讯云 CDB 或本机 MySQL)
DB_HOST=127.0.0.1
DB_PORT=3306
DB_NAME=mo-wen
DB_USER=mo_wen_user
DB_PASSWORD=你的数据库密码

# Redis 配置
REDIS_HOST=127.0.0.1
REDIS_PORT=6379
REDIS_PASSWORD=你的Redis密码

# Session 配置
SESSION_SECRET_KEY=生成一个随机字符串
SESSION_MAX_AGE=2592000

# AI 配置
DASHSCOPE_API_KEY=你的DeepSeek/通义APIKey
DASHSCOPE_MODEL=deepseek-v4-pro
DASHSCOPE_BASE_URL=https://api.deepseek.com/v1

# Pexels 图片搜索
PEXELS_API_KEY=你的PexelsKey

# 腾讯云 COS (图片上传)
TENCENT_COS_SECRET_ID=你的SecretId
TENCENT_COS_SECRET_KEY=你的SecretKey
TENCENT_COS_REGION=ap-beijing
TENCENT_COS_BUCKET=mo-wen-images-xxx
TENCENT_COS_DOMAIN=https://cdn.mo-wen.com

# Stripe 支付
STRIPE_API_KEY=sk_live_xxx
STRIPE_WEBHOOK_SECRET=whsec_xxx
STRIPE_SUCCESS_URL=https://mo-wen.com/payment/success
STRIPE_CANCEL_URL=https://mo-wen.com/payment/cancel
```

### 3.5 Systemd 服务

创建 `/etc/systemd/system/mo-wen.service`：

```ini
[Unit]
Description=Mo-Wen FastAPI Backend
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/mo-wen/python-backend
ExecStart=/root/.local/bin/uv run uvicorn app.main:app --host 127.0.0.1 --port 8567
Restart=always
RestartSec=5
EnvironmentFile=/opt/mo-wen/python-backend/.env

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable mo-wen
sudo systemctl start mo-wen
```

### 3.6 Nginx 反向代理 + SSL

```nginx
server {
    listen 80;
    server_name api.mo-wen.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name api.mo-wen.com;

    ssl_certificate     /etc/nginx/ssl/api.mo-wen.com.pem;
    ssl_certificate_key /etc/nginx/ssl/api.mo-wen.com.key;

    # CORS 预检请求快速返回
    location /api/ {
        if ($request_method = 'OPTIONS') {
            add_header 'Access-Control-Allow-Origin' 'https://mo-wen.com';
            add_header 'Access-Control-Allow-Methods' 'GET, POST, PUT, DELETE, OPTIONS';
            add_header 'Access-Control-Allow-Headers' 'Content-Type, Authorization';
            add_header 'Access-Control-Allow-Credentials' 'true';
            add_header 'Access-Control-Max-Age' 86400;
            return 204;
        }

        proxy_pass http://127.0.0.1:8567;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # SSE 支持（文章生成进度推送）
        proxy_buffering off;
        proxy_cache off;
        proxy_read_timeout 600s;
    }
}
```

## 四、云服务配置清单

| 服务 | 腾讯云产品 | 用途 |
|------|-----------|------|
| MySQL | 云数据库 CDB MySQL | 文章、用户、订单数据 |
| Redis | 云数据库 Redis | Session 缓存 |
| COS | 对象存储 COS | AI 生成的图片上传 |
| SSL 证书 | SSL 证书 (免费) | API 域名 HTTPS |

## 五、域名与 DNS

| 域名 | 解析目标 | 说明 |
|------|---------|------|
| `mo-wen.com` | Cloudflare Pages (CNAME) | 前端 SPA |
| `api.mo-wen.com` | 腾讯云 CVM 公网 IP (A 记录) | 后端 API |
| `cdn.mo-wen.com` | 腾讯云 COS (CNAME) | 图片 CDN（可选） |

## 六、CORS 配置调整

后端 `config.py` 中需要修改允许的源：

```python
# 开发环境
CORS_ORIGINS = [
    "http://localhost:5173",
]

# 生产环境
CORS_ORIGINS = [
    "https://mo-wen.com",
    "https://www.mo-wen.com",
]
```

建议通过环境变量控制：

```python
CORS_ORIGINS: list[str] = Field(
    default=["http://localhost:5173"],
    alias="CORS_ORIGINS",
)
```

## 七、部署检查清单

- [ ] 腾讯云 CVM 实例创建并初始化
- [ ] MySQL 数据库创建，执行 `sql/create_table.sql`
- [ ] Redis 实例创建并配置密码
- [ ] 域名购买并完成 ICP 备案（如使用中国大陆服务器）
- [ ] SSL 证书申请（DNSPod 免费证书 或 Let's Encrypt）
- [ ] 后端代码部署，.env 配置完毕
- [ ] Nginx 配置并启动
- [ ] Systemd 服务验证 `systemctl status mo-wen`
- [ ] Cloudflare Pages 连接 GitHub 仓库
- [ ] 前端构建环境变量配置 (`VITE_API_BASE_URL`)
- [ ] 自定义域名配置 + DNS 解析
- [ ] Stripe webhook 地址更新为生产 URL
- [ ] 全流程测试：注册 → 登录 → 创作 → 支付

## 八、成本估算 (月)

| 项目 | 配置 | 月费用（约） |
|------|------|-------------|
| CVM 轻量服务器 | 2C4G/40GB/5Mbps | ¥50-80 |
| CDB MySQL | 1C1G/20GB | ¥40-60 |
| Redis | 1G 标准版 | ¥30-50 |
| COS | 按量计费 | ¥5-20 |
| Cloudflare Pages | 免费额度 | ¥0 |
| 域名 | .com | ¥5/月均 |
| **合计** | | **约 ¥150-220/月** |

> 初期可使用轻量应用服务器自建 MySQL + Redis 降低成本至 ¥60-100/月。
