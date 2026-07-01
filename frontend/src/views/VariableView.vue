<!-- 变量读写页面 -->
<template>
  <div class="variable-page">
    <div class="page-header">
      <h3>变量读写</h3>
    </div>

    <PermissionGuard action="var_readwrite">
      <div class="variable-layout">
        <!-- 左侧：B 变量 -->
        <div class="panel">
          <h4 class="panel-title">B 变量 (字节型)</h4>
          <VariableEditor :var-type="'B'" :indices="bRange" :readonly="isObserver" />
        </div>

        <!-- 右侧：D 变量 -->
        <div class="panel">
          <h4 class="panel-title">D 变量 (整型)</h4>
          <VariableEditor :var-type="'D'" :indices="dRange" :readonly="isObserver" />
        </div>

        <!-- I 变量 -->
        <div class="panel">
          <h4 class="panel-title">I 变量 (整型, 只读)</h4>
          <VariableEditor :var-type="'I'" :indices="iRange" :readonly="true" />
        </div>

        <!-- IO 矩阵 -->
        <div class="panel">
          <h4 class="panel-title">IO 信号</h4>
          <IOMatrix :indices="ioRange" :readonly="isObserver" />
        </div>
      </div>
    </PermissionGuard>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import PermissionGuard from '@/components/common/PermissionGuard.vue'
import VariableEditor from '@/components/common/VariableEditor.vue'
import IOMatrix from '@/components/common/IOMatrix.vue'

const authStore = useAuthStore()
const isObserver = computed(() => authStore.userRole === 'observer')

const bRange = Array.from({ length: 10 }, (_, i) => i)
const dRange = Array.from({ length: 10 }, (_, i) => i)
const iRange = Array.from({ length: 8 }, (_, i) => i)
const ioRange = Array.from({ length: 32 }, (_, i) => i + 1)
</script>

<style scoped lang="scss">
.page-header {
  margin-bottom: $spacing-lg;
  h3 { margin: 0; color: $color-text-primary; font-size: 18px; }
}
.variable-layout {
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
.panel-title {
  font-size: 14px;
  font-weight: 600;
  color: $color-text-primary;
  margin: 0 0 $spacing-md;
}
</style>
