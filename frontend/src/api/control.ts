// ===== 机械臂控制 API =====
import { post, put } from './client'

export const controlAPI = {
  /** 伺服上电 */
  servoOn() { return post('/api/control/servo/on') },
  /** 伺服断电 */
  servoOff() { return post('/api/control/servo/off') },
  /** 启动程序 */
  programStart(name?: string) { return post('/api/control/program/start', { action: 'start', program_name: name }) },
  /** 停止程序 */
  programStop() { return post('/api/control/program/stop') },
  /** 暂停程序 */
  programPause() { return post('/api/control/program/pause') },
  /** 恢复程序 */
  programResume() { return post('/api/control/program/resume') },
  /** 报警复位 */
  alarmReset() { return post('/api/control/alarm/reset') },
  /** 开始点动 */
  jogStart(data: { axis: number; direction: string; speedPercent: number }) {
    return post('/api/control/jog/start', data)
  },
  /** 停止点动 */
  jogStop(axis: number) { return post('/api/control/jog/stop', { axis }) },
  /** 增量移动 */
  incrementMove(data: { axis: number; incrementDeg: number }) {
    return post('/api/control/increment', data)
  },
  /** 目标运动 */
  targetMove(data: { target: Record<string, number>; speedPercent: number; coordinateType: string }) {
    return post('/api/control/target-move', data)
  },
  /** 直角坐标 */
  cartesianMove(data: { axis: string; value: number; speedPercent: number }) {
    return post('/api/control/cartesian', data)
  },
  /** 设置速度 */
  setSpeed(speedPercent: number) {
    return put('/api/control/speed', { speed_percent: speedPercent })
  },
}
