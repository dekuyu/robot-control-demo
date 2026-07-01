// ===== WebSocket 连接生命周期管理 Composable =====
import { onMounted, onUnmounted, watch } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { wsConnection } from '@/ws/connection'
import { registerWSHandlers } from '@/ws/messageHandler'

const wsUrl = import.meta.env.VITE_WS_URL || `ws://${window.location.host}/ws`

export function useWebSocket() {
  const authStore = useAuthStore()

  onMounted(() => {
    if (authStore.isLoggedIn && authStore.accessToken) {
      registerWSHandlers()
      wsConnection.connect(wsUrl, authStore.accessToken)
    }
  })

  // 监听登录状态变化
  watch(() => authStore.isLoggedIn, (loggedIn) => {
    if (loggedIn && authStore.accessToken) {
      registerWSHandlers()
      wsConnection.connect(wsUrl, authStore.accessToken)
    } else {
      wsConnection.disconnect()
    }
  })

  onUnmounted(() => {
    wsConnection.disconnect()
  })

  return { wsConnection }
}
