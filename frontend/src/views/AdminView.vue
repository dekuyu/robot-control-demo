<!-- 用户管理页面（管理员专用） -->
<template>
  <div class="admin-page">
    <div class="page-header">
      <h3>用户管理</h3>
      <div class="header-actions">
        <el-button type="primary" @click="userStore.openCreate()">
          <el-icon><Plus /></el-icon> 新建用户
        </el-button>
      </div>
    </div>

    <!-- 筛选 -->
    <div class="filters">
      <el-select v-model="roleFilter" placeholder="角色筛选" clearable @change="userStore.setRoleFilter($event || '')">
        <el-option label="管理员" value="admin" />
        <el-option label="工程师" value="engineer" />
        <el-option label="操作员" value="operator" />
        <el-option label="观察员" value="observer" />
      </el-select>
    </div>

    <!-- 用户列表 -->
    <div class="panel">
      <el-table :data="userStore.users" v-loading="userStore.loading" stripe size="small">
        <el-table-column type="index" width="50" label="#" />
        <el-table-column prop="username" label="用户名" width="140" />
        <el-table-column label="角色" width="100">
          <template #default="{ row }">
            <el-tag :type="roleTagType(row.role)" size="small">{{ roleLabel(row.role) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="状态" width="80">
          <template #default="{ row }">
            <el-tag :type="row.isActive ? 'success' : 'danger'" size="small">
              {{ row.isActive ? '正常' : '已禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="锁定" width="70">
          <template #default="{ row }">
            <el-tag v-if="row.isLocked" type="warning" size="small">已锁定</el-tag>
            <span v-else class="muted">--</span>
          </template>
        </el-table-column>
        <el-table-column prop="lastLogin" label="最后登录" width="160">
          <template #default="{ row }">{{ formatDateTime(row.lastLogin) }}</template>
        </el-table-column>
        <el-table-column prop="createdAt" label="创建时间" width="160">
          <template #default="{ row }">{{ formatDateTime(row.createdAt) }}</template>
        </el-table-column>
        <el-table-column label="操作" width="220" fixed="right">
          <template #default="{ row }">
            <el-button text size="small" type="primary" @click="userStore.openEdit(row)">编辑</el-button>
            <el-button
              v-if="row.isLocked"
              text size="small"
              type="warning"
              @click="handleUnlock(row)"
            >解锁</el-button>
            <el-button
              text size="small"
              :type="row.isActive ? 'danger' : 'success'"
              @click="handleToggleStatus(row)"
            >
              {{ row.isActive ? '禁用' : '启用' }}
            </el-button>
            <el-popconfirm
              title="确认删除？"
              @confirm="handleDelete(row)"
            >
              <template #reference>
                <el-button text size="small" type="danger">删除</el-button>
              </template>
            </el-popconfirm>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <!-- 分页 -->
    <div class="pagination" v-if="userStore.total > userStore.pageSize">
      <el-pagination
        v-model:current-page="currentPage"
        :page-size="userStore.pageSize"
        :total="userStore.total"
        layout="prev, pager, next"
        @current-change="userStore.setPage"
      />
    </div>

    <!-- 创建/编辑对话框 -->
    <el-dialog
      :model-value="userStore.showDialog"
      :title="userStore.editingUser ? '编辑用户' : '新建用户'"
      width="460px"
      @update:model-value="userStore.closeDialog()"
    >
      <el-form v-if="userStore.showDialog" :model="userForm" label-width="80px">
        <el-form-item label="用户名" required>
          <el-input v-model="userForm.username" placeholder="请输入用户名" />
        </el-form-item>
        <el-form-item v-if="!userStore.editingUser" label="密码" required>
          <el-input v-model="userForm.password" type="password" placeholder="请输入密码" show-password />
        </el-form-item>
        <el-form-item label="角色" required>
          <el-select v-model="userForm.role" placeholder="选择角色">
            <el-option label="管理员" value="admin" />
            <el-option label="工程师" value="engineer" />
            <el-option label="操作员" value="operator" />
            <el-option label="观察员" value="observer" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="userStore.closeDialog()">取消</el-button>
        <el-button type="primary" @click="handleSaveUser" :loading="savingUser">
          {{ userStore.editingUser ? '保存' : '创建' }}
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, watch, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/stores/user'
import { formatDateTime } from '@/utils/format'
import type { UserInfo, UserRole } from '@/types/user'

const userStore = useUserStore()
const roleFilter = ref('')
const currentPage = ref(1)
const savingUser = ref(false)

const userForm = reactive({ username: '', password: '', role: 'observer' as UserRole })

watch(() => userStore.editingUser, (u) => {
  if (u) {
    userForm.username = u.username
    userForm.role = u.role
  } else {
    userForm.username = ''
    userForm.password = ''
    userForm.role = 'observer'
  }
})

function roleLabel(role: UserRole): string {
  return { admin: '管理员', engineer: '工程师', operator: '操作员', observer: '观察员' }[role] ?? role
}

function roleTagType(role: UserRole): string {
  return { admin: 'danger', engineer: 'warning', operator: 'info', observer: '' }[role] ?? ''
}

async function handleUnlock(user: UserInfo) {
  const res = await userStore.unlockUser(user.id)
  if (res.code === 0) ElMessage.success('用户已解锁')
}

async function handleToggleStatus(user: UserInfo) {
  const res = await userStore.updateUser(user.id, { isActive: !user.isActive })
  if (res.code === 0) ElMessage.success(`用户已${user.isActive ? '禁用' : '启用'}`)
}

async function handleDelete(user: UserInfo) {
  const res = await userStore.removeUser(user.id)
  if (res.code === 0) ElMessage.success('用户已删除')
}

async function handleSaveUser() {
  savingUser.value = true
  try {
    if (userStore.editingUser) {
      await userStore.updateUser(userStore.editingUser.id, { username: userForm.username, role: userForm.role })
      ElMessage.success('用户已更新')
    } else {
      await userStore.createUser({ username: userForm.username, password: userForm.password, role: userForm.role })
      ElMessage.success('用户已创建')
    }
    userStore.closeDialog()
  } finally { savingUser.value = false }
}

onMounted(() => userStore.fetchUsers())
</script>

<style scoped lang="scss">
.page-header {
  display: flex; justify-content: space-between; align-items: center; margin-bottom: $spacing-lg;
  h3 { margin: 0; color: $color-text-primary; font-size: 18px; }
}
.filters { margin-bottom: $spacing-lg; }
.panel {
  background: $color-bg-card; border: 1px solid $color-border;
  border-radius: $radius-lg; padding: $spacing-lg;
}
.muted { color: $color-text-muted; }
.pagination { display: flex; justify-content: center; margin-top: $spacing-lg; }
</style>
