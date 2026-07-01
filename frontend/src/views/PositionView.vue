<!-- 坐标管理页面 -->
<template>
  <div class="position-page">
    <div class="page-header">
      <h3>坐标管理</h3>
      <div class="header-actions">
        <el-button type="primary" @click="posStore.openCreate()">
          <el-icon><Plus /></el-icon> 新建点位
        </el-button>
        <el-button @click="posStore.fetchCurrentPosture()" :loading="posStore.loading">
          <el-icon><Refresh /></el-icon> 获取当前姿态
        </el-button>
      </div>
    </div>

    <PermissionGuard action="view">
      <!-- 搜索栏 -->
      <div class="search-bar">
        <el-input
          v-model="searchText"
          placeholder="搜索点位名称..."
          prefix-icon="Search"
          clearable
          @input="posStore.setSearchKeyword(searchText)"
          @clear="posStore.setSearchKeyword('')"
          class="search-input"
        />
      </div>

      <!-- 当前姿态 -->
      <div v-if="posStore.currentPosture" class="panel current-posture">
        <h4 class="panel-title">当前姿态</h4>
        <div class="posture-grid">
          <div class="posture-section">
            <span class="section-label">关节角度</span>
            <div class="posture-values">
              <span v-for="(val, key) in posStore.currentPosture.joints" :key="key" class="pv-item">
                {{ key }}: {{ (val as number).toFixed(1) }}°
              </span>
            </div>
          </div>
          <div class="posture-section">
            <span class="section-label">末端坐标</span>
            <div class="posture-values">
              <span v-for="(val, key) in posStore.currentPosture.endCoords" :key="key" class="pv-item">
                {{ key.toUpperCase() }}: {{ (val as number).toFixed(1) }}
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- 点位列表 -->
      <div class="panel">
        <div class="position-grid">
          <PositionCard
            v-for="pos in posStore.positions"
            :key="pos.id"
            :position="pos"
            @select="goToPosition"
            @edit="posStore.openEdit(pos)"
            @delete="handleDelete(pos)"
          />
        </div>
        <div v-if="!posStore.loading && posStore.positions.length === 0" class="empty-state">
          暂无命名点位，点击"新建点位"开始
        </div>
      </div>

      <!-- 分页 -->
      <div class="pagination" v-if="posStore.total > posStore.pageSize">
        <el-pagination
          v-model:current-page="currentPage"
          :page-size="posStore.pageSize"
          :total="posStore.total"
          layout="prev, pager, next"
          @current-change="posStore.setPage"
        />
      </div>
    </PermissionGuard>

    <!-- 创建/编辑对话框 -->
    <el-dialog
      :model-value="posStore.showCreateDialog"
      :title="posStore.editingPosition ? '编辑点位' : '新建点位'"
      width="500px"
      @update:model-value="posStore.closeCreate()"
    >
      <el-form v-if="posStore.showCreateDialog" :model="form" label-width="80px">
        <el-form-item label="名称" required>
          <el-input v-model="form.name" placeholder="点位名称" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="form.description" type="textarea" rows="2" placeholder="可选描述" />
        </el-form-item>
        <el-form-item label="姿态来源">
          <el-radio-group v-model="form.source">
            <el-radio value="current">当前姿态</el-radio>
            <el-radio value="variable">从P变量</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item v-if="form.source === 'variable'" label="P变量号">
          <el-input-number v-model="form.pIdx" :min="0" :max="127" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="posStore.closeCreate()">取消</el-button>
        <el-button type="primary" @click="handleSave" :loading="saving">
          {{ posStore.editingPosition ? '保存' : '创建' }}
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, watch } from 'vue'
import { usePositionStore } from '@/stores/position'
import { useRobotStore } from '@/stores/robot'
import { ElMessage, ElMessageBox } from 'element-plus'
import PermissionGuard from '@/components/common/PermissionGuard.vue'
import PositionCard from '@/components/common/PositionCard.vue'
import { onMounted } from 'vue'

const posStore = usePositionStore()
const robotStore = useRobotStore()

const searchText = ref('')
const currentPage = ref(1)
const saving = ref(false)

const form = reactive({
  name: '',
  description: '',
  source: 'current' as 'current' | 'variable',
  pIdx: 0,
})

watch(() => posStore.editingPosition, (pos) => {
  if (pos) {
    form.name = pos.name
    form.description = pos.description || ''
  } else {
    form.name = ''
    form.description = ''
    form.source = 'current'
    form.pIdx = 0
  }
})

onMounted(() => posStore.fetchPositions())

function goToPosition(pos: any) { /* 可扩展：发送目标移动指令 */ }

async function handleDelete(pos: any) {
  await ElMessageBox.confirm(`确认删除点位 "${pos.name}"？`, '确认删除', { type: 'warning' })
  await posStore.removePosition(pos.id)
  ElMessage.success('点位已删除')
}

async function handleSave() {
  saving.value = true
  try {
    let posture = posStore.currentPosture
    if (form.source === 'current' && !posture) {
      await posStore.fetchCurrentPosture()
      posture = posStore.currentPosture
    }
    if (form.source === 'variable') {
      const res = await posStore.readPVariable(form.pIdx)
      if (res.data) posture = res.data
    }
    if (!posture) { ElMessage.warning('无法获取姿态数据'); return }

    if (posStore.editingPosition) {
      await posStore.updatePosition(posStore.editingPosition.id, { name: form.name, description: form.description })
      ElMessage.success('点位已更新')
    } else {
      await posStore.createPosition({ name: form.name, description: form.description, posture })
      ElMessage.success('点位已创建')
    }
    posStore.closeCreate()
  } finally {
    saving.value = false
  }
}
</script>

<style scoped lang="scss">
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: $spacing-lg;
  h3 { margin: 0; color: $color-text-primary; font-size: 18px; }
  .header-actions { display: flex; gap: $spacing-sm; }
}
.search-bar { margin-bottom: $spacing-lg; }
.search-input { max-width: 400px; }
.panel {
  background: $color-bg-card;
  border: 1px solid $color-border;
  border-radius: $radius-lg;
  padding: $spacing-lg;
  margin-bottom: $spacing-lg;
}
.panel-title { font-size: 14px; font-weight: 600; color: $color-text-primary; margin: 0 0 $spacing-md; }
.position-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: $spacing-md;
}
.posture-grid { display: grid; grid-template-columns: 1fr 1fr; gap: $spacing-lg; }
.section-label { display: block; font-size: 12px; color: $color-text-muted; margin-bottom: $spacing-sm; }
.posture-values { display: flex; flex-wrap: wrap; gap: 6px; }
.pv-item {
  font-size: 11px;
  font-family: $font-family-mono;
  color: $color-text-secondary;
  background: rgba($color-bg-input, 0.6);
  padding: 2px 6px;
  border-radius: $radius-sm;
}
.pagination { display: flex; justify-content: center; }
.empty-state { text-align: center; color: $color-text-muted; padding: $spacing-2xl; }
</style>
