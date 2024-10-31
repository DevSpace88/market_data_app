<!--&lt;!&ndash;<template>&ndash;&gt;-->
<!--&lt;!&ndash;  <Card>&ndash;&gt;-->
<!--&lt;!&ndash;    <CardHeader>&ndash;&gt;-->
<!--&lt;!&ndash;      <CardTitle>Technical Indicators</CardTitle>&ndash;&gt;-->
<!--&lt;!&ndash;    </CardHeader>&ndash;&gt;-->
<!--&lt;!&ndash;    <CardContent>&ndash;&gt;-->
<!--&lt;!&ndash;      <div class="space-y-4">&ndash;&gt;-->
<!--&lt;!&ndash;        <div v-for="indicator in computedIndicators" :key="indicator.name"&ndash;&gt;-->
<!--&lt;!&ndash;             class="border-b pb-2 last:border-b-0">&ndash;&gt;-->
<!--&lt;!&ndash;          <div class="flex justify-between items-center">&ndash;&gt;-->
<!--&lt;!&ndash;            <span class="font-medium">{{ indicator.name }}</span>&ndash;&gt;-->
<!--&lt;!&ndash;            <span :class="getValueColor(indicator.value)">&ndash;&gt;-->
<!--&lt;!&ndash;              {{ formatValue(indicator.value) }}&ndash;&gt;-->
<!--&lt;!&ndash;            </span>&ndash;&gt;-->
<!--&lt;!&ndash;          </div>&ndash;&gt;-->
<!--&lt;!&ndash;          <div class="mt-1">&ndash;&gt;-->
<!--&lt;!&ndash;            <Progress&ndash;&gt;-->
<!--&lt;!&ndash;              :value="getProgressWidth(indicator.value)"&ndash;&gt;-->
<!--&lt;!&ndash;              :class="getProgressColor(indicator.value)"&ndash;&gt;-->
<!--&lt;!&ndash;            />&ndash;&gt;-->
<!--&lt;!&ndash;          </div>&ndash;&gt;-->
<!--&lt;!&ndash;          <p class="text-sm text-muted-foreground mt-1">{{ indicator.signal }}</p>&ndash;&gt;-->
<!--&lt;!&ndash;        </div>&ndash;&gt;-->
<!--&lt;!&ndash;      </div>&ndash;&gt;-->
<!--&lt;!&ndash;    </CardContent>&ndash;&gt;-->
<!--&lt;!&ndash;  </Card>&ndash;&gt;-->
<!--&lt;!&ndash;</template>&ndash;&gt;-->

<!--&lt;!&ndash;<script setup>&ndash;&gt;-->
<!--&lt;!&ndash;import { computed } from 'vue'&ndash;&gt;-->
<!--&lt;!&ndash;import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card'&ndash;&gt;-->
<!--&lt;!&ndash;import { Progress } from '@/components/ui/progress'&ndash;&gt;-->

<!--&lt;!&ndash;const props = defineProps({&ndash;&gt;-->
<!--&lt;!&ndash;  data: {&ndash;&gt;-->
<!--&lt;!&ndash;    type: Object,&ndash;&gt;-->
<!--&lt;!&ndash;    default: () => ({})&ndash;&gt;-->
<!--&lt;!&ndash;  }&ndash;&gt;-->
<!--&lt;!&ndash;})&ndash;&gt;-->

