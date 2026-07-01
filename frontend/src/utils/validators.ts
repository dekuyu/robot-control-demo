// ===== 输入校验工具 =====

/** 验证 IPv4 地址 */
export function isValidIP(ip: string): boolean {
  const pattern = /^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$/
  const match = ip.match(pattern)
  if (!match) return false
  return match.slice(1).every(n => parseInt(n) <= 255)
}

/** 验证端口号 */
export function isValidPort(port: number): boolean {
  return Number.isInteger(port) && port >= 0 && port <= 65535
}

/** 验证角度值 */
export function isValidAngle(angle: number): boolean {
  return angle >= -360 && angle <= 360
}

/** 验证速度百分比 */
export function isValidSpeed(speed: number): boolean {
  return Number.isInteger(speed) && speed >= 0 && speed <= 100
}

/** 验证十六进制输入 */
export function validateHexInput(input: string): { valid: boolean; message: string } {
  const cleaned = input.replace(/\s/g, '')
  if (!cleaned) return { valid: false, message: '输入不能为空' }
  if (cleaned.length % 2 !== 0) return { valid: false, message: '十六进制字符串长度必须为偶数' }
  if (!/^[0-9a-fA-F]+$/.test(cleaned)) return { valid: false, message: '包含无效的十六进制字符' }
  return { valid: true, message: '' }
}

/** 清理十六进制输入（移除非法字符） */
export function sanitizeHexInput(input: string): string {
  return input.replace(/[^0-9a-fA-F\s]/g, '')
}
