/** 文章状态映射 */
export const ARTICLE_STATUS_MAP: Record<string, { text: string; cls: string }> =
  {
    PENDING: { text: "等待中", cls: "pending" },
    PROCESSING: { text: "生成中", cls: "processing" },
    COMPLETED: { text: "已完成", cls: "completed" },
    FAILED: { text: "失败", cls: "failed" },
  };

/** 文章风格选项（含描述，用于表单） */
export const ARTICLE_STYLE_OPTIONS = [
  { value: "tech", label: "科技风格", desc: "专业、前沿、数据驱动" },
  { value: "emotional", label: "情感风格", desc: "温暖、共鸣、故事化" },
  { value: "educational", label: "教育风格", desc: "清晰、系统、干货满满" },
  { value: "humorous", label: "幽默风格", desc: "轻松、有趣、通俗易懂" },
] as const;

/** 文章风格标签映射（用于展示） */
export const ARTICLE_STYLE_LABELS: Record<string, string> = Object.fromEntries(
  ARTICLE_STYLE_OPTIONS.map((s) => [s.value, s.label]),
);

/** 配图方式选项 */
export const IMAGE_METHOD_OPTIONS = [
  { value: "PEXELS", label: "Pexels", desc: "高质量摄影图库", vipOnly: false },
  { value: "MERMAID", label: "Mermaid", desc: "代码驱动图表", vipOnly: false },
  { value: "ICONIFY", label: "Iconify", desc: "开源图标集", vipOnly: false },
  { value: "EMOJI_PACK", label: "表情包", desc: "趣味表情配图", vipOnly: false },
  { value: "NANO_BANANA", label: "AI 生图", desc: "AI 生成图片", vipOnly: true },
  { value: "SVG_DIAGRAM", label: "SVG 图表", desc: "矢量数据图表", vipOnly: true },
] as const;

/** 去除 Markdown 标记后统计字数 */
export function getWordCount(text: string | undefined | null): number {
  if (!text) return 0;
  return text.replace(/[#*`>\-\[\]!()\s\\|~]+/g, "").length;
}
