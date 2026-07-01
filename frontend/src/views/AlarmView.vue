<!-- 报警管理页面 -->
<template>
  <div class="alarm-page">
    <div class="page-header">
      <h3>报警管理</h3>
      <div class="header-actions">
        <el-button @click="fetchAlarms" :loading="loading">
          <el-icon><Refresh /></el-icon> 刷新
        </el-button>
        <el-button type="danger" plain @click="handleResetAll" :disabled="activeAlarmCount === 0">
          <el-icon><Bell /></el-icon> 全部复位
        </el-button>
      </div>
    </div>

    <!-- 活跃报警横幅 -->
    <AlarmBanner
      :visible="activeAlarmCount > 0"
      :message="`${activeAlarmCount} 个活跃报警需要处理`"
      :severity="highestSeverity"
    />

    <!-- 筛选 -->
    <div class="filters">
      <el-select v-model="filterLevel" placeholder="报警级别" clearable @change="applyFilter">
        <el-option label="严重" value="critical" />
        <el-option label="警告" value="warning" />
        <el-option label="信息" value="info" />
      </el-select>
      <el-select v-model="filterActive" placeholder="状态" clearable @change="applyFilter">
        <el-option label="活跃" :value="true" />
        <el-option label="已清除" :value="false" />
      </el-select>
    </div>

    <!-- 报警列表 -->
    <div class="panel">
      <el-table :data="alarms" v-loading="loading" stripe size="small">
        <el-table-column type="index" width="50" label="#" />
        <el-table-column prop="alarmCode" label="报警代码" width="120">
          <template #default="{ row }">
            <span class="mono alarm-code" :class="row.alarmLevel">{{ row.alarmCode }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="alarmLevel" label="级别" width="80">
          <template #default="{ row }">
            <el-tag :type="levelTagType(row.alarmLevel)" size="small">
              {{ levelLabel(row.alarmLevel) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="description" label="描述" min-width="160" />
        <el-table-column label="状态" width="80">
          <template #default="{ row }">
            <el-tag :type="row.isActive ? 'danger' : 'success'" size="small">
              {{ row.isActive ? '活跃' : '已清除' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="occurredAt" label="发生时间" width="160">
          <template #default="{ row }">{{ formatDateTime(row.occurredAt) }}</template>
        </el-table-column>
        <el-table-column label="清除时间" width="160">
          <template #default="{ row }">
            {{ row.clearedAt ? formatDateTime(row.clearedAt) : '--' }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="80" fixed="right">
          <template #default="{ row }">
            <el-button
              v-if="row.isActive"
              type="primary"
              size="small"
              text
              @click="handleResetOne(row)"
            >复位</el-button>
          </template>
        </el-table-column>
      </el-table>
      <div v-if="!loading && alarms.length === 0" class="empty-state">暂无报警记录</div>
    </div>

    <!-- 分页 -->
    <div class="pagination" v-if="total > pageSize">
      <el-pagination
        v-model:current-page="page"
        :page-size="pageSize"
        :total="total"
        layout="prev, pager, next"
        @current-change="fetchAlarms"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import type { AlarmInfo, AlarmLevel } from '@/types/alarm'
import { alarmAPI } from '@/api/alarm'
import { formatDateTime } from '@/utils/format'
import AlarmBanner from '@/components/common/AlarmBanner.vue'

const alarms = ref<AlarmInfo[]>([])
const total = ref(0)
const page = ref(1)
const pageSize = ref(20)
const loading = ref(false)
const filterLevel = ref('')
const filterActive = ref<boolean | ''>('')

const activeAlarmCount = computed(() => alarms.value.filter(a => a.isActive).length)

const highestSeverity = computed<'critical' | 'warning' | 'info'>(() => {
  if (alarms.value.some(a => a.isActive && a.alarmLevel === 'critical')) return 'critical'
  if (alarms.value.some(a => a.isActive && a.alarmLevel === 'warning')) return 'warning'
  return 'info'
})

function levelLabel(level: AlarmLevel): string {
  return { critical: '严重', warning: '警告', info: '信息' }[level] ?? level
}

function levelTagType(level: AlarmLevel): string {
  return { critical: 'danger', warning: 'warning', info: 'info' }[level] ?? 'info'
}

async function fetchAlarms() {
  loading.value = true
  try {
    const params: Record<string, unknown> = { page: page.value, pageSize: pageSize.value }
    if (filterLevel.value) params.level = filterLevel.value
    if (filterActive.value !== '') params.isActive = filterActive.value
    const res = await alarmAPI.list(params as any)
    if (res.data) { alarms.value = res.data.items; total.value = res.data.total }
  } finally { loading.value = false }
}

async function handleResetOne(alarm: AlarmInfo) {
  const res = await alarmAPI.reset(alarm.id)
  if (res.code === 0) { ElMessage.success('报警已复位'); fetchAlarms() }
}

async function handleResetAll() {
  const res = await alarmAPI.reset()
  if (res.code === 0) { ElMessage.success('所有报警已复位'); fetchAlarms() }
}

function applyFilter() { page.value = 1; fetchAlarms() }

onMounted(fetchAlarms)
</script>

<style scoped lang="scss">
.page-header {
  display: flex; justify-content: space-between; align-items: center; margin-bottom: $spacing-lg;
  h3 { margin: 0; color: $color-text-primary; font-size: 18px; }
  .header-actions { display: flex; gap: $spacing-sm; }
}
.filters { display: flex; gap: $spacing-sm; margin-bottom: $spacing-lg; }
.panel {
  background: $color-bg-card; border: 1px solid $color-border;
  border-radius: $radius-lg; padding: $spacing-lg;
}
.mono { font-family: $font-family-mono; }
.alarm-code {
  &.critical { color: $color-danger; font-weight: 700; }
  &.warning { color: $color-warning; }
}
.empty-state { text-align: center; color: $color-text-muted; padding: $spacing-2xl; }
.pagination { display: flex; justify-content: center; margin-top: $spacing-lg; }
</style>
