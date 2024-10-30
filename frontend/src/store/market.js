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
    websocket: null,
    connectionStatus: 'disconnected', // 'connected', 'disconnected', 'connecting', 'error'
    lastUpdateTimestamp: null
  }),

  getters: {
    isConnected: (state) => state.connectionStatus === 'connected',
    latestPrice: (state) => {
      if (!state.marketData.length) return null
      return state.marketData[state.marketData.length - 1].close
    },
    priceChange: (state) => {
      if (state.marketData.length < 2) return 0
      const latest = state.marketData[state.marketData.length - 1].close
      const previous = state.marketData[state.marketData.length - 2].close
      return ((latest - previous) / previous) * 100
    }
  },

  actions: {
    async fetchMarketData(symbol) {
      if (!symbol) return

      this.loading = true
      this.error = null

      try {
        const response = await axios.get(`/api/v1/market/data/${symbol}`, {
          params: {
            timeframe: this.timeframe
          }
        })

        if (response.data?.data) {
          this.marketData = response.data.data
          this.selectedSymbol = symbol
        }
      } catch (error) {
        this.error = error.response?.data?.detail || 'Failed to fetch market data'
        console.error('Error fetching market data:', error)
      } finally {
        this.loading = false
      }
    },

    async fetchMarketAnalysis(symbol) {
      if (!symbol) return

      this.loading = true
      this.error = null

      try {
        const response = await axios.get(`/api/v1/market/analysis/${symbol}`)

        if (response.data) {
          const {
            technical_indicators,
            patterns,
            signals,
            ai_analysis,
            market_data
          } = response.data

          this.technicalIndicators = technical_indicators || {}
          this.patterns = patterns || []
          this.signals = signals || []
          this.aiAnalysis = ai_analysis || null

          // Update market data if newer
          if (market_data?.length) {
            this.marketData = market_data
          }
        }
      } catch (error) {
        this.error = error.response?.data?.detail || 'Failed to fetch market analysis'
        console.error('Error fetching market analysis:', error)
      } finally {
        this.loading = false
      }
    },

    initializeWebSocket(symbol) {
      if (!symbol) return

      this.cleanup()
      this.connectionStatus = 'connecting'

      const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
      const host = window.location.host
      const wsUrl = `${protocol}//${host}/api/v1/ws/market/${symbol}`

      try {
        this.websocket = new WebSocket(wsUrl)

        this.websocket.onopen = () => {
          console.log('WebSocket connected')
          this.connectionStatus = 'connected'
        }

        this.websocket.onmessage = (event) => {
          try {
            const data = JSON.parse(event.data)

            switch (data.type) {
              case 'initial_data':
                this.handleInitialData(data)
                break

              case 'market_update':
                this.handleMarketUpdate(data)
                break

              case 'error':
                this.handleWebSocketError(data)
                break

              default:
                console.warn('Unknown message type:', data.type)
            }

            this.lastUpdateTimestamp = new Date()
          } catch (error) {
            console.error('WebSocket message error:', error)
          }
        }

        this.websocket.onerror = (error) => {
          console.error('WebSocket error:', error)
          this.error = 'WebSocket connection error'
          this.connectionStatus = 'error'
        }

        this.websocket.onclose = () => {
          console.log('WebSocket connection closed')
          this.connectionStatus = 'disconnected'

          // Reconnection logic
          if (this.selectedSymbol) {
            setTimeout(() => {
              console.log('Attempting to reconnect...')
              this.initializeWebSocket(this.selectedSymbol)
            }, 5000)
          }
        }

        // Setup ping interval to keep connection alive
        this.startPingInterval()

      } catch (error) {
        console.error('WebSocket initialization error:', error)
        this.connectionStatus = 'error'
      }
    },

    handleInitialData(data) {
      if (data.data) {
        this.marketData = data.data
      }
    },

    handleMarketUpdate(data) {
      if (data.data) {
        this.marketData = data.data
      }
      if (data.technical) {
        this.technicalIndicators = data.technical
      }
      if (data.patterns) {
        this.patterns = data.patterns
      }
      if (data.signals) {
        this.signals = data.signals
      }
    },

    handleWebSocketError(data) {
      this.error = data.message || 'WebSocket error occurred'
      console.error('WebSocket error message:', data)
    },

    startPingInterval() {
      this.pingInterval = setInterval(() => {
        if (this.websocket?.readyState === WebSocket.OPEN) {
          this.websocket.send(JSON.stringify({ type: 'ping' }))
        }
      }, 30000) // Ping every 30 seconds
    },

    setTimeframe(timeframe) {
      if (this.timeframe === timeframe) return

      this.timeframe = timeframe

      // Notify server about timeframe change
      if (this.websocket?.readyState === WebSocket.OPEN) {
        this.websocket.send(JSON.stringify({
          type: 'timeframe_change',
          timeframe: timeframe
        }))
      }

      // Also fetch new data via REST API
      if (this.selectedSymbol) {
        this.fetchMarketData(this.selectedSymbol)
      }
    },

    cleanup() {
      if (this.pingInterval) {
        clearInterval(this.pingInterval)
      }

      if (this.websocket) {
        this.websocket.close()
        this.websocket = null
      }

      this.connectionStatus = 'disconnected'
    }
  }
})