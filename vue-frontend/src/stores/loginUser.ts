import { defineStore } from "pinia";
import { ref } from "vue";
import { getLoginUserApiUserGetLoginGet } from "@/api/user";
import { DEFAULT_USERNAME } from "@/constants/user";

/**
 * 登录用户信息
 */
export const useLoginUserStore = defineStore("loginUser", () => {
  // 默认值（未登录态，仅填充展示字段）
  const loginUser = ref<API.LoginUserVO>({
    userName: DEFAULT_USERNAME,
  } as API.LoginUserVO);

  // 获取登录用户信息
  async function fetchLoginUser() {
    const res = await getLoginUserApiUserGetLoginGet({});
    if (res.data.code === 0 && res.data.data) {
      loginUser.value = res.data.data;
    }
  }

  // 更新登录用户信息
  function setLoginUser(newLoginUser: any) {
    loginUser.value = newLoginUser;
  }

  return { loginUser, fetchLoginUser, setLoginUser };
});
