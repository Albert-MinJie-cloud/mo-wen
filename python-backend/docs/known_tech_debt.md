# 已知技术债务

> 2026-07-14 代码审查确认，暂不处理

## 1. MermaidService 同步阻塞事件循环

- **位置**: `app/services/mermaid_service.py:116`
- **问题**: async 方法中使用 `subprocess.run()` 调用 mmdc CLI，阻塞事件循环
- **建议**: 改用 `asyncio.create_subprocess_exec`

## 2. _validate_and_filter_image_requirements 命名不当

- **位置**: `app/services/article_agent_service.py:333`
- **问题**: 方法名暗示"过滤"，实际是替换 source 后保留全部
- **建议**: 改名为 `_validate_and_normalize_image_requirements`

## 3. nano_banana_output_mime_type 死配置

- **位置**: `app/config.py:54`
- **问题**: 配置定义了但在 `nano_banana_service.py` 中未使用
- **建议**: 删除或作为 fallback 使用
