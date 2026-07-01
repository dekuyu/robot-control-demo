// ===== WebSocket 消息类型定义 =====

/** WS 消息类型 */
const WSMessageType = {
  ROBOT_STATUS: 'robot_status',
  ROBOT_POSITION: 'robot_position',
  ROBOT_TORQUE: 'robot_torque',
  ALARM_UPDATE: 'alarm_update',
  CONNECTION_UPDATE: 'connection_update',
  SAFETY_ALERT: 'safety_alert',
  ERROR: 'error',
  PACKET_LOG: 'packet_log',
} as const

type WSMessageTypeValue = typeof WSMessageType[keyof typeof WSMessageType]

/** WS 推送消息 */
interface WSMessage<T = Record<string, unknown>> {
  type: WSMessageTypeValue
  timestamp: string
  data: T
}

/** 机器人状态数据 */
interface WSRobotStatusData {
  servoOn: boolean
  runningMode: string
  alarmActive: boolean
  speedPercent: number
}

/** 位置数据 */
interface WSRobotPositionData {
  joints: Record<string, number>
  endCoords: Record<string, number>
}

/** 力矩数据 */
interface WSRobotTorqueData {
  torques: number[]
}

/** 报警数据 */
interface WSAlarmData {
  alarms: unknown[]
  hasActiveAlarm: boolean
}

/** 连接数据 */
interface WSConnectionData {
  connected: boolean
  lastHeartbeat: string
}

/** 安全告警 */
interface WSSafetyAlertData {
  alertType: string
  message: string
  severity: 'critical' | 'warning' | 'info'
}

export { WSMessageType }
export type {
  WSMessageTypeValue, WSMessage,
  WSRobotStatusData, WSRobotPositionData, WSRobotTorqueData,
  WSAlarmData, WSConnectionData, WSSafetyAlertData,
}
