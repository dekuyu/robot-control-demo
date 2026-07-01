// ===== 变量类型定义 =====

/** 变量数据 */
interface VariableData {
  varType: 'B' | 'P' | 'I' | 'D' | 'IO'
  index: number
  value: number | string
  rawHex?: string
}

/** IO 信号 */
interface IOSignal {
  index: number
  value: number
  label: string | null
}

export type { VariableData, IOSignal }
