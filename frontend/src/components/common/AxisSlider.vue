<!-- 轴滑块组件 -->
<template>
  <div class="axis-slider">
    <div class="slider-row">
      <span class="axis-label">{{ AXIS_NAMES[axis]?.name ?? `J${axis}` }}</span>
      <el-slider
        :model-value="value"
        :min="min"
        :max="max"
        :step="0.1"
        :disabled="disabled"
        :show-tooltip="false"
        class="slider-bar"
        @update:model-value="$emit('update:modelValue', $event as number)"
      />
      <span class="axis-value">{{ value?.toFixed(1) }}°</span>
      <div class="axis-buttons">
        <el-button
          size="small"
          :disabled="disabled || value >= max"
          @mousedown="$emit('jogStart', axis, 'positive')"
          @mouseup="$emit('jogStop', axis)"
          @mouseleave="$emit('jogStop', axis)"
        >+</el-button>
        <el-button
          size="small"
          :disabled="disabled || value <= min"
          @mousedown="$emit('jogStart', axis, 'negative')"
          @mouseup="$emit('jogStop', axis)"
          @mouseleave="$emit('jogStop', axis)"
        >−</el-button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { AXIS_NAMES } from '@/utils/constants'

defineProps<{
  axis: number
  value: number
  min?: number
  max?: number
  disabled?: boolean
}>()

defineEmits<{
  'update:modelValue': [value: number]
  jogStart: [axis: number, direction: string]
  jogStop: [axis: number]
}>()
</script>

<style scoped lang="scss">
.slider-row {
  display: flex;
  align-items: center;
  gap: $spacing-sm;
  padding: 6px 0;
}
.axis-label {
  width: 70px;
  font-size: 12px;
  font-weight: 600;
  color: $color-text-secondary;
}
.slider-bar {
  flex: 1;
}
.axis-value {
  width: 55px;
  font-size: 12px;
  font-family: $font-family-mono;
  color: $color-text-primary;
  text-align: right;
}
.axis-buttons {
  display: flex;
  gap: 4px;
}
</style>
