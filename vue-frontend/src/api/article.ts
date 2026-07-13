// @ts-ignore
/* eslint-disable */
import request from "@/request";

/** Get Article 获取文章详情 GET /api/article/${param0} */
export async function getArticleApiArticleTaskIdGet(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.getArticleApiArticleTaskIdGetParams,
  options?: { [key: string]: any }
) {
  const { task_id: param0, ...queryParams } = params;
  return request<API.BaseResponseArticleVO_>(`/api/article/${param0}`, {
    method: "GET",
    params: { ...queryParams },
    ...(options || {}),
  });
}

/** Create Article 创建文章任务 POST /api/article/create */
export async function createArticleApiArticleCreatePost(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.createArticleApiArticleCreatePostParams,
  body: API.ArticleCreateRequest,
  options?: { [key: string]: any }
) {
  return request<API.BaseResponseStr_>("/api/article/create", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    params: { ...params },
    data: body,
    ...(options || {}),
  });
}

/** Delete Article 删除文章 POST /api/article/delete */
export async function deleteArticleApiArticleDeletePost(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.deleteArticleApiArticleDeletePostParams,
  body: API.DeleteRequest,
  options?: { [key: string]: any }
) {
  return request<API.BaseResponseBool_>("/api/article/delete", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    params: { ...params },
    data: body,
    ...(options || {}),
  });
}

/** List Article 分页查询文章列表 POST /api/article/list */
export async function listArticleApiArticleListPost(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.listArticleApiArticleListPostParams,
  body: API.ArticleQueryRequest,
  options?: { [key: string]: any }
) {
  return request<API.BaseResponseDict_>("/api/article/list", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    params: { ...params },
    data: body,
    ...(options || {}),
  });
}

/** Get Progress SSE 进度推送 GET /api/article/progress/${param0} */
export async function getProgressApiArticleProgressTaskIdGet(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.getProgressApiArticleProgressTaskIdGetParams,
  options?: { [key: string]: any }
) {
  const { task_id: param0, ...queryParams } = params;
  return request<any>(`/api/article/progress/${param0}`, {
    method: "GET",
    params: { ...queryParams },
    ...(options || {}),
  });
}
