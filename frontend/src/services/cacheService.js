// Cache Service für bessere Performance
class CacheService {
  constructor() {
    this.cache = new Map()
    this.defaultTTL = 5 * 60 * 1000 // 5 Minuten
  }

  set(key, value, ttl = this.defaultTTL) {
    const expiresAt = Date.now() + ttl
    this.cache.set(key, {
      value,
      expiresAt
    })
  }

  get(key) {
    const item = this.cache.get(key)
    
    if (!item) {
      return null
    }

    if (Date.now() > item.expiresAt) {
      this.cache.delete(key)
      return null
    }

    return item.value
  }

  has(key) {
    const item = this.cache.get(key)
    return item && Date.now() <= item.expiresAt
  }

  delete(key) {
    this.cache.delete(key)
  }

  clear() {
    this.cache.clear()
  }

  // Spezielle Cache-Methoden für verschiedene Datentypen
  setMarketData(symbol, timeframe, data) {
    const key = `market_data_${symbol}_${timeframe}`
    this.set(key, data, 2 * 60 * 1000) // 2 Minuten für Marktdaten
  }

  getMarketData(symbol, timeframe) {
    const key = `market_data_${symbol}_${timeframe}`
    return this.get(key)
  }

  setAnalysis(symbol, data) {
    const key = `analysis_${symbol}`
    this.set(key, data, 10 * 60 * 1000) // 10 Minuten für Analysen
  }

  getAnalysis(symbol) {
    const key = `analysis_${symbol}`
    return this.get(key)
  }

  setWatchlist(data) {
    this.set('watchlist', data, 1 * 60 * 1000) // 1 Minute für Watchlist
  }

  getWatchlist() {
    return this.get('watchlist')
  }

  setHotStocks(data) {
    this.set('hot_stocks', data, 5 * 60 * 1000) // 5 Minuten für Hot Stocks
  }

  getHotStocks() {
    return this.get('hot_stocks')
  }
}

export default new CacheService()
