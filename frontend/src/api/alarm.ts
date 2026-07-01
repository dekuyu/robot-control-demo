// ===== 报警管理 API =====
import { get, post } from './client'
import type { AlarmInfo } from '@/types/alarm'
import type { PaginatedData } from '@/types/api'

export const alarmAPI = {
  /** 报警列表 */
  list(params?: { page?: number; pageSize?: number; level?: string; isActive?: boolean }) {
    return get<PaginatedData<AlarmInfo>>('/api/alarms', params as Record<string, unknown>)
  },
  /** 活跃报警 */
  getActive() {
    return get<AlarmInfo[]>('/api/alarms/active')
  },
  /** 报警重置 */
  reset(alarmId?: number) {
    return post('/api/alarms/reset', { alarm_id: alarmId })
  },
  /** 报警历史统计 */
  getStats(params?: { startTime?: string; endTime?: string }) {
    return get<Record<string, unknown>>('/api/alarms/stats', params as Record<string, unknown>)
  },
}
