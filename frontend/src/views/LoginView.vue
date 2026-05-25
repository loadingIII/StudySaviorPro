<template>
  <div class="login-page">
    <!-- 左侧品牌区域 -->
    <div class="brand-section">
      <div class="brand-content">
        <div class="brand-logo">
          <svg viewBox="0 0 200 200" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="100" cy="100" r="80" fill="rgba(255,255,255,0.1)" stroke="white" stroke-width="3"/>
            <path d="M100 40L130 90L100 140L70 90L100 40Z" fill="white"/>
            <circle cx="100" cy="100" r="20" fill="white"/>
          </svg>
        </div>
        <h1>Welcome Back</h1>
        <p>StudySaviorPro 你的学习助手</p>
        <div class="brand-features">
          <div class="feature-item">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>
              <polyline points="22 4 12 14.01 9 11.01"/>
            </svg>
            <span>高效筛选</span>
          </div>
          <div class="feature-item">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="3"/>
              <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/>
            </svg>
            <span>智能出题</span>
          </div>
          <div class="feature-item">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
              <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
            </svg>
            <span>精准回复</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 右侧登录表单 -->
    <div class="form-section">
      <div class="form-container">
        <div class="form-header">
          <h2>用户登录</h2>
          <p>请输入您的账户信息以继续</p>
        </div>

        <form class="login-form" @submit.prevent="handleLogin">
          <div class="form-group">
            <label for="phone">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/>
              </svg>
              <span>手机号</span>
            </label>
            <div class="input-group">
              <input
                id="phone"
                v-model="loginForm.phone"
                type="tel"
                placeholder="请输入手机号"
                required
                autocomplete="tel"
                class="form-input"
              />
            </div>
          </div>

          <div class="form-group">
            <label for="password">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
                <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
              </svg>
              <span>密码</span>
            </label>
            <div class="input-group">
              <input
                id="password"
                v-model="loginForm.password"
                :type="showPassword ? 'text' : 'password'"
                placeholder="请输入密码"
                required
                autocomplete="current-password"
                class="form-input"
              />
              <button 
                type="button" 
                class="password-toggle"
                @click="showPassword = !showPassword"
                tabindex="-1"
              >
                <svg v-if="!showPassword" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
                  <circle cx="12" cy="12" r="3"/>
                </svg>
                <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M1 1l22 22"/>
                  <path d="M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.45 18.45 0 0 1-4.9 5.94"/>
                  <path d="M11 11h.01"/>
                </svg>
              </button>
            </div>
          </div>

          <div class="form-options">
            <label class="checkbox-label">
              <input type="checkbox" v-model="loginForm.rememberMe" />
              <span class="checkmark"></span>
              <span>记住我</span>
            </label>
            <a href="#" class="forgot-link">忘记密码？</a>
          </div>

          <button type="submit" class="submit-btn" :disabled="isLoading">
            <span v-if="!isLoading" class="btn-text">登 录</span>
            <span v-else class="loading">
              <span class="spinner"></span>
              <span>登录中...</span>
            </span>
          </button>

          <div v-if="errorMessage" class="error-alert">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="10"/>
              <line x1="12" y1="8" x2="12" y2="12"/>
              <line x1="12" y1="16" x2="12.01" y2="16"/>
            </svg>
            <span>{{ errorMessage }}</span>
          </div>
        </form>

        <div class="form-footer">
          <p>还没有账户？<a href="#" class="register-link">立即注册</a></p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const loginForm = reactive({
  phone: '',
  password: '',
  rememberMe: false
})

const showPassword = ref(false)
const isLoading = ref(false)
const errorMessage = ref('')

