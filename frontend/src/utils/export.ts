// ===== 数据导出工具 =====
import { saveAs } from 'file-saver'

/**
 * 导出 JSON 文件
 */
export function exportJSON(data: unknown, filename: string): void {
  const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' })
  saveAs(blob, `${filename}.json`)
}

/**
 * 导出 CSV 文件
 */
export function exportCSV(rows: Record<string, unknown>[], filename: string): void {
  if (rows.length === 0) return

  const headers = Object.keys(rows[0])
  const csvContent = [
    headers.join(','),
    ...rows.map(row =>
      headers.map(h => {
        const val = row[h]
        if (val == null) return ''
        const str = String(val)
        return str.includes(',') || str.includes('"') ? `"${str.replace(/"/g, '""')}"` : str
      }).join(',')
    ),
  ].join('\n')

  const blob = new Blob(['\uFEFF' + csvContent], { type: 'text/csv;charset=utf-8' })
  saveAs(blob, `${filename}.csv`)
}

/**
 * 下载 Blob 文件
 */
export function downloadFile(blob: Blob, filename: string): void {
  saveAs(blob, filename)
}
