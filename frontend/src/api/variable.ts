// ===== 变量读写 API =====
import { get, put, post } from './client'
import type { VariableData, IOSignal } from '@/types/variable'

export const variableAPI = {
  /** 读取 B 变量 */
  readB(idx: number) { return get<VariableData>(`/api/variables/b/${idx}`) },
  /** 写入 B 变量 */
  writeB(idx: number, value: number) {
    return put<VariableData>(`/api/variables/b/${idx}`, { value })
  },
  /** 批量读取 B 变量 */
  batchReadB(indices: number[]) {
    return post<{ values: VariableData[] }>('/api/variables/b/batch', { var_type: 'B', indices })
  },
  /** 读取 IO */
  readIO(idx: number) { return get<IOSignal>(`/api/variables/io/${idx}`) },
  /** 写入 IO */
  writeIO(idx: number, value: number) {
    return put(`/api/variables/io/${idx}`, { value })
  },
  /** 读取 I 变量 */
  readI(idx: number) { return get<VariableData>(`/api/variables/i/${idx}`) },
  /** 读取 D 变量 */
  readD(idx: number) { return get<VariableData>(`/api/variables/d/${idx}`) },
  /** 写入 D 变量 */
  writeD(idx: number, value: number) {
    return put<VariableData>(`/api/variables/d/${idx}`, { value })
  },
}
