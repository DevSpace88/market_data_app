/**
 * Market Data Composable
 *
 * Handles fetching market data and AI analysis with caching support.
 */

import { ref } from 'vue'
import axios from 'axios'
import cacheService from '@/services/cacheService'
import type { MarketDataPoint, AIAnalysis, TechnicalIndicators } from '@/types'

/**
 * Timeframe mapping: Frontend format → Backend format
 */
const TIMEFRAME_MAP: Record<string, string> = {
  '1D': '1d',
  '1W': '5d',
  '1M': '1mo',
  '3M': '3mo',
  '6M': '6mo',
  '1Y': '1y',
  'YTD': 'ytd'
}

/**
 * Market data composable for fetching and caching market data
 */
export function useMarketData() {
  const loading = ref<boolean>(false)
  const error = ref<string | null>(null)
  const marketData = ref<MarketDataPoint[]>([])
  const technicalIndicators = ref<TechnicalIndicators>({})
  const patterns = ref<any[]>([])
  const signals = ref<any[]>([])
  const riskMetrics = ref<any | null>(null)
  const aiAnalysis = ref<AIAnalysis | null>(null)
  const currency = ref<string>('USD')
  const currencySymbol = ref<string>('$')

  /**
   * Fetch raw market data for a symbol and timeframe
   */
  async function fetchMarketData(symbol: string, timeframe: string): Promise<void> {
    if (!symbol) return

    // Check cache first
    const cachedData = cacheService.getMarketData(symbol, timeframe)
    if (cachedData) {
      console.log(`📊 Using cached market data for ${symbol} (${timeframe})`)
      marketData.value = cachedData.data || []
      currency.value = cachedData.currency || 'USD'
      currencySymbol.value = cachedData.currencySymbol || '$'
      return
    }

    loading.value = true
    error.value = null

    const tf = TIMEFRAME_MAP[timeframe] || '1mo'

    try {
      const response = await axios.get(`/api/v1/market/data/${symbol}`, {
        params: { timeframe: tf }
      })

      if (response.data) {
        marketData.value = response.data.data || []
        currency.value = response.data.currency || 'USD'
        currencySymbol.value = response.data.currencySymbol || '$'

        // Cache the data
        cacheService.setMarketData(symbol, timeframe, response.data)
      }
    } catch (err: any) {
      console.error('Error fetching market data:', err)
      error.value = err.response?.data?.detail || 'Failed to fetch market data'
    } finally {
      loading.value = false
    }
  }

  /**
   * Fetch comprehensive market analysis (indicators, patterns, signals, risk, AI)
   */
  async function fetchMarketAnalysis(symbol: string, timeframe: string): Promise<void> {
    if (!symbol) return

    // Check cache first
    const cachedAnalysis = cacheService.getAnalysis(symbol)
    if (cachedAnalysis) {
      console.log(`🤖 Using cached AI analysis for ${symbol} - saving API costs!`)
      technicalIndicators.value = cachedAnalysis.technical_indicators || {}
      patterns.value = cachedAnalysis.patterns || []
      signals.value = cachedAnalysis.signals || []
      riskMetrics.value = cachedAnalysis.risk_metrics || null
      aiAnalysis.value = cachedAnalysis.ai_analysis || null
      return
    }

    loading.value = true
    error.value = null

    try {
      const response = await axios.get(`/api/v1/market/analysis/${symbol}`, {
        params: {
          timeframe,
          include_news: true
        }
      })

      if (response.data) {
        technicalIndicators.value = response.data.technical_indicators || {}
        patterns.value = response.data.patterns || []
        signals.value = response.data.signals || []
        riskMetrics.value = response.data.risk_metrics || null
        aiAnalysis.value = response.data.ai_analysis || null

        // Cache the data
        cacheService.setAnalysis(symbol, response.data)

        // Set currency if provided
        if (response.data.currency && response.data.currencySymbol) {
          currency.value = response.data.currency
          currencySymbol.value = response.data.currencySymbol
        } else {
          console.warn('No currency data in API response. Defaulting to USD/$')
          currency.value = 'USD'
          currencySymbol.value = '$'
        }
      }
    } catch (err: any) {
      console.error('Error fetching market analysis:', err)
      error.value = err.response?.data?.detail || 'Failed to fetch market analysis'
    } finally {
      loading.value = false
    }
  }

  return {
    // State
    loading,
    error,
    marketData,
    technicalIndicators,
    patterns,
    signals,
    riskMetrics,
    aiAnalysis,
    currency,
    currencySymbol,

    // Methods
    fetchMarketData,
    fetchMarketAnalysis
  }
}
