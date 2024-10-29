<!--<template>-->
<!--  <div class="space-y-6">-->
<!--    <div class="flex justify-between items-center">-->
<!--      <h1 class="text-3xl font-bold tracking-tight">Market Dashboard</h1>-->
<!--      <TimeframeSelector @change="selectTimeframe" />-->
<!--    </div>-->

<!--    <div v-if="loading">-->
<!--      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">-->
<!--        <Skeleton v-for="i in 6" :key="i" class="h-[300px]" />-->
<!--      </div>-->
<!--    </div>-->

<!--    <div v-else-if="error" class="text-center py-12">-->
<!--      <Alert variant="destructive">-->
<!--        <AlertDescription>{{ error }}</AlertDescription>-->
<!--      </Alert>-->
<!--    </div>-->

<!--    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">-->
<!--      <MarketCard-->
<!--        v-for="symbol in watchlist"-->
<!--        :key="symbol"-->
<!--        :symbol="symbol"-->
<!--        :data="getMarketData(symbol)"-->
<!--        @click="navigateToSymbol(symbol)"-->
<!--      />-->
<!--    </div>-->
<!--  </div>-->
<!--</template>-->

<!--<script setup>-->
<!--import { ref, onMounted, computed } from 'vue'-->
<!--import { useRouter } from 'vue-router'-->
<!--import { useMarketStore } from '@/store/market'-->
<!--import { Skeleton } from '@/components/ui/skeleton'-->
<!--import { Alert, AlertDescription } from '@/components/ui/alert'-->
<!--import MarketCard from '@/components/MarketCard.vue'-->
<!--import TimeframeSelector from '@/components/TimeframeSelector.vue'-->

<!--const router = useRouter()-->
<!--const store = useMarketStore()-->
<!--const watchlist = ref(['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA', 'META'])-->
<!--const loading = computed(() => store.loading)-->
<!--const error = computed(() => store.error)-->

<!--const selectTimeframe = (tf) => {-->
<!--  store.setTimeframe(tf)-->
<!--  refreshData()-->
<!--}-->

<!--const refreshData = async () => {-->
<!--  for (const symbol of watchlist.value) {-->
<!--    await store.fetchMarketData(symbol)-->
<!--  }-->
<!--}-->

<!--const getMarketData = (symbol) => {-->
<!--  return store.marketData.find(data => data.symbol === symbol) || null-->
<!--}-->

<!--const navigateToSymbol = (symbol) => {-->
<!--  router.push(`/symbol/${symbol}`)-->
<!--}-->

<!--onMounted(() => {-->
<!--  refreshData()-->
<!--})-->
<!--</script>-->


<!-- src/views/MarketDashboard.vue -->
<template>
  <div class="space-y-6">
    <h2 class="text-3xl font-bold">Market Dashboard</h2>

    <!-- Watchlist Grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <Card
        v-for="symbol in watchlist"
        :key="symbol"
        class="hover:shadow-lg transition-all cursor-pointer"
        @click="navigateToSymbol(symbol)"
      >
        <CardHeader>
          <CardTitle>{{ symbol }}</CardTitle>
          <CardDescription>Loading...</CardDescription>
        </CardHeader>
      </Card>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { Card, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'

const router = useRouter()
const watchlist = ref(['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA'])

const navigateToSymbol = (symbol) => {
  router.push(`/symbol/${symbol}`)
}
</script>