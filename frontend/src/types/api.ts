// ===== 通用 API 响应结构 =====

/** API 通用响应 */
interface ApiResponse<T = unknown> {
  code: number
  message: string | null
  data: T | null
}

/** 分页数据 */
interface PaginatedData<T> {
  items: T[]
  total: number
  page: number
  pageSize: number
}

export type { ApiResponse, PaginatedData }
