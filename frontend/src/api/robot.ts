// ===== 机器人连接 API =====
import { get, post, put } from './client'
import type { RobotStatus, RobotConfig } from '@/types/robot'

export const robotAPI = {
  /** 连接到机器人 */
  connect(data: { ip: string; port: number }) {
    return post<{ connected: boolean; configId: number }>('/api/robot/connect', data)
  },
  /** 断开连接 */
  disconnect() {
    return post('/api/robot/disconnect')
  },
  /** 获取状态 */
  getStatus() {
    return get<RobotStatus>('/api/robot/status')
  },
  /** 获取配置 */
  getConfig() {
    return get<RobotConfig>('/api/robot/config')
  },
  /** 更新配置 */
  updateConfig(data: { name: string; ip: string; port: number }) {
    return put<RobotConfig>('/api/robot/config', data)
  },
  /** 心跳 */
  getHeartbeat() {
    return get<{ alive: boolean }>('/api/robot/heartbeat')
  },
}
