// ===== 用户类型定义 =====

/** 用户角色 */
type UserRole = 'admin' | 'operator' | 'engineer' | 'observer'

/** 用户信息 */
interface UserInfo {
  id: number
  username: string
  role: UserRole
  isActive: boolean
  isLocked: boolean
  lastLogin: string | null
  createdAt: string
}

/** 登录请求 */
interface LoginPayload {
  username: string
  password: string
}

/** 登录响应 */
interface LoginResult {
  accessToken: string
  refreshToken: string
  tokenType: string
  user: UserInfo
}

export type { UserRole, UserInfo, LoginPayload, LoginResult }
