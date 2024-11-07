// src/stores/auth.js
import { defineStore } from 'pinia'
import axios from 'axios'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: localStorage.getItem('token') || null,
    loading: false,
    error: null,
  }),

  getters: {
    isAuthenticated: (state) => !!state.token,
    getUser: (state) => state.user,
  },

  actions: {
    async login(username, password) {
      try {
        this.loading = true
        this.error = null

        const formData = new FormData()
        formData.append('username', username)
        formData.append('password', password)

        const response = await axios.post('http://localhost:8000/api/v1/auth/login', formData)

        const { access_token, user } = response.data

        this.token = access_token
        this.user = user

        localStorage.setItem('token', access_token)
        axios.defaults.headers.common['Authorization'] = `Bearer ${access_token}`

        return true
      } catch (error) {
        this.error = error.response?.data?.detail || 'Login failed'
        return false
      } finally {
        this.loading = false
      }
    },

    async register(userData) {
      try {
        this.loading = true
        this.error = null

        const response = await axios.post('http://localhost:8000/api/v1/auth/register', userData)

        // Automatisch einloggen nach Registrierung
        return await this.login(userData.username, userData.password)
      } catch (error) {
        this.error = error.response?.data?.detail || 'Registration failed'
        return false
      } finally {
        this.loading = false
      }
    },

    async checkAuth() {
      try {
        if (!this.token) return false

        axios.defaults.headers.common['Authorization'] = `Bearer ${this.token}`
        const response = await axios.get('http://localhost:8000/api/v1/auth/me')
        this.user = response.data
        return true
      } catch (error) {
        this.logout()
        return false
      }
    },

    logout() {
      this.user = null
      this.token = null
      localStorage.removeItem('token')
      delete axios.defaults.headers.common['Authorization']
    }
  }
})