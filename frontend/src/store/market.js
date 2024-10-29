import { defineStore } from 'pinia'
import axios from 'axios'

export const useMarketStore = defineStore('market', {
  state: () => ({
    marketData: [],
    technicalIndicators: [],
    patterns: [],
    signals: [],
    aiAnalysis: null,
    selectedSymbol: null,
    timeframe: '1D',
    loading: false,
    error: null,
    websocket: null
  }),

  actions: {
    async fetchMarketData(symbol) {
      this.loading = true
      this.error = null
      try {
        const response = await axios.get(`/api/v1/market/data/${symbol}`, {
          params: {
            timeframe: this.timeframe
          }
        })
        this.marketData = response.data.data
        this.selectedSymbol = symbol
      } catch (error) {
        this.error = error.response?.data?.detail || 'Failed to fetch market data'
        console.error('Error fetching market data:', error)
      } finally {
        this.loading = false
      }
    },

    async fetchMarketAnalysis(symbol) {
      this.loading = true
      this.error = null
      try {
        const response = await axios.get(`/api/v1/market/analysis/${symbol}`)
        const { technical_indicators, patterns, signals, ai_analysis } = response.data

        this.technicalIndicators = technical_indicators
        this.patterns = patterns
        this.signals = signals
        this.aiAnalysis = ai_analysis
      } catch (error) {
        this.error = error.response?.data?.detail || 'Failed to fetch market analysis'
        console.error('Error fetching market analysis:', error)
      } finally {
        this.loading = false
      }
    },

    initializeWebSocket(symbol) {
      this.cleanup()

      const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
      const wsUrl = `${protocol}//${window.location.host}/api/v1/ws/market/${symbol}`

      this.websocket = new WebSocket(wsUrl)

      this.websocket.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data)
          if (data.type === 'market_update') {
            this.marketData = data.data
          }
        } catch (error) {
          console.error('WebSocket message error:', error)
        }
      }

      this.websocket.onerror = (error) => {
        this.error = 'WebSocket connection error'
        console.error('WebSocket error:', error)
        setTimeout(() => this.initializeWebSocket(symbol), 5000)
      }

      this.websocket.onclose = () => {
        console.log('WebSocket connection closed')
        setTimeout(() => this.initializeWebSocket(symbol), 5000)
      }
    },

    setTimeframe(timeframe) {
      this.timeframe = timeframe
      if (this.selectedSymbol) {
        this.fetchMarketData(this.selectedSymbol)
      }
    },

    cleanup() {
      if (this.websocket) {
        this.websocket.close()
        this.websocket = null
      }
    }
  }
})
