# CORS 跨域错误：前端端口未加入允许列表

## 问题来源

后端 — CORS 中间件配置

## 现象

浏览器控制台报错：

```
Access to XMLHttpRequest at 'http://localhost:8567/api/user/get/login'
from origin 'http://localhost:5173' has been blocked by CORS policy:
No 'Access-Control-Allow-Origin' header is present on the requested resource.
```

## 根因

`main.py` 的 CORS 中间件只允许了 `http://localhost:3000`，但 Vite 默认开发端口是 `5173`：

```python
# 只允许了 3000 端口
allow_origins=["http://localhost:3000"],
```

Vite 启动在 `5173` 端口，后端没有返回对应的 `Access-Control-Allow-Origin` 头。

## 解决方案

将前端实际使用的端口加入允许列表：

```python
allow_origins=["http://localhost:3000", "http://localhost:5173"],
```

## 关键知识点

- Vite 默认端口是 `5173`，与传统的 `3000` 不同
- 使用 `allow_credentials=True` 时，`allow_origins` 不能设为 `["*"]`，必须明确列出具体域名

## 日期

2026-07-10
