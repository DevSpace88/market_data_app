/**
 * Market Store - Pinia store with TypeScript
 *
 * Orchestrates market data, WebSocket, and indicators using composables.
 * This is a thin layer that combines the functionality of:
 * - useMarketData (data fetching with caching)
 * - useMarketWebSocket (real-time updates)
 * - useMarketIndicators (individual data fetchers)
 */

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useMarketData } from '@/composables/useMarketData'
import { useMarketWebSocket } from '@/composables/useMarketWebSocket'
import { useMarketIndicators } from '@/composables/useMarketIndicators'
import { useAuthStore } from './auth'
import type { MarketDataPoint, TechnicalIndicators, AIAnalysis } from '@/types'

export const useMarketStore = defineStore('market', () => {
  // ===== State =====
  const selectedSymbol = ref<string | null>(null)
  const timeframe = ref<string>('1D')

  // Market data composable state
  const {
    loading: dataLoading,
    error: dataError,
    marketData,
    technicalIndicators,
    patterns,
    signals,
    riskMetrics,
    aiAnalysis,
    currency,
    currencySymbol,
    fetchMarketData,
    fetchMarketAnalysis
  } = useMarketData()

  // WebSocket composable state
  const {
    wsConnected,
    wsRetryAttempts,
    initializeWebSocket,
    handleMarketUpdate,
    sendTimeframeUpdate,
    cleanupWebSocket
  } = useMarketWebSocket()

  // Indicators composable state
  const {
    loadingIndicators,
    loadingPatterns,
    loadingSignals,
    loadingRiskMetrics,
    error: indicatorsError,
    fetchIndicators,
    fetchPatterns,
    fetchSignals,
    fetchRiskMetrics
  } = useMarketIndicators()

  // ===== Getters =====
  const loading = computed(() => dataLoading.value)

  const error = computed(() => dataError.value || indicatorsError.value)

  const priceChange = computed(() => {
    if (!marketData.value.length) return 0
    const latest = marketData.value[marketData.value.length - 1]
    const previous = marketData.value[marketData.value.length - 2]
    if (!latest || !previous) return 0
    return ((latest.close - previous.close) / previous.close) * 100
  })

  const isConnected = computed(() => wsConnected.value)

  const currentPrice = computed(() => {
    if (!marketData.value.length) return 0
    return marketData.value[marketData.value.length - 1].close
  })

  // ===== Actions =====

  /**
   * Load market data for a symbol (uses cache when available)
   */
  async function loadMarketData(symbol: string, tf: string): Promise<void> {
    if (!symbol) return
    selectedSymbol.value = symbol
    timeframe.value = tf
    await fetchMarketData(symbol, tf)
  }

  /**
   * Load full market analysis (indicators, patterns, signals, risk, AI)
   */
  async function loadMarketAnalysis(symbol: string, tf: string): Promise<void> {
    if (!symbol) return
    selectedSymbol.value = symbol
    timeframe.value = tf
    await fetchMarketAnalysis(symbol, tf)
  }

  /**
   * Change timeframe and reload data
   */
  function setTimeframe(tf: string): void {
    if (timeframe.value === tf) return
    timeframe.value = tf

    if (selectedSymbol.value) {
      loadMarketData(selectedSymbol.value, tf)
      loadMarketAnalysis(selectedSymbol.value, tf)
      sendTimeframeUpdate(tf)
    }
  }

  /**
   * Initialize WebSocket for real-time updates
   */
  function initWebSocket(symbol: string): void {
    const authStore = useAuthStore()
    initializeWebSocket(symbol, authStore.token)
  }

  /**
   * Handle WebSocket market updates
   */
  function onMarketUpdate(data: any): void {
    handleMarketUpdate(data, {
      onData: (newData) => { marketData.value = newData },
      onTechnical: (indicators) => { technicalIndicators.value = indicators },
      onPatterns: (newPatterns) => { patterns.value = newPatterns },
      onSignals: (newSignals) => { signals.value = newSignals },
      onCurrency: (curr, sym) => {
        currency.value = curr
        currencySymbol.value = sym
      }
    })
  }

  /**
   * Fetch indicators individually
   */
  async function loadIndicators(symbol: string, tf?: string): Promise<void> {
    const result = await fetchIndicators(symbol, tf || timeframe.value)
    if (result) {
      technicalIndicators.value = result
    }
  }

  /**
   * Fetch patterns individually
   */
  async function loadPatterns(symbol: string, tf?: string): Promise<void> {
    const result = await fetchPatterns(symbol, tf || timeframe.value)
    if (result) {
      patterns.value = result
    }
  }

  /**
   * Fetch signals individually
   */
  async function loadSignals(symbol: string, tf?: string): Promise<void> {
    const result = await fetchSignals(symbol, tf || timeframe.value)
    if (result) {
      signals.value = result
    }
  }

  /**
   * Fetch risk metrics individually
   */
  async function loadRiskMetrics(symbol: string, tf?: string): Promise<void> {
    const result = await fetchRiskMetrics(symbol, tf || timeframe.value)
    if (result) {
      riskMetrics.value = result
    }
  }

  /**
   * Get cache status for debugging
   */
  function getCacheStatus() {
    return {
      marketData: `market_data_${selectedSymbol.value}_${timeframe.value}`,
      analysis: `analysis_${selectedSymbol.value}`,
      watchlist: 'watchlist',
      hotStocks: 'hot_stocks'
    }
  }

  return {
    // State
    selectedSymbol,
    timeframe,
    marketData,
    technicalIndicators,
    patterns,
    signals,
    riskMetrics,
    aiAnalysis,
    currency,
    currencySymbol,
    wsConnected,
    wsRetryAttempts,
    loadingIndicators,
    loadingPatterns,
    loadingSignals,
    loadingRiskMetrics,

    // Getters
    loading,
    error,
    priceChange,
    isConnected,
    currentPrice,

    // Actions
    loadMarketData,
    loadMarketAnalysis,
    setTimeframe,
    initWebSocket,
    onMarketUpdate,
    loadIndicators,
    loadPatterns,
    loadSignals,
    loadRiskMetrics,
    cleanupWebSocket,
    getCacheStatus
  }
})