const handleLogin = async () => {
  isLoading.value = true
  errorMessage.value = ''

  try {
    const response = await fetch('/user/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        phone: loginForm.phone,
        password: loginForm.password
      })
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    const result = await response.json()

    if (result.code === 1) {
      // 缓存 Token 到 localStorage
      if (result.data && result.data.Authorization) {
        localStorage.setItem('token', result.data.Authorization)
      }
      // 缓存用户信息到 localStorage
      if (result.data) {
        localStorage.setItem('userInfo', JSON.stringify({
          id: result.data.id,
          username: result.data.username || result.data.phone || 'User'
        }))
      }
      // 登录成功，跳转到聊天页面
      router.push('/chat')
    } else {
      errorMessage.value = result.message || '手机号或密码错误，请重试'
    }
  } catch (error) {
    console.error('Login error:', error)
    errorMessage.value = '登录失败，请稍后重试'
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
:global(html), :global(body) {
  margin: 0;
  padding: 0;
  width: 100%;
  height: 100%;
  overflow-x: hidden;
}

:global(*) {
  box-sizing: border-box;
}

.login-page {
  width: 100%;
  height: 100vh;
  display: flex;
  background: linear-gradient(135deg, #6FB3C6 0%, #7FB8C7 30%, #FDE8D3 70%, #F3C6C2 100%);
  position: relative;
  overflow: hidden;
  margin: 0;
  padding: 0;
}

.login-page::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image: url('https://images.unsplash.com/photo-1579546929518-9e396f3cc809?w=1920&q=80');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  opacity: 0.15;
  pointer-events: none;
}

.login-page::after {
  content: '';
  position: absolute;
  bottom: -50%;
  right: -10%;
  width: 60%;
  height: 200%;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.15) 0%, transparent 70%);
  animation: rotate 25s linear infinite reverse;
  pointer-events: none;
}

