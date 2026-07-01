// ===== 机器人实时状态 Store =====
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { RobotStatus, JointAngles, EndCoords, RobotMode } from '@/types/robot'

export const useRobotStore = defineStore('robot', () => {
  const connected = ref(false)
  const servoOn = ref(false)
  const runningMode = ref<RobotMode>('unknown')
  const alarmActive = ref(false)
  const speedPercent = ref(0)
  const joints = ref<JointAngles>({ j1:0, j2:0, j3:0, j4:0, j5:0, j6:0 })
  const endCoords = ref<EndCoords>({ x:0, y:0, z:0, rx:0, ry:0, rz:0 })
  const torques = ref<number[]>([])
  const executingProgram = ref<string | null>(null)
  const lastUpdate = ref<string | null>(null)

  const statusLabel = computed(() => {
    if (!connected.value) return { text: '未连接', color: '#ff1744' }
    if (alarmActive.value) return { text: '报警中', color: '#ff9100' }
    if (!servoOn.value) return { text: '伺服关闭', color: '#9aa0a6' }
    return { text: '运行中', color: '#00c853' }
  })

  const modeLabel = computed(() => {
    const map: Record<string, string> = {
      teaching: '示教模式', play: '再现模式', remote: '远程模式',
      idle: '空闲', error: '错误', unknown: '未知',
    }
    return map[runningMode.value] ?? runningMode.value
  })

  function updateStatus(data: Partial<RobotStatus>) {
    if (data.connected !== undefined) connected.value = data.connected
    if (data.servoOn !== undefined) servoOn.value = data.servoOn
    if (data.runningMode !== undefined) runningMode.value = data.runningMode
    if (data.alarmActive !== undefined) alarmActive.value = data.alarmActive
    if (data.speedPercent !== undefined) speedPercent.value = data.speedPercent
    if (data.joints) joints.value = data.joints
    if (data.endCoords) endCoords.value = data.endCoords
    if (data.torques) torques.value = data.torques
    if (data.executingProgram !== undefined) executingProgram.value = data.executingProgram
    lastUpdate.value = new Date().toISOString()
  }

  function updateFromWS(type: string, data: Record<string, unknown>) {
    if (type === 'robot_status') {
      if (typeof data.servoOn === 'boolean') servoOn.value = data.servoOn
      if (typeof data.runningMode === 'string') runningMode.value = data.runningMode as RobotMode
      if (typeof data.alarmActive === 'boolean') alarmActive.value = data.alarmActive
    } else if (type === 'robot_position' && data.joints) {
      joints.value = data.joints as unknown as JointAngles
      if (data.endCoords) endCoords.value = data.endCoords as unknown as EndCoords
    } else if (type === 'robot_torque' && data.torques) {
      torques.value = data.torques as number[]
    }
    lastUpdate.value = new Date().toISOString()
  }

  function reset() {
    connected.value = false; servoOn.value = false; runningMode.value = 'unknown'
    alarmActive.value = false; speedPercent.value = 0
    joints.value = { j1:0, j2:0, j3:0, j4:0, j5:0, j6:0 }
    endCoords.value = { x:0, y:0, z:0, rx:0, ry:0, rz:0 }
    torques.value = []; executingProgram.value = null
  }

  return { connected, servoOn, runningMode, alarmActive, speedPercent, joints, endCoords,
    torques, executingProgram, lastUpdate, statusLabel, modeLabel,
    updateStatus, updateFromWS, reset }
})
