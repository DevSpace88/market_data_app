import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import i18n from './i18n'
import axios from 'axios'
import type { App as VueApp } from 'vue'
import './assets/styles/main.css'

// Axios Configuration with TypeScript
// In development, use empty baseURL to let Vite proxy handle requests
// In production, use the actual backend URL
axios.defaults.baseURL = import.meta.env.MODE === 'production'
  ? (import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000')
  : '/'
axios.defaults.headers.common['Accept'] = 'application/json'
axios.defaults.withCredentials = true // Important: Send httpOnly cookies

// Request interceptor - inject Authorization header with token
axios.interceptors.request.use(
  (config) => {
    // Get token from localStorage (fallback for cross-origin scenarios)
    const token = localStorage.getItem('auth_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
      console.log('[Auth] ✅ Token added to Authorization header:', {
        url: config.url,
        authHeader: config.headers.Authorization
      })
    } else {
      console.log('[Auth] ❌ No token found in localStorage. Available keys:', Object.keys(localStorage))
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor with 401 handling
axios.interceptors.response.use(
  (response) => {
    return response
  },
  async (error) => {
    // Handle 401 Unauthorized - redirect to login
    if (error.response?.status === 401 && router.currentRoute.value.meta?.requiresAuth) {
      router.push('/login')
    }
    return Promise.reject(error)
  }
)

const app: VueApp = createApp(App)
const pinia = createPinia()

// v-click-outside directive
app.directive('click-outside', {
  beforeMount(el: HTMLElement, binding: any) {
    el.clickOutsideHandler = (event: Event) => {
      if (!(el === event.target || el.contains(event.target as Node))) {
        binding.value(event)
      }
    }
    document.addEventListener('click', el.clickOutsideHandler)
  },
  unmounted(el: HTMLElement) {
    document.removeEventListener('click', el.clickOutsideHandler)
    delete el.clickOutsideHandler
  }
})

app.use(pinia)
app.use(router)
app.use(i18n)

// Set initial locale from localStorage
const savedLanguage = localStorage.getItem('language') || 'en'
i18n.global.locale.value = savedLanguage

app.mount('#app')
