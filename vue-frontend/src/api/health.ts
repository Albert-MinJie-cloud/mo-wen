// @ts-ignore
/* eslint-disable */
import request from "@/request";

/** Health Check 健康检查接口 GET /api/health */
export async function healthCheckApiHealthGet(options?: {
  [key: string]: any;
}) {
  return request<API.BaseResponseStr_>("/api/health", {
    method: "GET",
    ...(options || {}),
  });
}
