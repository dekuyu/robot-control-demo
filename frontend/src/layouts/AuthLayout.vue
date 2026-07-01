<!--
  认证布局：居中登录卡片
-->
<template>
  <div class="auth-layout">
    <div class="auth-card">
      <div class="auth-header">
        <h1>YRC1000</h1>
        <p>机械臂远程控制系统</p>
      </div>
      <router-view />
    </div>
  </div>
</template>

<style scoped lang="scss">
.auth-layout {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100vh;
  background: $color-bg-primary;
  position: relative;

  &::before {
    content: '';
    position: absolute;
    top: 10%;
    left: 50%;
    transform: translateX(-50%);
    width: 600px;
    height: 600px;
    background: radial-gradient(circle, rgba($color-info, 0.08), transparent 60%);
    pointer-events: none;
  }
}

.auth-card {
  position: relative;
  width: 420px;
  padding: $spacing-2xl;
  background: rgba($color-bg-card, 0.9);
  border: 1px solid $color-border;
  border-radius: $radius-xl;
  backdrop-filter: blur(16px);
  box-shadow: $shadow-glass;

  .auth-header {
    text-align: center;
    margin-bottom: $spacing-xl;

    h1 {
      font-size: 28px;
      font-weight: 700;
      color: $color-text-primary;
      margin-bottom: $spacing-xs;
    }

    p {
      font-size: 14px;
      color: $color-text-muted;
    }
  }
}
</style>
