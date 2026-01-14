/**
 * Authentication Store - Pinia store with TypeScript
 *
 * Handles user authentication state, login, logout, and token management.
 * Uses httpOnly cookies for token storage (no localStorage for tokens).
 */

import { defineStore } from 'pinia'
import axios from 'axios'
import type { User, AuthState } from '@/types'

interface AuthStoreState {
  // Token is kept in memory for reference, but primary auth is via httpOnly cookies
  token: string | null
  user: User | null
  isLoading: boolean
  error: string | null
}

interface LoginRequest {
  username: string
  password: string
}

interface RegisterRequest {
  username: string
  email: string
  password: string
  full_name?: string
}

interface LoginResponse {
  access_token: string
  token_type: string
  user: User
  must_change_password?: boolean
}

export const useAuthStore = defineStore('auth', {
  state: (): AuthStoreState => ({
    user: null,
    token: null, // Stored in memory and localStorage as fallback
    isLoading: false,
    error: null
  }),

  getters: {
    /**
     * Check if user is authenticated (has valid user data)
     */
    isAuthenticated: (state): boolean => {
      return !!state.user && !!state.user.is_active
    },

    /**
     * Get current user
     */
    getUser: (state): User | null => {
      return state.user
    },

    /**
     * Check if user must change password
     */
    mustChangePassword: (state): boolean => {
      return state.user?.must_change_password || false
    },

    /**
     * Check if user is admin
     */
    isAdmin: (state): boolean => {
      return state.user?.is_admin || false
    }
  },

  actions: {
    /**
     * Login user with username and password
     * Token is stored in httpOnly cookie by the backend
     */
    async login(username: string, password: string): Promise<boolean> {
      try {
        this.isLoading = true
        this.error = null

        const formData = new FormData()
        formData.append('username', username)
        formData.append('password', password)

        const response = await axios.post<LoginResponse>('/api/v1/auth/login', formData)

        const { access_token, user } = response.data

        // Store token in memory and localStorage (fallback for cross-origin)
        this.token = access_token
        localStorage.setItem('auth_token', access_token)
        this.user = user

        return true
      } catch (error: any) {
        console.error('Login error:', error.response || error)
        this.error = error.response?.data?.detail || 'Login failed'
        return false
      } finally {
        this.isLoading = false
      }
    },

    /**
     * Register a new user
     */
    async register(userData: RegisterRequest): Promise<boolean> {
      try {
        this.isLoading = true
        this.error = null

        const response = await axios.post<{ id: number; username: string; email: string }>('/api/v1/auth/register', userData)

        // Auto-login after registration
        return await this.login(userData.username, userData.password)
      } catch (error: any) {
        console.error('Registration error:', error.response || error)
        this.error = error.response?.data?.detail || 'Registration failed'
        return false
      } finally {
        this.isLoading = false
      }
    },

    /**
     * Check authentication status on app load
     * Validates session with backend via httpOnly cookie
     */
    async checkAuth(): Promise<boolean> {
      try {
        this.isLoading = true

        // Try to get token from localStorage first
        const storedToken = localStorage.getItem('auth_token')
        if (storedToken) {
          this.token = storedToken
        }

        // Backend validates httpOnly cookie OR Authorization header
        const config = storedToken 
          ? { headers: { Authorization: `Bearer ${storedToken}` } }
          : {}
          
        console.log('[Auth Store] Checking auth with token:', storedToken ? 'Token present' : 'No token')
        
        const response = await axios.get<User>('/api/v1/auth/me', config)

        this.user = response.data
        return true
      } catch (error: any) {
        console.error('Auth check error:', error.response?.status, error.response?.data)
        // Only clear token if it's a real 401 (unauthorized), not network error
        if (error.response?.status === 401) {
          console.warn('Token invalid, clearing...')
          this.logout()
        }
        return false
      } finally {
        this.isLoading = false
      }
    },

    /**
     * Logout user
     * Clears local state and backend clears httpOnly cookie
     */
    async logout(): Promise<void> {
      try {
        // Call backend logout endpoint to clear httpOnly cookie
        await axios.post('/api/v1/auth/logout')
      } catch (error) {
        console.error('Logout error:', error)
      } finally {
        // Clear local state regardless of API call result
        this.user = null
        this.token = null
        localStorage.removeItem('auth_token')
        this.error = null
      }
    },

    /**
     * Update user profile
     */
    async updateProfile(userData: Partial<User>): Promise<boolean> {
      try {
        this.isLoading = true
        this.error = null

        const response = await axios.put<User>('/api/v1/auth/me', userData)

        this.user = response.data
        return true
      } catch (error: any) {
        console.error('Profile update error:', error.response || error)
        this.error = error.response?.data?.detail || 'Update failed'
        return false
      } finally {
        this.isLoading = false
      }
    },

    /**
     * Clear error state
     */
    clearError(): void {
      this.error = null
    }
  }
})