@keyframes rotate {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

/* 左侧品牌区域 */
.brand-section {
  flex: 1;
  max-width: 50%;
  background: transparent;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 60px;
  position: relative;
  margin: 0;
}

.brand-content {
  position: relative;
  z-index: 1;
  color: white;
  max-width: 480px;
}

.brand-logo {
  width: 120px;
  height: 120px;
  margin-bottom: 40px;
  animation: float 3s ease-in-out infinite;
  background: rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  backdrop-filter: blur(10px);
  box-shadow: 0 8px 32px rgba(101, 113, 102, 0.2);
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

.brand-logo svg {
  width: 60%;
  height: 60%;
  filter: drop-shadow(0 2px 4px rgba(101, 113, 102, 0.3));
}

.brand-content h1 {
  font-size: 48px;
  font-weight: 700;
  margin-bottom: 16px;
  letter-spacing: -1px;
  color: #657166;
  text-shadow: 0 2px 4px rgba(255, 255, 255, 0.5);
}

.brand-content > p {
  font-size: 18px;
  color: #657166;
  opacity: 0.85;
  margin-bottom: 48px;
  line-height: 1.6;
}

.brand-features {
  display: flex;
  flex-direction: column;
  gap: 24px;
  background: rgba(255, 255, 255, 0.2);
  padding: 32px;
  border-radius: 16px;
  backdrop-filter: blur(10px);
  box-shadow: 0 8px 32px rgba(101, 113, 102, 0.15);
}

.feature-item {
  display: flex;
  align-items: center;
  gap: 16px;
  font-size: 16px;
  color: #657166;
  font-weight: 500;
}

.feature-item svg {
  width: 24px;
  height: 24px;
  color: #657166;
}

/* 右侧表单区域 */
.form-section {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 60px;
  background: rgba(255, 255, 255, 0.92);
  backdrop-filter: blur(20px);
  position: relative;
  overflow: hidden;
  margin: 0;
}

.form-container {
  width: 100%;
  max-width: 420px;
  background: white;
  padding: 40px;
  border-radius: 20px;
  margin: 0;
}

.form-header {
  margin-bottom: 40px;
}

.form-header h2 {
  font-size: 32px;
  font-weight: 700;
  color: #657166;
  margin-bottom: 8px;
}

.form-header p {
  font-size: 15px;
  color: #657166;
  opacity: 0.7;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-group label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  font-weight: 600;
  color: #657166;
}

.form-group label svg {
  width: 18px;
  height: 18px;
  color: #657166;
  opacity: 0.7;
}

.input-group {
  position: relative;
  display: flex;
  align-items: center;
}

.form-input {
  width: 100%;
  padding: 14px 16px;
  border: 2px solid #7FB8C7;
  border-radius: 12px;
  font-size: 15px;
  color: #657166;
  background: white;
  transition: all 0.3s ease;
  outline: none;
}

.form-input::placeholder {
  color: #6FB3C6;
}

.form-input:focus {
  border-color: #6FB3C6;
  box-shadow: 0 0 0 4px rgba(111, 179, 198, 0.25);
}

.password-toggle {
  position: absolute;
  right: 12px;
  background: none;
  border: none;
  cursor: pointer;
  padding: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #6FB3C6;
  transition: color 0.3s ease;
}

.password-toggle:hover {
  color: #657166;
}

.password-toggle svg {
  width: 20px;
  height: 20px;
}

.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 14px;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
  color: #657166;
  user-select: none;
}

.checkbox-label input[type="checkbox"] {
  display: none;
}

.checkmark {
  width: 20px;
  height: 20px;
  border: 2px solid #7FB8C7;
  border-radius: 6px;
  position: relative;
  transition: all 0.3s ease;
  flex-shrink: 0;
}

.checkbox-label input[type="checkbox"]:checked + .checkmark {
  background: linear-gradient(135deg, #6FB3C6 0%, #7FB8C7 100%);
  border-color: #6FB3C6;
}

.forgot-link {
  color: #6FB3C6;
  text-decoration: none;
  font-weight: 600;
  transition: color 0.3s ease;
}

.forgot-link:hover {
  color: #657166;
}

.submit-btn {
  width: 100%;
  padding: 16px;
  background: linear-gradient(135deg, #6FB3C6 0%, #7FB8C7 100%);
  color: #657166;
  border: none;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(111, 179, 198, 0.5);
}

.submit-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(111, 179, 198, 0.6);
  background: linear-gradient(135deg, #7FB8C7 0%, #6FB3C6 100%);
}

.submit-btn:active:not(:disabled) {
  transform: translateY(0);
}

.submit-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.btn-text {
  letter-spacing: 4px;
}

.loading {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  color: #657166;
}

.spinner {
  width: 20px;
  height: 20px;
  border: 3px solid rgba(101, 113, 102, 0.2);
  border-radius: 50%;
  border-top-color: #657166;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.error-alert {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 16px;
  background: #FDE8D3;
  border: 1px solid #F3C6C2;
  border-radius: 12px;
  color: #657166;
  font-size: 14px;
  animation: slideIn 0.3s ease-out;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.error-alert svg {
  width: 20px;
  height: 20px;
  flex-shrink: 0;
  color: #657166;
}

.form-footer {
  margin-top: 32px;
  text-align: center;
  font-size: 14px;
  color: #657166;
  opacity: 0.8;
}

.form-footer a {
  color: #6FB3C6;
  text-decoration: none;
  font-weight: 600;
  transition: color 0.3s ease;
}

.form-footer a:hover {
  color: #657166;
}

/* 响应式设计 */
@media (max-width: 1024px) {
  .brand-section {
    max-width: 45%;
    padding: 40px;
  }

  .brand-content h1 {
    font-size: 40px;
  }
  
  .form-section {
    padding: 40px;
  }
}

@media (max-width: 768px) {
  .brand-section {
    display: none;
  }

  .form-section {
    max-width: 100%;
    padding: 40px 24px;
    min-height: 100vh;
  }

  .form-container {
    max-width: 100%;
  }
}

/* 确保在所有设备上都没有顶部空白 */
@media (min-width: 769px) {
  .form-section {
    height: 100vh;
  }
}
</style>
