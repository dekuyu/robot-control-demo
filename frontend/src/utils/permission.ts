// ===== 权限判断工具 =====
import { PERMISSION_MATRIX } from './constants'
import type { UserRole } from '@/types/user'

/**
 * 检查用户是否有指定操作权限
 */
export function hasPermission(role: UserRole, action: string): boolean {
  const allowed = PERMISSION_MATRIX[role]
  if (!allowed) return false
  return allowed.includes('*') || allowed.includes(action)
}

/**
 * 是否可以发送控制指令
 */
export function canControl(role: UserRole): boolean {
  return hasPermission(role, 'jog') || hasPermission(role, 'move')
}

/**
 * 是否可以发送 UDP 调试报文
 */
export function canSendTerminal(role: UserRole): boolean {
  return hasPermission(role, 'terminal_send')
}

/**
 * 是否可以管理用户（管理员专用）
 */
export function canManageUsers(role: UserRole): boolean {
  return role === 'admin'
}

/**
 * 检查速度设置权限
 */
export function getMaxSpeed(role: UserRole): number {
  const limits: Record<string, number> = {
    admin: 100,
    engineer: 80,
    operator: 30,
    observer: 0,
  }
  return limits[role] ?? 0
}
