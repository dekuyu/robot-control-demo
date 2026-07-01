<!-- 确认对话框（危险操作二次确认） -->
<template>
  <el-dialog
    :model-value="modelValue"
    :title="title"
    :width="420"
    :close-on-click-modal="false"
    :before-close="handleCancel"
  >
    <div class="confirm-body">
      <el-icon class="confirm-icon" :class="typeIconClass" :size="48">
        <WarningFilled />
      </el-icon>
      <p class="confirm-message">{{ message }}</p>
      <p v-if="detail" class="confirm-detail">{{ detail }}</p>
    </div>
    <template #footer>
      <el-button @click="handleCancel">取消</el-button>
      <el-button :type="confirmType" @click="$emit('confirm')" :loading="loading">
        {{ confirmText }}
      </el-button>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = withDefaults(defineProps<{
  modelValue: boolean
  title?: string
  message?: string
  detail?: string
  type?: 'danger' | 'warning'
  confirmText?: string
  loading?: boolean
}>(), {
  title: '确认操作',
  message: '请确认执行此操作',
  type: 'warning',
  confirmText: '确认',
  loading: false,
})

defineEmits<{ 'update:modelValue': [value: boolean]; confirm: []; cancel: [] }>()

const confirmType = computed(() => props.type === 'danger' ? 'danger' : 'warning')
const typeIconClass = computed(() => props.type === 'danger' ? 'icon-danger' : 'icon-warning')

function handleCancel() { /* handled by dialog before-close */ }
</script>

<style scoped lang="scss">
.confirm-body {
  text-align: center;
  padding: $spacing-lg 0;
}
.confirm-icon {
  margin-bottom: $spacing-md;
  &.icon-danger { color: $color-danger; }
  &.icon-warning { color: $color-warning; }
}
.confirm-message {
  font-size: 15px;
  color: $color-text-primary;
  margin-bottom: $spacing-sm;
}
.confirm-detail {
  font-size: 12px;
  color: $color-text-secondary;
}
</style>
