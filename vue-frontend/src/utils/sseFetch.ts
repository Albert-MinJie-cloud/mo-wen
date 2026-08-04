export interface SSEMessage {
  type: string;
  data?: any;
  [key: string]: any;
}

export interface FetchSSEController {
  /** 主动关闭连接（可安全多次调用） */
  abort: () => void;
}

export interface FetchSSEOptions {
  onMessage: (message: SSEMessage) => void;
  onError?: (error: string) => void;
  onComplete?: () => void;
  /** 收到指定 type 时自动关闭连接并触发 onComplete，默认 ["ALL_COMPLETE", "ERROR"] */
  closeOnTypes?: string[];
}

/**
 * 基于 fetch + ReadableStream 的 SSE 连接
 *
 * 相比 EventSource 的优势：
 * - AbortController 精确控制生命周期，组件卸载时直接 abort
 * - 可区分 HTTP 错误、网络错误
 * - closeOnTypes 可配置，不再硬编码关闭条件
 */
export function connectFetchSSE(
  taskId: string,
  options: FetchSSEOptions,
): FetchSSEController {
  const { onMessage, onError, onComplete, closeOnTypes } = options;
  const closeTypes = closeOnTypes ?? ["ALL_COMPLETE", "ERROR"];

  const abortController = new AbortController();
  let aborted = false;

  async function connect() {
    try {
      const response = await fetch(`/api/article/progress/${taskId}`, {
        signal: abortController.signal,
        headers: { Accept: "text/event-stream" },
      });

      if (!response.ok) {
        onError?.(`HTTP ${response.status}: ${response.statusText}`);
        onComplete?.();
        return;
      }

      if (!response.body) {
        onError?.("浏览器不支持 ReadableStream");
        onComplete?.();
        return;
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let buffer = "";

      while (true) {
        const { done, value } = await reader.read();

        if (done) {
          onComplete?.();
          return;
        }

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split("\n");
        buffer = lines.pop() || "";

        for (const line of lines) {
          if (line.startsWith("data: ")) {
            const jsonStr = line.slice(6);
            try {
              const message: SSEMessage = JSON.parse(jsonStr);
              onMessage(message);

              if (closeTypes.includes(message.type)) {
                abortController.abort();
                aborted = true;
                onComplete?.();
                return;
              }
            } catch {
              console.error("SSE JSON 解析失败:", jsonStr);
            }
          }
        }
      }
    } catch (err: any) {
      if (err.name === "AbortError") {
        return;
      }
      const msg = err?.message || "未知连接错误";
      console.error("SSE fetch 连接错误:", msg);
      onError?.(msg);
      onComplete?.();
    }
  }

  connect();

  return {
    abort: () => {
      if (!aborted) {
        aborted = true;
        abortController.abort();
      }
    },
  };
}
