// ===== Vue Router 路由定义 + 导航守卫 =====
import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const routes: RouteRecordRaw[] = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/LoginView.vue'),
    meta: { requiresAuth: false },
  },
  {
    path: '/',
    component: () => import('@/layouts/MainLayout.vue'),
    meta: { requiresAuth: true },
    children: [
      { path: '', redirect: '/dashboard' },
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: () => import('@/views/DashboardView.vue'),
        meta: { title: '仪表盘', requiresAuth: true },
      },
      {
        path: 'control',
        name: 'Control',
        component: () => import('@/views/ControlView.vue'),
        meta: { title: '机械臂控制', requiresAuth: true, permission: 'jog' },
      },
      {
        path: 'positions',
        name: 'Positions',
        component: () => import('@/views/PositionView.vue'),
        meta: { title: '坐标管理', requiresAuth: true },
      },
      {
        path: 'variables',
        name: 'Variables',
        component: () => import('@/views/VariableView.vue'),
        meta: { title: '变量读写', requiresAuth: true },
      },
      {
        path: 'alarms',
        name: 'Alarms',
        component: () => import('@/views/AlarmView.vue'),
        meta: { title: '报警管理', requiresAuth: true },
      },
      {
        path: 'logs',
        name: 'Logs',
        component: () => import('@/views/LogView.vue'),
        meta: { title: '操作日志', requiresAuth: true },
      },
      {
        path: 'terminal',
        name: 'Terminal',
        component: () => import('@/views/TerminalView.vue'),
        meta: { title: '调试终端', requiresAuth: true, permission: 'terminal_send' },
      },
      {
        path: 'safety',
        name: 'Safety',
        component: () => import('@/views/SafetyView.vue'),
        meta: { title: '安全配置', requiresAuth: true, permission: '*' },
      },
      {
        path: 'settings',
        name: 'Settings',
        component: () => import('@/views/SettingsView.vue'),
        meta: { title: '系统设置', requiresAuth: true },
      },
      {
        path: 'admin',
        name: 'Admin',
        component: () => import('@/views/AdminView.vue'),
        meta: { title: '用户管理', requiresAuth: true, permission: '*' },
      },
    ],
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// 导航守卫：认证 + 权限检查
router.beforeEach((to, _from, next) => {
  const authStore = useAuthStore()

  if (to.meta.requiresAuth && !authStore.isLoggedIn) {
    next('/login')
    return
  }

  if (to.path === '/login' && authStore.isLoggedIn) {
    next('/dashboard')
    return
  }

  next()
})

export default router
