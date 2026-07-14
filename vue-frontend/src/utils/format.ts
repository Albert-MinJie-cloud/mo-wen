import dayjs from "dayjs";

/**
 * 格式化时间
 * @param time 时间字符串
 * @param fmt 格式，默认 "YYYY-MM-DD HH:mm"
 * @param fallback 无效时间时的回退值，默认 "--"
 */
export function formatTime(
  time: string | undefined | null,
  fmt = "YYYY-MM-DD HH:mm",
  fallback = "--"
): string {
  if (!time) return fallback;
  return dayjs(time).format(fmt);
}
