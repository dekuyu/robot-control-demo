<!-- 报警横幅组件 -->
<template>
  <transition name="slide-down">
    <div v-if="visible" class="alarm-banner" :class="severity">
      <div class="banner-content">
        <el-icon class="banner-icon"><WarningFilled /></el-icon>
        <span class="banner-text">{{ message }}</span>
      </div>
      <el-button text class="banner-close" @click="$emit('close')">
        <el-icon><Close /></el-icon>
      </el-button>
    </div>
  </transition>
</template>

<script setup lang="ts">
defineProps<{
  visible: boolean
  message: string
  severity: 'critical' | 'warning' | 'info'
}>()

defineEmits<{ close: [] }>()
</script>

<style scoped lang="scss">
.alarm-banner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px $spacing-lg;
  border-radius: $radius-md;
  margin-bottom: $spacing-md;
  &.critical { background: rgba($color-danger, 0.15); border: 1px solid rgba($color-danger, 0.4); }
  &.warning { background: rgba($color-warning, 0.15); border: 1px solid rgba($color-warning, 0.4); }
  &.info { background: rgba($color-info, 0.1); border: 1px solid rgba($color-info, 0.3); }
}
.banner-content {
  display: flex;
  align-items: center;
  gap: $spacing-sm;
}
.banner-icon {
  font-size: 18px;
  color: $color-danger;
}
.critical .banner-icon { color: $color-danger; }
.warning .banner-icon { color: $color-warning; }
.info .banner-icon { color: $color-info; }
.banner-text {
  color: $color-text-primary;
  font-size: 13px;
}
.slide-down-enter-active, .slide-down-leave-active {
  transition: all 0.3s ease;
}
.slide-down-enter-from, .slide-down-leave-to {
  opacity: 0;
  transform: translateY(-100%);
}
</style>
