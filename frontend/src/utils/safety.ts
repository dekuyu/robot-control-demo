// ===== 安全计算工具 =====

/**
 * 计算实际生效速度
 * actual = setting × globalLimit
 */
export function calculateActualSpeed(settingSpeed: number, globalLimit: number): number {
  return Math.min(settingSpeed, globalLimit)
}

/**
 * 检查角度是否在软件限位内
 */
export function isAngleInLimit(angle: number, min: number, max: number): boolean {
  return angle >= min && angle <= max
}

/**
 * 计算限位百分比（用于进度条显示）
 */
export function angleToPercent(angle: number, min: number, max: number): number {
  const range = max - min
  if (range === 0) return 50
  const percent = ((angle - min) / range) * 100
  return Math.max(0, Math.min(100, percent))
}

/**
 * 生成轴限位配置的默认值
 */
export function getDefaultAxisLimits() {
  return {
    j1: { min: -180, max: 180 },
    j2: { min: -90, max: 135 },
    j3: { min: -90, max: 180 },
    j4: { min: -360, max: 360 },
    j5: { min: -135, max: 135 },
    j6: { min: -360, max: 360 },
  }
}
