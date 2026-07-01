<!--
  YRC1000 机械臂远程控制系统 - 根组件
  全局挂载：急停按钮、报警横幅、连接状态
-->
<template>
  <EmergencyStop @trigger="handleEstop" :active="estopActive" />
  <AlarmBanner v-if="alarmStore.hasActiveAlarm" :alarms="alarmStore.activeAlarms" />
  <router-view />
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useAlarmStore } from '@/stores/alarm'
import { useControlStore } from '@/stores/control'
import { safetyAPI } from '@/api/safety'
import EmergencyStop from '@/components/common/EmergencyStop.vue'
import AlarmBanner from '@/components/common/AlarmBanner.vue'
import { useKeyboard } from '@/composables/useKeyboard'

const router = useRouter()
const authStore = useAuthStore()
const alarmStore = useAlarmStore()
const controlStore = useControlStore()
const estopActive = ref(false)

// Ctrl+E 快捷键触发急停
useKeyboard([{
  key: 'e',
  ctrl: true,
  handler: () => handleEstop(),
  description: '紧急停止',
}])

/** 触发急停 */
async function handleEstop() {
  try {
    const res = await safetyAPI.emergencyStop()
    if (res.data?.stopped) {
      estopActive.value = true
      controlStore.setEstop(true)
    }
  } catch (e) {
    console.error('急停失败:', e)
  }
}

onMounted(async () => {
  // 尝试从 localStorage 恢复登录状态
  if (authStore.accessToken) {
    try {
      await authStore.fetchCurrentUser()
      router.push('/dashboard')
    } catch {
      authStore.clearAuth()
      router.push('/login')
    }
  }
})
</script>
