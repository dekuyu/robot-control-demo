<!--
  主布局：侧边栏 + 顶栏 + 内容区 + 连接状态
  工业暗色主题 + 毛玻璃侧边栏
-->
<template>
  <div class="main-layout">
    <!-- 顶部栏 -->
    <header class="layout-header">
      <div class="header-left">
        <h1 class="app-title">YRC1000 控制系统</h1>
      </div>
      <div class="header-center">
        <StatusIndicator
          :connected="robotStore.connected"
          :servo-on="robotStore.servoOn"
          :mode="robotStore.runningMode"
          :alarm-active="robotStore.alarmActive"
        />
      </div>
      <div class="header-right">
        <span class="user-info">
          <el-icon><User /></el-icon>
          {{ authStore.user?.username }}
        </span>
        <el-tag :type="roleTagType" size="small">{{ roleLabel }}</el-tag>
        <el-button text @click="handleLogout">
          <el-icon><SwitchButton /></el-icon>
        </el-button>
      </div>
    </header>

    <!-- 侧边栏 -->
    <aside class="layout-sidebar">
      <el-menu
        :default-active="activeMenu"
        router
        class="sidebar-menu"
      >
        <el-menu-item index="/dashboard">
          <el-icon><Odometer /></el-icon>
          <span>仪表盘</span>
        </el-menu-item>
        <el-menu-item index="/control">
          <el-icon><Operation /></el-icon>
          <span>机械臂控制</span>
        </el-menu-item>
        <el-menu-item index="/positions">
          <el-icon><Location /></el-icon>
          <span>坐标管理</span>
        </el-menu-item>
        <el-menu-item index="/variables">
          <el-icon><SetUp /></el-icon>
          <span>变量读写</span>
        </el-menu-item>
        <el-menu-item index="/terminal">
          <el-icon><Connection /></el-icon>
          <span>调试终端</span>
        </el-menu-item>
        <div class="menu-divider"></div>
        <el-menu-item index="/alarms">
          <el-icon><Bell /></el-icon>
          <span>报警管理</span>
        </el-menu-item>
        <el-menu-item index="/logs">
          <el-icon><Document /></el-icon>
          <span>操作日志</span>
        </el-menu-item>
        <el-menu-item index="/safety">
          <el-icon><Lock /></el-icon>
          <span>安全配置</span>
        </el-menu-item>
        <el-menu-item index="/settings">
          <el-icon><Setting /></el-icon>
          <span>系统设置</span>
        </el-menu-item>
        <el-menu-item v-if="authStore.isAdmin" index="/admin">
          <el-icon><UserFilled /></el-icon>
          <span>用户管理</span>
        </el-menu-item>
      </el-menu>
    </aside>

    <!-- 内容区 -->
    <main class="layout-content">
      <router-view />
    </main>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useRobotStore } from '@/stores/robot'
import StatusIndicator from '@/components/common/StatusIndicator.vue'
import { useWebSocket } from '@/composables/useWebSocket'

const route = useRoute()
const authStore = useAuthStore()
const robotStore = useRobotStore()

// 初始化 WebSocket 连接
useWebSocket()

const activeMenu = computed(() => route.path)

const roleLabel = computed(() => {
  const labels: Record<string, string> = {
    admin: '管理员', operator: '操作员', engineer: '工程师', observer: '观察员',
  }
  return labels[authStore.userRole] || authStore.userRole
})

const roleTagType = computed(() => {
  if (authStore.isAdmin) return 'danger'
  if (authStore.userRole === 'engineer') return 'warning'
  return 'info'
})

async function handleLogout() {
  await authStore.logout()
}
</script>

<style scoped lang="scss">
.main-layout {
  display: grid;
  grid-template-columns: $sidebar-width 1fr;
  grid-template-rows: $header-height 1fr;
  height: 100vh;
  overflow: hidden;
}

.layout-header {
  grid-column: 1 / -1;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 $spacing-lg;
  background: rgba($color-bg-secondary, 0.95);
  border-bottom: 1px solid $color-border;
  backdrop-filter: blur(12px);
  z-index: $z-header;

  .app-title {
    font-size: 16px;
    font-weight: 700;
    color: $color-text-primary;
    letter-spacing: 1px;
  }

  .header-right {
    display: flex;
    align-items: center;
    gap: $spacing-md;
  }

  .user-info {
    display: flex;
    align-items: center;
    gap: $spacing-xs;
    color: $color-text-secondary;
    font-size: 13px;
  }
}

.layout-sidebar {
  grid-row: 2;
  background: rgba($color-bg-secondary, 0.8);
  border-right: 1px solid $color-border;
  backdrop-filter: blur(12px);
  overflow-y: auto;

  .sidebar-menu {
    border-right: none;
    background: transparent;
  }

  .menu-divider {
    height: 1px;
    background: $color-border;
    margin: $spacing-sm $spacing-md;
  }
}

.layout-content {
  grid-row: 2;
  padding: $spacing-lg;
  overflow-y: auto;
  background: $color-bg-primary;
}

// Element Plus Menu 暗色覆盖
:deep(.el-menu) {
  --el-menu-bg-color: transparent;
  --el-menu-hover-bg-color: rgba($color-info, 0.1);
  --el-menu-text-color: #{$color-text-secondary};
  --el-menu-active-color: #{$color-info};
}

// 响应式
@media (max-width: $breakpoint-md) {
  .main-layout {
    grid-template-columns: 60px 1fr;
  }
  .layout-sidebar .el-menu-item span {
    display: none;
  }
}
</style>
