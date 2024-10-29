<template>
  <Card>
    <CardHeader>
      <CardTitle>Technical Indicators</CardTitle>
    </CardHeader>
    <CardContent>
      <div class="space-y-4">
        <div v-for="indicator in computedIndicators" :key="indicator.name"
             class="border-b pb-2 last:border-b-0">
          <div class="flex justify-between items-center">
            <span class="font-medium">{{ indicator.name }}</span>
            <span :class="getValueColor(indicator.value)">
              {{ formatValue(indicator.value) }}
            </span>
          </div>
          <div class="mt-1">
            <Progress
              :value="getProgressWidth(indicator.value)"
              :class="getProgressColor(indicator.value)"
            />
          </div>
          <p class="text-sm text-muted-foreground mt-1">{{ indicator.signal }}</p>
        </div>
      </div>
    </CardContent>
  </Card>
</template>

<script setup>
import { computed } from 'vue'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card'
import { Progress } from '@/components/ui/progress'

const props = defineProps({
  data: {
    type: Object,
    default: () => ({})
  }
})

const computedIndicators = computed(() => [
  {
    name: 'RSI',
    value: props.data.rsi || 0,
    signal: getRSISignal(props.data.rsi)
  },
  {
    name: 'MACD',
    value: props.data.macd || 0,
    signal: getMACDSignal(props.data.macd, props.data.macd_signal)
  },
  {
    name: 'SMA20',
    value: props.data.sma_20 || 0,
    signal: getSMASignal(props.data.sma_20, props.data.close)
  }
])

const getValueColor = (value) => {
  if (value > 70) return 'text-green-600'
  if (value < 30) return 'text-red-600'
  return 'text-foreground'
}

const getProgressColor = (value) => {
  if (value > 70) return 'bg-green-500'
  if (value < 30) return 'bg-red-500'
  return 'bg-blue-500'
}

const getProgressWidth = (value) => {
  return Math.min(Math.max(value, 0), 100)
}

const formatValue = (value) => {
  return value?.toFixed(2) || '0.00'
}

const getRSISignal = (value) => {
  if (!value) return 'No signal'
  if (value > 70) return 'Overbought'
  if (value < 30) return 'Oversold'
  return 'Neutral'
}

const getMACDSignal = (macd, signal) => {
  if (!macd || !signal) return 'No signal'
  if (macd > signal) return 'Bullish Crossover'
  if (macd < signal) return 'Bearish Crossover'
  return 'Neutral'
}

const getSMASignal = (sma, price) => {
  if (!sma || !price) return 'No signal'
  if (price > sma) return 'Above Average'
  if (price < sma) return 'Below Average'
  return 'At Average'
}
</script>
