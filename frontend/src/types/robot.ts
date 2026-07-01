// ===== 机器人类型定义 =====

/** 机器人运行模式 */
type RobotMode = 'teaching' | 'play' | 'remote' | 'idle' | 'error'

/** 关节角度 */
interface JointAngles {
  j1: number; j2: number; j3: number
  j4: number; j5: number; j6: number
  j7?: number
}

/** 末端笛卡尔坐标 */
interface EndCoords {
  x: number; y: number; z: number
  rx: number; ry: number; rz: number
}

/** 机器人完整状态 */
interface RobotStatus {
  connected: boolean
  servoOn: boolean
  runningMode: RobotMode
  alarmActive: boolean
  speedPercent: number
  joints: JointAngles | null
  endCoords: EndCoords | null
  torques: number[]
  executingProgram: string | null
}

/** 机器人连接配置 */
interface RobotConfig {
  id: number
  name: string
  ip: string
  port: number
  isActive: boolean
  createdAt: string
}

export type { RobotMode, JointAngles, EndCoords, RobotStatus, RobotConfig }
