// ===== Axios 实例 + 拦截器 =====
import axios from 'axios'
import type { AxiosInstance, AxiosRequestConfig } from 'axios'
import { useAuthStore } from '@/stores/auth'

const baseURL = import.meta.env.VITE_API_BASE_URL || ''

/** 创建通用 Axios 实例 */
const client: AxiosInstance = axios.create({
  baseURL,
  timeout: 15000,
  headers: { 'Content-Type': 'application/json' },
})

// 请求拦截器：注入 JWT Token
client.interceptors.request.use((config) => {
  const authStore = useAuthStore()
  if (authStore.accessToken) {
    config.headers.Authorization = `Bearer ${authStore.accessToken}`
  }
  return config
})

// 响应拦截器：错误统一处理
client.interceptors.response.use(
  (response) => response.data,
  (error) => {
    if (error.response?.status === 401) {
      const authStore = useAuthStore()
      authStore.clearAuth()
      window.location.href = '/login'
    }
    return Promise.reject(error)
  },
)

/** 通用 GET 请求 */
export async function get<T = unknown>(url: string, params?: Record<string, unknown>): Promise<{ code: number; data: T | null; message?: string }> {
  return client.get(url, { params }) as Promise<{ code: number; data: T | null; message?: string }>
}

/** 通用 POST 请求 */
export async function post<T = unknown>(url: string, data?: unknown): Promise<{ code: number; data: T | null; message?: string }> {
  return client.post(url, data) as Promise<{ code: number; data: T | null; message?: string }>
}

/** 通用 PUT 请求 */
export async function put<T = unknown>(url: string, data?: unknown): Promise<{ code: number; data: T | null; message?: string }> {
  return client.put(url, data) as Promise<{ code: number; data: T | null; message?: string }>
}

/** 通用 DELETE 请求 */
export async function del<T = unknown>(url: string): Promise<{ code: number; data: T | null; message?: string }> {
  return client.delete(url) as Promise<{ code: number; data: T | null; message?: string }>
}

export default client
