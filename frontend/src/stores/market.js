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
// //       console.log(`Setting timeframe to ${timeframe}`)
// //       this.timeframe = timeframe
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
// //         console.log('Initializing WebSocket connection:', wsUrl)
// //         this.websocket = new WebSocket(wsUrl)
// //
// //         this.websocket.onopen = () => {
// //           console.log('WebSocket connected successfully')
// //           this.wsConnected = true
// //           this.startPingInterval()
// //         }
// //
// //         this.websocket.onmessage = (event) => {
// //           try {
// //             const data = JSON.parse(event.data)
// //             switch (data.type) {
// //               case 'market_update':
// //                 console.log('Received market update')
// //                 this.handleMarketUpdate(data)
// //                 break
// //               case 'pong':
// //                 this.lastPongTime = Date.now()
// //                 break
// //               case 'error':
// //                 console.error('WebSocket error message:', data.message)
// //                 break
// //               default:
// //                 console.log('Received unknown message type:', data.type)
// //             }
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
// //           console.log('WebSocket disconnected, cleaning up')
// //           this.wsConnected = false
// //           this.cleanupWebSocket()
// //
// //           console.log('Attempting to reconnect in 5 seconds...')
// //           setTimeout(() => {
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
// //         console.log('Updated market data:', this.marketData.length, 'points')
// //       }
// //       if (data.technical) {
// //         this.technicalIndicators = data.technical
// //         console.log('Updated technical indicators')
// //       }
// //       if (data.patterns) {
// //         this.patterns = data.patterns
// //         console.log('Updated patterns:', this.patterns.length)
// //       }
// //       if (data.signals) {
// //         this.signals = data.signals
// //         console.log('Updated signals:', this.signals.length)
// //       }
// //     },
// //
// //     startPingInterval() {
// //       if (this.pingInterval) {
// //         clearInterval(this.pingInterval)
// //       }
// //
// //       this.pingInterval = setInterval(() => {
// //         if (this.websocket?.readyState === WebSocket.OPEN) {
// //           console.log('Sending ping')
// //           this.websocket.send(JSON.stringify({ type: 'ping' }))
// //
// //           // Check if we haven't received a pong in 45 seconds
// //           if (this.lastPongTime && Date.now() - this.lastPongTime > 45000) {
// //             console.log('No pong received, reconnecting...')
// //             this.cleanupWebSocket()
// //             this.initializeWebSocket(this.selectedSymbol)
// //           }
// //         }
// //       }, 30000) // Send ping every 30 seconds
// //     },
// //
// //     sendTimeframeUpdate(timeframe) {
// //       if (this.websocket?.readyState === WebSocket.OPEN) {
// //         console.log('Sending timeframe update:', timeframe)
// //         this.websocket.send(JSON.stringify({
// //           type: 'timeframe_change',
// //           timeframe: timeframe
// //         }))
// //       }
// //     },
// //
// //     cleanupWebSocket() {
// //       console.log('Cleaning up WebSocket connection')
// //
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
//       console.log(`Setting timeframe to ${timeframe}`)
//       this.timeframe = timeframe
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
//         console.log('Initializing WebSocket connection:', wsUrl)
//         this.websocket = new WebSocket(wsUrl)
//
//         this.websocket.onopen = () => {
//           console.log('WebSocket connected successfully')
//           this.wsConnected = true
//           this.startPingInterval()
//         }
//
//         this.websocket.onmessage = (event) => {
//           try {
//             const data = JSON.parse(event.data)
//             switch (data.type) {
//               case 'market_update':
//                 console.log('Received market update')
//                 this.handleMarketUpdate(data)
//                 break
//               case 'pong':
//                 this.lastPongTime = Date.now()
//                 break
//               case 'error':
//                 console.error('WebSocket error message:', data.message)
//                 break
//               default:
//                 console.log('Received unknown message type:', data.type)
//             }
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
//           console.log('WebSocket disconnected, cleaning up')
//           this.wsConnected = false
//           this.cleanupWebSocket()
//
//           console.log('Attempting to reconnect in 5 seconds...')
//           setTimeout(() => {
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
//         console.log('Updated market data:', this.marketData.length, 'points')
//       }
//       if (data.technical) {
//         this.technicalIndicators = data.technical
//         console.log('Updated technical indicators')
//       }
//       if (data.patterns) {
//         this.patterns = data.patterns
//         console.log('Updated patterns:', this.patterns.length)
//       }
//       if (data.signals) {
//         this.signals = data.signals
//         console.log('Updated signals:', this.signals.length)
//       }
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
//           console.log('Sending ping')
//           this.websocket.send(JSON.stringify({ type: 'ping' }))
//
//           // Check if we haven't received a pong in 45 seconds
//           if (this.lastPongTime && Date.now() - this.lastPongTime > 45000) {
//             console.log('No pong received, reconnecting...')
//             this.cleanupWebSocket()
//             this.initializeWebSocket(this.selectedSymbol)
//           }
//         }
//       }, 30000) // Send ping every 30 seconds
//     },
//
//     sendTimeframeUpdate(timeframe) {
//       if (this.websocket?.readyState === WebSocket.OPEN) {
//         console.log('Sending timeframe update:', timeframe)
//         this.websocket.send(JSON.stringify({
//           type: 'timeframe_change',
//           timeframe: timeframe
//         }))
//       }
//     },
//
//     cleanupWebSocket() {
//       console.log('Cleaning up WebSocket connection')
//
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
    aiAnalysis: null,
    selectedSymbol: null,
    timeframe: '1D',
    loading: false,
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
        console.log(`Fetching market analysis for ${symbol} with timeframe ${timeframe}`);
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
          this.aiAnalysis = response.data.ai_analysis || null;
          this.selectedSymbol = symbol;
          this.timeframe = timeframe || this.timeframe;

          // Debugging: Überprüfe die Antwort von der API
          console.log("API Response - Currency:", response.data.currency); // Soll 'JPY' anzeigen
          console.log("API Response - Currency Symbol:", response.data.currencySymbol); // Soll '¥' anzeigen

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
          console.log('Currency:', this.currency);
          console.log('Currency Symbol:', this.currencySymbol);
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
      console.log(`Setting timeframe to ${timeframe}`)
      this.timeframe = timeframe
      if (this.selectedSymbol) {
        this.fetchMarketData(this.selectedSymbol, timeframe)
        this.fetchMarketAnalysis(this.selectedSymbol, timeframe)
        this.sendTimeframeUpdate(timeframe)
      }
    },

    initializeWebSocket(symbol) {
      if (!symbol) return
      this.cleanupWebSocket()

      const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
      const host = window.location.host
      const wsUrl = `${protocol}//${host}/api/v1/ws/market/${symbol}`

      try {
        console.log('Initializing WebSocket connection:', wsUrl)
        this.websocket = new WebSocket(wsUrl)

        this.websocket.onopen = () => {
          console.log('WebSocket connected successfully')
          this.wsConnected = true
          this.startPingInterval()
        }

        this.websocket.onmessage = (event) => {
          try {
            const data = JSON.parse(event.data)
            switch (data.type) {
              case 'market_update':
                console.log('Received market update')
                this.handleMarketUpdate(data)
                break
              case 'pong':
                this.lastPongTime = Date.now()
                break
              case 'error':
                console.error('WebSocket error message:', data.message)
                break
              default:
                console.log('Received unknown message type:', data.type)
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
          console.log('WebSocket disconnected, cleaning up')
          this.wsConnected = false
          this.cleanupWebSocket()

          console.log('Attempting to reconnect in 5 seconds...')
          setTimeout(() => {
            if (this.selectedSymbol) {
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
        console.log('Updated market data:', this.marketData.length, 'points')
      }
      if (data.technical) {
        this.technicalIndicators = data.technical
        console.log('Updated technical indicators')
      }
      if (data.patterns) {
        this.patterns = data.patterns
        console.log('Updated patterns:', this.patterns.length)
      }
      if (data.signals) {
        this.signals = data.signals
        console.log('Updated signals:', this.signals.length)
      }
      if (data.currency) {
        console.log('WebSocket Currency:', data.currency); // Debugging
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
          console.log('Sending ping')
          this.websocket.send(JSON.stringify({ type: 'ping' }))

          // Check if we haven't received a pong in 45 seconds
          if (this.lastPongTime && Date.now() - this.lastPongTime > 45000) {
            console.log('No pong received, reconnecting...')
            this.cleanupWebSocket()
            this.initializeWebSocket(this.selectedSymbol)
          }
        }
      }, 30000) // Send ping every 30 seconds
    },

    sendTimeframeUpdate(timeframe) {
      if (this.websocket?.readyState === WebSocket.OPEN) {
        console.log('Sending timeframe update:', timeframe)
        this.websocket.send(JSON.stringify({
          type: 'timeframe_change',
          timeframe: timeframe
        }))
      }
    },

    cleanupWebSocket() {
      console.log('Cleaning up WebSocket connection')

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
    }
  }
})
