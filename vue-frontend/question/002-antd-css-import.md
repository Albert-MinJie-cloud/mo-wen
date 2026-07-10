# ant-design-vue CSS 文件导入错误

## 问题来源

前端 — 依赖配置

## 现象

Vite 启动时报错：

```
Failed to run dependency scan. Error: The following dependencies are imported but could not be resolved:
  ant-design-vue/dist/react.css
```

## 根因

`main.ts` 中导入了一个不存在的 CSS 文件：

```ts
import "ant-design-vue/dist/react.css";  // 不存在
```

Ant Design Vue v4 中 CSS 文件名是 `reset.css`，`react.css` 是笔误（可能是从 React 项目的 `antd` 文档复制过来的）。

## 解决方案

```ts
import "ant-design-vue/dist/reset.css";
```

## 关键知识点

- Ant Design Vue v4 的全局样式文件是 `reset.css`，不是 `antd.css`（v3）或 `react.css`
- 确认使用的 UI 框架版本对应的正确 CSS 路径

## 日期

2026-07-10
