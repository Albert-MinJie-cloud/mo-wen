// @ts-ignore
/* eslint-disable */
import request from "@/request";

/** Create Vip Payment Session 创建 VIP 支付会话

productType 可选值：VIP_MONTHLY（月付）/ VIP_YEARLY（年付）/ VIP_PERMANENT（永久，默认） POST /api/payment/create-vip-session */
export async function createVipPaymentSessionApiPaymentCreateVipSessionPost(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.createVipPaymentSessionApiPaymentCreateVipSessionPostParams,
  body: API.CreatePaymentSessionRequest,
  options?: { [key: string]: any }
) {
  return request<API.BaseResponseStr_>("/api/payment/create-vip-session", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    params: { ...params },
    data: body,
    ...(options || {}),
  });
}

/** Get Payment Records 获取当前用户支付记录 GET /api/payment/records */
export async function getPaymentRecordsApiPaymentRecordsGet(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.getPaymentRecordsApiPaymentRecordsGetParams,
  options?: { [key: string]: any }
) {
  return request<API.BaseResponseListPaymentRecordVO_>("/api/payment/records", {
    method: "GET",
    params: { ...params },
    ...(options || {}),
  });
}

/** Refund 申请退款 POST /api/payment/refund */
export async function refundApiPaymentRefundPost(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.refundApiPaymentRefundPostParams,
  options?: { [key: string]: any }
) {
  return request<API.BaseResponseBool_>("/api/payment/refund", {
    method: "POST",
    params: {
      ...params,
    },
    ...(options || {}),
  });
}
