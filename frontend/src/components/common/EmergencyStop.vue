<!-- 紧急停止按钮 -->
<template>
  <div class="emergency-stop-wrapper">
    <el-popconfirm
      title="确认执行紧急停止？这将立即停止机械臂所有运动！"
      confirm-button-text="确认急停"
      cancel-button-text="取消"
      confirm-button-type="danger"
      @confirm="handleEstop"
    >
      <template #reference>
        <button
          class="estop-button"
          :class="{ active: isActive, disabled: disabled }"
          :disabled="disabled"
        >
          <span class="estop-text">急停</span>
        </button>
      </template>
    </el-popconfirm>
  </div>
</template>

<script setup lang="ts">
import { ElMessage } from 'element-plus'
import { safetyAPI } from '@/api/safety'

const props = withDefaults(defineProps<{
  isActive?: boolean
  disabled?: boolean
}>(), { isActive: false, disabled: false })

const emit = defineEmits<{ estop: [] }>()

async function handleEstop() {
  try {
    const res = await safetyAPI.emergencyStop()
    if (res.code === 0) {
      ElMessage.warning('紧急停止已执行')
      emit('estop')
    }
  } catch {
    ElMessage.error('急停指令发送失败')
  }
}
</script>

<style scoped lang="scss">
.estop-button {
  width: $estop-size;
  height: $estop-size;
  border-radius: 50%;
  border: 4px solid $color-danger;
  background: rgba($color-danger, 0.15);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all $transition-fast;
  &:hover:not(.disabled) {
    background: rgba($color-danger, 0.3);
    box-shadow: 0 0 20px rgba($color-danger, 0.4);
  }
  &.active {
    background: $color-danger;
    box-shadow: 0 0 24px rgba($color-danger, 0.6);
    animation: pulse 1s infinite;
  }
  &.disabled {
    opacity: 0.4;
    cursor: not-allowed;
  }
}
.estop-text {
  color: $color-danger;
  font-size: 14px;
  font-weight: 700;
  letter-spacing: 2px;
  .active & { color: white; }
}
@keyframes pulse {
  0%, 100% { box-shadow: 0 0 24px rgba($color-danger, 0.6); }
  50% { box-shadow: 0 0 36px rgba($color-danger, 0.9); }
}
</style>
