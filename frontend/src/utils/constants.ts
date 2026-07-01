// ===== 全局常量定义 =====

/** 默认机器人 IP */
export const DEFAULT_ROBOT_IP = '192.168.255.1'
/** 默认机器人端口 */
export const DEFAULT_ROBOT_PORT = 10040
/** 默认本地端口 */
export const DEFAULT_LOCAL_PORT = 0

/** 轴名称映射 */
export const AXIS_NAMES: Record<number, { name: string; desc: string }> = {
  1: { name: 'S轴(J1)', desc: '本体旋转' },
  2: { name: 'L轴(J2)', desc: '下臂前后' },
  3: { name: 'U轴(J3)', desc: '上臂上下' },
  4: { name: 'R轴(J4)', desc: '下臂旋转' },
  5: { name: 'B轴(J5)', desc: '手腕上下' },
  6: { name: 'T轴(J6)', desc: '手腕旋转' },
  7: { name: 'E轴(J7)', desc: '第7轴' },
}

/** 角色速度上限 */
export const ROLE_SPEED_LIMITS: Record<string, number> = {
  admin: 100,
  operator: 30,
  engineer: 80,
  observer: 0,
}

/** 预设速度档位 */
export const SPEED_PRESETS = [
  { label: '微动档', value: 5 },
  { label: '慢速档', value: 15 },
  { label: '正常档', value: 50 },
  { label: '高速档', value: 80 },
]

/** 操作类型标签 */
export const OPERATION_TYPE_LABELS: Record<string, string> = {
  SERVO_ON: '伺服上电',
  SERVO_OFF: '伺服断电',
  PROGRAM_START: '程序启动',
  PROGRAM_STOP: '程序停止',
  PROGRAM_PAUSE: '程序暂停',
  JOG_START: '点动开始',
  JOG_STOP: '点动停止',
  INCREMENT: '增量移动',
  TARGET_MOVE: '目标移动',
  CARTESIAN: '直角坐标',
  SPEED_SET: '速度设置',
  VAR_WRITE: '变量写入',
  IO_WRITE: 'IO 写入',
  ESTOP: '急停',
  ALARM_RESET: '报警复位',
  SAFETY_CONFIG_UPDATE: '安全配置更新',
}

/** 权限矩阵：角色 -> 允许的操作 */
export const PERMISSION_MATRIX: Record<string, string[]> = {
  admin: ['*'],
  operator: ['view', 'servo', 'program_control', 'monitor', 'log_view_own'],
  engineer: ['view', 'servo', 'program_control', 'monitor', 'jog', 'move', 'terminal_send', 'var_readwrite', 'log_view'],
  observer: ['view', 'monitor'],
}

/** WebSocket 重连配置 */
export const WS_RECONNECT_INTERVAL = 3000
export const WS_MAX_RECONNECT = 10
