<!-- 力矩显示组件 -->
<template>
  <div class="torque-display">
    <h4 class="panel-title">关节力矩</h4>
    <div class="torque-grid">
      <div v-for="(torque, idx) in torques" :key="idx" class="torque-item">
        <span class="torque-name">{{ axisName(idx) }}</span>
        <span class="torque-value" :class="torqueClass(torque)">
          {{ formatTorque(torque) }}
        </span>
      </div>
    </div>
    <div v-if="torques.length === 0" class="empty-state">暂无数据</div>
  </div>
</template>

<script setup lang="ts">
import { AXIS_NAMES } from '@/utils/constants'
import { formatTorque } from '@/utils/format'

defineProps<{ torques: number[] }>()

function axisName(idx: number): string {
  return AXIS_NAMES[idx + 1]?.name ?? `J${idx + 1}`
}

function torqueClass(value: number): string {
  if (value > 80) return 'danger'
  if (value > 60) return 'warning'
  return ''
}
</script>

<style scoped lang="scss">
.panel-title {
  font-size: 14px;
  font-weight: 600;
  color: $color-text-primary;
  margin: 0 0 $spacing-md;
}
.torque-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: $spacing-sm;
}
.torque-item {
  display: flex;
  flex-direction: column;
  gap: 2px;
  padding: $spacing-sm;
  background: rgba($color-bg-input, 0.5);
  border-radius: $radius-sm;
}
.torque-name {
  font-size: 11px;
  color: $color-text-muted;
}
.torque-value {
  font-size: 12px;
  font-family: $font-family-mono;
  color: $color-text-primary;
  &.danger { color: $color-danger; }
  &.warning { color: $color-warning; }
}
.empty-state {
  text-align: center;
  color: $color-text-muted;
  font-size: 13px;
  padding: $spacing-lg;
}
</style>
