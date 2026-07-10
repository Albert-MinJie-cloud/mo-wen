# API_BASE_URL 端口错误 + 双 /api 前缀导致请求失败

## 问题来源

前端 — 环境配置

## 现象

1. 接口请求发到了 `http://localhost:8123`，实际后端在 `8567`，连接被拒
2. 请求路径变成了 `/api/api/user/get/login`，出现双重 `/api` 前缀

## 根因

`src/config/env.ts` 中的 `API_BASE_URL` 配置有两个错误：

```ts
// 错误配置
export const API_BASE_URL = "http://localhost:8123/api";
```

1. **端口错误**：`8123` 是模板默认值，未改为实际后端端口 `8567`
2. **多余的 `/api` 后缀**：`openapi2ts` 生成的接口函数中路径已经包含 `/api` 前缀（如 `/api/user/get/login`），axios 的 `baseURL` 会与路径拼接，导致双重前缀

## 解决方案

`API_BASE_URL` 只设置协议+主机+端口，不要带路径前缀：

```ts
// 正确配置
export const API_BASE_URL = "http://localhost:8567";
```

## 日期

2026-07-10
