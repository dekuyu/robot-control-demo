<!-- 登录页面 -->
<template>
  <div class="login-page">
    <div class="login-card">
      <div class="login-header">
        <h1 class="login-title">YRC1000</h1>
        <p class="login-subtitle">机器人控制系统</p>
      </div>
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        @submit.prevent="handleLogin"
        class="login-form"
      >
        <el-form-item prop="username">
          <el-input
            v-model="form.username"
            placeholder="用户名"
            prefix-icon="User"
            size="large"
          />
        </el-form-item>
        <el-form-item prop="password">
          <el-input
            v-model="form.password"
            type="password"
            placeholder="密码"
            prefix-icon="Lock"
            size="large"
            show-password
          />
        </el-form-item>
        <el-form-item>
          <el-button
            type="primary"
            size="large"
            native-type="submit"
            :loading="loading"
            class="login-btn"
          >
            登录
          </el-button>
        </el-form-item>
      </el-form>
      <p v-if="errorMsg" class="error-msg">{{ errorMsg }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import type { FormInstance, FormRules } from 'element-plus'

const router = useRouter()
const authStore = useAuthStore()

const form = reactive({ username: '', password: '' })
const loading = ref(false)
const errorMsg = ref('')
const formRef = ref<FormInstance>()

const rules: FormRules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }],
}

async function handleLogin() {
  const valid = await formRef.value?.validate().catch(() => false)
  if (!valid) return
  loading.value = true
  errorMsg.value = ''
  try {
    const res = await authStore.login(form.username, form.password)
    if (res.code === 0) {
      router.push('/dashboard')
    } else {
      errorMsg.value = res.message || '登录失败'
    }
  } catch (e: any) {
    errorMsg.value = e?.message || '网络错误'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped lang="scss">
.login-page {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background: $color-bg-primary;
}
.login-card {
  width: 380px;
  padding: $spacing-xl $spacing-2xl;
  background: $color-bg-glass;
  border: 1px solid $color-border;
  border-radius: $radius-xl;
  box-shadow: $shadow-glass;
  backdrop-filter: blur(20px);
}
.login-header {
  text-align: center;
  margin-bottom: $spacing-xl;
}
.login-title {
  font-size: 28px;
  font-weight: 700;
  color: $color-text-primary;
  margin: 0;
  letter-spacing: 4px;
}
.login-subtitle {
  color: $color-text-secondary;
  font-size: 13px;
  margin: $spacing-xs 0 0;
}
.login-btn {
  width: 100%;
}
.error-msg {
  text-align: center;
  color: $color-danger;
  font-size: 12px;
  margin-top: $spacing-sm;
}
</style>
