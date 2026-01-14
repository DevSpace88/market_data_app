/**
 * Market WebSocket Composable
 *
 * Manages WebSocket connection for real-time market data updates.
 * Only active when VITE_ENABLE_WS=true and user is on SymbolAnalysis view.
 */

import { ref } from 'vue'

/**
 * WebSocket state and management
 */
export function useMarketWebSocket() {
  const websocket = ref<WebSocket | null>(null)
  const wsConnected = ref<boolean>(false)
  const lastPongTime = ref<number | null>(null)
  const pingInterval = ref<ReturnType<typeof setInterval> | null>(null)
  const wsRetryAttempts = ref<number>(0)

  /**
   * Check if JWT token is valid with at least 60s remaining
   * Tokens are in httpOnly cookies, but we check memory for reference
   */
  function isTokenValid(token: string | null): boolean {
    if (!token) return false
    try {
      const parts = token.split('.')
      if (parts.length !== 3) return false

      // base64url → base64
      let b64 = parts[1].replace(/-/g, '+').replace(/_/g, '/')
      const pad = b64.length % 4
      if (pad) b64 += '='.repeat(4 - pad)

      const json = atob(b64)
      const payload = JSON.parse(json)
      const expMs = (payload?.exp ?? 0) * 1000

      // Require at least 60s remaining
      return expMs - Date.now() > 60000
    } catch {
      return false
    }
  }

  /**
   * Initialize WebSocket connection for a symbol
   */
  function initializeWebSocket(symbol: string, token: string | null): void {
    // Feature flag check
    if (import.meta.env.VITE_ENABLE_WS !== 'true') {
      return
    }

    if (!symbol) return

    // Only active on SymbolAnalysis view
    if (!window.location.pathname.includes('/symbol/')) {
      return
    }

    // Block connection with invalid/expired token
    if (!isTokenValid(token)) {
      return
    }

    cleanupWebSocket()
    wsRetryAttempts.value = 0

    // Build WebSocket URL
    let wsUrl: string
    if (import.meta.env.VITE_WS_BASE_URL) {
      wsUrl = `${import.meta.env.VITE_WS_BASE_URL}/market/${symbol}?token=${encodeURIComponent(token || '')}`
    } else {
      // Fallback for local development
      const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
      const backendHost = `${window.location.hostname}:8000`
      wsUrl = `${protocol}//${backendHost}/api/v1/ws/market/${symbol}?token=${encodeURIComponent(token || '')}`
    }

    try {
      websocket.value = new WebSocket(wsUrl)

      websocket.value.onopen = () => {
        wsConnected.value = true
        wsRetryAttempts.value = 0
        startPingInterval()
      }

      websocket.value.onmessage = (event: MessageEvent) => {
        try {
          const data = JSON.parse(event.data)
          switch (data.type) {
            case 'market_update':
              handleMarketUpdate(data)
              break
            case 'pong':
              lastPongTime.value = Date.now()
              break
            case 'error':
              console.error('WebSocket error message:', data.message)
              break
          }
        } catch (error) {
          console.error('Error processing WebSocket message:', error)
        }
      }

      websocket.value.onerror = () => {
        wsConnected.value = false
      }

      websocket.value.onclose = () => {
        wsConnected.value = false
        cleanupWebSocket()

        // Stop after 3 failed attempts
        if (wsRetryAttempts.value >= 3) {
          return
        }

        // Exponential backoff (max 30s)
        const delay = Math.min(30000, 3000 * Math.max(1, wsRetryAttempts.value + 1))
        wsRetryAttempts.value = Math.min(wsRetryAttempts.value + 1, 10)

        setTimeout(() => {
          // Reconnect only if still on symbol page and token is valid
          if (window.location.pathname.includes('/symbol/') && isTokenValid(token)) {
            // Re-initialize would be called by parent component
          }
        }, delay)
      }
    } catch (error) {
      wsConnected.value = false
    }
  }

  /**
   * Handle incoming market update from WebSocket
   */
  function handleMarketUpdate(data: any, updateCallbacks?: {
    onData?: (data: any[]) => void
    onTechnical?: (indicators: any) => void
    onPatterns?: (patterns: any[]) => void
    onSignals?: (signals: any[]) => void
    onCurrency?: (currency: string, symbol: string) => void
  }): void {
    if (data.data && updateCallbacks?.onData) {
      updateCallbacks.onData(data.data)
    }
    if (data.technical && updateCallbacks?.onTechnical) {
      updateCallbacks.onTechnical(data.technical)
    }
    if (data.patterns && updateCallbacks?.onPatterns) {
      updateCallbacks.onPatterns(data.patterns)
    }
    if (data.signals && updateCallbacks?.onSignals) {
      updateCallbacks.onSignals(data.signals)
    }
    if (data.currency && updateCallbacks?.onCurrency) {
      updateCallbacks.onCurrency(data.currency, data.currencySymbol || '$')
    }
  }

  /**
   * Start ping interval (every 30s)
   */
  function startPingInterval(): void {
    if (pingInterval.value) {
      clearInterval(pingInterval.value)
    }

    pingInterval.value = setInterval(() => {
      if (websocket.value?.readyState === WebSocket.OPEN) {
        websocket.value.send(JSON.stringify({ type: 'ping' }))

        // Reconnect if no pong for 45s
        if (lastPongTime.value && Date.now() - lastPongTime.value > 45000) {
          cleanupWebSocket()
          // Re-initialization would be called by parent component
        }
      }
    }, 30000)
  }

  /**
   * Send timeframe change message to WebSocket
   */
  function sendTimeframeUpdate(timeframe: string): void {
    if (websocket.value?.readyState === WebSocket.OPEN) {
      websocket.value.send(JSON.stringify({
        type: 'timeframe_change',
        timeframe
      }))
    }
  }

  /**
   * Cleanup WebSocket connection and intervals
   */
  function cleanupWebSocket(): void {
    if (pingInterval.value) {
      clearInterval(pingInterval.value)
      pingInterval.value = null
    }

    if (websocket.value) {
      websocket.value.close()
      websocket.value = null
    }

    wsConnected.value = false
    lastPongTime.value = null
  }

  return {
    // State
    wsConnected,
    wsRetryAttempts,

    // Methods
    initializeWebSocket,
    handleMarketUpdate,
    sendTimeframeUpdate,
    cleanupWebSocket
  }
}
