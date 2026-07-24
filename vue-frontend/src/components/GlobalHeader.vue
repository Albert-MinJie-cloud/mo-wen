<template>
  <a-layout-header class="header">
    <div class="header-container">
      <div class="header-left">
        <RouterLink to="/" class="logo-link">
          <div class="logo-wrapper">
            <Logo />
            <h1 class="site-title">AI文章创作器</h1>
          </div>
        </RouterLink>
      </div>

      <!-- 中间：导航菜单 -->
      <nav class="nav-center">
        <RouterLink
          v-for="item in menuItems"
          :key="item.key"
          :to="item.key"
          :class="['nav-item', { active: selectedKeys.includes(item.key) }]"
        >
          <component :is="item.icon" class="nav-icon" />
          <span>{{ item.label }}</span>
        </RouterLink>
      </nav>

      <!-- 右侧：用户操作区域 -->
      <div class="header-right">
        <!-- 主题切换 -->
        <button class="theme-toggle" @click="toggleTheme" :title="themeTitle">
          <!-- 太阳图标：暗色模式下显示，表示切换到浅色 -->
          <svg v-if="currentTheme === 'dark'" width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="5"/>
            <line x1="12" y1="1" x2="12" y2="3"/>
            <line x1="12" y1="21" x2="12" y2="23"/>
            <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/>
            <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/>
            <line x1="1" y1="12" x2="3" y2="12"/>
            <line x1="21" y1="12" x2="23" y2="12"/>
            <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/>
            <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/>
          </svg>
          <!-- 月亮图标：浅色模式下显示，表示切换到深色 -->
          <svg v-else width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>
          </svg>
        </button>

        <div v-if="loginUserStore.loginUser.id" class="user-dropdown">
          <!-- VIP 标识 -->
          <RouterLink v-if="!isVip" to="/vip" class="upgrade-vip-btn">
            <CrownOutlined />
            <span>升级 VIP</span>
          </RouterLink>
          <RouterLink v-else to="/vip" class="vip-badge">
            <CrownOutlined />
            <span>VIP</span>
          </RouterLink>

          <a-dropdown>
            <a-space class="user-info">
              <a-avatar
                :src="loginUserStore.loginUser.userAvatar"
                :size="36"
                class="user-avatar"
              />
              <span class="user-name">
                {{ loginUserStore.loginUser.userName ?? "无名" }}
              </span>
            </a-space>
            <template #overlay>
              <a-menu class="dropdown-menu">
                <a-menu-item
                  v-if="isVip"
                  key="vip-info"
                  class="vip-info-item"
                  @click="router.push('/vip')"
                >
                  <CrownOutlined />
                  <span>会员中心</span>
                </a-menu-item>
                <a-menu-divider v-if="isVip" />
                <a-menu-item @click="doLogout" class="dropdown-item">
                  <LogoutOutlined />
                  <span>退出登录</span>
                </a-menu-item>
              </a-menu>
            </template>
          </a-dropdown>
        </div>
        <div v-else>
          <Button to="/user/login" size="sm">登录</Button>
        </div>
      </div>
    </div>
  </a-layout-header>
</template>

<script setup lang="ts">
import { computed, ref } from "vue";
import { useRouter } from "vue-router";
import { message } from "@/message";
import { useLoginUserStore } from "@/stores/loginUser";
import { useTheme } from "@/composables/useTheme";
import { logoutApiUserLogoutPost } from "@/api/user";
import {
  LogoutOutlined,
  HomeOutlined,
  EditOutlined,
  UnorderedListOutlined,
  SettingOutlined,
  CrownOutlined,
  BarChartOutlined,
} from "@ant-design/icons-vue";
import { isVip as checkIsVip } from "@/utils/permission";
import Button from "@/components/Button.vue";
import Logo from "@/components/Logo.vue";

const loginUserStore = useLoginUserStore();
const { currentTheme, toggleTheme } = useTheme();
const themeTitle = computed(() =>
  currentTheme.value === "dark" ? "切换到浅色模式" : "切换到深色模式"
);
const router = useRouter();
// 当前选中菜单
const selectedKeys = ref<string[]>(["/"]);
// 监听路由变化，更新当前选中菜单
router.afterEach((to) => {
  selectedKeys.value = [to.path];
});

// 判断是否为 VIP（管理员也视为 VIP）
const isVip = computed(() => checkIsVip(loginUserStore.loginUser));

// 菜单配置项
const originItems = [
  {
    key: "/",
    icon: HomeOutlined,
    label: "首页",
  },
  {
    key: "/create",
    icon: EditOutlined,
    label: "创作",
  },
  {
    key: "/article/list",
    icon: UnorderedListOutlined,
    label: "历史",
  },
  {
    key: "/admin/userManage",
    icon: SettingOutlined,
    label: "管理",
    admin: true,
  },
  {
    key: "/admin/statistics",
    icon: BarChartOutlined,
    label: "数据",
    admin: true,
  },
];

