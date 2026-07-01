// ===== 报警类型定义 =====

/** 报警级别 */
type AlarmLevel = 'critical' | 'warning' | 'info'

/** 报警信息 */
interface AlarmInfo {
  id: number
  alarmCode: string
  alarmLevel: AlarmLevel
  description: string | null
  isActive: boolean
  occurredAt: string
  clearedAt: string | null
}

export type { AlarmLevel, AlarmInfo }
