// ===== 用户管理 API（管理员专用） =====
import { get, post, put, del } from './client'
import type { UserInfo } from '@/types/user'
import type { PaginatedData } from '@/types/api'

export const userAPI = {
  /** 用户列表 */
  list(params?: { page?: number; pageSize?: number; role?: string }) {
    return get<PaginatedData<UserInfo>>('/api/users', params as Record<string, unknown>)
  },
  /** 创建用户 */
  create(data: { username: string; password: string; role: string }) {
    return post<UserInfo>('/api/users', data)
  },
  /** 更新用户 */
  update(id: number, data: { username?: string; role?: string; isActive?: boolean }) {
    return put<UserInfo>(`/api/users/${id}`, data)
  },
  /** 删除（软删除） */
  remove(id: number) { return del(`/api/users/${id}`) },
  /** 解锁用户 */
  unlock(id: number) { return post(`/api/users/${id}/unlock`) },
}
