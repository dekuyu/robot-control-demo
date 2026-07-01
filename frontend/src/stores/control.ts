// ===== 控制指令状态 Store =====
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useAuthStore } from './auth'
import { calculateActualSpeed } from '@/utils/safety'

export const useControlStore = defineStore('control', () => {
  const authStore = useAuthStore()
  const speedSetting = ref(30)
  const globalSpeedLimit = ref(50)
  const requireConfirm = ref(true)

  const actualSpeed = computed(() => {
    return calculateActualSpeed(speedSetting.value, globalSpeedLimit.value)
  })

  const isEstopActive = ref(false)
  const isJogging = ref<Record<number, boolean>>({})
  const controlLock = ref(false) // 操作互斥锁

  function setSpeed(pct: number) { speedSetting.value = pct }
  function setGlobalLimit(pct: number) { globalSpeedLimit.value = pct }
  function setRequireConfirm(val: boolean) { requireConfirm.value = val }
  function setEstop(val: boolean) { isEstopActive.value = val }
  function setJogging(axis: number, val: boolean) { isJogging.value[axis] = val }

  return { speedSetting, globalSpeedLimit, requireConfirm, actualSpeed,
    isEstopActive, isJogging, controlLock,
    setSpeed, setGlobalLimit, setRequireConfirm, setEstop, setJogging }
})
