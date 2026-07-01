// ===== 坐标与位置 API =====
import { get, post, put, del } from './client'
import type { SavedPosition, PositionPosture } from '@/types/position'
import type { PaginatedData } from '@/types/api'

export const positionAPI = {
  /** 命名点位列表 */
  list(params?: { page?: number; pageSize?: number; search?: string }) {
    return get<PaginatedData<SavedPosition>>('/api/positions', params as Record<string, unknown>)
  },
  /** 创建命名点位 */
  create(data: { name: string; description?: string; posture: PositionPosture }) {
    return post<SavedPosition>('/api/positions', data)
  },
  /** 更新命名点位 */
  update(id: number, data: { name?: string; description?: string }) {
    return put<SavedPosition>(`/api/positions/${id}`, data)
  },
  /** 删除 */
  remove(id: number) { return del(`/api/positions/${id}`) },
  /** 获取当前姿态 */
  getCurrent() { return get<PositionPosture>('/api/positions/current') },
  /** 读取 P 变量 */
  readPVar(index: number) { return get<PositionPosture>(`/api/positions/p-variable/${index}`) },
  /** 写入 P 变量 */
  writePVar(index: number, data: PositionPosture) {
    return put(`/api/positions/p-variable/${index}`, data)
  },
}
