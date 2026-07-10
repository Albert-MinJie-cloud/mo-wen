import { ref } from "vue";

export interface ToastItem {
  id: number;
  type: "success" | "error" | "warning" | "info";
  message: string;
}

const toasts = ref<ToastItem[]>([]);
let nextId = 0;

export function useToast() {
  const show = (
    type: ToastItem["type"],
    message: string,
    duration = 3000,
  ) => {
    const id = nextId++;
    toasts.value.push({ id, type, message });

    if (duration > 0) {
      setTimeout(() => {
        remove(id);
      }, duration);
    }

    return id;
  };

  const remove = (id: number) => {
    const index = toasts.value.findIndex((t) => t.id === id);
    if (index !== -1) {
      toasts.value.splice(index, 1);
    }
  };

  const success = (message: string, duration?: number) =>
    show("success", message, duration);
  const error = (message: string, duration?: number) =>
    show("error", message, duration);
  const warning = (message: string, duration?: number) =>
    show("warning", message, duration);
  const info = (message: string, duration?: number) =>
    show("info", message, duration);

  return { toasts, show, remove, success, error, warning, info };
}
