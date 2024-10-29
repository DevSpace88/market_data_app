<!--<template>-->
<!--  <div class="space-y-6">-->
<!--    <div class="flex justify-between items-center">-->
<!--      <div class="flex items-center gap-4">-->
<!--        <h1 class="text-2xl font-bold">{{ symbol }}</h1>-->
<!--        <Badge-->
<!--          :variant="priceChange >= 0 ? 'default' : 'destructive'"-->
<!--          class="text-lg px-3 py-1"-->
<!--        >-->
<!--          {{ priceChange >= 0 ? '+' : '' }}{{ priceChange.toFixed(2) }}%-->
<!--        </Badge>-->
<!--      </div>-->
<!--      <TimeframeSelector @change="handleTimeframeChange" />-->
<!--    </div>-->

<!--    <div v-if="loading" class="space-y-4">-->
<!--      <Skeleton class="h-[500px]" />-->
<!--      <div class="grid grid-cols-1 lg:grid-cols-3 gap-4">-->
<!--        <Skeleton class="h-[300px]" v-for="i in 3" :key="i" />-->
<!--      </div>-->
<!--    </div>-->

<!--    <div v-else-if="error" class="text-center py-12">-->
<!--      <Alert variant="destructive">-->
<!--        <AlertDescription>{{ error }}</AlertDescription>-->
<!--      </Alert>-->
<!--    </div>-->

<!--    <div v-else>-->
<!--      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">-->
<!--        <div class="lg:col-span-2">-->
<!--          <PriceChart-->
<!--            :data="marketData"-->
<!--            :indicators="selectedIndicators"-->
<!--          />-->
<!--        </div>-->
<!--        <div class="space-y-4">-->
<!--          <TechnicalIndicators :data="technicalIndicators" />-->
<!--          <PatternList :patterns="patterns" />-->
<!--          <SignalList :signals="signals" />-->
<!--        </div>-->
<!--      </div>-->

<!--      <div class="mt-8">-->
<!--        <AIAnalysis :analysis="aiAnalysis" />-->
<!--      </div>-->
<!--    </div>-->
<!--  </div>-->
<!--</template>-->

<!--<script setup>-->
<!--import { ref, onMounted, computed, watch, onUnmounted } from 'vue'-->
<!--import { useRoute } from 'vue-router'-->
<!--import { useMarketStore } from '@/store/market'-->
<!--import { Badge } from '@/components/ui/badge'-->
<!--import { Skeleton } from '@/components/ui/skeleton'-->
<!--import { Alert, AlertDescription } from '@/components/ui/alert'-->
<!--import PriceChart from '@/components/PriceChart.vue'-->
<!--import TechnicalIndicators from '@/components/TechnicalIndicators.vue'-->
<!--import PatternList from '@/components/PatternList.vue'-->
<!--import SignalList from '@/components/SignalList.vue'-->
<!--import AIAnalysis from '@/components/AIAnalysis.vue'-->
<!--import TimeframeSelector from '@/components/TimeframeSelector.vue'-->

<!--const route = useRoute()-->
<!--const store = useMarketStore()-->
<!--const symbol = computed(() => route.params.symbol)-->
<!--const selectedIndicators = ref(['SMA20', 'SMA50', 'BB'])-->

<!--const marketData = computed(() => store.marketData)-->
<!--const technicalIndicators = computed(() => store.technicalIndicators)-->
<!--const patterns = computed(() => store.patterns)-->
<!--const signals = computed(() => store.signals)-->
<!--const aiAnalysis = computed(() => store.aiAnalysis)-->
<!--const loading = computed(() => store.loading)-->
<!--const error = computed(() => store.error)-->

<!--const priceChange = computed(() => {-->
<!--  if (!marketData.value || marketData.value.length < 2) return 0-->
<!--  const latest = marketData.value[marketData.value.length - 1]-->
<!--  const previous = marketData.value[marketData.value.length - 2]-->
<!--  return ((latest.close - previous.close) / previous.close) * 100-->
<!--})-->

<!--const handleTimeframeChange = (timeframe) => {-->
<!--  store.setTimeframe(timeframe)-->
<!--  store.fetchMarketData(symbol.value)-->
<!--}-->

<!--onMounted(async () => {-->
<!--  await store.fetchMarketData(symbol.value)-->
<!--  await store.fetchMarketAnalysis(symbol.value)-->
<!--  store.initializeWebSocket(symbol.value)-->
<!--})-->

<!--watch(() => route.params.symbol, async (newSymbol) => {-->
<!--  if (newSymbol) {-->
<!--    await store.fetchMarketData(newSymbol)-->
<!--    await store.fetchMarketAnalysis(newSymbol)-->
<!--    store.initializeWebSocket(newSymbol)-->
<!--  }-->
<!--})-->

<!--onUnmounted(() => {-->
<!--  store.cleanup()-->
<!--})-->
<!--</script>-->

<!-- src/views/SymbolAnalysis.vue -->
<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <h2 class="text-3xl font-bold">{{ symbol }}</h2>
      <Badge>Loading...</Badge>
    </div>

    <Card>
      <CardHeader>
        <CardTitle>Market Data</CardTitle>
        <CardDescription>
          Analyzing {{ symbol }}...
        </CardDescription>
      </CardHeader>
      <CardContent>
        <p class="text-muted-foreground">
          Loading market data and analysis...
        </p>
      </CardContent>
    </Card>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'

const route = useRoute()
const symbol = computed(() => route.params.symbol)
</script>