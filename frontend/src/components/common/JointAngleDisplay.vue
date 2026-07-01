<!-- 关节角度显示组件 -->
<template>
  <div class="joint-display">
    <h4 class="panel-title">关节角度</h4>
    <div class="joint-grid">
      <div v-for="axis in axes" :key="axis.key" class="joint-item">
        <span class="joint-name">{{ axis.name }}</span>
        <div class="joint-bar-wrapper">
          <div class="joint-bar" :style="{ width: axis.percent + '%', background: axis.color }"></div>
        </div>
        <span class="joint-value">{{ formatAngle(joints[axis.key]) }}</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { JointAngles } from '@/types/robot'
import { AXIS_NAMES } from '@/utils/constants'
import { formatAngle } from '@/utils/format'
import { angleToPercent, getDefaultAxisLimits } from '@/utils/safety'

const props = defineProps<{ joints: JointAngles }>()

const limits = getDefaultAxisLimits()

const axes = computed(() => {
  const keys = ['j1', 'j2', 'j3', 'j4', 'j5', 'j6'] as const
  const colors = ['#2196f3', '#00c853', '#ff9100', '#e040fb', '#00bcd4', '#ff5252']
  return keys.map((key, i) => {
    const angle = props.joints[key] ?? 0
    const limit = limits[key as keyof typeof limits]
    const percent = angleToPercent(angle, limit?.min ?? -180, limit?.max ?? 180)
    return {
      key,
      name: AXIS_NAMES[i + 1]?.name ?? key.toUpperCase(),
      percent,
      color: colors[i],
    }
  })
})
</script>

<style scoped lang="scss">
.panel-title {
  font-size: 14px;
  font-weight: 600;
  color: $color-text-primary;
  margin: 0 0 $spacing-md;
}
.joint-grid {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.joint-item {
  display: grid;
  grid-template-columns: 80px 1fr 70px;
  align-items: center;
  gap: $spacing-sm;
}
.joint-name {
  font-size: 12px;
  color: $color-text-secondary;
}
.joint-bar-wrapper {
  height: 6px;
  background: rgba($color-border, 0.5);
  border-radius: 3px;
  overflow: hidden;
}
.joint-bar {
  height: 100%;
  border-radius: 3px;
  transition: width 0.3s ease;
  min-width: 2px;
}
.joint-value {
  font-size: 13px;
  font-family: $font-family-mono;
  color: $color-text-primary;
  text-align: right;
}
</style>
