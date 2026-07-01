// ===== 数值格式化工具 =====

/**
 * 格式化角度值（保留1位小数）
 */
export function formatAngle(angle: number | null | undefined): string {
  if (angle == null) return '--'
  return `${angle.toFixed(1)}°`
}

/**
 * 格式化坐标值（保留1位小数）
 */
export function formatCoord(value: number | null | undefined, unit: string = 'mm'): string {
  if (value == null) return '--'
  return `${value.toFixed(1)} ${unit}`
}

/**
 * 格式化百分比
 */
export function formatPercent(value: number | null | undefined): string {
  if (value == null) return '--'
  return `${Math.round(value)}%`
}

/**
 * 格式化力矩值
 */
export function formatTorque(value: number | null | undefined): string {
  if (value == null) return '--'
  return `${value.toFixed(2)} N·m`
}

/**
 * 格式化字节大小
 */
export function formatBytes(bytes: number): string {
  if (bytes < 1024) return `${bytes} B`
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`
}

/**
 * 格式化时间戳为可读时间
 */
export function formatTime(date: string | Date | null): string {
  if (!date) return '--'
  return new Date(date).toLocaleTimeString('zh-CN', { hour12: false })
}

/**
 * 格式化日期时间
 */
export function formatDateTime(date: string | Date | null): string {
  if (!date) return '--'
  return new Date(date).toLocaleString('zh-CN', { hour12: false })
}
