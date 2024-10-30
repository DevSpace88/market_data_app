<!--<template>-->
<!--  <div class="space-y-6">-->
<!--    <div class="flex items-center justify-between">-->
<!--      <h2 class="text-3xl font-bold">{{ symbol }}</h2>-->
<!--      <Badge>Loading...</Badge>-->
<!--    </div>-->

<!--    <Card>-->
<!--      <CardHeader>-->
<!--        <CardTitle>Market Data</CardTitle>-->
<!--        <CardDescription>-->
<!--          Analyzing {{ symbol }}...-->
<!--        </CardDescription>-->
<!--      </CardHeader>-->
<!--      <CardContent>-->
<!--        <p class="text-muted-foreground">-->
<!--          Loading market data and analysis...-->
<!--        </p>-->
<!--      </CardContent>-->
<!--    </Card>-->
<!--  </div>-->
<!--</template>-->

<!--<script setup>-->
<!--import { computed } from 'vue'-->
<!--import { useRoute } from 'vue-router'-->
<!--import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ui/card'-->
<!--import { Badge } from '@/components/ui/badge'-->

<!--const route = useRoute()-->
<!--const symbol = computed(() => route.params.symbol)-->
<!--</script>-->


<template>
  <div class="space-y-6">
    <!-- Header -->
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
      <TimeframeSelector v-model="timeframe" @change="handleTimeframeChange" />
    </div>

    <div v-if="loading" class="py-8 text-center text-muted-foreground">
      <Loader2 class="h-6 w-6 animate-spin mx-auto mb-2" />
      Analyzing market data...
    </div>

    <div v-else class="grid gap-6 grid-cols-1 lg:grid-cols-2">
      <!-- Price Chart -->
      <div class="lg:col-span-2">
        <PriceChart
          :data="marketData"
          :indicators="selectedIndicators"
        />
      </div>

      <!-- Technical Indicators -->
      <TechnicalIndicators
        :data="technicalIndicators"
        @indicator-toggle="handleIndicatorToggle"
      />

      <!-- Trading Signals -->
      <SignalList :signals="signals" />

      <!-- Technical Patterns -->
      <PatternList :patterns="patterns" />

      <!-- AI Analysis -->
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

const route = useRoute()
const marketStore = useMarketStore()
const timeframe = ref('1D')
const selectedIndicators = ref(['SMA20', 'SMA50'])

const symbol = computed(() => route.params.symbol)
const loading = computed(() => marketStore.loading)
const marketData = computed(() => marketStore.marketData)
const technicalIndicators = computed(() => marketStore.technicalIndicators)
const patterns = computed(() => marketStore.patterns)
const signals = computed(() => marketStore.signals)
const aiAnalysis = computed(() => marketStore.aiAnalysis)

const currentPrice = computed(() => {
  if (!marketData.value.length) return 0
  return marketData.value[marketData.value.length - 1].close
})

const priceChange = computed(() => marketStore.priceChange)

const handleTimeframeChange = (newTimeframe) => {
  timeframe.value = newTimeframe
  fetchData()
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
  await marketStore.fetchMarketAnalysis(symbol.value)
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