<!--&lt;!&ndash;const computedIndicators = computed(() => [&ndash;&gt;-->
<!--&lt;!&ndash;  {&ndash;&gt;-->
<!--&lt;!&ndash;    name: 'RSI',&ndash;&gt;-->
<!--&lt;!&ndash;    value: props.data.rsi || 0,&ndash;&gt;-->
<!--&lt;!&ndash;    signal: getRSISignal(props.data.rsi)&ndash;&gt;-->
<!--&lt;!&ndash;  },&ndash;&gt;-->
<!--&lt;!&ndash;  {&ndash;&gt;-->
<!--&lt;!&ndash;    name: 'MACD',&ndash;&gt;-->
<!--&lt;!&ndash;    value: props.data.macd || 0,&ndash;&gt;-->
<!--&lt;!&ndash;    signal: getMACDSignal(props.data.macd, props.data.macd_signal)&ndash;&gt;-->
<!--&lt;!&ndash;  },&ndash;&gt;-->
<!--&lt;!&ndash;  {&ndash;&gt;-->
<!--&lt;!&ndash;    name: 'SMA20',&ndash;&gt;-->
<!--&lt;!&ndash;    value: props.data.sma_20 || 0,&ndash;&gt;-->
<!--&lt;!&ndash;    signal: getSMASignal(props.data.sma_20, props.data.close)&ndash;&gt;-->
<!--&lt;!&ndash;  }&ndash;&gt;-->
<!--&lt;!&ndash;])&ndash;&gt;-->

<!--&lt;!&ndash;const getValueColor = (value) => {&ndash;&gt;-->
<!--&lt;!&ndash;  if (value > 70) return 'text-green-600'&ndash;&gt;-->
<!--&lt;!&ndash;  if (value < 30) return 'text-red-600'&ndash;&gt;-->
<!--&lt;!&ndash;  return 'text-foreground'&ndash;&gt;-->
<!--&lt;!&ndash;}&ndash;&gt;-->

<!--&lt;!&ndash;const getProgressColor = (value) => {&ndash;&gt;-->
<!--&lt;!&ndash;  if (value > 70) return 'bg-green-500'&ndash;&gt;-->
<!--&lt;!&ndash;  if (value < 30) return 'bg-red-500'&ndash;&gt;-->
<!--&lt;!&ndash;  return 'bg-blue-500'&ndash;&gt;-->
<!--&lt;!&ndash;}&ndash;&gt;-->

<!--&lt;!&ndash;const getProgressWidth = (value) => {&ndash;&gt;-->
<!--&lt;!&ndash;  return Math.min(Math.max(value, 0), 100)&ndash;&gt;-->
<!--&lt;!&ndash;}&ndash;&gt;-->

<!--&lt;!&ndash;const formatValue = (value) => {&ndash;&gt;-->
<!--&lt;!&ndash;  return value?.toFixed(2) || '0.00'&ndash;&gt;-->
<!--&lt;!&ndash;}&ndash;&gt;-->

<!--&lt;!&ndash;const getRSISignal = (value) => {&ndash;&gt;-->
<!--&lt;!&ndash;  if (!value) return 'No signal'&ndash;&gt;-->
<!--&lt;!&ndash;  if (value > 70) return 'Overbought'&ndash;&gt;-->
<!--&lt;!&ndash;  if (value < 30) return 'Oversold'&ndash;&gt;-->
<!--&lt;!&ndash;  return 'Neutral'&ndash;&gt;-->
<!--&lt;!&ndash;}&ndash;&gt;-->

<!--&lt;!&ndash;const getMACDSignal = (macd, signal) => {&ndash;&gt;-->
<!--&lt;!&ndash;  if (!macd || !signal) return 'No signal'&ndash;&gt;-->
<!--&lt;!&ndash;  if (macd > signal) return 'Bullish Crossover'&ndash;&gt;-->
<!--&lt;!&ndash;  if (macd < signal) return 'Bearish Crossover'&ndash;&gt;-->
<!--&lt;!&ndash;  return 'Neutral'&ndash;&gt;-->
<!--&lt;!&ndash;}&ndash;&gt;-->

<!--&lt;!&ndash;const getSMASignal = (sma, price) => {&ndash;&gt;-->
<!--&lt;!&ndash;  if (!sma || !price) return 'No signal'&ndash;&gt;-->
<!--&lt;!&ndash;  if (price > sma) return 'Above Average'&ndash;&gt;-->
<!--&lt;!&ndash;  if (price < sma) return 'Below Average'&ndash;&gt;-->
<!--&lt;!&ndash;  return 'At Average'&ndash;&gt;-->
<!--&lt;!&ndash;}&ndash;&gt;-->
<!--&lt;!&ndash;</script>&ndash;&gt;-->


