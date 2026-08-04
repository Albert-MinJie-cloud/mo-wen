// @ts-ignore
/* eslint-disable */
import request from "@/request";

/** 获取当前月份热门选题 GET /api/topic/hot */
export async function getHotTopicsApiTopicHotGet(options?: {
  [key: string]: any;
}) {
  return request<API.BaseResponseHotTopicResponse_>("/api/topic/hot", {
    method: "GET",
    ...(options || {}),
  });
}
