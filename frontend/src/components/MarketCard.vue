<template>
  <Card class="hover:shadow-lg transition-shadow cursor-pointer" @click="$emit('click')">
    <CardHeader>
      <CardTitle class="flex justify-between items-center">
        <span>{{ symbol }}</span>
        <Badge :variant="priceChange >= 0 ? 'default' : 'destructive'">
          {{ priceChange >= 0 ? '+' : '' }}{{ priceChange.toFixed(2) }}%
        </Badge>
      </CardTitle>
      <CardDescription>
        <div class="flex justify-between items-center">
          <span class="font-medium text-lg">
            ${{ currentPrice.toFixed(2) }}
          </span>
          <span class="text-sm text-muted-foreground">
            Vol: {{ formatNumber(volume) }}
          </span>
        </div>
      </CardDescription>
    </CardHeader>
    <CardContent>
      <div class="h-32">
        <PriceChart :data="chartData" :indicators="[]" />
      </div>
      <div class="mt-4 grid grid-cols-2 gap-2 text-sm">
        <div>
          <span class="text-muted-foreground">High</span>
          <p class="font-medium">${{ dayHigh.toFixed(2) }}</p>
        </div>
        <div>
          <span class="text-muted-foreground">Low</span>
          <p class="font-medium">${{ dayLow.toFixed(2) }}</p>
        </div>
      </div>
    </CardContent>
  </Card>
</template>

<script setup>
import { computed } from 'vue'
import {
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
  CardContent,
} from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import PriceChart from './PriceChart.vue'

const props = defineProps({
  symbol: String,
  data: Object
})

const currentPrice = computed(() => props.data?.price || 0)
const priceChange = computed(() => props.data?.change || 0)
const volume = computed(() => props.data?.volume || 0)
const dayHigh = computed(() => props.data?.high || 0)
const dayLow = computed(() => props.data?.low || 0)
const chartData = computed(() => props.data?.history || [])

const formatNumber = (num) => {
  return new Intl.NumberFormat('en-US', {
    notation: 'compact',
    compactDisplay: 'short'
  }).format(num)
}
</script>