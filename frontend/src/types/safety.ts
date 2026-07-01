// ===== 安全类型定义 =====

/** 轴限位 */
interface AxisLimit {
  min: number
  max: number
}

/** 安全检查结果 */
interface SafetyCheckResult {
  servoOk: boolean
  modeOk: boolean
  alarmOk: boolean
  speedOk: boolean
  operatorConfirmed: boolean
  allPassed: boolean
  failures: string[]
}

/** 安全配置 */
interface SafetyConfig {
  id: number
  maxSpeedPercent: number
  requireConfirm: boolean
  axisLimits: Record<string, AxisLimit>
}

export type { AxisLimit, SafetyCheckResult, SafetyConfig }
