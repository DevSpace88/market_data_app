<!--<template>-->
<!--  <Card>-->
<!--    <CardHeader>-->
<!--      <CardTitle>Technical Indicators</CardTitle>-->
<!--    </CardHeader>-->
<!--    <CardContent>-->
<!--      <div class="space-y-4">-->
<!--        <div v-for="indicator in computedIndicators" :key="indicator.name"-->
<!--             class="border-b pb-2 last:border-b-0">-->
<!--          <div class="flex justify-between items-center">-->
<!--            <span class="font-medium">{{ indicator.name }}</span>-->
<!--            <span :class="getValueColor(indicator.value)">-->
<!--              {{ formatValue(indicator.value) }}-->
<!--            </span>-->
<!--          </div>-->
<!--          <div class="mt-1">-->
<!--            <Progress-->
<!--              :value="getProgressWidth(indicator.value)"-->
<!--              :class="getProgressColor(indicator.value)"-->
<!--            />-->
<!--          </div>-->
<!--          <p class="text-sm text-muted-foreground mt-1">{{ indicator.signal }}</p>-->
<!--        </div>-->
<!--      </div>-->
<!--    </CardContent>-->
<!--  </Card>-->
<!--</template>-->

<!--<script setup>-->
<!--import { computed } from 'vue'-->
<!--import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card'-->
<!--import { Progress } from '@/components/ui/progress'-->

<!--const props = defineProps({-->
<!--  data: {-->
<!--    type: Object,-->
<!--    default: () => ({})-->
<!--  }-->
<!--})-->

<!--const computedIndicators = computed(() => [-->
<!--  {-->
<!--    name: 'RSI',-->
<!--    value: props.data.rsi || 0,-->
<!--    signal: getRSISignal(props.data.rsi)-->
<!--  },-->
<!--  {-->
<!--    name: 'MACD',-->
<!--    value: props.data.macd || 0,-->
<!--    signal: getMACDSignal(props.data.macd, props.data.macd_signal)-->
<!--  },-->
<!--  {-->
<!--    name: 'SMA20',-->
<!--    value: props.data.sma_20 || 0,-->
<!--    signal: getSMASignal(props.data.sma_20, props.data.close)-->
<!--  }-->
<!--])-->

<!--const getValueColor = (value) => {-->
<!--  if (value > 70) return 'text-green-600'-->
<!--  if (value < 30) return 'text-red-600'-->
<!--  return 'text-foreground'-->
<!--}-->

<!--const getProgressColor = (value) => {-->
<!--  if (value > 70) return 'bg-green-500'-->
<!--  if (value < 30) return 'bg-red-500'-->
<!--  return 'bg-blue-500'-->
<!--}-->

<!--const getProgressWidth = (value) => {-->
<!--  return Math.min(Math.max(value, 0), 100)-->
<!--}-->

<!--const formatValue = (value) => {-->
<!--  return value?.toFixed(2) || '0.00'-->
<!--}-->

<!--const getRSISignal = (value) => {-->
<!--  if (!value) return 'No signal'-->
<!--  if (value > 70) return 'Overbought'-->
<!--  if (value < 30) return 'Oversold'-->
<!--  return 'Neutral'-->
<!--}-->

<!--const getMACDSignal = (macd, signal) => {-->
<!--  if (!macd || !signal) return 'No signal'-->
<!--  if (macd > signal) return 'Bullish Crossover'-->
<!--  if (macd < signal) return 'Bearish Crossover'-->
<!--  return 'Neutral'-->
<!--}-->

<!--const getSMASignal = (sma, price) => {-->
<!--  if (!sma || !price) return 'No signal'-->
<!--  if (price > sma) return 'Above Average'-->
<!--  if (price < sma) return 'Below Average'-->
<!--  return 'At Average'-->
<!--}-->
<!--</script>-->


<template>
  <Card>
    <CardHeader>
      <CardTitle>Technical Indicators</CardTitle>
    </CardHeader>
    <CardContent>
      <div class="space-y-4">
        <!-- RSI -->
        <div v-if="data?.rsi" class="border-b pb-2">
          <div class="flex justify-between items-center">
            <span class="font-medium">RSI</span>
            <span :class="getRSIColor(data.rsi)">
              {{ formatNumber(data.rsi) }}
            </span>
          </div>
          <div class="mt-1">
            <Progress :value="data.rsi" class="h-2" :class="getRSIColor(data.rsi)" />
          </div>
          <p class="text-sm text-muted-foreground mt-1">
            {{ getRSISignal(data.rsi) }}
          </p>
        </div>

        <!-- MACD -->
        <div v-if="data?.macd" class="border-b pb-2">
          <div class="flex justify-between items-center">
            <span class="font-medium">MACD</span>
            <span :class="getMACDColor(data.macd, data.macd_signal)">
              {{ formatNumber(data.macd) }}
            </span>
          </div>
          <div class="mt-1">
            <Progress
              :value="getMACDProgress(data.macd)"
              class="h-2"
              :class="getMACDColor(data.macd, data.macd_signal)"
            />
          </div>
          <p class="text-sm text-muted-foreground mt-1">
            Signal: {{ formatNumber(data.macd_signal) }}
          </p>
        </div>

        <!-- Bollinger Bands -->
        <div v-if="data?.bb_middle" class="border-b pb-2">
          <div class="flex justify-between items-center">
            <span class="font-medium">Bollinger Bands</span>
          </div>
          <div class="grid grid-cols-3 gap-2 mt-1 text-sm">
            <div>
              <span class="text-muted-foreground">Upper</span>
              <p>${{ formatNumber(data.bb_upper) }}</p>
            </div>
            <div>
              <span class="text-muted-foreground">Middle</span>
              <p>${{ formatNumber(data.bb_middle) }}</p>
            </div>
            <div>
              <span class="text-muted-foreground">Lower</span>
              <p>${{ formatNumber(data.bb_lower) }}</p>
            </div>
          </div>
        </div>

        <!-- Moving Averages -->
        <div v-if="data?.sma_20" class="pt-2">
          <div class="flex justify-between items-center">
            <span class="font-medium">Moving Averages</span>
          </div>
          <div class="grid grid-cols-2 gap-2 mt-1 text-sm">
            <div>
              <span class="text-muted-foreground">SMA20</span>
              <p>${{ formatNumber(data.sma_20) }}</p>
            </div>
            <div v-if="data?.sma_50">
              <span class="text-muted-foreground">SMA50</span>
              <p>${{ formatNumber(data.sma_50) }}</p>
            </div>
          </div>
        </div>
      </div>
    </CardContent>
  </Card>
</template>

<script setup>
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card'
import { Progress } from '@/components/ui/progress'

defineProps({
  data: {
    type: Object,
    default: () => ({})
  }
})

const formatNumber = (value) => {
  return value?.toFixed(2) || '0.00'
}

const getRSIColor = (value) => {
  if (value > 70) return 'text-red-500'
  if (value < 30) return 'text-green-500'
  return 'text-blue-500'
}

const getRSISignal = (value) => {
  if (value > 70) return 'Overbought'
  if (value < 30) return 'Oversold'
  return 'Neutral'
}

const getMACDColor = (macd, signal) => {
  if (macd > signal) return 'text-green-500'
  if (macd < signal) return 'text-red-500'
  return 'text-blue-500'
}

const getMACDProgress = (macd) => {
  return Math.abs(macd) * 10
}
</script>