<!--<template>-->
<!--  <Card>-->
<!--    <CardHeader>-->
<!--      <CardTitle>Technical Indicators</CardTitle>-->
<!--    </CardHeader>-->
<!--    <CardContent>-->
<!--      <div class="space-y-4">-->
<!--        &lt;!&ndash; RSI &ndash;&gt;-->
<!--        <div v-if="data?.rsi" class="border-b pb-2">-->
<!--          <div class="flex justify-between items-center">-->
<!--            <span class="font-medium">RSI</span>-->
<!--            <span :class="getRSIColor(data.rsi)">-->
<!--              {{ formatNumber(data.rsi) }}-->
<!--            </span>-->
<!--          </div>-->
<!--          <div class="mt-1">-->
<!--            <Progress :value="data.rsi" class="h-2" :class="getRSIColor(data.rsi)" />-->
<!--          </div>-->
<!--          <p class="text-sm text-muted-foreground mt-1">-->
<!--            {{ getRSISignal(data.rsi) }}-->
<!--          </p>-->
<!--        </div>-->

<!--        &lt;!&ndash; MACD &ndash;&gt;-->
<!--        <div v-if="data?.macd" class="border-b pb-2">-->
<!--          <div class="flex justify-between items-center">-->
<!--            <span class="font-medium">MACD</span>-->
<!--            <span :class="getMACDColor(data.macd, data.macd_signal)">-->
<!--              {{ formatNumber(data.macd) }}-->
<!--            </span>-->
<!--          </div>-->
<!--          <div class="mt-1">-->
<!--            <Progress-->
<!--              :value="getMACDProgress(data.macd)"-->
<!--              class="h-2"-->
<!--              :class="getMACDColor(data.macd, data.macd_signal)"-->
<!--            />-->
<!--          </div>-->
<!--          <p class="text-sm text-muted-foreground mt-1">-->
<!--            Signal: {{ formatNumber(data.macd_signal) }}-->
<!--          </p>-->
<!--        </div>-->

<!--        &lt;!&ndash; Bollinger Bands &ndash;&gt;-->
<!--        <div v-if="data?.bb_middle" class="border-b pb-2">-->
<!--          <div class="flex justify-between items-center">-->
<!--            <span class="font-medium">Bollinger Bands</span>-->
<!--          </div>-->
<!--          <div class="grid grid-cols-3 gap-2 mt-1 text-sm">-->
<!--            <div>-->
<!--              <span class="text-muted-foreground">Upper</span>-->
<!--              <p>${{ formatNumber(data.bb_upper) }}</p>-->
<!--            </div>-->
<!--            <div>-->
<!--              <span class="text-muted-foreground">Middle</span>-->
<!--              <p>${{ formatNumber(data.bb_middle) }}</p>-->
<!--            </div>-->
<!--            <div>-->
<!--              <span class="text-muted-foreground">Lower</span>-->
<!--              <p>${{ formatNumber(data.bb_lower) }}</p>-->
<!--            </div>-->
<!--          </div>-->
<!--        </div>-->

<!--        &lt;!&ndash; Moving Averages &ndash;&gt;-->
<!--        <div v-if="data?.sma_20" class="pt-2">-->
<!--          <div class="flex justify-between items-center">-->
<!--            <span class="font-medium">Moving Averages</span>-->
<!--          </div>-->
<!--          <div class="grid grid-cols-2 gap-2 mt-1 text-sm">-->
<!--            <div>-->
<!--              <span class="text-muted-foreground">SMA20</span>-->
<!--              <p>${{ formatNumber(data.sma_20) }}</p>-->
<!--            </div>-->
<!--            <div v-if="data?.sma_50">-->
<!--              <span class="text-muted-foreground">SMA50</span>-->
<!--              <p>${{ formatNumber(data.sma_50) }}</p>-->
<!--            </div>-->
<!--          </div>-->
<!--        </div>-->
<!--      </div>-->
<!--    </CardContent>-->
<!--  </Card>-->
<!--</template>-->

