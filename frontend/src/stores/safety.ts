// ===== 安全状态 Store =====
import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { SafetyCheckResult } from '@/types/safety'

export const useSafetyStore = defineStore('safety', () => {
  const checkResult = ref<SafetyCheckResult>({
    servoOk: false, modeOk: false, alarmOk: false,
    speedOk: true, operatorConfirmed: false,
    allPassed: false, failures: [],
  })

  function updateCheckResult(result: SafetyCheckResult) {
    checkResult.value = result
  }

  return { checkResult, updateCheckResult }
})
