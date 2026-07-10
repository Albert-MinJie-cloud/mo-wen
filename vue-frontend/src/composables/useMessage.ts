import { ref } from "vue";

export interface MessageItem {
  id: number;
  type: "success" | "error" | "warning" | "info";
  content: string;
}

const messages = ref<MessageItem[]>([]);
let nextId = 0;

export function useMessage() {
  const show = (type: MessageItem["type"], content: string, duration = 3000) => {
    const id = nextId++;
    messages.value.push({ id, type, content });

    if (duration > 0) {
      setTimeout(() => {
        remove(id);
      }, duration);
    }

    return id;
  };

  const remove = (id: number) => {
    const index = messages.value.findIndex((m) => m.id === id);
    if (index !== -1) {
      messages.value.splice(index, 1);
    }
  };

  const success = (content: string, duration?: number) =>
    show("success", content, duration);
  const error = (content: string, duration?: number) =>
    show("error", content, duration);
  const warning = (content: string, duration?: number) =>
    show("warning", content, duration);
  const info = (content: string, duration?: number) =>
    show("info", content, duration);

  return { messages, show, remove, success, error, warning, info };
}
