// ===== 报警状态 Store =====
import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { AlarmInfo } from '@/types/alarm'

export const useAlarmStore = defineStore('alarm', () => {
  const activeAlarms = ref<AlarmInfo[]>([])
  const hasActiveAlarm = ref(false)

  function updateActiveAlarms(alarms: AlarmInfo[]) {
    activeAlarms.value = alarms
    hasActiveAlarm.value = alarms.length > 0
  }

  function setAlarmState(active: boolean) {
    hasActiveAlarm.value = active
  }

  return { activeAlarms, hasActiveAlarm, updateActiveAlarms, setAlarmState }
})
