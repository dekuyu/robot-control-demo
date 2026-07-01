<!-- 速度滑块组件 -->
<template>
  <div class="speed-slider">
    <div class="slider-header">
      <span class="slider-label">速度控制</span>
      <span class="slider-value">{{ modelValue }}%</span>
    </div>
    <el-slider
      :model-value="modelValue"
      :min="0"
      :max="maxSpeed"
      :step="1"
      :disabled="disabled"
      :show-tooltip="false"
      @update:model-value="$emit('update:modelValue', $event as number)"
    />
    <div class="speed-presets">
      <el-button
        v-for="preset in speedPresets"
        :key="preset.value"
        size="small"
        :type="modelValue === preset.value ? 'primary' : 'default'"
        :disabled="disabled || preset.value > maxSpeed"
        @click="$emit('update:modelValue', preset.value)"
      >
        {{ preset.label }}
      </el-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { SPEED_PRESETS } from '@/utils/constants'

defineProps<{
  modelValue: number
  maxSpeed?: number
  disabled?: boolean
}>()

defineEmits<{ 'update:modelValue': [value: number] }>()

const speedPresets = SPEED_PRESETS
</script>

<style scoped lang="scss">
.speed-slider {
  background: $color-bg-card;
  border: 1px solid $color-border;
  border-radius: $radius-lg;
  padding: $spacing-md $spacing-lg;
}
.slider-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: $spacing-sm;
}
.slider-label {
  font-size: 13px;
  color: $color-text-secondary;
}
.slider-value {
  font-size: 20px;
  font-weight: 700;
  color: $color-info;
  font-family: $font-family-mono;
}
.speed-presets {
  display: flex;
  gap: $spacing-sm;
  margin-top: $spacing-sm;
}
</style>
