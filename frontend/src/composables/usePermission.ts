// ===== 权限判断 Composable =====
import { computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { hasPermission, canControl, canSendTerminal } from '@/utils/permission'

export function usePermission() {
  const authStore = useAuthStore()
  const role = computed(() => authStore.userRole)

  function check(action: string): boolean {
    return hasPermission(role.value, action)
  }

  const canOperate = computed(() => canControl(role.value))
  const canSendUDP = computed(() => canSendTerminal(role.value))
  const canManage = computed(() => role.value === 'admin')

  return { role, check, canOperate, canSendUDP, canManage }
}
