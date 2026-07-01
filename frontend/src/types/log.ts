// ===== 操作日志类型定义 =====

/** 操作日志条目 */
interface OperationLog {
  id: number
  timestamp: string
  userId: number
  username: string
  operationType: string
  target: string | null
  parameters: Record<string, unknown> | null
  result: string
  robotResponse: string | null
}

export type { OperationLog }
