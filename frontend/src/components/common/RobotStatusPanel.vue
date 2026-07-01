<!-- 机器人状态面板组件 -->
<template>
  <div class="robot-status-panel">
    <h4 class="panel-title">机器人状态</h4>
    <div class="status-grid">
      <div class="status-row">
        <span class="key">连接状态</span>
        <span class="value">
          <el-tag :type="robot.connected ? 'success' : 'danger'" size="small">
            {{ robot.connected ? '已连接' : '未连接' }}
          </el-tag>
        </span>
      </div>
      <div class="status-row">
        <span class="key">伺服状态</span>
        <span class="value">
          <el-tag :type="robot.servoOn ? 'success' : 'info'" size="small">
            {{ robot.servoOn ? '已开启' : '已关闭' }}
          </el-tag>
        </span>
      </div>
      <div class="status-row">
        <span class="key">运行模式</span>
        <span class="value">{{ robot.modeLabel }}</span>
      </div>
      <div class="status-row">
        <span class="key">当前速度</span>
        <span class="value mono">{{ robot.speedPercent }}%</span>
      </div>
      <div class="status-row">
        <span class="key">报警状态</span>
        <span class="value">
          <el-tag :type="robot.alarmActive ? 'danger' : 'info'" size="small">
            {{ robot.alarmActive ? '报警中' : '正常' }}
          </el-tag>
        </span>
      </div>
      <div class="status-row" v-if="robot.executingProgram">
        <span class="key">执行程序</span>
        <span class="value mono">{{ robot.executingProgram }}</span>
      </div>
      <div class="status-row">
        <span class="key">最后更新</span>
        <span class="value mono small">{{ robot.lastUpdate ? formatDateTime(robot.lastUpdate) : '--' }}</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRobotStore } from '@/stores/robot'
import { formatDateTime } from '@/utils/format'

const robot = useRobotStore()
</script>

<style scoped lang="scss">
.panel-title {
  font-size: 14px;
  font-weight: 600;
  color: $color-text-primary;
  margin: 0 0 $spacing-md;
}
.status-grid {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.status-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.key {
  font-size: 13px;
  color: $color-text-secondary;
}
.value {
  font-size: 13px;
  color: $color-text-primary;
  &.mono { font-family: $font-family-mono; }
  &.small { font-size: 11px; color: $color-text-muted; }
}
</style>
