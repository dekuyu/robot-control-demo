<!-- 变量编辑器组件 -->
<template>
  <div class="variable-editor">
    <div class="editor-row" v-for="idx in indices" :key="idx">
      <span class="var-index">{{ varType }}{{ idx }}</span>
      <el-input-number
        :model-value="getValue(idx)"
        :disabled="readonly"
        size="small"
        controls-position="right"
        @update:model-value="handleWrite(idx, $event ?? 0)"
      />
      <el-button size="small" :loading="loadingIdx === idx" @click="handleRead(idx)">
        <el-icon><Refresh /></el-icon>
      </el-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useVariableStore } from '@/stores/variable'

const props = withDefaults(defineProps<{
  varType: 'B' | 'I' | 'D' | 'IO'
  indices: number[]
  readonly?: boolean
}>(), { readonly: false })

const varStore = useVariableStore()
const loadingIdx = ref<number | null>(null)

function getValue(idx: number): number {
  if (props.varType === 'B') return varStore.getBValue(idx) ?? 0
  if (props.varType === 'I') return varStore.getIValue(idx) ?? 0
  if (props.varType === 'D') return varStore.getDValue(idx) ?? 0
  if (props.varType === 'IO') return varStore.getIOValue(idx) ?? 0
  return 0
}

async function handleRead(idx: number) {
  loadingIdx.value = idx
  try {
    if (props.varType === 'B') await varStore.readB(idx)
    else if (props.varType === 'I') await varStore.readI(idx)
    else if (props.varType === 'D') await varStore.readD(idx)
    else if (props.varType === 'IO') await varStore.readIO(idx)
  } finally {
    loadingIdx.value = null
  }
}

async function handleWrite(idx: number, value: number) {
  if (props.varType === 'B') await varStore.writeB(idx, value)
  else if (props.varType === 'D') await varStore.writeD(idx, value)
  else if (props.varType === 'IO') await varStore.writeIO(idx, value)
}
</script>

<style scoped lang="scss">
.editor-row {
  display: flex;
  align-items: center;
  gap: $spacing-sm;
  padding: 4px 0;
}
.var-index {
  width: 48px;
  font-family: $font-family-mono;
  font-size: 12px;
  color: $color-text-secondary;
  font-weight: 600;
}
</style>
