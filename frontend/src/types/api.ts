/**
 * API-related types for the market analysis application.
 */

/** HTTP Methods */
export type HttpMethod = 'GET' | 'POST' | 'PUT' | 'DELETE' | 'PATCH'

/** API Response wrapper */
export interface ApiResponse<T = any> {
  data?: T
  error?: string
  detail?: string
  message?: string
}

/** Paginated API Response */
export interface PaginatedResponse<T> {
  items: T[]
  total: number
  page: number
  page_size: number
  total_pages: number
}

/** Login Request */
export interface LoginRequest {
  username: string
  password: string
}

/** Login Response */
export interface LoginResponse {
  access_token: string
  token_type: string
  user: User
  must_change_password?: boolean
}

/** Register Request */
export interface RegisterRequest {
  username: string
  email: string
  password: string
  full_name?: string
}

/** API Error Response */
export interface ApiError {
  detail: string
  status_code: number
  timestamp?: string
}

/** Rate Limit Error Response */
export interface RateLimitError extends ApiError {
  retry_after?: string
  'X-RateLimit-Limit'?: string
  'X-RateLimit-Remaining': string
  'X-RateLimit-Reset'?: string
}

/** Axios request config with abort controller */
export interface RequestConfig {
  signal?: AbortSignal
  headers?: Record<string, string>
}

/** Watchlist operations */
export interface WatchlistItem {
  id: number
  symbol: string
  name?: string
  added_at: string
}

export interface AddToWatchlistRequest {
  symbol: string
  name?: string
}

export interface UpdateWatchlistRequest {
  name?: string
}

/** Hot Stocks Response */
export interface HotStock {
  symbol: string
  name: string
  price: number
  change: number
  change_percent: number
  volume: number
  market_cap: number
}

/** AI Settings */
export interface AIProvider {
  name: string
  display_name: string
  description: string
  models: string[]
  base_url?: string
}

export interface AISettings {
  ai_provider: string
  ai_model: string
  ai_temperature: number
  ai_max_tokens: number
  has_api_key: boolean
}

export interface AISettingsUpdate extends Omit<AISettings, 'has_api_key'> {
  ai_api_key?: string
}

export interface AIConnectionTest {
  success: boolean
  message: string
  response?: string
  error?: string
}

/** Timeframe options */
export type Timeframe = '1D' | '1W' | '1M' | '3M' | '6M' | 'YTD' | '1Y'

/** Analysis Request Parameters */
export interface AnalysisParams {
  symbol: string
  timeframe?: Timeframe
  include_news?: boolean
}
