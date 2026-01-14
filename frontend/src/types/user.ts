/**
 * User-related types for the market analysis application.
 */

/** User entity */
export interface User {
  id: number
  username: string
  email: string
  full_name?: string
  is_active: boolean
  is_admin: boolean
  must_change_password?: boolean
  created_at: string
  updated_at?: string
}

/** User create request */
export interface UserCreate {
  username: string
  email: string
  password: string
  full_name?: string
}

/** User update request */
export interface UserUpdate {
  email?: string
  full_name?: string
  password?: string
}

/** Auth state in Pinia store */
export interface AuthState {
  user: User | null
  isAuthenticated: boolean
  isLoading: boolean
  error: string | null
}

/** Token data from JWT */
export interface TokenData {
  sub: string
  exp: number
  iat?: number
}
