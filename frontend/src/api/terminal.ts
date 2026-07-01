// ===== UDP/串口调试终端 API =====
import { get, post } from './client'

export const terminalAPI = {
  /** 发送十六进制报文 */
  send(data: { hexData: string; waitResponse?: boolean }) {
    return post<{ sentHex: string; responseHex: string; responseTimeMs: number }>(
      '/api/terminal/send', { hex_data: data.hexData, wait_response: data.waitResponse ?? true }
    )
  },
  /** 获取终端统计 */
  getStats() {
    return get<{ bytesSent: number; bytesReceived: number; packetsSent: number; packetsReceived: number }>(
      '/api/terminal/stats'
    )
  },
  /** 获取命令模板 */
  getTemplates() {
    return get<{ name: string; description: string; command: string }[]>('/api/terminal/templates')
  },
  /** 查询报文日志 */
  queryPacketLogs(params?: Record<string, unknown>) {
    return get('/api/terminal/packet-logs', params)
  },
}
