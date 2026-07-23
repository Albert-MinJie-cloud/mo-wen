// @ts-ignore
/* eslint-disable */
import request from "@/request";

/** Stripe Webhook Stripe webhook 回调 POST /api/webhook/stripe */
export async function stripeWebhookApiWebhookStripePost(options?: {
  [key: string]: any;
}) {
  return request<any>("/api/webhook/stripe", {
    method: "POST",
    ...(options || {}),
  });
}
