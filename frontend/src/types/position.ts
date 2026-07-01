// ===== 位置类型定义 =====

/** 位置姿态 */
interface PositionPosture {
  joints: Record<string, number>
  endCoords: Record<string, number>
}

/** 命名点位 */
interface SavedPosition {
  id: number
  name: string
  description: string | null
  pVariableIndex: number | null
  posture: PositionPosture
  createdBy: number
  createdAt: string
}

export type { PositionPosture, SavedPosition }
