<!-- 系统设置页面 -->
<template>
  <div class="settings-page">
    <div class="page-header">
      <h3>系统设置</h3>
    </div>

    <div class="settings-grid">
      <!-- 机器人连接配置 -->
      <div class="panel">
        <h4 class="panel-title">连接配置</h4>
        <el-form label-width="80px" size="small">
          <el-form-item label="机器人名称">
            <el-input v-model="configForm.name" placeholder="YRC1000" />
          </el-form-item>
          <el-form-item label="IP 地址">
            <el-input v-model="configForm.ip" placeholder="192.168.255.1" />
          </el-form-item>
          <el-form-item label="端口号">
            <el-input-number v-model="configForm.port" :min="1" :max="65535" />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="saveConfig" :loading="saving">
              保存配置
            </el-button>
            <el-button @click="testConnection" :loading="testing">
              测试连接
            </el-button>
          </el-form-item>
        </el-form>
      </div>

      <!-- 连接状态 -->
      <div class="panel">
        <h4 class="panel-title">当前连接</h4>
        <div class="conn-status">
          <div class="status-row">
            <span class="key">状态</span>
            <el-tag :type="connectionStore.isConnected ? 'success' : 'danger'" size="small">
              {{ connectionStore.isConnected ? '已连接' : '未连接' }}
            </el-tag>
          </div>
          <div class="status-row">
            <span class="key">机器人 IP</span>
            <span class="value mono">{{ connectionStore.robotIP }}</span>
          </div>
          <div class="status-row">
            <span class="key">端口</span>
            <span class="value mono">{{ connectionStore.robotPort }}</span>
          </div>
          <div class="status-row" v-if="connectionStore.reconnectCount > 0">
            <span class="key">重连次数</span>
            <span class="value mono">{{ connectionStore.reconnectCount }}</span>
          </div>
        </div>
        <div class="conn-actions">
          <el-button
            :type="connectionStore.isConnected ? 'danger' : 'success'"
            size="small"
            :loading="connectionStore.isConnecting"
            @click="toggleConnection"
          >
            {{ connectionStore.isConnected ? '断开连接' : '连接机器人' }}
          </el-button>
        </div>
      </div>

      <!-- 个人信息 -->
      <div class="panel">
        <h4 class="panel-title">账户信息</h4>
        <div class="user-info" v-if="authStore.user">
          <div class="info-row">
            <span class="key">用户名</span>
            <span class="value">{{ authStore.user.username }}</span>
          </div>
          <div class="info-row">
            <span class="key">角色</span>
            <el-tag size="small">{{ roleLabel }}</el-tag>
          </div>
          <div class="info-row">
            <span class="key">状态</span>
            <el-tag :type="authStore.user.isActive ? 'success' : 'danger'" size="small">
              {{ authStore.user.isActive ? '正常' : '已禁用' }}
            </el-tag>
          </div>
          <div class="info-row">
            <span class="key">最后登录</span>
            <span class="value">{{ authStore.user.lastLogin ? formatDateTime(authStore.user.lastLogin) : '--' }}</span>
          </div>
        </div>
      </div>

      <!-- 关于 -->
      <div class="panel">
        <h4 class="panel-title">关于系统</h4>
        <div class="about">
          <p><strong>YRC1000 机器人控制系统</strong></p>
          <p>版本: 1.0.0</p>
          <p>基于 FastAPI + Vue3 + Element Plus</p>
          <p>YERC 协议通信</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '@/stores/auth'
import { useConnectionStore } from '@/stores/connection'
import { useRobotStore } from '@/stores/robot'
import { robotAPI } from '@/api/robot'
import { formatDateTime } from '@/utils/format'
import { DEFAULT_ROBOT_IP, DEFAULT_ROBOT_PORT } from '@/utils/constants'

const authStore = useAuthStore()
const connectionStore = useConnectionStore()
const robotStore = useRobotStore()

const saving = ref(false)
const testing = ref(false)

const configForm = reactive({
  name: '',
  ip: DEFAULT_ROBOT_IP,
  port: DEFAULT_ROBOT_PORT,
})

const roleLabel = computed(() => {
  const map: Record<string, string> = { admin: '管理员', operator: '操作员', engineer: '工程师', observer: '观察员' }
  return map[authStore.userRole] || authStore.userRole
})

async function saveConfig() {
  saving.value = true
  try {
    await robotAPI.updateConfig(configForm)
    ElMessage.success('配置已保存')
  } finally { saving.value = false }
}

async function testConnection() {
  testing.value = true
  try {
    const res = await robotAPI.getHeartbeat()
    if (res.data?.alive) ElMessage.success('连接测试成功')
    else ElMessage.warning('机器人无响应')
  } catch {
    ElMessage.error('连接测试失败')
  } finally { testing.value = false }
}

async function toggleConnection() {
  if (connectionStore.isConnected) {
    await connectionStore.disconnect()
    robotStore.reset()
  } else {
    await connectionStore.connect(configForm.ip, configForm.port)
  }
}

onMounted(async () => {
  try {
    const res = await robotAPI.getConfig()
    if (res.data) {
      configForm.name = res.data.name
      configForm.ip = res.data.ip
      configForm.port = res.data.port
    }
  } catch { /* ignore */ }
})
</script>

<style scoped lang="scss">
.page-header {
  margin-bottom: $spacing-lg;
  h3 { margin: 0; color: $color-text-primary; font-size: 18px; }
}
.settings-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: $spacing-lg;
}
.panel {
  background: $color-bg-card; border: 1px solid $color-border;
  border-radius: $radius-lg; padding: $spacing-lg;
}
.panel-title { font-size: 14px; font-weight: 600; color: $color-text-primary; margin: 0 0 $spacing-md; }
.status-row, .info-row {
  display: flex; justify-content: space-between; align-items: center;
  padding: 6px 0; font-size: 13px;
  .key { color: $color-text-secondary; }
  .value { color: $color-text-primary; }
}
.mono { font-family: $font-family-mono; }
.conn-actions { margin-top: $spacing-md; }
.about {
  p { font-size: 13px; color: $color-text-secondary; margin: 4px 0; }
}
</style>
