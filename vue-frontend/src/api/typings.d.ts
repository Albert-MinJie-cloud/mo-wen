declare namespace API {
  type addUserApiUserAddPostParams = {
    SESSION?: string | null;
  };

  type ArticleCreateRequest = {
    /** Topic 选题 */
    topic: string;
    /** Style 文章风格：tech/emotional/educational/humorous */
    style?: string | null;
    /** Enabledimagemethods 允许的配图方式列表（为空表示支持所有方式） */
    enabledImageMethods?: string[] | null;
  };

  type ArticleQueryRequest = {
    /** Current 当前页码 */
    current?: number;
    /** Pagesize 每页大小 */
    pageSize?: number;
    /** Sortfield 排序字段 */
    sortField?: string | null;
    /** Sortorder 排序顺序 */
    sortOrder?: string | null;
    /** Id 文章 ID */
    id?: number | null;
    /** Taskid 任务 ID */
    taskId?: string | null;
    /** Userid 用户 ID */
    userId?: number | null;
    /** Topic 选题 */
    topic?: string | null;
    /** Status 状态 */
    status?: string | null;
  };

  type ArticleVO = {
    /** Id */
    id: number;
    /** Taskid */
    taskId: string;
    /** Userid */
    userId: number;
    /** Topic */
    topic: string;
    /** Userdescription */
    userDescription?: string | null;
    /** Style */
    style?: string | null;
    /** Maintitle */
    mainTitle?: string | null;
    /** Subtitle */
    subTitle?: string | null;
    /** Titleoptions */
    titleOptions?: TitleOption[] | null;
    /** Outline */
    outline?: any[] | null;
    /** Content */
    content?: string | null;
    /** Fullcontent */
    fullContent?: string | null;
    /** Coverimage */
    coverImage?: string | null;
    /** Images */
    images?: any[] | null;
    /** Status */
    status: string;
    /** Phase */
    phase?: string | null;
    /** Errormessage */
    errorMessage?: string | null;
    /** Createtime */
    createTime: string;
    /** Completedtime */
    completedTime?: string | null;
    /** Updatetime */
    updateTime: string;
  };

  type BaseResponseArticleVO_ = {
    /** Code 状态码 */
    code?: number;
    /** 响应数据 */
    data?: ArticleVO | null;
    /** Message 响应消息 */
    message?: string;
  };

  type BaseResponseBool_ = {
    /** Code 状态码 */
    code?: number;
    /** Data 响应数据 */
    data?: boolean | null;
    /** Message 响应消息 */
    message?: string;
  };

  type BaseResponseDict_ = {
    /** Code 状态码 */
    code?: number;
    /** Data 响应数据 */
    data?: Record<string, any> | null;
    /** Message 响应消息 */
    message?: string;
  };

  type BaseResponseInt_ = {
    /** Code 状态码 */
    code?: number;
    /** Data 响应数据 */
    data?: number | null;
    /** Message 响应消息 */
    message?: string;
  };

  type BaseResponseLoginUserVO_ = {
    /** Code 状态码 */
    code?: number;
    /** 响应数据 */
    data?: LoginUserVO | null;
    /** Message 响应消息 */
    message?: string;
  };

  type BaseResponseStr_ = {
    /** Code 状态码 */
    code?: number;
    /** Data 响应数据 */
    data?: string | null;
    /** Message 响应消息 */
    message?: string;
  };

  type BaseResponseUserVO_ = {
    /** Code 状态码 */
    code?: number;
    /** 响应数据 */
    data?: UserVO | null;
    /** Message 响应消息 */
    message?: string;
  };

  type createArticleApiArticleCreatePostParams = {
    SESSION?: string | null;
  };

  type deleteArticleApiArticleDeletePostParams = {
    SESSION?: string | null;
  };

  type DeleteRequest = {
    /** Id 要删除的 ID */
    id: number;
  };

  type deleteUserApiUserDeletePostParams = {
    SESSION?: string | null;
  };

  type getArticleApiArticleTaskIdGetParams = {
    task_id: string;
    SESSION?: string | null;
  };

  type getLoginUserApiUserGetLoginGetParams = {
    SESSION?: string | null;
  };

  type getProgressApiArticleProgressTaskIdGetParams = {
    task_id: string;
    SESSION?: string | null;
  };

  type getUserByIdApiUserGetGetParams = {
    id: number;
  };

  type HTTPValidationError = {
    /** Detail */
    detail?: ValidationError[];
  };

  type listArticleApiArticleListPostParams = {
    SESSION?: string | null;
  };

  type listUsersByPageApiUserListPagePostParams = {
    SESSION?: string | null;
  };

  type LoginUserVO = {
    /** Id */
    id: number;
    /** Useraccount */
    userAccount: string;
    /** Username */
    userName?: string | null;
    /** Useravatar */
    userAvatar?: string | null;
    /** Userprofile */
    userProfile?: string | null;
    /** Userrole */
    userRole: string;
    /** Createtime */
    createTime: string;
    /** Updatetime */
    updateTime: string;
    /** Quota 用户额度 */
    quota?: number | null;
    /** Viptime VIP过期时间 */
    vipTime?: string | null;
  };

  type logoutApiUserLogoutPostParams = {
    SESSION?: string | null;
  };

  type TitleOption = {
    /** Maintitle */
    mainTitle: string;
    /** Subtitle */
    subTitle: string;
  };

  type updateUserApiUserUpdatePostParams = {
    SESSION?: string | null;
  };

  type UserAddRequest = {
    /** Useraccount 账号 */
    userAccount: string;
    /** Userpassword 密码 */
    userPassword: string;
    /** Username 用户昵称 */
    userName?: string | null;
    /** Useravatar 用户头像 */
    userAvatar?: string | null;
    /** Userprofile 用户简介 */
    userProfile?: string | null;
    /** Userrole 用户角色 */
    userRole?: string;
  };

  type UserLoginRequest = {
    /** Useraccount 账号 */
    userAccount: string;
    /** Userpassword 密码 */
    userPassword: string;
  };

  type UserQueryRequest = {
    /** Current 当前页码 */
    current?: number;
    /** Pagesize 每页大小 */
    pageSize?: number;
    /** Sortfield 排序字段 */
    sortField?: string | null;
    /** Sortorder 排序顺序 */
    sortOrder?: string | null;
    /** Id 用户 ID */
    id?: number | null;
    /** Useraccount 账号 */
    userAccount?: string | null;
    /** Username 用户昵称 */
    userName?: string | null;
    /** Userprofile 用户简介 */
    userProfile?: string | null;
    /** Userrole 用户角色 */
    userRole?: string | null;
  };

  type UserRegisterRequest = {
    /** Useraccount 账号 */
    userAccount: string;
    /** Userpassword 密码 */
    userPassword: string;
    /** Checkpassword 确认密码 */
    checkPassword: string;
  };

  type UserUpdateRequest = {
    /** Id 用户 ID */
    id: number;
    /** Username 用户昵称 */
    userName?: string | null;
    /** Useravatar 用户头像 */
    userAvatar?: string | null;
    /** Userprofile 用户简介 */
    userProfile?: string | null;
    /** Userrole 用户角色 */
    userRole?: string | null;
  };

  type UserVO = {
    /** Id */
    id: number;
    /** Useraccount */
    userAccount: string;
    /** Username */
    userName?: string | null;
    /** Useravatar */
    userAvatar?: string | null;
    /** Userprofile */
    userProfile?: string | null;
    /** Userrole */
    userRole: string;
    /** Createtime */
    createTime: string;
    /** Quota 用户额度 */
    quota?: number | null;
    /** Viptime VIP过期时间 */
    vipTime?: string | null;
  };

  type ValidationError = {
    /** Location */
    loc: (string | number)[];
    /** Message */
    msg: string;
    /** Error Type */
    type: string;
  };
}
