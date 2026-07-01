<!-- 末端笛卡尔坐标显示 -->
<template>
  <div class="end-coord-display">
    <h4 class="panel-title">末端坐标</h4>
    <div class="coord-grid">
      <div v-for="coord in coords" :key="coord.key" class="coord-item">
        <span class="coord-label">{{ coord.label }}</span>
        <span class="coord-value" :class="coord.key.startsWith('r') ? 'rotation' : ''">
          {{ formatCoord(coord.value, coord.unit) }}
        </span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { EndCoords } from '@/types/robot'
import { formatCoord } from '@/utils/format'

const props = defineProps<{ endCoords: EndCoords }>()

const coords = computed(() => [
  { key: 'x', label: 'X', value: props.endCoords.x, unit: 'mm' },
  { key: 'y', label: 'Y', value: props.endCoords.y, unit: 'mm' },
  { key: 'z', label: 'Z', value: props.endCoords.z, unit: 'mm' },
  { key: 'rx', label: 'RX', value: props.endCoords.rx, unit: '°' },
  { key: 'ry', label: 'RY', value: props.endCoords.ry, unit: '°' },
  { key: 'rz', label: 'RZ', value: props.endCoords.rz, unit: '°' },
])
</script>

<style scoped lang="scss">
.panel-title {
  font-size: 14px;
  font-weight: 600;
  color: $color-text-primary;
  margin: 0 0 $spacing-md;
}
.coord-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: $spacing-sm;
}
.coord-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding: $spacing-sm;
  background: rgba($color-bg-input, 0.5);
  border-radius: $radius-sm;
}
.coord-label {
  font-size: 11px;
  color: $color-text-muted;
  font-weight: 600;
}
.coord-value {
  font-size: 12px;
  font-family: $font-family-mono;
  color: $color-text-primary;
  &.rotation { color: $color-info; }
}
</style>
