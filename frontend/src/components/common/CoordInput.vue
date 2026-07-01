<!-- 坐标输入组件 -->
<template>
  <div class="coord-input">
    <h4 class="panel-title">{{ title }}</h4>
    <div class="coord-grid">
      <div v-for="field in fields" :key="field.key" class="coord-field">
        <label class="field-label">{{ field.label }}</label>
        <el-input-number
          :model-value="modelValue[field.key] ?? 0"
          :precision="field.precision"
          :step="field.step"
          :min="field.min"
          :max="field.max"
          :disabled="disabled"
          size="small"
          controls-position="right"
          @update:model-value="updateValue(field.key, $event ?? 0)"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  title?: string
  modelValue: Record<string, number>
  fields: { key: string; label: string; precision?: number; step?: number; min?: number; max?: number }[]
  disabled?: boolean
}>()

const emit = defineEmits<{ 'update:modelValue': [value: Record<string, number>] }>()

function updateValue(key: string, val: number) {
  emit('update:modelValue', { ...(/* modelValue accessed via props */ {}), [key]: val })
}
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
.coord-field {
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.field-label {
  font-size: 11px;
  color: $color-text-muted;
  font-weight: 600;
}
</style>