// 过滤菜单项
const menuItems = computed(() => {
  return originItems.filter((item) => {
    if (item.admin) {
      const loginUser = loginUserStore.loginUser;
      return loginUser && loginUser.userRole === "admin";
    }
    return true;
  });
});

// 退出登录
const doLogout = async () => {
  const res = await logoutApiUserLogoutPost({});
  if (res.data.code === 0) {
    loginUserStore.setLoginUser({
      userName: "未登录",
    });
    message.success("退出登录成功");
    await router.push("/user/login");
  } else {
    message.error("退出登录失败，" + res.data.message);
  }
};
</script>

<style scoped lang="scss">
.header {
  position: sticky;
  top: 0;
  z-index: 100;
  background: var(--glass-bg);
  backdrop-filter: var(--glass-blur);
  -webkit-backdrop-filter: var(--glass-blur);
  padding: 0;
  height: 64px;
  line-height: 64px;
  border-bottom: 1px solid var(--color-border);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
  transition: all var(--transition-normal);
  overflow: hidden;
}

.header-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 100%;
}

.header-left {
  display: flex;
  align-items: center;
}

.logo-link {
  display: block;
  transition: opacity var(--transition-fast);
}

.logo-link:hover {
  opacity: 0.8;
}

.logo-wrapper {
  display: flex;
  align-items: center;
  gap: 10px;
}

.site-title {
  margin: 0;
  font-size: 17px;
  font-weight: 700;
  color: var(--color-text);
  white-space: nowrap;
  letter-spacing: -0.3px;
}

/* 导航菜单 */
.nav-center {
  display: flex;
  align-items: center;
  gap: 8px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  border-radius: var(--radius-md);
  font-size: 14px;
  font-weight: 500;
  color: var(--color-text-secondary);
  transition: all var(--transition-fast);
  text-decoration: none;
}

.nav-item:hover {
  color: var(--color-text);
  background: var(--color-background-secondary);
}

.nav-item.active {
  color: var(--color-text);
}

.nav-icon {
  font-size: 16px;
}

/* 主题切换 */
.theme-toggle {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  background: transparent;
  color: var(--color-text-secondary);
  font-size: 18px;
  cursor: pointer;
  transition: all var(--transition-fast);
  flex-shrink: 0;
}

.theme-toggle:hover {
  color: var(--color-primary);
  background: var(--color-background-secondary);
  border-color: var(--color-primary);
}

/* 用户区域 */
.header-right {
  display: flex;
  align-items: center;
  gap: 16px;
}

.user-dropdown {
  cursor: pointer;
  height: 64px;
  display: flex;
  align-items: center;
  gap: 16px;
}

.upgrade-vip-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 14px;
  border-radius: var(--radius-md);
  font-size: 13px;
  font-weight: 500;
  background: transparent;
  color: var(--color-primary);
  text-decoration: none;
  transition: all var(--transition-fast);

  &:hover {
    background: rgba(59, 130, 246, 0.08);
    color: var(--color-primary-dark);
  }

  .anticon {
    font-size: 13px;
  }
}

.vip-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 14px;
  font-size: 13px;
  font-weight: 500;
  color: var(--color-primary);
  text-decoration: none;
  transition: all var(--transition-fast);

  &:hover {
    color: var(--color-primary-dark);
  }

  .anticon {
    font-size: 13px;
  }
}

.user-info {
  padding: 6px 12px;
  border-radius: var(--radius-md);
  transition: all var(--transition-fast);
  display: flex;
  align-items: center;
}

.user-info:hover {
  background: var(--color-background-secondary);
}

.user-avatar {
  border: 2px solid var(--color-border);
}

.user-name {
  font-weight: 500;
  color: var(--color-text);
  font-size: 14px;
}

.dropdown-menu {
  border-radius: var(--radius-md);
  overflow: hidden;
  box-shadow: var(--shadow-lg);
  border: 1px solid var(--color-border);
}

.dropdown-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  transition: all var(--transition-fast);
}

.dropdown-item:hover {
  background: var(--color-background-secondary);
}

.vip-info-item {
  color: var(--color-primary-dark);
  background: rgba(59, 130, 246, 0.1);
  font-weight: 600;
  cursor: default;

  &:hover {
    background: rgba(59, 130, 246, 0.15);
  }
}

/* 响应式 */
@media (max-width: 768px) {
  .header-container {
    padding: 0 16px;
  }

  .site-title {
    display: none;
  }

  .nav-item span {
    display: none;
  }

  .nav-item {
    padding: 8px 12px;
  }

  .user-name {
    display: none;
  }
}
</style>
