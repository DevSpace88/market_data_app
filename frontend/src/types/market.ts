/**
 * Market data and analysis types for the financial application.
 */

import type { Timeframe } from './api'

/** Market Data */
export interface MarketData {
  symbol: string
  price: number
  change: number
  change_percent: number
  volume: number
  market_cap: number
  pe_ratio: number
  high_52w?: number
  low_52w?: number
  chart_data: number[]
  currency?: string
  currencySymbol?: string
}

/** Technical Indicators */
export interface TechnicalIndicators {
  current: IndicatorValues
  historical?: HistoricalIndicatorValues
}

export interface HistoricalIndicatorValues {
  sma_20?: Record<number, number>
  sma_50?: Record<number, number>
  bb_upper?: Record<number, number>
  bb_lower?: Record<number, number>
  bb_middle?: Record<number, number>
}

export interface IndicatorValues {
  // Moving Averages
  sma_20?: number
  sma_50?: number
  sma_200?: number
  ema_12?: number
  ema_26?: number

  // Momentum
  rsi?: number
  stoch_k?: number
  stoch_d?: number
  williams_r?: number
  cci?: number

  // Trend
  macd?: number
  macd_signal?: number
  macd_histogram?: number
  adx?: number
  plus_di?: number
  minus_di?: number

  // Volatility
  bb_upper?: number
  bb_lower?: number
  bb_middle?: number
  bb_width?: number
  bb_percent?: number
  atr?: number

  // Volume
  obv?: number
  vroc?: number
  ad_line?: number

  // Support/Resistance
  support_1?: number
  support_2?: number
  resistance_1?: number
  resistance_2?: number
  pivot_point?: number
  recent_high?: number
  recent_low?: number
}

/** Chart Pattern */
export interface Pattern {
  type: string
  confidence: number
  description: string
  timestamp: string
}

/** Trading Signal */
export interface Signal {
  type: 'BUY' | 'SELL' | 'HOLD'
  strength: 'VERY_STRONG' | 'STRONG' | 'MEDIUM' | 'WEAK'
  indicator: string
  reason: string
  timeframe: 'short' | 'medium' | 'long'
}

/** Risk Metrics */
export interface RiskMetrics {
  // Volatility
  historical_volatility_20d?: number
  atr_percentage?: number
  bb_width_percentage?: number
  volatility_regime?: 'EXTREME' | 'HIGH' | 'MODERATE' | 'LOW'

  // Drawdown
  max_drawdown?: number
  current_drawdown?: number
  drawdown_status?: 'SEVERE' | 'HIGH' | 'MODERATE' | 'NORMAL'

  // Momentum Risk
  rsi_risk?: 'EXTREME_OVERBOUGHT' | 'OVERBOUGHT' | 'NEUTRAL' | 'OVERSOLD' | 'EXTREME_OVERSOLD'
  trend_strength?: 'VERY_STRONG' | 'STRONG' | 'MODERATE' | 'WEAK'

  // Liquidity
  average_volume_20d?: number
  volume_volatility?: number

  // Price Action
  price_range_20d?: number
  gap_percentage?: number

  // Composite
  overall_risk_score?: number
  risk_level?: 'VERY_HIGH' | 'HIGH' | 'MODERATE' | 'LOW' | 'VERY_LOW'
}

/** AI Analysis */
export interface AIAnalysis {
  sentiment: 'bullish' | 'bearish' | 'neutral'
  sentiment_summary: string
  technical_analysis: string
  support_resistance: {
    support_levels: number[]
    resistance_levels: number[]
  }
  key_insights: string[]
  risk_factors: string[]
  short_term_outlook: string
}

/** Complete Market Analysis */
export interface MarketAnalysis {
  symbol: string
  timestamp: string
  timeframe: Timeframe
  market_data: MarketData
  technical_indicators: TechnicalIndicators
  patterns: Pattern[]
  signals: Signal[]
  risk_metrics: RiskMetrics
  ai_analysis?: AIAnalysis
  currency: string
  currencySymbol: string
}

/** Currency Information */
export interface CurrencyInfo {
  currency: string
  currencySymbol: string
}

/** Market Analysis Response (from API) */
export interface MarketAnalysisResponse extends MarketAnalysis {
  [key: string]: any
}

/** Chart Data Point */
export interface ChartDataPoint {
  time: number
  open: number
  high: number
  low: number
  close: number
  volume: number
}
