import { ref } from "vue";

export type ThemeMode = "dark" | "light";

const THEME_KEY = "mo-wen-theme";

function getInitialTheme(): ThemeMode {
  const saved = localStorage.getItem(THEME_KEY);
  if (saved === "dark" || saved === "light") {
    return saved;
  }
  return "dark";
}

const currentTheme = ref<ThemeMode>(getInitialTheme());

function applyTheme(theme: ThemeMode) {
  document.documentElement.setAttribute("data-theme", theme);
  localStorage.setItem(THEME_KEY, theme);
}

// 初始化时立即应用主题
applyTheme(currentTheme.value);

export function useTheme() {
  const toggleTheme = () => {
    currentTheme.value = currentTheme.value === "dark" ? "light" : "dark";
    applyTheme(currentTheme.value);
  };

  return {
    currentTheme,
    toggleTheme,
  };
}
