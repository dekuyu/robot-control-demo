<!-- 操作日志页面 -->
<template>
  <div class="log-page">
    <div class="page-header">
      <h3>操作日志</h3>
      <div class="header-actions">
        <el-button @click="exportLogs" :disabled="logStore.logs.length === 0">
          <el-icon><Download /></el-icon> 导出
        </el-button>
        <el-button @click="logStore.fetchLogs()" :loading="logStore.loading">
          <el-icon><Refresh /></el-icon> 刷新
        </el-button>
      </div>
    </div>

    <!-- 筛选 -->
    <div class="filters">
      <el-select v-model="filterResult" placeholder="操作结果" clearable @change="setFilter('result', $event)">
        <el-option label="成功" value="success" />
        <el-option label="失败" value="failure" />
      </el-select>
      <el-select v-model="filterType" placeholder="操作类型" clearable @change="setFilter('operation_type', $event)">
        <el-option v-for="(label, key) in OPERATION_TYPE_LABELS" :key="key" :label="label" :value="key" />
      </el-select>
      <el-button @click="logStore.clearFilters()">清除筛选</el-button>
    </div>

    <!-- 日志表格 -->
    <div class="panel log-panel">
      <LogTable :logs="logStore.logs" :loading="logStore.loading" />
    </div>

    <!-- 分页 -->
    <div class="pagination" v-if="logStore.total > logStore.pageSize">
      <el-pagination
        v-model:current-page="currentPage"
        :page-size="logStore.pageSize"
        :total="logStore.total"
        layout="prev, pager, next"
        @current-change="logStore.setPage"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useLogStore } from '@/stores/log'
import { exportCSV } from '@/utils/export'
import { OPERATION_TYPE_LABELS } from '@/utils/constants'
import LogTable from '@/components/common/LogTable.vue'

const logStore = useLogStore()
const filterResult = ref('')
const filterType = ref('')
const currentPage = ref(1)

function setFilter(key: string, value: unknown) {
  if (value === '' || value === undefined) {
    logStore.setFilter(key, undefined as any)
  } else {
    logStore.setFilter(key, value)
  }
}

function exportLogs() {
  const rows = logStore.logs.map(log => ({
    ID: log.id,
    时间: log.timestamp,
    用户: log.username,
    操作类型: OPERATION_TYPE_LABELS[log.operationType] ?? log.operationType,
    目标: log.target ?? '',
    结果: log.result,
    响应: log.robotResponse ?? '',
  }))
  exportCSV(rows, `操作日志_${new Date().toLocaleDateString()}`)
}

onMounted(() => logStore.fetchLogs())
</script>

<style scoped lang="scss">
.page-header {
  display: flex; justify-content: space-between; align-items: center; margin-bottom: $spacing-lg;
  h3 { margin: 0; color: $color-text-primary; font-size: 18px; }
  .header-actions { display: flex; gap: $spacing-sm; }
}
.filters { display: flex; gap: $spacing-sm; margin-bottom: $spacing-lg; }
.log-panel {
  background: $color-bg-card; border: 1px solid $color-border;
  border-radius: $radius-lg; padding: $spacing-lg; height: calc(100vh - 280px);
}
.pagination { display: flex; justify-content: center; margin-top: $spacing-lg; }
</style>
