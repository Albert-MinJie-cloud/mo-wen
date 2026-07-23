import { USER_ROLE_ADMIN, USER_ROLE_VIP } from "@/constants/user";

/**
 * 权限判断工具
 */

/**
 * 判断用户是否为管理员
 */
export const isAdmin = (user?: API.LoginUserVO): boolean => {
  return user?.userRole === USER_ROLE_ADMIN;
};

/**
 * 判断用户是否为 VIP（包括管理员），含过期检查
 */
export const isVip = (user?: API.LoginUserVO): boolean => {
  if (!user) return false;
  if (user.userRole === USER_ROLE_ADMIN) return true;
  if (user.userRole !== USER_ROLE_VIP) return false;
  // 永久会员（无过期时间）
  if (!user.vipExpireTime) return true;
  // 检查是否在有效期内
  return new Date(user.vipExpireTime) > new Date();
};

/**
 * 判断用户是否有配额
 */
export const hasQuota = (user?: API.LoginUserVO): boolean => {
  if (isAdmin(user) || isVip(user)) {
    return true;
  }
  return (user?.quota ?? 0) > 0;
};
