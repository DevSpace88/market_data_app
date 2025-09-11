// // import { defineStore } from 'pinia'
// // import axios from 'axios'
// //
// // export const useMarketStore = defineStore('market', {
// //   state: () => ({
// //     marketData: [],
// //     technicalIndicators: {},
// //     patterns: [],
// //     signals: [],
// //     aiAnalysis: null,
// //     selectedSymbol: null,
// //     timeframe: '1D',
// //     loading: false,
// //     error: null,
// //     websocket: null,
// //     wsConnected: false,
// //     lastPongTime: null,
// //     pingInterval: null
// //   }),
// //
// //   getters: {
// //     priceChange: (state) => {
// //       if (!state.marketData.length) return 0
// //       const latest = state.marketData[state.marketData.length - 1]
// //       const previous = state.marketData[state.marketData.length - 2]
// //       if (!latest || !previous) return 0
// //       return ((latest.close - previous.close) / previous.close) * 100
// //     },
// //
// //     isConnected: (state) => state.wsConnected,
// //
// //     currentPrice: (state) => {
// //       if (!state.marketData.length) return 0
// //       return state.marketData[state.marketData.length - 1].close
// //     }
// //   },
// //
// //   actions: {
// //     async fetchMarketAnalysis(symbol, timeframe) {
// //       if (!symbol) return
// //       this.loading = true
// //       this.error = null
// //
// //       try {
// //         console.log(`Fetching market analysis for ${symbol} with timeframe ${timeframe}`)
// //         const response = await axios.get(`/api/v1/market/analysis/${symbol}`, {
// //           params: {
// //             timeframe: timeframe || this.timeframe,
// //             include_news: true
// //           }
// //         })
// //
// //         if (response.data) {
// //           this.marketData = response.data.market_data || []
// //           this.technicalIndicators = response.data.technical_indicators || {}
// //           this.patterns = response.data.patterns || []
// //           this.signals = response.data.signals || []
// //           this.aiAnalysis = response.data.ai_analysis || null
// //           this.selectedSymbol = symbol
// //           this.timeframe = timeframe || this.timeframe
// //
// //           console.log('Market data updated:', {
// //             dataPoints: this.marketData.length,
// //             indicators: Object.keys(this.technicalIndicators),
// //             patterns: this.patterns.length,
// //             signals: this.signals.length
// //           })
// //         }
// //       } catch (error) {
// //         console.error('Error fetching market analysis:', error)
// //         this.error = error.response?.data?.detail || 'Failed to fetch market analysis'
// //       } finally {
// //         this.loading = false
// //       }
// //     },
// //
// //     setTimeframe(timeframe) {
// //       if (this.timeframe === timeframe) return
// // // //       this.timeframe = timeframe
// //       if (this.selectedSymbol) {
// //         this.fetchMarketAnalysis(this.selectedSymbol, timeframe)
// //         this.sendTimeframeUpdate(timeframe)
// //       }
// //     },
// //
// //     initializeWebSocket(symbol) {
// //       if (!symbol) return
// //       this.cleanupWebSocket()
// //
// //       const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
// //       const host = window.location.host
// //       const wsUrl = `${protocol}//${host}/api/v1/ws/market/${symbol}`
// //
// //       try {
// // // //         this.websocket = new WebSocket(wsUrl)
// //
// //         this.websocket.onopen = () => {
// // // //           this.wsConnected = true
// //           this.startPingInterval()
// //         }
// //
// //         this.websocket.onmessage = (event) => {
// //           try {
// //             const data = JSON.parse(event.data)
// //             switch (data.type) {
// //               case 'market_update':
// // // //                 this.handleMarketUpdate(data)
// //                 break
// //               case 'pong':
// //                 this.lastPongTime = Date.now()
// //                 break
// //               case 'error':
// //                 console.error('WebSocket error message:', data.message)
// //                 break
// //               default:
// // // //             }
// //           } catch (error) {
// //             console.error('Error processing WebSocket message:', error)
// //           }
// //         }
// //
// //         this.websocket.onerror = (error) => {
// //           console.error('WebSocket error:', error)
// //           this.wsConnected = false
// //         }
// //
// //         this.websocket.onclose = () => {
// // // //           this.wsConnected = false
// //           this.cleanupWebSocket()
// //
// // // //           setTimeout(() => {
// //             if (this.selectedSymbol) {
// //               this.initializeWebSocket(this.selectedSymbol)
// //             }
// //           }, 5000)
// //         }
// //
// //       } catch (error) {
// //         console.error('WebSocket initialization error:', error)
// //         this.wsConnected = false
// //       }
// //     },
// //
// //     handleMarketUpdate(data) {
// //       if (data.data) {
// //         this.marketData = data.data
// // // //       }
// //       if (data.technical) {
// //         this.technicalIndicators = data.technical
// // // //       }
// //       if (data.patterns) {
// //         this.patterns = data.patterns
// // // //       }
// //       if (data.signals) {
// //         this.signals = data.signals
// // // //       }
// //     },
// //
// //     startPingInterval() {
// //       if (this.pingInterval) {
// //         clearInterval(this.pingInterval)
// //       }
// //
// //       this.pingInterval = setInterval(() => {
// //         if (this.websocket?.readyState === WebSocket.OPEN) {
// // // //           this.websocket.send(JSON.stringify({ type: 'ping' }))
// //
// //           // Check if we haven't received a pong in 45 seconds
// //           if (this.lastPongTime && Date.now() - this.lastPongTime > 45000) {
// // // //             this.cleanupWebSocket()
// //             this.initializeWebSocket(this.selectedSymbol)
// //           }
// //         }
// //       }, 30000) // Send ping every 30 seconds
// //     },
// //
// //     sendTimeframeUpdate(timeframe) {
// //       if (this.websocket?.readyState === WebSocket.OPEN) {
// // // //         this.websocket.send(JSON.stringify({
// //           type: 'timeframe_change',
// //           timeframe: timeframe
// //         }))
// //       }
// //     },
// //
// //     cleanupWebSocket() {
// // // //
// //       if (this.pingInterval) {
// //         clearInterval(this.pingInterval)
// //         this.pingInterval = null
// //       }
// //
// //       if (this.websocket) {
// //         this.websocket.close()
// //         this.websocket = null
// //       }
// //
// //       this.wsConnected = false
// //       this.lastPongTime = null
// //     }
// //   }
// // })
//
//
// // stores/market.js
// import { defineStore } from 'pinia'
// import axios from 'axios'
//
// export const useMarketStore = defineStore('market', {
//   state: () => ({
//     marketData: [],
//     technicalIndicators: {},
//     patterns: [],
//     signals: [],
//     aiAnalysis: null,
//     selectedSymbol: null,
//     timeframe: '1D',
//     loading: false,
//     error: null,
//     websocket: null,
//     wsConnected: false,
//     lastPongTime: null,
//     pingInterval: null,
//     currency: 'USD',
//     currencySymbol: '$'
//   }),
//
//   getters: {
//     priceChange: (state) => {
//       if (!state.marketData.length) return 0
//       const latest = state.marketData[state.marketData.length - 1]
//       const previous = state.marketData[state.marketData.length - 2]
//       if (!latest || !previous) return 0
//       return ((latest.close - previous.close) / previous.close) * 100
//     },
//
//     isConnected: (state) => state.wsConnected,
//
//     currentPrice: (state) => {
//       if (!state.marketData.length) return 0
//       return state.marketData[state.marketData.length - 1].close
//     }
//   },
//
//   actions: {
//     async fetchMarketAnalysis(symbol, timeframe) {
//       if (!symbol) return
//       this.loading = true
//       this.error = null
//
//       try {
//         console.log(`Fetching market analysis for ${symbol} with timeframe ${timeframe}`)
//         const response = await axios.get(`/api/v1/market/analysis/${symbol}`, {
//           params: {
//             timeframe: timeframe || this.timeframe,
//             include_news: true
//           }
//         })
//
//         if (response.data) {
//           this.marketData = response.data.market_data || []
//           this.technicalIndicators = response.data.technical_indicators || {}
//           this.patterns = response.data.patterns || []
//           this.signals = response.data.signals || []
//           this.aiAnalysis = response.data.ai_analysis || null
//           this.selectedSymbol = symbol
//           this.timeframe = timeframe || this.timeframe
//           this.currency = response.data.currency || 'USD'
//           this.currencySymbol = response.data.currencySymbol || '$'
//
//           console.log('Market data updated:', {
//             dataPoints: this.marketData.length,
//             indicators: Object.keys(this.technicalIndicators),
//             patterns: this.patterns.length,
//             signals: this.signals.length,
//             currency: this.currency,
//             currencySymbol: this.currencySymbol
//           })
//         }
//       } catch (error) {
//         console.error('Error fetching market analysis:', error)
//         this.error = error.response?.data?.detail || 'Failed to fetch market analysis'
//       } finally {
//         this.loading = false
//       }
//     },
//
//     setTimeframe(timeframe) {
//       if (this.timeframe === timeframe) return
// //       this.timeframe = timeframe
//       if (this.selectedSymbol) {
//         this.fetchMarketAnalysis(this.selectedSymbol, timeframe)
//         this.sendTimeframeUpdate(timeframe)
//       }
//     },
//
//     initializeWebSocket(symbol) {
//       if (!symbol) return
//       this.cleanupWebSocket()
//
//       const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
//       const host = window.location.host
//       const wsUrl = `${protocol}//${host}/api/v1/ws/market/${symbol}`
//
//       try {
// //         this.websocket = new WebSocket(wsUrl)
//
//         this.websocket.onopen = () => {
// //           this.wsConnected = true
//           this.startPingInterval()
//         }
//
//         this.websocket.onmessage = (event) => {
//           try {
//             const data = JSON.parse(event.data)
//             switch (data.type) {
//               case 'market_update':
// //                 this.handleMarketUpdate(data)
//                 break
//               case 'pong':
//                 this.lastPongTime = Date.now()
//                 break
//               case 'error':
//                 console.error('WebSocket error message:', data.message)
//                 break
//               default:
// //             }
//           } catch (error) {
//             console.error('Error processing WebSocket message:', error)
//           }
//         }
//
//         this.websocket.onerror = (error) => {
//           console.error('WebSocket error:', error)
//           this.wsConnected = false
//         }
//
//         this.websocket.onclose = () => {
// //           this.wsConnected = false
//           this.cleanupWebSocket()
//
// //           setTimeout(() => {
//             if (this.selectedSymbol) {
//               this.initializeWebSocket(this.selectedSymbol)
//             }
//           }, 5000)
//         }
//
//       } catch (error) {
//         console.error('WebSocket initialization error:', error)
//         this.wsConnected = false
//       }
//     },
//
//     handleMarketUpdate(data) {
//       if (data.data) {
//         this.marketData = data.data
// //       }
//       if (data.technical) {
//         this.technicalIndicators = data.technical
// //       }
//       if (data.patterns) {
//         this.patterns = data.patterns
// //       }
//       if (data.signals) {
//         this.signals = data.signals
// //       }
//       if (data.currency) {
//         this.currency = data.currency
//         this.currencySymbol = data.currencySymbol || '$'
//       }
//     },
//
//     startPingInterval() {
//       if (this.pingInterval) {
//         clearInterval(this.pingInterval)
//       }
//
//       this.pingInterval = setInterval(() => {
//         if (this.websocket?.readyState === WebSocket.OPEN) {
// //           this.websocket.send(JSON.stringify({ type: 'ping' }))
//
//           // Check if we haven't received a pong in 45 seconds
//           if (this.lastPongTime && Date.now() - this.lastPongTime > 45000) {
// //             this.cleanupWebSocket()
//             this.initializeWebSocket(this.selectedSymbol)
//           }
//         }
//       }, 30000) // Send ping every 30 seconds
//     },
//
//     sendTimeframeUpdate(timeframe) {
//       if (this.websocket?.readyState === WebSocket.OPEN) {
// //         this.websocket.send(JSON.stringify({
//           type: 'timeframe_change',
//           timeframe: timeframe
//         }))
//       }
//     },
//
//     cleanupWebSocket() {
// //
//       if (this.pingInterval) {
//         clearInterval(this.pingInterval)
//         this.pingInterval = null
//       }
//
//       if (this.websocket) {
//         this.websocket.close()
//         this.websocket = null
//       }
//
//       this.wsConnected = false
//       this.lastPongTime = null
//     }
//   }
// })



