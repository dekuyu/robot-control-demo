<!-- UDP 调试终端组件 -->
<template>
  <div class="udp-terminal">
    <div class="terminal-output" ref="outputRef">
      <div v-for="(entry, i) in entries" :key="i" class="terminal-line" :class="entry.type">
        <span class="ts">[{{ entry.time }}]</span>
        <span class="dir">{{ entry.direction }}</span>
        <span class="hex">{{ entry.data }}</span>
      </div>
      <div v-if="entries.length === 0" class="empty-state">
        <el-icon :size="32"><Connection /></el-icon>
        <p>等待收发数据...</p>
      </div>
    </div>
    <div class="terminal-input">
      <el-input
        v-model="inputHex"
        placeholder="输入十六进制报文，如: A5 01 02 03 ..."
        @keyup.enter="handleSend"
        :disabled="sending"
      >
        <template #append>
          <el-button @click="handleSend" :loading="sending" :disabled="sending">
            <el-icon><Promotion /></el-icon> 发送
          </el-button>
        </template>
      </el-input>
    </div>
    <div class="terminal-actions">
      <el-button size="small" @click="entries = []">
        <el-icon><Delete /></el-icon> 清屏
      </el-button>
      <span class="stats">
        发送: {{ stats.sent }} | 接收: {{ stats.recv }}
      </span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, nextTick, watch } from 'vue'
import { terminalAPI } from '@/api/terminal'
import { formatTime } from '@/utils/format'

interface LogEntry {
  time: string
  direction: string
  data: string
  type: 'send' | 'recv' | 'error'
}

const entries = ref<LogEntry[]>([])
const inputHex = ref('')
const sending = ref(false)
const outputRef = ref<HTMLElement | null>(null)
const stats = ref({ sent: 0, recv: 0 })

async function handleSend() {
  const hex = inputHex.value.trim()
  if (!hex) return
  sending.value = true
  const time = formatTime(new Date())
  try {
    entries.value.push({ time, direction: '>>', data: hex, type: 'send' })
    stats.value.sent++
    const res = await terminalAPI.send({ hexData: hex.replace(/\s/g, '') })
    if (res.data) {
      entries.value.push({
        time: formatTime(new Date()),
        direction: '<<',
        data: res.data.responseHex || '',
        type: 'recv',
      })
      stats.value.recv++
    }
  } catch (e: any) {
    entries.value.push({
      time: formatTime(new Date()),
      direction: '!!',
      data: e?.message || '发送失败',
      type: 'error',
    })
  } finally {
    sending.value = false
    inputHex.value = ''
    await nextTick()
    scrollToBottom()
  }
}

function scrollToBottom() {
  if (outputRef.value) {
    outputRef.value.scrollTop = outputRef.value.scrollHeight
  }
}

// 尝试获取统计
terminalAPI.getStats().then(res => {
  if (res.data) stats.value = { sent: res.data.packetsSent, recv: res.data.packetsReceived }
}).catch(() => {})
</script>

<style scoped lang="scss">
.udp-terminal {
  display: flex;
  flex-direction: column;
  height: 100%;
  background: $color-bg-input;
  border: 1px solid $color-border;
  border-radius: $radius-lg;
  overflow: hidden;
}
.terminal-output {
  flex: 1;
  overflow-y: auto;
  padding: $spacing-md;
  min-height: 200px;
  font-family: $font-family-mono;
  font-size: 12px;
  line-height: 1.8;
}
.terminal-line {
  display: flex;
  gap: $spacing-sm;
  &.send .hex { color: $color-send; }
  &.recv .hex { color: $color-receive; }
  &.error .hex { color: $color-danger; }
}
.ts { color: $color-text-muted; }
.dir { color: $color-text-secondary; font-weight: 700; }
.hex { word-break: break-all; }
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: $color-text-muted;
  p { margin-top: $spacing-sm; font-size: 13px; }
}
.terminal-input {
  padding: $spacing-sm $spacing-md;
  border-top: 1px solid $color-border;
}
.terminal-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: $spacing-xs $spacing-md $spacing-sm;
}
.stats {
  font-size: 11px;
  color: $color-text-muted;
  font-family: $font-family-mono;
}
</style>
