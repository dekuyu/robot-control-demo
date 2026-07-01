// ===== 操作日志 API =====
import { get } from './client'
import type { OperationLog } from '@/types/log'
import type { PaginatedData } from '@/types/api'

export const logAPI = {
  /** 查询日志 */
  query(params?: Record<string, unknown>) {
    return get<PaginatedData<OperationLog>>('/api/logs', params)
  },
  /** 日志统计 */
  getStats(params?: { startTime?: string; endTime?: string }) {
    return get('/api/logs/stats', params as Record<string, unknown>)
  },
}