// stores/market.js
import { defineStore } from 'pinia'
import axios from 'axios'

export const useMarketStore = defineStore('market', {
  state: () => ({
    marketData: [],
    technicalIndicators: {},
    patterns: [],
    signals: [],
    riskMetrics: null,
    aiAnalysis: null,
    selectedSymbol: null,
    timeframe: '1D',
    loading: false,
    loadingIndicators: false,
    loadingPatterns: false,
    loadingSignals: false,
    loadingRiskMetrics: false,
    loadingAI: false,
    error: null,
    websocket: null,
    wsConnected: false,
    lastPongTime: null,
    pingInterval: null,
    currency: 'USD',
    currencySymbol: '$'
  }),

  getters: {
    priceChange: (state) => {
      if (!state.marketData.length) return 0
      const latest = state.marketData[state.marketData.length - 1]
      const previous = state.marketData[state.marketData.length - 2]
      if (!latest || !previous) return 0
      return ((latest.close - previous.close) / previous.close) * 100
    },

    isConnected: (state) => state.wsConnected,

    currentPrice: (state) => {
      if (!state.marketData.length) return 0
      return state.marketData[state.marketData.length - 1].close
    }
  },

  actions: {
    async fetchMarketData(symbol, timeframe) {
      if (!symbol) return;
      this.loading = true;
      this.error = null;

      // Map Frontend-Zeitrahmen zu Backend-Param
      const map = {
        '1D': '1d',
        '1W': '5d',
        '1M': '1mo',
        '3M': '3mo',
        '6M': '6mo',
        '1Y': '1y',
        'YTD': 'ytd'
      };
      const tf = map[timeframe] || '1mo';

      try {
        const response = await axios.get(`/api/v1/market/data/${symbol}`, {
          params: { timeframe: tf }
        });
        if (response.data) {
          this.marketData = response.data.data || [];
          this.currency = response.data.currency || 'USD';
          this.currencySymbol = response.data.currencySymbol || '$';
        }
      } catch (error) {
        console.error('Error fetching market data:', error);
        this.error = error.response?.data?.detail || 'Failed to fetch market data';
      } finally {
        this.loading = false;
      }
    },
    async fetchMarketAnalysis(symbol, timeframe) {
      if (!symbol) return;
      this.loading = true;
      this.error = null;

      try {
        const response = await axios.get(`/api/v1/market/analysis/${symbol}`, {
          params: {
            timeframe: timeframe || this.timeframe,
            include_news: true
          }
        });

        if (response.data) {
          // Belasse Chart-Daten unverändert; kommen aus /market/data
          this.technicalIndicators = response.data.technical_indicators || {};
          this.patterns = response.data.patterns || [];
          this.signals = response.data.signals || [];
          this.riskMetrics = response.data.risk_metrics || null;
          this.aiAnalysis = response.data.ai_analysis || null;
          this.selectedSymbol = symbol;
          this.timeframe = timeframe || this.timeframe;

          // Debugging: Überprüfe die Antwort von der API

          // Setze Währung und Symbol
          if (response.data.currency && response.data.currencySymbol) {
            this.currency = response.data.currency;
            this.currencySymbol = response.data.currencySymbol;
          } else {
            // Falls keine Währungsdaten vorhanden sind, setze Standardwerte
            console.warn('No currency data found in API response. Defaulting to USD and $');
            this.currency = 'USD';
            this.currencySymbol = '$';
          }

          // Debugging: Überprüfe gesetzte Werte
        }
      } catch (error) {
        console.error('Error fetching market analysis:', error);
        this.error = error.response?.data?.detail || 'Failed to fetch market analysis';
      } finally {
        this.loading = false;
      }
    },

    setTimeframe(timeframe) {
      if (this.timeframe === timeframe) return
      this.timeframe = timeframe
      if (this.selectedSymbol) {
        this.fetchMarketData(this.selectedSymbol, timeframe)
        this.fetchMarketAnalysis(this.selectedSymbol, timeframe)
        this.sendTimeframeUpdate(timeframe)
      }
    },

    initializeWebSocket(symbol) {
      if (!symbol) return
      
      // Only initialize WebSocket if we're in SymbolAnalysis view
      if (!window.location.pathname.includes('/symbol/')) {
        return
      }
      
      this.cleanupWebSocket()

      const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
      const host = window.location.host
      const wsUrl = `${protocol}//${host}/api/v1/ws/market/${symbol}`

      try {
        this.websocket = new WebSocket(wsUrl)

        this.websocket.onopen = () => {
          this.wsConnected = true
          this.startPingInterval()
        }

        this.websocket.onmessage = (event) => {
          try {
            const data = JSON.parse(event.data)
            switch (data.type) {
              case 'market_update':
                this.handleMarketUpdate(data)
                break
              case 'pong':
                this.lastPongTime = Date.now()
                break
              case 'error':
                console.error('WebSocket error message:', data.message)
                break
              default:
            }
          } catch (error) {
            console.error('Error processing WebSocket message:', error)
          }
        }

        this.websocket.onerror = (error) => {
          console.error('WebSocket error:', error)
          this.wsConnected = false
        }

        this.websocket.onclose = () => {
          this.wsConnected = false
          this.cleanupWebSocket()

          // Only auto-reconnect if still in SymbolAnalysis view
          setTimeout(() => {
            if (this.selectedSymbol && window.location.pathname.includes('/symbol/')) {
              this.initializeWebSocket(this.selectedSymbol)
            }
          }, 5000)
        }

      } catch (error) {
        console.error('WebSocket initialization error:', error)
        this.wsConnected = false
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
      if (data.currency) {
        this.currency = data.currency
        this.currencySymbol = data.currencySymbol || '$'
      }
    },

    startPingInterval() {
      if (this.pingInterval) {
        clearInterval(this.pingInterval)
      }

      this.pingInterval = setInterval(() => {
        if (this.websocket?.readyState === WebSocket.OPEN) {
          this.websocket.send(JSON.stringify({ type: 'ping' }))

          // Check if we haven't received a pong in 45 seconds
          if (this.lastPongTime && Date.now() - this.lastPongTime > 45000) {
            this.cleanupWebSocket()
            this.initializeWebSocket(this.selectedSymbol)
          }
        }
      }, 30000) // Send ping every 30 seconds
    },

    sendTimeframeUpdate(timeframe) {
      if (this.websocket?.readyState === WebSocket.OPEN) {
        this.websocket.send(JSON.stringify({
          type: 'timeframe_change',
          timeframe: timeframe
        }))
      }
    },

    cleanupWebSocket() {

      if (this.pingInterval) {
        clearInterval(this.pingInterval)
        this.pingInterval = null
      }

      if (this.websocket) {
        this.websocket.close()
        this.websocket = null
      }

      this.wsConnected = false
      this.lastPongTime = null
    },

    // Separate actions for individual components
    async fetchIndicators(symbol, timeframe = '1M') {
      try {
        this.loadingIndicators = true
        const response = await axios.get(`/api/v1/market/indicators/${symbol}`, {
          params: { timeframe }
        })
        this.technicalIndicators = response.data.technical_indicators || {}
      } catch (error) {
        console.error('Error fetching indicators:', error)
        this.error = error.response?.data?.detail || 'Failed to fetch indicators'
      } finally {
        this.loadingIndicators = false
      }
    },

    async fetchPatterns(symbol, timeframe = '1M') {
      try {
        this.loadingPatterns = true
        const response = await axios.get(`/api/v1/market/patterns/${symbol}`, {
          params: { timeframe }
        })
        this.patterns = response.data.patterns || []
      } catch (error) {
        console.error('Error fetching patterns:', error)
        this.error = error.response?.data?.detail || 'Failed to fetch patterns'
      } finally {
        this.loadingPatterns = false
      }
    },

    async fetchSignals(symbol, timeframe = '1M') {
      try {
        this.loadingSignals = true
        const response = await axios.get(`/api/v1/market/signals/${symbol}`, {
          params: { timeframe }
        })
        this.signals = response.data.signals || []
      } catch (error) {
        console.error('Error fetching signals:', error)
        this.error = error.response?.data?.detail || 'Failed to fetch signals'
      } finally {
        this.loadingSignals = false
      }
    },

    async fetchRiskMetrics(symbol, timeframe = '1M') {
      try {
        this.loadingRiskMetrics = true
        const response = await axios.get(`/api/v1/market/risk-metrics/${symbol}`, {
          params: { timeframe }
        })
        this.riskMetrics = response.data.risk_metrics || null
      } catch (error) {
        console.error('Error fetching risk metrics:', error)
        this.error = error.response?.data?.detail || 'Failed to fetch risk metrics'
      } finally {
        this.loadingRiskMetrics = false
      }
    }
  }
})