<!--<script setup>-->
<!--import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card'-->
<!--import { Progress } from '@/components/ui/progress'-->

<!--defineProps({-->
<!--  data: {-->
<!--    type: Object,-->
<!--    default: () => ({})-->
<!--  }-->
<!--})-->

<!--const formatNumber = (value) => {-->
<!--  return value?.toFixed(2) || '0.00'-->
<!--}-->

<!--const getRSIColor = (value) => {-->
<!--  if (value > 70) return 'text-red-500'-->
<!--  if (value < 30) return 'text-green-500'-->
<!--  return 'text-blue-500'-->
<!--}-->

<!--const getRSISignal = (value) => {-->
<!--  if (value > 70) return 'Overbought'-->
<!--  if (value < 30) return 'Oversold'-->
<!--  return 'Neutral'-->
<!--}-->

<!--const getMACDColor = (macd, signal) => {-->
<!--  if (macd > signal) return 'text-green-500'-->
<!--  if (macd < signal) return 'text-red-500'-->
<!--  return 'text-blue-500'-->
<!--}-->

<!--const getMACDProgress = (macd) => {-->
<!--  return Math.abs(macd) * 10-->
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
            <Progress
              :value="data.rsi"
              class="h-2"
              :class="getRSIColor(data.rsi)"
            />
          </div>
          <p class="text-sm text-muted-foreground mt-1">
            {{ getRSISignal(data.rsi) }}
          </p>
        </div>

        <!-- MACD -->
        <div v-if="data?.macd != null" class="border-b pb-2">
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

        <!-- Moving Averages -->
        <div v-if="data?.sma_20 != null" class="border-b pb-2">
          <div class="flex justify-between items-center">
            <span class="font-medium">Moving Averages</span>
          </div>
          <div class="grid grid-cols-2 gap-2 mt-1">
            <div>
              <span class="text-muted-foreground text-sm">SMA20</span>
              <p class="font-medium">${{ formatNumber(data.sma_20) }}</p>
            </div>
            <div v-if="data?.sma_50 != null">
              <span class="text-muted-foreground text-sm">SMA50</span>
              <p class="font-medium">${{ formatNumber(data.sma_50) }}</p>
            </div>
          </div>
        </div>

        <!-- Bollinger Bands -->
        <div v-if="data?.bb_middle != null" class="pt-2">
          <div class="flex justify-between items-center">
            <span class="font-medium">Bollinger Bands</span>
          </div>
          <div class="grid grid-cols-3 gap-2 mt-1">
            <div>
              <span class="text-muted-foreground text-sm">Upper</span>
              <p class="font-medium">${{ formatNumber(data.bb_upper) }}</p>
            </div>
            <div>
              <span class="text-muted-foreground text-sm">Middle</span>
              <p class="font-medium">${{ formatNumber(data.bb_middle) }}</p>
            </div>
            <div>
              <span class="text-muted-foreground text-sm">Lower</span>
              <p class="font-medium">${{ formatNumber(data.bb_lower) }}</p>
            </div>
          </div>
        </div>

        <!-- No Data Message -->
        <div v-if="!hasAnyIndicator" class="text-muted-foreground text-center py-4">
          No technical indicators available
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

const hasAnyIndicator = computed(() => {
  return props.data && Object.keys(props.data).some(key =>
    props.data[key] != null && !isNaN(props.data[key])
  )
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
  if (value > 70) return 'Overbought - Consider Selling'
  if (value < 30) return 'Oversold - Consider Buying'
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