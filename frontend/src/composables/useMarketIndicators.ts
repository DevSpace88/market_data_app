/**
 * Market Indicators Composable
 *
 * Fetches individual data types: indicators, patterns, signals, risk metrics.
 */

import { ref } from 'vue'
import axios from 'axios'

/**
 * Individual market data fetchers with separate loading states
 */
export function useMarketIndicators() {
  const loadingIndicators = ref<boolean>(false)
  const loadingPatterns = ref<boolean>(false)
  const loadingSignals = ref<boolean>(false)
  const loadingRiskMetrics = ref<boolean>(false)
  const error = ref<string | null>(null)

  /**
   * Fetch technical indicators for a symbol
   */
  async function fetchIndicators(
    symbol: string,
    timeframe: string = '1M'
  ): Promise<any | null> {
    try {
      loadingIndicators.value = true
      error.value = null

      const response = await axios.get(`/api/v1/market/indicators/${symbol}`, {
        params: { timeframe }
      })

      return response.data.technical_indicators || {}
    } catch (err: any) {
      console.error('Error fetching indicators:', err)
      error.value = err.response?.data?.detail || 'Failed to fetch indicators'
      return null
    } finally {
      loadingIndicators.value = false
    }
  }

  /**
   * Fetch detected patterns for a symbol
   */
  async function fetchPatterns(
    symbol: string,
    timeframe: string = '1M'
  ): Promise<any[] | null> {
    try {
      loadingPatterns.value = true
      error.value = null

      const response = await axios.get(`/api/v1/market/patterns/${symbol}`, {
        params: { timeframe }
      })

      return response.data.patterns || []
    } catch (err: any) {
      console.error('Error fetching patterns:', err)
      error.value = err.response?.data?.detail || 'Failed to fetch patterns'
      return null
    } finally {
      loadingPatterns.value = false
    }
  }

  /**
   * Fetch trading signals for a symbol
   */
  async function fetchSignals(
    symbol: string,
    timeframe: string = '1M'
  ): Promise<any[] | null> {
    try {
      loadingSignals.value = true
      error.value = null

      const response = await axios.get(`/api/v1/market/signals/${symbol}`, {
        params: { timeframe }
      })

      return response.data.signals || []
    } catch (err: any) {
      console.error('Error fetching signals:', err)
      error.value = err.response?.data?.detail || 'Failed to fetch signals'
      return null
    } finally {
      loadingSignals.value = false
    }
  }

  /**
   * Fetch risk metrics for a symbol
   */
  async function fetchRiskMetrics(
    symbol: string,
    timeframe: string = '1M'
  ): Promise<any | null> {
    try {
      loadingRiskMetrics.value = true
      error.value = null

      const response = await axios.get(`/api/v1/market/risk-metrics/${symbol}`, {
        params: { timeframe }
      })

      return response.data.risk_metrics || null
    } catch (err: any) {
      console.error('Error fetching risk metrics:', err)
      error.value = err.response?.data?.detail || 'Failed to fetch risk metrics'
      return null
    } finally {
      loadingRiskMetrics.value = false
    }
  }

  return {
    // State
    loadingIndicators,
    loadingPatterns,
    loadingSignals,
    loadingRiskMetrics,
    error,

    // Methods
    fetchIndicators,
    fetchPatterns,
    fetchSignals,
    fetchRiskMetrics
  }
}
