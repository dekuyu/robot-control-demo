<!-- 权限守卫组件 -->
<template>
  <slot v-if="hasAccess" />
  <div v-else class="permission-denied">
    <el-icon :size="32"><Lock /></el-icon>
    <p>无操作权限</p>
    <span class="denied-detail">当前角色：{{ roleLabel }}</span>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { hasPermission } from '@/utils/permission'

const props = withDefaults(defineProps<{
  action?: string
  roles?: string[]
}>(), { action: '', roles: () => [] })

const authStore = useAuthStore()

const hasAccess = computed(() => {
  if (props.roles.length > 0) {
    return props.roles.includes(authStore.userRole)
  }
  if (props.action) {
    return hasPermission(authStore.userRole, props.action)
  }
  return true
})

const roleLabel = computed(() => {
  const map: Record<string, string> = {
    admin: '管理员', operator: '操作员', engineer: '工程师', observer: '观察员',
  }
  return map[authStore.userRole] || authStore.userRole
})
</script>

<style scoped lang="scss">
.permission-denied {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: $spacing-2xl;
  color: $color-text-muted;
  p { margin: $spacing-sm 0 4px; font-size: 14px; }
  .denied-detail { font-size: 12px; }
}
</style>
