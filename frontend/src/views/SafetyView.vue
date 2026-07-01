<!-- 安全配置页面 -->
<template>
  <div class="safety-page">
    <div class="page-header">
      <h3>安全配置</h3>
      <el-button @click="handleCheck" :loading="checkLoading">
        <el-icon><Refresh /></el-icon> 执行安全检查
      </el-button>
    </div>

    <!-- 检查结果 -->
    <SafetyBanner v-if="checkResult" :check-result="checkResult" />

    <div class="safety-grid">
      <!-- 速度限制 -->
      <div class="panel">
        <h4 class="panel-title">速度限制配置</h4>
        <el-form label-width="120px" size="small">
          <el-form-item label="最大速度百分比">
            <el-input-number v-model="speedForm.maxSpeedPercent" :min="1" :max="100" />
          </el-form-item>
          <el-form-item label="需要操作确认">
            <el-switch v-model="speedForm.requireConfirm" />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="saveSpeedConfig" :loading="savingSpeed">
              保存速度配置
            </el-button>
          </el-form-item>
        </el-form>
      </div>

      <!-- 轴限位 -->
      <div class="panel">
        <h4 class="panel-title">软件限位配置</h4>
        <div v-for="axis in 6" :key="axis" class="limit-row">
          <span class="limit-label">{{ axisNames[axis] }}</span>
          <el-input-number
            v-model="limits[`j${axis}`].min"
            :min="-360"
            :max="360"
            size="small"
            controls-position="right"
            placeholder="最小值"
          />
          <span class="limit-sep">~</span>
          <el-input-number
            v-model="limits[`j${axis}`].max"
            :min="-360"
            :max="360"
            size="small"
            controls-position="right"
            placeholder="最大值"
          />
        </div>
        <el-button type="primary" class="save-limits-btn" @click="saveLimits" :loading="savingLimits">
          保存限位配置
        </el-button>
      </div>

      <!-- 急停 -->
      <div class="panel estop-panel">
        <h4 class="panel-title">紧急停止</h4>
        <EmergencyStop />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { safetyAPI } from '@/api/safety'
import type { SafetyCheckResult } from '@/types/safety'
import { AXIS_NAMES } from '@/utils/constants'
import { getDefaultAxisLimits } from '@/utils/safety'
import SafetyBanner from '@/components/common/SafetyBanner.vue'
import EmergencyStop from '@/components/common/EmergencyStop.vue'

const checkResult = ref<SafetyCheckResult | null>(null)
const checkLoading = ref(false)
const savingSpeed = ref(false)
const savingLimits = ref(false)

const speedForm = reactive({ maxSpeedPercent: 50, requireConfirm: true })
const limits = reactive(getDefaultAxisLimits())

const axisNames: Record<number, string> = {}
for (const [key, val] of Object.entries(AXIS_NAMES)) {
  axisNames[Number(key)] = val.name
}

async function handleCheck() {
  checkLoading.value = true
  try {
    const res = await safetyAPI.check()
    if (res.data) checkResult.value = res.data
  } finally { checkLoading.value = false }
}

async function saveSpeedConfig() {
  savingSpeed.value = true
  try {
    await safetyAPI.updateConfig(speedForm)
    ElMessage.success('速度配置已保存')
  } finally { savingSpeed.value = false }
}

async function saveLimits() {
  savingLimits.value = true
  try {
    await safetyAPI.updateLimits(limits)
    ElMessage.success('限位配置已保存')
  } finally { savingLimits.value = false }
}

onMounted(async () => {
  try {
    const res = await safetyAPI.getConfig()
    if (res.data) {
      speedForm.maxSpeedPercent = res.data.maxSpeedPercent
      speedForm.requireConfirm = res.data.requireConfirm
      if (res.data.axisLimits) Object.assign(limits, res.data.axisLimits)
    }
  } catch { /* ignore */ }
})
</script>

<style scoped lang="scss">
.page-header {
  display: flex; justify-content: space-between; align-items: center; margin-bottom: $spacing-lg;
  h3 { margin: 0; color: $color-text-primary; font-size: 18px; }
}
.safety-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: $spacing-lg;
  margin-top: $spacing-lg;
}
.panel {
  background: $color-bg-card; border: 1px solid $color-border;
  border-radius: $radius-lg; padding: $spacing-lg;
}
.panel-title { font-size: 14px; font-weight: 600; color: $color-text-primary; margin: 0 0 $spacing-md; }
.limit-row {
  display: flex; align-items: center; gap: $spacing-sm; margin-bottom: 8px;
}
.limit-label { width: 70px; font-size: 12px; color: $color-text-secondary; }
.limit-sep { color: $color-text-muted; }
.save-limits-btn { margin-top: $spacing-md; }
.estop-panel { display: flex; flex-direction: column; align-items: center; }
</style>
