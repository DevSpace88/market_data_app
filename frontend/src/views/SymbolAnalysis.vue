<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <div>
        <h2 class="text-3xl font-bold">{{ symbol }}</h2>
        <p class="text-muted-foreground">
          {{ t('symbolAnalysis.currentPrice') }}: {{ marketStore.currencySymbol }}{{ formatNumber(currentPrice) }}
          <Badge :variant="priceChange >= 0 ? 'default' : 'destructive'" class="ml-2">
            {{ priceChange >= 0 ? '+' : '' }}{{ formatNumber(priceChange) }}%
          </Badge>
        </p>
      </div>
      <div class="flex items-center gap-3">
        <button
          @click="toggleWatchlist"
          :disabled="isWatchlistLoading"
          class="p-2 rounded-md transition-colors hover:bg-accent"
          :class="isInWatchlist 
            ? 'text-destructive hover:text-destructive/80' 
            : 'text-muted-foreground hover:text-foreground'"
        >
          <svg v-if="isWatchlistLoading" class="w-5 h-5 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
          </svg>
          <svg v-else-if="isInWatchlist" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
          </svg>
          <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path>
          </svg>
        </button>
        <TimeframeSelector v-model="timeframe" @change="handleTimeframeChange" />
      </div>
    </div>

    <div v-if="loading" class="py-8 text-center text-muted-foreground">
      <Loader2 class="h-6 w-6 animate-spin mx-auto mb-2"/>
      Analyzing market data...
    </div>
    <div v-else class="grid gap-6 grid-cols-1 lg:grid-cols-2">
      <div class="lg:col-span-2">
        <PriceChart
            :data="marketData"
            :technical-data="technicalIndicators"
            :currency="marketStore.currency"
            :currency-symbol="marketStore.currencySymbol"
        />
      </div>
      <TechnicalIndicators
          :data="technicalIndicators?.current"
          :currency="marketStore.currency"
          :currency-symbol="marketStore.currencySymbol"
          :current-price="currentPrice"
          @indicator-toggle="handleIndicatorToggle"
      />
      <SignalList :signals="signals"/>
      <PatternList :patterns="patterns"/>
      <RiskMetrics :data="riskMetrics" />
      <div class="lg:col-span-2">
        <AIAnalysis
          :analysis="aiAnalysis"
          :currency="marketStore.currency"
          :currency-symbol="marketStore.currencySymbol"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watchEffect } from 'vue'
import { useRoute } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { useMarketStore } from '@/stores/market'
import { useAuthStore } from '@/stores/auth'
import { Loader2 } from 'lucide-vue-next'
import { Badge } from '@/components/ui/badge'
import TimeframeSelector from '@/components/TimeframeSelector.vue'
import PriceChart from '@/components/PriceChart.vue'
import TechnicalIndicators from '@/components/TechnicalIndicators.vue'
import SignalList from '@/components/SignalList.vue'
import PatternList from '@/components/PatternList.vue'
import RiskMetrics from '@/components/RiskMetrics.vue'
import AIAnalysis from '@/components/AIAnalysis.vue'
import ConnectionStatus from '@/components/ConnectionStatus.vue'

const route = useRoute()
const { t } = useI18n()
const marketStore = useMarketStore()
const authStore = useAuthStore()
const timeframe = ref('1Y')
const selectedIndicators = ref(['sma_20', 'sma_50', 'bb_upper', 'bb_lower', 'bb_middle'])

// Watchlist state
const isInWatchlist = ref(false)
const isWatchlistLoading = ref(false)
const watchlistItemId = ref(null)

const symbol = computed(() => route.params.symbol)
const loading = computed(() => marketStore.loading)
const marketData = computed(() => marketStore.marketData || [])
const technicalIndicators = computed(() => marketStore.technicalIndicators || {})
const patterns = computed(() => marketStore.patterns || [])
const signals = computed(() => marketStore.signals || [])
const riskMetrics = computed(() => marketStore.riskMetrics)
const aiAnalysis = computed(() => marketStore.aiAnalysis)

// Computed Property für aktive Indikatoren mit Werten
const activeIndicators = computed(() => {
  if (!technicalIndicators.value?.current) return []
  return selectedIndicators.value.filter(indicator =>
      technicalIndicators.value.current[indicator] !== undefined
  )
})

const currentPrice = computed(() => {
  if (!marketData.value.length) return 0
  return marketData.value[marketData.value.length - 1].close
})

const priceChange = computed(() => {
  if (marketData.value.length < 2) return 0
  const latest = marketData.value[marketData.value.length - 1]
  const previous = marketData.value[marketData.value.length - 2]
  return ((latest.close - previous.close) / previous.close) * 100
})

const handleTimeframeChange = async (newTimeframe) => {
  timeframe.value = newTimeframe
  await fetchData()
}

const handleIndicatorToggle = (indicator) => {
  const index = selectedIndicators.value.indexOf(indicator)
  if (index === -1) {
    selectedIndicators.value.push(indicator)
  } else {
    selectedIndicators.value.splice(index, 1)
  }
}

const fetchData = async () => {
  // Reset watchlist status when switching symbols
  isInWatchlist.value = false
  watchlistItemId.value = null
  await marketStore.fetchMarketData(symbol.value, timeframe.value)
  await marketStore.fetchMarketAnalysis(symbol.value, timeframe.value)
  // Check watchlist status for new symbol
  await checkWatchlistStatus()
}

const formatNumber = (num) => {
  return num ? Number(num).toFixed(2) : '0.00'
}

// Watchlist functions
const checkWatchlistStatus = async () => {
  try {
    const response = await fetch('/api/v1/watchlist/', {
      headers: {
        'Authorization': `Bearer ${authStore.token}`
      }
    })
    
    if (response.ok) {
      const watchlist = await response.json()
      const item = watchlist.find(item => item.symbol === symbol.value)
      if (item) {
        isInWatchlist.value = true
        watchlistItemId.value = item.id
      } else {
        isInWatchlist.value = false
        watchlistItemId.value = null
      }
    }
  } catch (err) {
    console.error('Error checking watchlist status:', err)
  }
}

const toggleWatchlist = async () => {
  isWatchlistLoading.value = true
  
  try {
    if (isInWatchlist.value) {
      // Remove from watchlist
      const response = await fetch(`/api/v1/watchlist/${watchlistItemId.value}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${authStore.token}`
        }
      })
      
      if (response.ok) {
        isInWatchlist.value = false
        watchlistItemId.value = null
      }
    } else {
      // Add to watchlist
      const response = await fetch('/api/v1/watchlist/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${authStore.token}`
        },
        body: JSON.stringify({
          symbol: symbol.value,
          display_name: symbol.value
        })
      })
      
      if (response.ok) {
        const newItem = await response.json()
        isInWatchlist.value = true
        watchlistItemId.value = newItem.id
      }
    }
  } catch (err) {
    console.error('Error toggling watchlist:', err)
  } finally {
    isWatchlistLoading.value = false
  }
}

onMounted(() => {
  fetchData()
  if (import.meta.env.VITE_ENABLE_WS === 'true') {
    marketStore.initializeWebSocket(symbol.value)
  }
  checkWatchlistStatus()
})

onUnmounted(() => {
  // Clean up WebSocket when leaving SymbolAnalysis view
  marketStore.cleanupWebSocket()
})

watchEffect(() => {
  if (route.params.symbol) {
    fetchData()
  }
})
</script>