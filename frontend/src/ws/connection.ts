// ===== WebSocket 连接管理 =====
import { ref } from 'vue'
import { WS_RECONNECT_INTERVAL, WS_MAX_RECONNECT } from '@/utils/constants'

type MessageHandler = (data: Record<string, unknown>) => void

class WSConnection {
  private ws: WebSocket | null = null
  private url: string = ''
  private token: string = ''
  private reconnectTimer: number | null = null
  private reconnectCount = 0
  private handlers: Map<string, MessageHandler[]> = new Map()
  private isManualClose = false

  connected = ref(false)

  /** 建立连接 */
  connect(url: string, token: string) {
    this.url = url
    this.token = token
    this.isManualClose = false
    this.doConnect()
  }

  private doConnect() {
    if (this.ws) {
      this.ws.close()
    }

    const wsUrl = `${this.url}?token=${this.token}`
    this.ws = new WebSocket(wsUrl)

    this.ws.onopen = () => {
      this.connected.value = true
      this.reconnectCount = 0
      // 启动心跳
      this.startHeartbeat()
    }

    this.ws.onmessage = (event) => {
      try {
        const msg = JSON.parse(event.data)
        this.dispatch(msg.type, msg.data ?? msg)
      } catch {
        // 忽略解析错误
      }
    }

    this.ws.onclose = () => {
      this.connected.value = false
      if (!this.isManualClose) {
        this.scheduleReconnect()
      }
    }

    this.ws.onerror = () => {
      // 由 onclose 处理
    }
  }

  /** 断开连接 */
  disconnect() {
    this.isManualClose = true
    this.clearReconnectTimer()
    this.clearHeartbeat()
    if (this.ws) {
      this.ws.close()
      this.ws = null
    }
    this.connected.value = false
  }

  /** 注册消息处理器 */
  on(type: string, handler: MessageHandler) {
    if (!this.handlers.has(type)) {
      this.handlers.set(type, [])
    }
    this.handlers.get(type)!.push(handler)
  }

  /** 移除消息处理器 */
  off(type: string, handler: MessageHandler) {
    const handlers = this.handlers.get(type)
    if (handlers) {
      const idx = handlers.indexOf(handler)
      if (idx >= 0) handlers.splice(idx, 1)
    }
  }

  /** 发送消息 */
  send(data: unknown) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(data))
    }
  }

  /** 分发消息到对应处理器 */
  private dispatch(type: string, data: Record<string, unknown>) {
    const handlers = this.handlers.get(type)
    if (handlers) {
      handlers.forEach(h => h(data))
    }
  }

  /** 自动重连 */
  private scheduleReconnect() {
    if (this.reconnectCount >= WS_MAX_RECONNECT) return
    this.reconnectTimer = window.setTimeout(() => {
      this.reconnectCount++
      this.doConnect()
    }, WS_RECONNECT_INTERVAL)
  }

  /** 心跳 */
  private heartbeatTimer: number | null = null
  private startHeartbeat() {
    this.heartbeatTimer = window.setInterval(() => {
      this.send('ping')
    }, 30000)
  }
  private clearHeartbeat() {
    if (this.heartbeatTimer) {
      clearInterval(this.heartbeatTimer)
      this.heartbeatTimer = null
    }
  }
  private clearReconnectTimer() {
    if (this.reconnectTimer) {
      clearTimeout(this.reconnectTimer)
      this.reconnectTimer = null
    }
  }
}

/** 全局 WebSocket 连接实例 */
export const wsConnection = new WSConnection()
