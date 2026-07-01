<!-- 仪表盘页面 -->
<template>
  <div class="dashboard-page">
    <AlarmBanner
      :visible="alarmStore.hasActiveAlarm"
      :message="'存在活跃报警，请及时处理！'"
      :severity="'critical'"
      @close="alarmStore.setAlarmState(false)"
    />
    <div class="dashboard-grid">
      <!-- 左侧：机器人状态 -->
      <div class="panel">
        <RobotStatusPanel />
      </div>
      <!-- 右侧上：关节 + 坐标 -->
      <div class="panel">
        <div class="panel-grid">
          <JointAngleDisplay :joints="robotStore.joints" />
          <EndCoordDisplay :endCoords="robotStore.endCoords" />
        </div>
      </div>
      <!-- 右侧下：力矩 + 连接 -->
      <div class="panel">
        <div class="panel-grid">
          <TorqueDisplay :torques="robotStore.torques" />
          <ConnectionPanel />
        </div>
      </div>
      <!-- 急停按钮 -->
      <div class="panel panel-center">
        <EmergencyStop :is-active="controlStore.isEstopActive" />
      </div>
      <!-- 快速操作 -->
      <div class="panel">
        <h4 class="panel-title">快速操作</h4>
        <div class="quick-actions">
          <el-button type="success" @click="handleServoOn" :disabled="!robotStore.connected || robotStore.servoOn">
            <el-icon><VideoPlay /></el-icon> 伺服上电
          </el-button>
          <el-button type="danger" @click="handleServoOff" :disabled="!robotStore.servoOn">
            <el-icon><VideoPause /></el-icon> 伺服断电
          </el-button>
          <el-button type="primary" plain @click="handleProgramStart">
            <el-icon><CaretRight /></el-icon> 启动程序
          </el-button>
          <el-button type="warning" plain @click="handleProgramStop">
            <el-icon><Close /></el-icon> 停止程序
          </el-button>
          <el-button @click="handleAlarmReset" :disabled="!robotStore.alarmActive">
            <el-icon><Refresh /></el-icon> 报警复位
          </el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ElMessage } from 'element-plus'
import { useRobotStore } from '@/stores/robot'
import { useAlarmStore } from '@/stores/alarm'
import { useConnectionStore } from '@/stores/connection'
import { useControlStore } from '@/stores/control'
import { controlAPI } from '@/api/control'
import AlarmBanner from '@/components/common/AlarmBanner.vue'
import RobotStatusPanel from '@/components/common/RobotStatusPanel.vue'
import JointAngleDisplay from '@/components/common/JointAngleDisplay.vue'
import EndCoordDisplay from '@/components/common/EndCoordDisplay.vue'
import TorqueDisplay from '@/components/common/TorqueDisplay.vue'
import EmergencyStop from '@/components/common/EmergencyStop.vue'

const robotStore = useRobotStore()
const alarmStore = useAlarmStore()
const connectionStore = useConnectionStore()
const controlStore = useControlStore()

async function handleServoOn() {
  const res = await controlAPI.servoOn()
  if (res.code === 0) { robotStore.servoOn = true; ElMessage.success('伺服已上电') }
}
async function handleServoOff() {
  const res = await controlAPI.servoOff()
  if (res.code === 0) { robotStore.servoOn = false; ElMessage.success('伺服已断电') }
}
async function handleProgramStart() {
  const res = await controlAPI.programStart()
  if (res.code === 0) ElMessage.success('程序已启动')
}
async function handleProgramStop() {
  const res = await controlAPI.programStop()
  if (res.code === 0) ElMessage.success('程序已停止')
}
async function handleAlarmReset() {
  const res = await controlAPI.alarmReset()
  if (res.code === 0) { robotStore.alarmActive = false; ElMessage.success('报警已复位') }
}
</script>

<script lang="ts">
import { defineComponent, h } from 'vue'

// 连接面板内联组件
const ConnectionPanel = defineComponent({
  setup() {
    const conn = useConnectionStore()
    const robot = useRobotStore()
    return () => h('div', { class: 'connection-panel' }, [
      h('h4', { class: 'panel-title' }, '连接状态'),
      h('div', { class: 'conn-info' }, [
        h('span', { class: 'conn-label' }, 'IP:'),
        h('span', { class: 'conn-value mono' }, conn.robotIP),
      ]),
      h('div', { class: 'conn-info' }, [
        h('span', { class: 'conn-label' }, '端口:'),
        h('span', { class: 'conn-value mono' }, String(conn.robotPort)),
      ]),
      h('el-button', {
        type: conn.isConnected ? 'danger' : 'success',
        size: 'small',
        loading: conn.isConnecting,
        onClick: () => conn.isConnected ? conn.disconnect() : conn.connect(),
      }, conn.isConnected ? '断开连接' : '连接机器人'),
    ])
  },
})
</script>

<style scoped lang="scss">
.dashboard-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: $spacing-lg;
}
.panel {
  background: $color-bg-card;
  border: 1px solid $color-border;
  border-radius: $radius-lg;
  padding: $spacing-lg;
}
.panel-center {
  display: flex;
  justify-content: center;
  align-items: center;
}
.panel-title {
  font-size: 14px;
  font-weight: 600;
  color: $color-text-primary;
  margin: 0 0 $spacing-md;
}
.panel-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: $spacing-lg;
}
.quick-actions {
  display: flex;
  flex-wrap: wrap;
  gap: $spacing-sm;
}
.conn-info {
  display: flex;
  justify-content: space-between;
  padding: 4px 0;
  font-size: 13px;
  .conn-label { color: $color-text-secondary; }
  .conn-value { color: $color-text-primary; }
}
.mono { font-family: $font-family-mono; }
</style>
