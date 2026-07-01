<!-- 日志表格组件 -->
<template>
  <div class="log-table">
    <el-table :data="logs" stripe size="small" height="100%" v-loading="loading">
      <el-table-column prop="id" label="ID" width="60" />
      <el-table-column prop="timestamp" label="时间" width="160">
        <template #default="{ row }">{{ formatDateTime(row.timestamp) }}</template>
      </el-table-column>
      <el-table-column prop="username" label="用户" width="100" />
      <el-table-column prop="operationType" label="操作类型" width="120">
        <template #default="{ row }">{{ getOperationTypeLabel(row.operationType) }}</template>
      </el-table-column>
      <el-table-column prop="target" label="目标" width="120" />
      <el-table-column prop="result" label="结果" width="70">
        <template #default="{ row }">
          <el-tag :type="row.result === 'success' ? 'success' : 'danger'" size="small">
            {{ row.result === 'success' ? '成功' : '失败' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="robotResponse" label="响应" min-width="140">
        <template #default="{ row }">
          <span class="mono">{{ row.robotResponse || '--' }}</span>
        </template>
      </el-table-column>
    </el-table>
    <div v-if="logs.length === 0 && !loading" class="empty-state">暂无日志</div>
  </div>
</template>

<script setup lang="ts">
import type { OperationLog } from '@/types/log'
import { formatDateTime } from '@/utils/format'
import { OPERATION_TYPE_LABELS } from '@/utils/constants'

defineProps<{
  logs: OperationLog[]
  loading?: boolean
}>()

function getOperationTypeLabel(type: string): string {
  return OPERATION_TYPE_LABELS[type] ?? type
}
</script>

<style scoped lang="scss">
.log-table {
  height: 100%;
}
.mono { font-family: $font-family-mono; font-size: 11px; }
.empty-state {
  text-align: center;
  color: $color-text-muted;
  padding: $spacing-2xl;
}
</style>
