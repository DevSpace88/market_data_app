<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <div>
        <h2 class="text-3xl font-bold">{{ symbol }}</h2>
        <p class="text-muted-foreground">
          Current Price: ${{ formatNumber(currentPrice) }}
          <Badge :variant="priceChange >= 0 ? 'default' : 'destructive'" class="ml-2">
            {{ priceChange >= 0 ? '+' : '' }}{{ formatNumber(priceChange) }}%
          </Badge>
        </p>
      </div>
      <ConnectionStatus />
      <TimeframeSelector v-model="timeframe" @change="handleTimeframeChange" />
    </div>

    <div v-if="loading" class="py-8 text-center text-muted-foreground">
      <Loader2 class="h-6 w-6 animate-spin mx-auto mb-2" />
      Analyzing market data...
    </div>
    <div v-else class="grid gap-6 grid-cols-1 lg:grid-cols-2">
      <div class="lg:col-span-2">
        <PriceChart
          :data="marketData"
          :indicators="activeIndicators"
          :technical-data="technicalIndicators"
        />
      </div>
      <TechnicalIndicators
        :data="technicalIndicators?.current"
        @indicator-toggle="handleIndicatorToggle"
      />
      <SignalList :signals="signals" />
      <PatternList :patterns="patterns" />
      <div class="lg:col-span-2">
        <AIAnalysis :analysis="aiAnalysis" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watchEffect } from 'vue'
import { useRoute } from 'vue-router'
import { useMarketStore } from '@/store/market'
import { Loader2 } from 'lucide-vue-next'
import { Badge } from '@/components/ui/badge'
import TimeframeSelector from '@/components/TimeframeSelector.vue'
import PriceChart from '@/components/PriceChart.vue'
import TechnicalIndicators from '@/components/TechnicalIndicators.vue'
import SignalList from '@/components/SignalList.vue'
import PatternList from '@/components/PatternList.vue'
import AIAnalysis from '@/components/AIAnalysis.vue'
import ConnectionStatus from '@/components/ConnectionStatus.vue'

const route = useRoute()
const marketStore = useMarketStore()
const timeframe = ref('1M')
const selectedIndicators = ref(['sma_20', 'sma_50', 'bb_upper', 'bb_lower', 'bb_middle'])

const symbol = computed(() => route.params.symbol)
const loading = computed(() => marketStore.loading)
const marketData = computed(() => marketStore.marketData || [])
const technicalIndicators = computed(() => marketStore.technicalIndicators || {})
const patterns = computed(() => marketStore.patterns || [])
const signals = computed(() => marketStore.signals || [])
const aiAnalysis = computed(() => marketStore.aiAnalysis)

// Neue Computed Property für aktive Indikatoren mit Werten
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
  console.log(`Fetching data for ${symbol.value} with timeframe ${timeframe.value}`)
  await marketStore.fetchMarketAnalysis(symbol.value, timeframe.value)
}

const formatNumber = (num) => {
  return num ? Number(num).toFixed(2) : '0.00'
}

onMounted(() => {
  fetchData()
  marketStore.initializeWebSocket(symbol.value)
})

watchEffect(() => {
  if (route.params.symbol) {
    fetchData()
  }
})
</script>