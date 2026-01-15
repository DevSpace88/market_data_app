/**
 * Investment Decision Engine Composables

 * Provides composables for:
 * - Master Investment Score
 * - Sentiment Analysis
 * - Unusual Activity Detection
 * - Signal Performance Tracking
 */

import { ref, computed, type Ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import axios from 'axios'

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

// ============================================================================
// Types
// ============================================================================

export interface ScoreBreakdown {
  score: number
  weight: number
  label: string
}

export interface TopFactor {
  name: string
  score: number
  contribution: number
}

export interface MasterScoreData {
  master_score: number
  recommendation: 'STRONG_BUY' | 'BUY' | 'HOLD' | 'SELL' | 'STRONG_SELL'
  confidence: 'HIGH' | 'MEDIUM' | 'LOW'
  breakdown: {
    short_term: ScoreBreakdown
    medium_term: ScoreBreakdown
    long_term: ScoreBreakdown
    risk: ScoreBreakdown
  }
  top_factors: TopFactor[]
  timestamp: string
}

export interface SentimentBreakdown {
  score: number
  count: number
  positive: number
  negative: number
  neutral: number
}

export interface TopHeadline {
  title: string
  sentiment_contribution: string
  timestamp?: string
  link?: string
}

export interface SocialBuzz {
  score: number
  trend: 'RISING' | 'STABLE' | 'FALLING'
  mentions_24h: number
}

export interface SentimentData {
  symbol: string
  sentiment_score: number
  sentiment_label: string
  confidence: 'HIGH' | 'MEDIUM' | 'LOW'
  breakdown: {
    news: SentimentBreakdown
  }
  top_headlines: TopHeadline[]
  social_buzz: SocialBuzz
  price_correlation?: number
  data_sources: string
  timestamp: string
  warning?: string
}

export interface ActivityDetails {
  current_volume?: number
  average_volume?: number
  ratio?: number
  z_score?: number
  deviation?: string
  current_price?: number
  average_price?: number
  daily_change_percent?: number
}

export interface UnusualActivityItem {
  type: 'VOLUME_SPIKE' | 'PRICE_ANOMALY' | 'OPTIONS_FLOW' | 'DARK_POOL'
  severity: 'LOW' | 'MEDIUM' | 'HIGH' | 'EXTREME'
  confidence: number
  details: ActivityDetails
  price_at_detection?: number
  timestamp?: string
  interpretation?: string
}

export interface UnusualActivityData {
  symbol: string
  has_unusual_activity: boolean
  activities: UnusualActivityItem[]
  overall_severity: 'LOW' | 'MEDIUM' | 'HIGH' | 'EXTREME' | 'NONE'
  timestamp: string
  warning?: string
}

export interface PerformanceByType {
  count: number
  win_rate: number
  avg_return: number
}

export interface OverallPerformance {
  total_signals: number
  profitable_signals: number
  win_rate: number
  avg_return_percent: number
  avg_benchmark_return_percent: number
  avg_excess_return_percent: number
}

export interface SignalPerformanceData {
  overall: OverallPerformance
  by_signal_type: Record<string, PerformanceByType>
  by_timeframe: Record<string, PerformanceByType>
  vs_benchmark: {
    outperformed: number
    underperformed: number
    beat_rate: number
  }
  timestamp: string
  message?: string
}

export interface InvestmentDecisionData {
  symbol: string
  master_score: MasterScoreData
  sentiment?: SentimentData
  unusual_activity?: UnusualActivityData
  signal_performance?: SignalPerformanceData
  generated_at: string
  data_quality: 'HIGH' | 'MEDIUM' | 'LOW'
}

// ============================================================================
// Master Investment Score Composable
// ============================================================================

export function useMasterScore() {
  const masterScore: Ref<MasterScoreData | null> = ref(null)
  const isLoading = ref(false)
  const error: Ref<string | null> = ref(null)

  const authStore = useAuthStore()

  const scoreColor = computed(() => {
    if (!masterScore.value) return 'gray'
    const score = masterScore.value.master_score
    if (score >= 80) return 'green'
    if (score >= 60) return 'lime'
    if (score >= 40) return 'yellow'
    if (score >= 20) return 'orange'
    return 'red'
  })

  const recommendationLabel = computed(() => {
    if (!masterScore.value) return ''
    const labels = {
      STRONG_BUY: 'Strong Buy',
      BUY: 'Buy',
      HOLD: 'Hold',
      SELL: 'Sell',
      STRONG_SELL: 'Strong Sell'
    }
    return labels[masterScore.value.recommendation] || masterScore.value.recommendation
  })

  const fetchMasterScore = async (symbol: string, timeframe = '3mo') => {
    isLoading.value = true
    error.value = null

    try {
      const token = authStore.token
      const response = await axios.get<MasterScoreData>(
        `${API_BASE}/api/v1/investment-engine/master-score/${symbol}`,
        {
          params: { timeframe },
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
      )

      masterScore.value = response.data
      return response.data
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to fetch master score'
      console.error('Error fetching master score:', err)
      throw err
    } finally {
      isLoading.value = false
    }
  }

  return {
    masterScore,
    isLoading,
    error,
    scoreColor,
    recommendationLabel,
    fetchMasterScore
  }
}

// ============================================================================
// Sentiment Analysis Composable
// ============================================================================

export function useSentiment() {
  const sentiment: Ref<SentimentData | null> = ref(null)
  const isLoading = ref(false)
  const error: Ref<string | null> = ref(null)

  const authStore = useAuthStore()

  const sentimentColor = computed(() => {
    if (!sentiment.value) return 'gray'
    const score = sentiment.value.sentiment_score
    if (score >= 60) return 'green'
    if (score >= 30) return 'lime'
    if (score >= -30) return 'yellow'
    if (score >= -60) return 'orange'
    return 'red'
  })

  const sentimentIcon = computed(() => {
    if (!sentiment.value) return 'minus'
    const score = sentiment.value.sentiment_score
    if (score >= 60) return 'trending-up'
    if (score >= 30) return 'arrow-up'
    if (score >= -30) return 'minus'
    if (score >= -60) return 'arrow-down'
    return 'trending-down'
  })

  const fetchSentiment = async (symbol: string, useAi = false) => {
    isLoading.value = true
    error.value = null

    try {
      const token = authStore.token
      const response = await axios.get<SentimentData>(
        `${API_BASE}/api/v1/investment-engine/sentiment/${symbol}`,
        {
          params: { use_ai: useAi },
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
      )

      sentiment.value = response.data
      return response.data
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to fetch sentiment'
      console.error('Error fetching sentiment:', err)
      // Return null instead of throwing - sentiment is optional
      sentiment.value = null
      return null
    } finally {
      isLoading.value = false
    }
  }

  return {
    sentiment,
    isLoading,
    error,
    sentimentColor,
    sentimentIcon,
    fetchSentiment
  }
}

// ============================================================================
// Unusual Activity Composable
// ============================================================================

export function useUnusualActivity() {
  const unusualActivity: Ref<UnusualActivityData | null> = ref(null)
  const isLoading = ref(false)
  const error: Ref<string | null> = ref(null)

  const authStore = useAuthStore()

  const severityColor = computed(() => {
    if (!unusualActivity.value) return 'gray'
    const severity = unusualActivity.value.overall_severity
    const colors = {
      NONE: 'gray',
      LOW: 'blue',
      MEDIUM: 'yellow',
      HIGH: 'orange',
      EXTREME: 'red'
    }
    return colors[severity] || 'gray'
  })

  const fetchUnusualActivity = async (symbol: string, timeframe = '3mo') => {
    isLoading.value = true
    error.value = null

    try {
      const token = authStore.token
      const response = await axios.get<UnusualActivityData>(
        `${API_BASE}/api/v1/investment-engine/unusual-activity/${symbol}`,
        {
          params: { timeframe },
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
      )

      unusualActivity.value = response.data
      return response.data
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to fetch unusual activity'
      console.error('Error fetching unusual activity:', err)
      // Return null instead of throwing - activity is optional
      unusualActivity.value = null
      return null
    } finally {
      isLoading.value = false
    }
  }

  return {
    unusualActivity,
    isLoading,
    error,
    severityColor,
    fetchUnusualActivity
  }
}

// ============================================================================
// Signal Performance Composable
// ============================================================================

export function useSignalPerformance() {
  const signalPerformance: Ref<SignalPerformanceData | null> = ref(null)
  const isLoading = ref(false)
  const error: Ref<string | null> = ref(null)

  const authStore = useAuthStore()

  const winRateColor = computed(() => {
    if (!signalPerformance.value) return 'gray'
    const winRate = signalPerformance.value.overall.win_rate
    if (winRate >= 70) return 'green'
    if (winRate >= 55) return 'lime'
    if (winRate >= 45) return 'yellow'
    return 'red'
  })

  const fetchSignalPerformance = async (symbol?: string) => {
    isLoading.value = true
    error.value = null

    try {
      const token = authStore.token
      const response = await axios.get<SignalPerformanceData>(
        `${API_BASE}/api/v1/investment-engine/signal-performance`,
        {
          params: { symbol },
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
      )

      signalPerformance.value = response.data
      return response.data
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to fetch signal performance'
      console.error('Error fetching signal performance:', err)
      // Return null instead of throwing - performance is optional
      signalPerformance.value = null
      return null
    } finally {
      isLoading.value = false
    }
  }

  return {
    signalPerformance,
    isLoading,
    error,
    winRateColor,
    fetchSignalPerformance
  }
}

// ============================================================================
// Combined Investment Decision Composable
// ============================================================================

export function useInvestmentDecision() {
  const decisionData: Ref<InvestmentDecisionData | null> = ref(null)
  const isLoading = ref(false)
  const error: Ref<string | null> = ref(null)

  const authStore = useAuthStore()

  // Individual composables
  const { masterScore, fetchMasterScore } = useMasterScore()
  const { sentiment, fetchSentiment } = useSentiment()
  const { unusualActivity, fetchUnusualActivity } = useUnusualActivity()
  const { signalPerformance, fetchSignalPerformance } = useSignalPerformance()

  const fetchInvestmentDecision = async (
    symbol: string,
    options: {
      timeframe?: string
      includeSentiment?: boolean
      includeActivity?: boolean
    } = {}
  ) => {
    isLoading.value = true
    error.value = null

    const {
      timeframe = '3mo',
      includeSentiment = true,
      includeActivity = true
    } = options

    try {
      const token = authStore.token

      // Use the combined endpoint
      const response = await axios.get<InvestmentDecisionData>(
        `${API_BASE}/api/v1/investment-engine/decision/${symbol}`,
        {
          params: {
            timeframe,
            include_sentiment: includeSentiment,
            include_activity: includeActivity
          },
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
      )

      decisionData.value = response.data

      // Update individual refs
      masterScore.value = response.data.master_score
      sentiment.value = response.data.sentiment || null
      unusualActivity.value = response.data.unusual_activity || null
      signalPerformance.value = response.data.signal_performance || null

      return response.data
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to fetch investment decision'
      console.error('Error fetching investment decision:', err)

      // Fallback: Try to fetch individual components
      try {
        await fetchMasterScore(symbol, timeframe)
        if (includeSentiment) await fetchSentiment(symbol)
        if (includeActivity) await fetchUnusualActivity(symbol, timeframe)
        await fetchSignalPerformance(symbol)

        decisionData.value = {
          symbol,
          master_score: masterScore.value!,
          sentiment: sentiment.value || undefined,
          unusual_activity: unusualActivity.value || undefined,
          signal_performance: signalPerformance.value || undefined,
          generated_at: new Date().toISOString(),
          data_quality: 'MEDIUM'
        }
      } catch (fallbackErr) {
        console.error('Fallback fetch also failed:', fallbackErr)
        throw err
      }
    } finally {
      isLoading.value = false
    }
  }

  return {
    decisionData,
    masterScore,
    sentiment,
    unusualActivity,
    signalPerformance,
    isLoading,
    error,
    fetchInvestmentDecision
  }
}
