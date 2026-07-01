<!-- 连接状态指示灯组件 -->
<template>
  <div class="status-indicator">
    <div class="status-dots">
      <div class="status-item" :title="`连接: ${props.connected ? '已连接' : '未连接'}`">
        <span class="dot" :class="{ active: props.connected, error: !props.connected }"></span>
        <span class="label">连接</span>
      </div>
      <div class="status-item" :title="`伺服: ${props.servoOn ? '已开启' : '已关闭'}`">
        <span class="dot" :class="{ active: props.servoOn, warning: !props.servoOn }"></span>
        <span class="label">伺服</span>
      </div>
      <div class="status-item" :title="`模式: ${modeText}`">
        <span class="dot" :class="modeClass"></span>
        <span class="label">模式</span>
      </div>
      <div class="status-item" v-if="props.alarmActive" title="报警活跃">
        <span class="dot error pulse"></span>
        <span class="label">报警</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { RobotMode } from '@/types/robot'

const props = withDefaults(defineProps<{
  connected: boolean
  servoOn: boolean
  mode: RobotMode
  alarmActive?: boolean
}>(), { alarmActive: false })

const modeText = computed(() => {
  const map: Record<string, string> = {
    teaching: '示教', play: '再现', remote: '远程', idle: '空闲', error: '错误', unknown: '未知',
  }
  return map[props.mode] ?? props.mode
})

const modeClass = computed(() => {
  if (props.mode === 'teaching') return 'warning'
  if (props.mode === 'play') return 'active'
  if (props.mode === 'remote') return 'info'
  if (props.mode === 'error') return 'error'
  return ''
})
</script>

<style scoped lang="scss">
.status-indicator {
  display: flex;
  align-items: center;
}
.status-dots {
  display: flex;
  gap: $spacing-md;
}
.status-item {
  display: flex;
  align-items: center;
  gap: 6px;
  cursor: default;
}
.dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: $color-text-muted;
  transition: background $transition-fast;
  &.active { background: $color-success; }
  &.error { background: $color-danger; }
  &.warning { background: $color-warning; }
  &.info { background: $color-info; }
  &.pulse { animation: pulse 1.5s infinite; }
}
.label {
  font-size: 11px;
  color: $color-text-secondary;
}
@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.4; }
}
</style>
