// ===== 用户管理 Store =====
import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { UserInfo } from '@/types/user'
import { userAPI } from '@/api/user'

export const useUserStore = defineStore('user', () => {
  const users = ref<UserInfo[]>([])
  const total = ref(0)
  const page = ref(1)
  const pageSize = ref(20)
  const loading = ref(false)
  const roleFilter = ref('')
  const editingUser = ref<UserInfo | null>(null)
  const showDialog = ref(false)

  async function fetchUsers() {
    loading.value = true
    try {
      const params: Record<string, unknown> = { page: page.value, pageSize: pageSize.value }
      if (roleFilter.value) params.role = roleFilter.value
      const res = await userAPI.list(params as { page?: number; pageSize?: number; role?: string })
      if (res.data) {
        users.value = res.data.items
        total.value = res.data.total
      }
    } finally {
      loading.value = false
    }
  }

  async function createUser(data: { username: string; password: string; role: string }) {
    const res = await userAPI.create(data)
    if (res.code === 0) await fetchUsers()
    return res
  }

  async function updateUser(id: number, data: { username?: string; role?: string; isActive?: boolean }) {
    const res = await userAPI.update(id, data)
    if (res.code === 0) await fetchUsers()
    return res
  }

  async function removeUser(id: number) {
    const res = await userAPI.remove(id)
    if (res.code === 0) await fetchUsers()
    return res
  }

  async function unlockUser(id: number) {
    const res = await userAPI.unlock(id)
    if (res.code === 0) await fetchUsers()
    return res
  }

  function setRoleFilter(role: string) {
    roleFilter.value = role
    page.value = 1
    fetchUsers()
  }

  function setPage(p: number) {
    page.value = p
    fetchUsers()
  }

  function openCreate() { editingUser.value = null; showDialog.value = true }
  function openEdit(user: UserInfo) { editingUser.value = user; showDialog.value = true }
  function closeDialog() { showDialog.value = false; editingUser.value = null }

  return {
    users, total, page, pageSize, loading, roleFilter, editingUser, showDialog,
    fetchUsers, createUser, updateUser, removeUser, unlockUser,
    setRoleFilter, setPage, openCreate, openEdit, closeDialog,
  }
})
