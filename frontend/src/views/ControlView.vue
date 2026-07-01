<!-- 机械臂控制页面 -->
<template>
  <div class="control-page">
    <AlarmBanner
      :visible="alarmStore.hasActiveAlarm"
      :message="'存在活跃报警！'"
      :severity="'critical'"
      @close="alarmStore.setAlarmState(false)"
    />
    <div class="control-layout">
      <!-- 左侧：速度控制 -->
      <div class="panel speed-panel">
        <h4 class="section-title">速度控制</h4>
        <SpeedSlider v-model="speedPercent" :maxSpeed="maxSpeed" :disabled="!robotStore.servoOn" />
        <div class="actual-speed">
          <span>实际生效速度: </span>
          <strong>{{ controlStore.actualSpeed }}%</strong>
        </div>
        <el-button type="primary" plain class="save-speed-btn" @click="handleSetSpeed" :disabled="!robotStore.servoOn">
          应用速度设置
        </el-button>
      </div>

      <!-- 中间：关节控制 -->
      <div class="panel joint-panel">
        <h4 class="section-title">关节控制</h4>
        <AxisSlider
          v-for="axis in 6"
          :key="axis"
          :axis="axis"
          :value="getJointValue(axis)"
          :disabled="!robotStore.servoOn"
          @jogStart="handleJogStart"
          @jogStop="handleJogStop"
        />
      </div>

      <!-- 右侧：操作面板 -->
      <div class="panel-right">
        <div class="panel status-panel">
          <RobotStatusPanel />
        </div>
        <div class="panel estop-panel">
          <EmergencyStop :is-active="controlStore.isEstopActive" :disabled="!robotStore.connected" />
        </div>
        <div class="panel coord-panel">
          <h4 class="section-title">坐标系</h4>
          <EndCoordDisplay :endCoords="robotStore.endCoords" />
        </div>
      </div>
    </div>

    <!-- 确认对话框 -->
    <ConfirmDialog
      v-model="showServoConfirm"
      title="伺服上电确认"
      message="确认开启伺服？请确保工作区域安全。"
      type="warning"
      @confirm="confirmServoOn"
      @cancel="showServoConfirm = false"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { useRobotStore } from '@/stores/robot'
import { useAlarmStore } from '@/stores/alarm'
import { useControlStore } from '@/stores/control'
import { useAuthStore } from '@/stores/auth'
import { controlAPI } from '@/api/control'
import { getMaxSpeed } from '@/utils/permission'
import AlarmBanner from '@/components/common/AlarmBanner.vue'
import SpeedSlider from '@/components/common/SpeedSlider.vue'
import AxisSlider from '@/components/common/AxisSlider.vue'
import RobotStatusPanel from '@/components/common/RobotStatusPanel.vue'
import EndCoordDisplay from '@/components/common/EndCoordDisplay.vue'
import EmergencyStop from '@/components/common/EmergencyStop.vue'
import ConfirmDialog from '@/components/common/ConfirmDialog.vue'

const robotStore = useRobotStore()
const alarmStore = useAlarmStore()
const controlStore = useControlStore()
const authStore = useAuthStore()

const speedPercent = ref(30)
const showServoConfirm = ref(false)
const maxSpeed = computed(() => getMaxSpeed(authStore.userRole))

function getJointValue(axis: number): number {
  const key = `j${axis}` as keyof typeof robotStore.joints
  return robotStore.joints[key] ?? 0
}

async function handleJogStart(axis: number, direction: string) {
  await controlAPI.jogStart({ axis, direction, speedPercent: speedPercent.value })
}

async function handleJogStop(axis: number) {
  await controlAPI.jogStop(axis)
}

async function handleSetSpeed() {
  const res = await controlAPI.setSpeed(speedPercent.value)
  if (res.code === 0) {
    controlStore.setSpeed(speedPercent.value)
    ElMessage.success(`速度已设置为 ${speedPercent.value}%`)
  }
}

async function confirmServoOn() {
  const res = await controlAPI.servoOn()
  if (res.code === 0) { robotStore.servoOn = true; ElMessage.success('伺服已上电') }
  showServoConfirm.value = false
}
</script>

<style scoped lang="scss">
.control-layout {
  display: grid;
  grid-template-columns: 250px 1fr 280px;
  gap: $spacing-lg;
}
.panel {
  background: $color-bg-card;
  border: 1px solid $color-border;
  border-radius: $radius-lg;
  padding: $spacing-lg;
}
.panel-right {
  display: flex;
  flex-direction: column;
  gap: $spacing-lg;
}
.section-title {
  font-size: 14px;
  font-weight: 600;
  color: $color-text-primary;
  margin: 0 0 $spacing-md;
}
.actual-speed {
  margin: $spacing-sm 0;
  font-size: 13px;
  color: $color-text-secondary;
  strong { color: $color-info; font-family: $font-family-mono; }
}
.save-speed-btn { width: 100%; margin-top: $spacing-sm; }
.estop-panel {
  display: flex;
  justify-content: center;
}
</style>
