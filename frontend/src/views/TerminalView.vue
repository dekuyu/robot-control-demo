<!-- 调试终端页面 -->
<template>
  <div class="terminal-page">
    <div class="page-header">
      <h3>UDP 调试终端</h3>
      <div class="header-actions">
        <el-button size="small" @click="fetchTemplates">
          <el-icon><Collection /></el-icon> 命令模板
        </el-button>
      </div>
    </div>

    <div class="terminal-layout">
      <!-- 左侧：终端 -->
      <div class="terminal-main">
        <UdpTerminal />
      </div>

      <!-- 右侧：模板 + 统计 -->
      <div class="terminal-side">
        <div class="panel">
          <h4 class="panel-title">命令模板</h4>
          <div class="template-list">
            <div
              v-for="tpl in templates"
              :key="tpl.name"
              class="template-item"
              @click="applyTemplate(tpl.command)"
            >
              <span class="tpl-name">{{ tpl.name }}</span>
              <span class="tpl-desc">{{ tpl.description }}</span>
              <span class="tpl-cmd mono">{{ tpl.command }}</span>
            </div>
            <div v-if="templates.length === 0" class="empty">暂无模板</div>
          </div>
        </div>

        <div class="panel">
          <h4 class="panel-title">常用指令</h4>
          <div class="quick-commands">
            <el-tag
              v-for="cmd in quickCommands"
              :key="cmd.label"
              @click="applyTemplate(cmd.hex)"
              class="cmd-tag"
            >
              {{ cmd.label }}
            </el-tag>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { terminalAPI } from '@/api/terminal'
import UdpTerminal from '@/components/common/UdpTerminal.vue'

interface Template {
  name: string
  description: string
  command: string
}

const templates = ref<Template[]>([])

const quickCommands = [
  { label: '状态读取', hex: 'A5 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 A5' },
  { label: '报警读取', hex: 'A5 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 A6' },
  { label: '位置读取', hex: 'A5 02 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 A7' },
]

function applyTemplate(cmd: string) {
  // 向终端输入框赋值 - 通过触发自定义事件
  const inputEl = document.querySelector('.terminal-input input') as HTMLInputElement
  if (inputEl) {
    inputEl.value = cmd
    inputEl.dispatchEvent(new Event('input', { bubbles: true }))
  }
}

async function fetchTemplates() {
  const res = await terminalAPI.getTemplates()
  if (res.data) templates.value = res.data
}
</script>

<style scoped lang="scss">
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: $spacing-lg;
  h3 { margin: 0; color: $color-text-primary; font-size: 18px; }
}
.terminal-layout {
  display: grid;
  grid-template-columns: 1fr 280px;
  gap: $spacing-lg;
  height: calc(100vh - 160px);
}
.terminal-main { overflow: hidden; }
.panel {
  background: $color-bg-card;
  border: 1px solid $color-border;
  border-radius: $radius-lg;
  padding: $spacing-md;
  margin-bottom: $spacing-md;
}
.panel-title {
  font-size: 13px;
  font-weight: 600;
  color: $color-text-primary;
  margin: 0 0 $spacing-sm;
}
.template-item {
  padding: $spacing-sm;
  cursor: pointer;
  border-radius: $radius-sm;
  transition: background $transition-fast;
  &:hover { background: rgba($color-info, 0.1); }
}
.tpl-name {
  display: block;
  font-size: 12px;
  color: $color-text-primary;
  font-weight: 500;
}
.tpl-desc {
  display: block;
  font-size: 11px;
  color: $color-text-muted;
  margin: 2px 0;
}
.tpl-cmd {
  display: block;
  font-size: 10px;
  color: $color-info;
  word-break: break-all;
}
.mono { font-family: $font-family-mono; }
.empty { text-align: center; color: $color-text-muted; font-size: 12px; padding: $spacing-md; }
.quick-commands { display: flex; flex-wrap: wrap; gap: 6px; }
.cmd-tag { cursor: pointer; }
</style>
