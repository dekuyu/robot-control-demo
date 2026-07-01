// ===== 连接管理 Store =====
import { defineStore } from 'pinia'
import { ref } from 'vue'
import { DEFAULT_ROBOT_IP, DEFAULT_ROBOT_PORT } from '@/utils/constants'
import { robotAPI } from '@/api/robot'

export const useConnectionStore = defineStore('connection', () => {
  const isConnected = ref(false)
  const robotIP = ref(DEFAULT_ROBOT_IP)
  const robotPort = ref(DEFAULT_ROBOT_PORT)
  const isConnecting = ref(false)
  const reconnectCount = ref(0)

  async function connect(ip?: string, port?: number) {
    isConnecting.value = true
    try {
      const res = await robotAPI.connect({ ip: ip || robotIP.value, port: port || robotPort.value })
      if (res.code === 0) {
        isConnected.value = true
        robotIP.value = ip || robotIP.value
        robotPort.value = port || robotPort.value
        reconnectCount.value = 0
      }
    } finally {
      isConnecting.value = false
    }
  }

  async function disconnect() {
    await robotAPI.disconnect()
    isConnected.value = false
  }

  function setConnected(val: boolean) { isConnected.value = val }
  function incrementReconnect() { reconnectCount.value++ }
  function resetReconnect() { reconnectCount.value = 0 }

  return { isConnected, robotIP, robotPort, isConnecting, reconnectCount,
    connect, disconnect, setConnected, incrementReconnect, resetReconnect }
})
