// ===== 控制指令类型定义 =====

/** 点动控制参数 */
interface JogParams {
  axis: number        // 1~7
  direction: 'positive' | 'negative'
  speedPercent: number
}

/** 增量移动参数 */
interface IncrementParams {
  axis: number
  incrementDeg: number
}

/** 目标移动参数 */
interface TargetMoveParams {
  target: Record<string, number>
  speedPercent: number
  coordinateType: 'joint' | 'cartesian'
}

/** 直角坐标参数 */
interface CartesianParams {
  axis: 'x'|'y'|'z'|'rx'|'ry'|'rz'
  value: number
  speedPercent: number
}

/** 速度参数 */
interface SpeedParams {
  speedPercent: number
}

export type { JogParams, IncrementParams, TargetMoveParams, CartesianParams, SpeedParams }
