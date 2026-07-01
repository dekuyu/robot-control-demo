// ===== 认证 API =====
import { post, get } from './client'
import type { LoginPayload, LoginResult, UserInfo } from '@/types/user'

export const authAPI = {
  /** 登录 */
  login(data: LoginPayload) {
    return post<LoginResult>('/api/auth/login', data)
  },
  /** 登出 */
  logout() {
    return post('/api/auth/logout')
  },
  /** 获取当前用户信息 */
  getMe() {
    return get<UserInfo>('/api/auth/me')
  },
  /** 刷新 Token */
  refreshToken(refreshToken: string) {
    return post<{ accessToken: string; refreshToken: string }>(
      '/api/auth/refresh', { refresh_token: refreshToken }
    )
  },
}
