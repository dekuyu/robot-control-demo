<!-- 通知提示组件 -->
<template>
  <teleport to="body">
    <transition name="toast-fade" group>
      <div
        v-for="toast in toasts"
        :key="toast.id"
        class="notification-toast"
        :class="toast.type"
      >
        <el-icon class="toast-icon"><WarningFilled /></el-icon>
        <span class="toast-text">{{ toast.message }}</span>
        <el-button text class="toast-close" @click="remove(toast.id)">
          <el-icon><Close /></el-icon>
        </el-button>
      </div>
    </transition>
  </teleport>
</template>

<script setup lang="ts">
import { ref } from 'vue'

interface Toast {
  id: number
  message: string
  type: 'success' | 'warning' | 'error' | 'info'
  duration: number
}

const toasts = ref<Toast[]>([])
let nextId = 0

function add(message: string, type: Toast['type'] = 'info', duration: number = 4000) {
  const id = nextId++
  toasts.value.push({ id, message, type, duration })
  if (duration > 0) {
    setTimeout(() => remove(id), duration)
  }
}

function remove(id: number) {
  toasts.value = toasts.value.filter(t => t.id !== id)
}

defineExpose({ add, remove })
</script>

<style scoped lang="scss">
.notification-toast {
  position: fixed;
  top: 16px;
  right: 16px;
  z-index: $z-tooltip;
  display: flex;
  align-items: center;
  gap: $spacing-sm;
  padding: 10px $spacing-md;
  border-radius: $radius-md;
  min-width: 280px;
  max-width: 420px;
  box-shadow: $shadow-glass;
  backdrop-filter: blur(12px);
  margin-bottom: 8px;
  &.success { background: rgba($color-success, 0.2); border: 1px solid rgba($color-success, 0.4); }
  &.warning { background: rgba($color-warning, 0.2); border: 1px solid rgba($color-warning, 0.4); }
  &.error { background: rgba($color-danger, 0.2); border: 1px solid rgba($color-danger, 0.4); }
  &.info { background: rgba($color-info, 0.2); border: 1px solid rgba($color-info, 0.4); }
}
.toast-text { flex: 1; font-size: 13px; color: $color-text-primary; }
.toast-fade-enter-active { transition: all 0.3s ease; }
.toast-fade-leave-active { transition: all 0.3s ease; }
.toast-fade-enter-from { opacity: 0; transform: translateX(100%); }
.toast-fade-leave-to { opacity: 0; transform: translateX(100%); }
</style>
