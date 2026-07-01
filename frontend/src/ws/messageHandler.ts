// ===== WebSocket 消息分发器 =====
import { wsConnection } from './connection'
import { useRobotStore } from '@/stores/robot'
import { useAlarmStore } from '@/stores/alarm'
import { useConnectionStore } from '@/stores/connection'

/**
 * 注册所有 WS 消息处理器
 * 将不同类型的推送消息路由到对应的 Pinia Store
 */
export function registerWSHandlers() {
  const robotStore = useRobotStore()
  const alarmStore = useAlarmStore()
  const connStore = useConnectionStore()

  // 机器人状态更新
  wsConnection.on('robot_status', (data: Record<string, unknown>) => {
    robotStore.updateFromWS('robot_status', data)
  })

  // 位置数据更新
  wsConnection.on('robot_position', (data: Record<string, unknown>) => {
    robotStore.updateFromWS('robot_position', data)
  })

  // 力矩数据更新
  wsConnection.on('robot_torque', (data: Record<string, unknown>) => {
    robotStore.updateFromWS('robot_torque', data)
  })

  // 报警更新
  wsConnection.on('alarm_update', (data: Record<string, unknown>) => {
    alarmStore.setAlarmState(!!data.hasActiveAlarm)
  })

  // 连接状态更新
  wsConnection.on('connection_update', (data: Record<string, unknown>) => {
    connStore.setConnected(!!data.connected)
  })
}
