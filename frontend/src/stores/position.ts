// ===== 坐标位置 Store =====
import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { SavedPosition, PositionPosture } from '@/types/position'
import { positionAPI } from '@/api/position'

export const usePositionStore = defineStore('position', () => {
  const positions = ref<SavedPosition[]>([])
  const total = ref(0)
  const page = ref(1)
  const pageSize = ref(20)
  const loading = ref(false)
  const searchKeyword = ref('')
  const currentPosture = ref<PositionPosture | null>(null)
  const editingPosition = ref<SavedPosition | null>(null)
  const showCreateDialog = ref(false)

  async function fetchPositions() {
    loading.value = true
    try {
      const params: Record<string, unknown> = { page: page.value, pageSize: pageSize.value }
      if (searchKeyword.value) params.search = searchKeyword.value
      const res = await positionAPI.list(params as { page?: number; pageSize?: number; search?: string })
      if (res.data) {
        positions.value = res.data.items
        total.value = res.data.total
      }
    } finally {
      loading.value = false
    }
  }

  async function createPosition(data: { name: string; description?: string; posture: PositionPosture }) {
    const res = await positionAPI.create(data)
    if (res.code === 0) await fetchPositions()
    return res
  }

  async function updatePosition(id: number, data: { name?: string; description?: string }) {
    const res = await positionAPI.update(id, data)
    if (res.code === 0) await fetchPositions()
    return res
  }

  async function removePosition(id: number) {
    const res = await positionAPI.remove(id)
    if (res.code === 0) await fetchPositions()
    return res
  }

  async function fetchCurrentPosture() {
    const res = await positionAPI.getCurrent()
    if (res.data) currentPosture.value = res.data
    return res
  }

  async function readPVariable(index: number) {
    return positionAPI.readPVar(index)
  }

  async function writePVariable(index: number, posture: PositionPosture) {
    return positionAPI.writePVar(index, posture)
  }

  function setSearchKeyword(keyword: string) {
    searchKeyword.value = keyword
    page.value = 1
  }

  function setPage(p: number) {
    page.value = p
    fetchPositions()
  }

  function openCreate() { editingPosition.value = null; showCreateDialog.value = true }
  function openEdit(pos: SavedPosition) { editingPosition.value = pos; showCreateDialog.value = true }
  function closeCreate() { showCreateDialog.value = false; editingPosition.value = null }

  return {
    positions, total, page, pageSize, loading, searchKeyword,
    currentPosture, editingPosition, showCreateDialog,
    fetchPositions, createPosition, updatePosition, removePosition,
    fetchCurrentPosture, readPVariable, writePVariable,
    setSearchKeyword, setPage, openCreate, openEdit, closeCreate,
  }
})
