// ===== 安全检查 Composable =====
import { ref } from 'vue'
import { safetyAPI } from '@/api/safety'
import { useSafetyStore } from '@/stores/safety'

export function useSafetyCheck() {
  const safetyStore = useSafetyStore()
  const checking = ref(false)
  const operatorConfirmed = ref(false)

  async function runCheck(): Promise<boolean> {
    checking.value = true
    try {
      const res = await safetyAPI.check()
      if (res.data) {
        // 合并操作员确认状态
        const result = {
          servoOk: res.data.servoOk,
          modeOk: res.data.modeOk,
          alarmOk: res.data.alarmOk,
          speedOk: res.data.speedOk,
          operatorConfirmed: operatorConfirmed.value,
          allPassed: res.data.servoOk && res.data.modeOk && res.data.alarmOk && operatorConfirmed.value,
          failures: res.data.failures || [],
        }
        safetyStore.updateCheckResult(result)
        return result.allPassed
      }
      return false
    } finally {
      checking.value = false
    }
  }

  function confirmOperation() { operatorConfirmed.value = true }
  function resetConfirm() { operatorConfirmed.value = false }

  return { checking, operatorConfirmed, runCheck, confirmOperation, resetConfirm }
}
