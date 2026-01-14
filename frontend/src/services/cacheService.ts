/**
 * Cache Service for better performance
 *
 * Provides TTL-based caching for various data types with different expiration times.
 */

interface CacheItem<T = any> {
  value: T
  expiresAt: number
}

class CacheService {
  private cache: Map<string, CacheItem>
  private defaultTTL: number = 5 * 60 * 1000 // 5 minutes

  constructor() {
    this.cache = new Map()
  }

  /**
   * Set a value in the cache with optional TTL
   * @param key Cache key
   * @param value Value to cache
   * @param ttl Time to live in milliseconds (default: 5 minutes)
   */
  set<T = any>(key: string, value: T, ttl?: number): void {
    const expiresAt = Date.now() + (ttl ?? this.defaultTTL)
    this.cache.set(key, {
      value,
      expiresAt
    })
  }

  /**
   * Get a value from the cache
   * @param key Cache key
   * @returns Cached value or null if not found/expired
   */
  get<T = any>(key: string): T | null {
    const item = this.cache.get(key) as CacheItem<T> | undefined

    if (!item) {
      return null
    }

    if (Date.now() > item.expiresAt) {
      this.cache.delete(key)
      return null
    }

    return item.value
  }

  /**
   * Check if a key exists and is not expired
   * @param key Cache key
   * @returns True if key exists and is valid
   */
  has(key: string): boolean {
    const item = this.cache.get(key)
    return item !== undefined && Date.now() <= item.expiresAt
  }

  /**
   * Delete a key from the cache
   * @param key Cache key
   */
  delete(key: string): void {
    this.cache.delete(key)
  }

  /**
   * Clear all cache entries
   */
  clear(): void {
    this.cache.clear()
  }

  // ===== Specific cache methods for different data types =====

  /**
   * Cache market data (2 minutes TTL)
   */
  setMarketData<T = any>(symbol: string, timeframe: string, data: T): void {
    const key = `market_data_${symbol}_${timeframe}`
    this.set(key, data, 2 * 60 * 1000)
  }

  getMarketData<T = any>(symbol: string, timeframe: string): T | null {
    const key = `market_data_${symbol}_${timeframe}`
    return this.get<T>(key)
  }

  /**
   * Cache AI analysis (10 minutes TTL)
   */
  setAnalysis<T = any>(symbol: string, data: T): void {
    const key = `analysis_${symbol}`
    this.set(key, data, 10 * 60 * 1000)
  }

  getAnalysis<T = any>(symbol: string): T | null {
    const key = `analysis_${symbol}`
    return this.get<T>(key)
  }

  /**
   * Cache watchlist (1 minute TTL)
   */
  setWatchlist<T = any>(data: T): void {
    this.set('watchlist', data, 1 * 60 * 1000)
  }

  getWatchlist<T = any>(): T | null {
    return this.get<T>('watchlist')
  }

  /**
   * Cache hot stocks (5 minutes TTL)
   */
  setHotStocks<T = any>(data: T): void {
    this.set('hot_stocks', data, 5 * 60 * 1000)
  }

  getHotStocks<T = any>(): T | null {
    return this.get<T>('hot_stocks')
  }

  /**
   * Get cache status for debugging
   */
  getCacheStatus(): { size: number; keys: string[] } {
    return {
      size: this.cache.size,
      keys: Array.from(this.cache.keys())
    }
  }
}

// Singleton instance
export default new CacheService()
