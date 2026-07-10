# FastAPI tags 重复导致 openapi2ts 生成重复接口函数

## 问题来源

后端 — FastAPI 路由 tags 配置

## 现象

`@umijs/openapi` (openapi2ts) 根据 `/openapi.json` 生成前端 API 文件时，每个接口都会出现两个同名函数，例如：

```ts
// user.ts
export async function addUserApiUserAddPost(...)  // 第一个
export async function addUserApiUserAddPost2(...) // 重复的，多了个 2 后缀
```

## 根因

在 `APIRouter` 和 `app.include_router()` 中**同时设置了 tags**，FastAPI 会将两处的 tags **合并**而不是覆盖，导致 OpenAPI 规范中每个 operation 的 `tags` 数组出现重复值。

```python
# routers/user.py — 第一次设置
router = APIRouter(prefix="/user", tags=["user"])

# main.py — 第二次设置（与上面合并，不会覆盖）
app.include_router(user_router, prefix="/api", tags=["user"])
```

最终每个 operation 的 tags 变成 `["user", "user"]`。`openapi2ts` 遍历所有 tags 时将同一接口注册两次，第二次因函数名冲突追加了 `2` 后缀。

## 解决方案

只在一处设置 tags，推荐保留在 `APIRouter` 中，去掉 `include_router` 中的 tags：

```python
# main.py — 修复后
app.include_router(user_router, prefix="/api")    # 不再重复设置 tags
app.include_router(health_router, prefix="/api")
```

## 关键知识点

- FastAPI 的 `include_router` 中的 `tags` 参数会与路由装饰器/路由器自身的 tags **合并追加**，而非覆盖
- 如果确实需要在 `include_router` 中覆盖 tags，需要逐个在路由装饰器中不设置 tags

## 日期

2026-07-10
