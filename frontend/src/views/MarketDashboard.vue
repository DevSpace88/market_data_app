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