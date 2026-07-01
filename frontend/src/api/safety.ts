// ===== 安全管理 API =====
import { get, put, post } from './client'
import type { SafetyCheckResult, SafetyConfig } from '@/types/safety'

export const safetyAPI = {
  /** 执行安全检查 */
  check() { return get<SafetyCheckResult>('/api/safety/check') },
  /** 获取安全配置 */
  getConfig() { return get<SafetyConfig>('/api/safety/config') },
  /** 更新安全配置 */
  updateConfig(data: { maxSpeedPercent?: number; requireConfirm?: boolean }) {
    return put<SafetyConfig>('/api/safety/config', data)
  },
  /** 更新轴限位 */
  updateLimits(axisLimits: Record<string, { min: number; max: number }>) {
    return put('/api/safety/limits', { axis_limits: axisLimits })
  },
  /** 紧急停止 */
  emergencyStop() { return post<{ stopped: boolean }>('/api/safety/emergency-stop') },
}
