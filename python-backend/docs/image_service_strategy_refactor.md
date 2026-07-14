# 图片服务策略模式重构

## 背景

将文章配图从单一 Pexels 搜索扩展为支持 6 种图片来源，通过策略模式统一管理。

## 架构

```
ImageRequest → ImageServiceStrategy → ImageSearchService (ABC)
                                          ├── PexelsService        # 真实场景照片
                                          ├── NanoBananaService    # Gemini AI 生图
                                          ├── MermaidService       # 流程图/架构图
                                          ├── IconifyService       # SVG 图标
                                          ├── EmojiPackService     # 表情包
                                          └── SvgDiagramService    # LLM 生成概念图
```

## 新增文件

| 文件 | 说明 |
|------|------|
| `app/services/image_service_strategy.py` | 策略选择器，包含获取+上传 COS 流程 |
| `app/services/nano_banana_service.py` | Gemini AI 原生图片生成 |
| `app/services/mermaid_service.py` | Mermaid CLI 流程图生成 |
| `app/services/iconify_service.py` | Iconify API 图标检索 |
| `app/services/emoji_pack_service.py` | Bing 表情包搜索 |
| `app/services/svg_diagram_service.py` | LLM 生成 SVG 示意图 |

## 核心修改

- **agent_article_service.py** — agent5 改用 `ImageServiceStrategy`；agent4 支持动态构建 prompt
- **schemas/image.py** — 新增 `ImageData` 类（Bytes/URL/DataURL 三格式封装）
- **models/enums.py** — `ImageMethodEnum` 扩展为 7 种，新增 `is_ai_generated()`、`is_fallback()`
- **config.py** — 新增各图片服务配置项
- **cos_service.py** — 新增 `upload_image_data()` 统一上传方法

## 数据流

1. agent4 分析正文 → 指定每个配图的 `imageSource`
2. agent5 遍历 → `ImageServiceStrategy.get_image_and_upload()`
3. 各服务返回 `ImageData`
4. 统一上传 COS，返回 COS URL
5. 失败降级为 Picsum 兜底
