<!-- IO 矩阵组件 -->
<template>
  <div class="io-matrix">
    <h4 class="panel-title">IO 信号</h4>
    <div class="io-grid">
      <div
        v-for="idx in indices"
        :key="idx"
        class="io-cell"
        :class="{ active: getValue(idx) === 1, disabled: readonly }"
        @click="!readonly && toggleIO(idx)"
        :title="`IO${idx}: ${getValue(idx) ? 'ON' : 'OFF'}`"
      >
        <span class="io-num">{{ idx }}</span>
        <span class="io-state">{{ getValue(idx) ? 'ON' : 'OFF' }}</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useVariableStore } from '@/stores/variable'

const props = withDefaults(defineProps<{
  indices: number[]
  readonly?: boolean
}>(), { readonly: false })

const varStore = useVariableStore()

function getValue(idx: number): number {
  return varStore.getIOValue(idx) ?? 0
}

async function toggleIO(idx: number) {
  const current = getValue(idx)
  await varStore.writeIO(idx, current ? 0 : 1)
}
</script>

<style scoped lang="scss">
.panel-title {
  font-size: 14px;
  font-weight: 600;
  color: $color-text-primary;
  margin: 0 0 $spacing-md;
}
.io-grid {
  display: grid;
  grid-template-columns: repeat(8, 1fr);
  gap: 4px;
}
.io-cell {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 8px 4px;
  background: rgba($color-bg-input, 0.5);
  border: 1px solid $color-border;
  border-radius: $radius-sm;
  cursor: pointer;
  transition: all $transition-fast;
  &.active {
    background: rgba($color-success, 0.2);
    border-color: rgba($color-success, 0.5);
  }
  &.disabled { cursor: default; opacity: 0.6; }
  &:hover:not(.disabled) { border-color: $color-info; }
}
.io-num {
  font-size: 10px;
  color: $color-text-muted;
  font-family: $font-family-mono;
}
.io-state {
  font-size: 11px;
  font-weight: 700;
  color: $color-text-secondary;
  font-family: $font-family-mono;
  .active & { color: $color-success; }
}
</style>
