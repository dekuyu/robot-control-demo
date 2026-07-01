<!-- 安全横幅组件 -->
<template>
  <div class="safety-banner" :class="status">
    <div class="check-results">
      <div class="check-item" v-for="item in checks" :key="item.key">
        <el-icon :class="item.ok ? 'pass' : 'fail'">
          <CircleCheck v-if="item.ok" />
          <CircleClose v-else />
        </el-icon>
        <span>{{ item.label }}</span>
      </div>
    </div>
    <div class="safety-status">
      <el-tag :type="status === 'pass' ? 'success' : 'danger'" size="large">
        {{ status === 'pass' ? '安全检查通过' : '安全检查未通过' }}
      </el-tag>
    </div>
    <div v-if="failures.length > 0" class="failure-list">
      <p v-for="f in failures" :key="f" class="failure-item">{{ f }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { SafetyCheckResult } from '@/types/safety'

const props = defineProps<{ checkResult: SafetyCheckResult }>()

const status = computed(() => props.checkResult.allPassed ? 'pass' : 'fail')
const failures = computed(() => props.checkResult.failures ?? [])

const checks = computed(() => [
  { key: 'servo', label: '伺服状态', ok: props.checkResult.servoOk },
  { key: 'mode', label: '运行模式', ok: props.checkResult.modeOk },
  { key: 'alarm', label: '报警状态', ok: props.checkResult.alarmOk },
  { key: 'speed', label: '速度限制', ok: props.checkResult.speedOk },
  { key: 'confirm', label: '操作确认', ok: props.checkResult.operatorConfirmed },
])
</script>

<style scoped lang="scss">
.safety-banner {
  display: flex;
  align-items: center;
  gap: $spacing-lg;
  padding: $spacing-md $spacing-lg;
  border-radius: $radius-lg;
  flex-wrap: wrap;
  &.pass { background: rgba($color-success, 0.1); border: 1px solid rgba($color-success, 0.3); }
  &.fail { background: rgba($color-danger, 0.1); border: 1px solid rgba($color-danger, 0.3); }
}
.check-results {
  display: flex;
  gap: $spacing-md;
  flex-wrap: wrap;
}
.check-item {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  color: $color-text-secondary;
  .pass { color: $color-success; }
  .fail { color: $color-danger; }
}
.failure-list {
  width: 100%;
  margin-top: $spacing-sm;
}
.failure-item {
  font-size: 12px;
  color: $color-danger;
  margin: 2px 0;
  &::before { content: '• '; }
}
</style>
