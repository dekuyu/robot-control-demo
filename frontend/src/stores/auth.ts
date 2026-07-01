// ===== 认证状态 Store =====
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { UserInfo, UserRole } from '@/types/user'
import { authAPI } from '@/api/auth'
import router from '@/router'

export const useAuthStore = defineStore('auth', () => {
  const user = ref<UserInfo | null>(null)
  const accessToken = ref<string | null>(localStorage.getItem('accessToken'))
  const refreshToken = ref<string | null>(localStorage.getItem('refreshToken'))

  const isLoggedIn = computed(() => !!accessToken.value && !!user.value)
  const userRole = computed<UserRole>(() => user.value?.role ?? 'observer')
  const isAdmin = computed(() => userRole.value === 'admin')

  async function login(username: string, password: string) {
    const res = await authAPI.login({ username, password })
    if (res.data) {
      const { accessToken: at, refreshToken: rt, user: u } = res.data
      accessToken.value = at
      refreshToken.value = rt
      user.value = {
        id: u.id,
        username: u.username,
        role: u.role as UserRole,
        isActive: u.isActive,
        isLocked: u.isLocked,
        lastLogin: u.lastLogin,
        createdAt: u.createdAt,
      }
      localStorage.setItem('accessToken', at)
      localStorage.setItem('refreshToken', rt)
    }
    return res
  }

  async function logout() {
    try { await authAPI.logout() } catch { /* ignore */ }
    clearAuth()
    router.push('/login')
  }

  function clearAuth() {
    user.value = null
    accessToken.value = null
    refreshToken.value = null
    localStorage.removeItem('accessToken')
    localStorage.removeItem('refreshToken')
  }

  async function fetchCurrentUser() {
    const res = await authAPI.getMe()
    if (res.data) {
      const u = res.data
      user.value = {
        id: u.id,
        username: u.username,
        role: u.role as UserRole,
        isActive: u.isActive,
        isLocked: u.isLocked,
        lastLogin: u.lastLogin,
        createdAt: u.createdAt,
      }
    }
  }

  return { user, accessToken, refreshToken, isLoggedIn, userRole, isAdmin,
    login, logout, clearAuth, fetchCurrentUser }
})
