// ===== 操作日志 Store =====
import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { OperationLog } from '@/types/log'
import { logAPI } from '@/api/log'

export const useLogStore = defineStore('log', () => {
  const logs = ref<OperationLog[]>([])
  const total = ref(0)
  const page = ref(1)
  const pageSize = ref(50)
  const loading = ref(false)
  const stats = ref<Record<string, unknown>>({})
  const filters = ref<Record<string, unknown>>({})

  async function fetchLogs() {
    loading.value = true
    try {
      const params: Record<string, unknown> = {
        page: page.value,
        page_size: pageSize.value,
        ...filters.value,
      }
      const res = await logAPI.query(params)
      if (res.data) {
        logs.value = res.data.items
        total.value = res.data.total
      }
    } finally {
      loading.value = false
    }
  }

  async function fetchStats(startTime?: string, endTime?: string) {
    const res = await logAPI.getStats({ startTime, endTime })
    if (res.data) stats.value = res.data as Record<string, unknown>
    return res
  }

  function setFilter(key: string, value: unknown) {
    filters.value[key] = value
    page.value = 1
    fetchLogs()
  }

  function clearFilters() {
    filters.value = {}
    page.value = 1
    fetchLogs()
  }

  function setPage(p: number) {
    page.value = p
    fetchLogs()
  }

  return {
    logs, total, page, pageSize, loading, stats, filters,
    fetchLogs, fetchStats, setFilter, clearFilters, setPage,
  }
})
