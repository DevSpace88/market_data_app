<!--&lt;!&ndash;&lt;!&ndash;<template>&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;  <Card>&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;    <CardHeader>&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;      <CardTitle>Technical Indicators</CardTitle>&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;    </CardHeader>&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;    <CardContent>&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;      <div class="space-y-4">&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;        <div v-for="indicator in computedIndicators" :key="indicator.name"&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;             class="border-b pb-2 last:border-b-0">&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;          <div class="flex justify-between items-center">&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;            <span class="font-medium">{{ indicator.name }}</span>&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;            <span :class="getValueColor(indicator.value)">&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;              {{ formatValue(indicator.value) }}&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;            </span>&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;          </div>&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;          <div class="mt-1">&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;            <Progress&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;              :value="getProgressWidth(indicator.value)"&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;              :class="getProgressColor(indicator.value)"&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;            />&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;          </div>&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;          <p class="text-sm text-muted-foreground mt-1">{{ indicator.signal }}</p>&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;        </div>&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;      </div>&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;    </CardContent>&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;  </Card>&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;</template>&ndash;&gt;&ndash;&gt;-->

<!--&lt;!&ndash;&lt;!&ndash;<script setup>&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;import { computed } from 'vue'&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card'&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;import { Progress } from '@/components/ui/progress'&ndash;&gt;&ndash;&gt;-->

<!--&lt;!&ndash;&lt;!&ndash;const props = defineProps({&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;  data: {&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;    type: Object,&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;    default: () => ({})&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;  }&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;})&ndash;&gt;&ndash;&gt;-->

<!--&lt;!&ndash;&lt;!&ndash;const computedIndicators = computed(() => [&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;  {&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;    name: 'RSI',&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;    value: props.data.rsi || 0,&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;    signal: getRSISignal(props.data.rsi)&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;  },&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;  {&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;    name: 'MACD',&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;    value: props.data.macd || 0,&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;    signal: getMACDSignal(props.data.macd, props.data.macd_signal)&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;  },&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;  {&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;    name: 'SMA20',&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;    value: props.data.sma_20 || 0,&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;    signal: getSMASignal(props.data.sma_20, props.data.close)&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;  }&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;])&ndash;&gt;&ndash;&gt;-->

<!--&lt;!&ndash;&lt;!&ndash;const getValueColor = (value) => {&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;  if (value > 70) return 'text-green-600'&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;  if (value < 30) return 'text-red-600'&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;  return 'text-foreground'&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;}&ndash;&gt;&ndash;&gt;-->

<!--&lt;!&ndash;&lt;!&ndash;const getProgressColor = (value) => {&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;  if (value > 70) return 'bg-green-500'&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;  if (value < 30) return 'bg-red-500'&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;  return 'bg-blue-500'&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;}&ndash;&gt;&ndash;&gt;-->

<!--&lt;!&ndash;&lt;!&ndash;const getProgressWidth = (value) => {&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;  return Math.min(Math.max(value, 0), 100)&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;}&ndash;&gt;&ndash;&gt;-->

<!--&lt;!&ndash;&lt;!&ndash;const formatValue = (value) => {&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;  return value?.toFixed(2) || '0.00'&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;}&ndash;&gt;&ndash;&gt;-->

<!--&lt;!&ndash;&lt;!&ndash;const getRSISignal = (value) => {&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;  if (!value) return 'No signal'&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;  if (value > 70) return 'Overbought'&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;  if (value < 30) return 'Oversold'&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;  return 'Neutral'&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;}&ndash;&gt;&ndash;&gt;-->

<!--&lt;!&ndash;&lt;!&ndash;const getMACDSignal = (macd, signal) => {&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;  if (!macd || !signal) return 'No signal'&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;  if (macd > signal) return 'Bullish Crossover'&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;  if (macd < signal) return 'Bearish Crossover'&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;  return 'Neutral'&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;}&ndash;&gt;&ndash;&gt;-->

<!--&lt;!&ndash;&lt;!&ndash;const getSMASignal = (sma, price) => {&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;  if (!sma || !price) return 'No signal'&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;  if (price > sma) return 'Above Average'&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;  if (price < sma) return 'Below Average'&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;  return 'At Average'&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;}&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;</script>&ndash;&gt;&ndash;&gt;-->


<!--&lt;!&ndash;<template>&ndash;&gt;-->
<!--&lt;!&ndash;  <Card>&ndash;&gt;-->
<!--&lt;!&ndash;    <CardHeader>&ndash;&gt;-->
<!--&lt;!&ndash;      <CardTitle>Technical Indicators</CardTitle>&ndash;&gt;-->
<!--&lt;!&ndash;    </CardHeader>&ndash;&gt;-->
<!--&lt;!&ndash;    <CardContent>&ndash;&gt;-->
<!--&lt;!&ndash;      <div class="space-y-4">&ndash;&gt;-->
<!--&lt;!&ndash;        &lt;!&ndash; RSI &ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;        <div v-if="data?.rsi" class="border-b pb-2">&ndash;&gt;-->
<!--&lt;!&ndash;          <div class="flex justify-between items-center">&ndash;&gt;-->
<!--&lt;!&ndash;            <span class="font-medium">RSI</span>&ndash;&gt;-->
<!--&lt;!&ndash;            <span :class="getRSIColor(data.rsi)">&ndash;&gt;-->
<!--&lt;!&ndash;              {{ formatNumber(data.rsi) }}&ndash;&gt;-->
<!--&lt;!&ndash;            </span>&ndash;&gt;-->
<!--&lt;!&ndash;          </div>&ndash;&gt;-->
<!--&lt;!&ndash;          <div class="mt-1">&ndash;&gt;-->
<!--&lt;!&ndash;            <Progress :value="data.rsi" class="h-2" :class="getRSIColor(data.rsi)" />&ndash;&gt;-->
<!--&lt;!&ndash;          </div>&ndash;&gt;-->
<!--&lt;!&ndash;          <p class="text-sm text-muted-foreground mt-1">&ndash;&gt;-->
<!--&lt;!&ndash;            {{ getRSISignal(data.rsi) }}&ndash;&gt;-->
<!--&lt;!&ndash;          </p>&ndash;&gt;-->
<!--&lt;!&ndash;        </div>&ndash;&gt;-->

<!--&lt;!&ndash;        &lt;!&ndash; MACD &ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;        <div v-if="data?.macd" class="border-b pb-2">&ndash;&gt;-->
<!--&lt;!&ndash;          <div class="flex justify-between items-center">&ndash;&gt;-->
<!--&lt;!&ndash;            <span class="font-medium">MACD</span>&ndash;&gt;-->
<!--&lt;!&ndash;            <span :class="getMACDColor(data.macd, data.macd_signal)">&ndash;&gt;-->
<!--&lt;!&ndash;              {{ formatNumber(data.macd) }}&ndash;&gt;-->
<!--&lt;!&ndash;            </span>&ndash;&gt;-->
<!--&lt;!&ndash;          </div>&ndash;&gt;-->
<!--&lt;!&ndash;          <div class="mt-1">&ndash;&gt;-->
<!--&lt;!&ndash;            <Progress&ndash;&gt;-->
<!--&lt;!&ndash;              :value="getMACDProgress(data.macd)"&ndash;&gt;-->
<!--&lt;!&ndash;              class="h-2"&ndash;&gt;-->
<!--&lt;!&ndash;              :class="getMACDColor(data.macd, data.macd_signal)"&ndash;&gt;-->
<!--&lt;!&ndash;            />&ndash;&gt;-->
<!--&lt;!&ndash;          </div>&ndash;&gt;-->
<!--&lt;!&ndash;          <p class="text-sm text-muted-foreground mt-1">&ndash;&gt;-->
<!--&lt;!&ndash;            Signal: {{ formatNumber(data.macd_signal) }}&ndash;&gt;-->
<!--&lt;!&ndash;          </p>&ndash;&gt;-->
<!--&lt;!&ndash;        </div>&ndash;&gt;-->

<!--&lt;!&ndash;        &lt;!&ndash; Bollinger Bands &ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;        <div v-if="data?.bb_middle" class="border-b pb-2">&ndash;&gt;-->
<!--&lt;!&ndash;          <div class="flex justify-between items-center">&ndash;&gt;-->
<!--&lt;!&ndash;            <span class="font-medium">Bollinger Bands</span>&ndash;&gt;-->
<!--&lt;!&ndash;          </div>&ndash;&gt;-->
<!--&lt;!&ndash;          <div class="grid grid-cols-3 gap-2 mt-1 text-sm">&ndash;&gt;-->
<!--&lt;!&ndash;            <div>&ndash;&gt;-->
<!--&lt;!&ndash;              <span class="text-muted-foreground">Upper</span>&ndash;&gt;-->
<!--&lt;!&ndash;              <p>${{ formatNumber(data.bb_upper) }}</p>&ndash;&gt;-->
<!--&lt;!&ndash;            </div>&ndash;&gt;-->
<!--&lt;!&ndash;            <div>&ndash;&gt;-->
<!--&lt;!&ndash;              <span class="text-muted-foreground">Middle</span>&ndash;&gt;-->
<!--&lt;!&ndash;              <p>${{ formatNumber(data.bb_middle) }}</p>&ndash;&gt;-->
<!--&lt;!&ndash;            </div>&ndash;&gt;-->
<!--&lt;!&ndash;            <div>&ndash;&gt;-->
<!--&lt;!&ndash;              <span class="text-muted-foreground">Lower</span>&ndash;&gt;-->
<!--&lt;!&ndash;              <p>${{ formatNumber(data.bb_lower) }}</p>&ndash;&gt;-->
<!--&lt;!&ndash;            </div>&ndash;&gt;-->
<!--&lt;!&ndash;          </div>&ndash;&gt;-->
<!--&lt;!&ndash;        </div>&ndash;&gt;-->

<!--&lt;!&ndash;        &lt;!&ndash; Moving Averages &ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;        <div v-if="data?.sma_20" class="pt-2">&ndash;&gt;-->
<!--&lt;!&ndash;          <div class="flex justify-between items-center">&ndash;&gt;-->
<!--&lt;!&ndash;            <span class="font-medium">Moving Averages</span>&ndash;&gt;-->
<!--&lt;!&ndash;          </div>&ndash;&gt;-->
<!--&lt;!&ndash;          <div class="grid grid-cols-2 gap-2 mt-1 text-sm">&ndash;&gt;-->
<!--&lt;!&ndash;            <div>&ndash;&gt;-->
<!--&lt;!&ndash;              <span class="text-muted-foreground">SMA20</span>&ndash;&gt;-->
<!--&lt;!&ndash;              <p>${{ formatNumber(data.sma_20) }}</p>&ndash;&gt;-->
<!--&lt;!&ndash;            </div>&ndash;&gt;-->
<!--&lt;!&ndash;            <div v-if="data?.sma_50">&ndash;&gt;-->
<!--&lt;!&ndash;              <span class="text-muted-foreground">SMA50</span>&ndash;&gt;-->
<!--&lt;!&ndash;              <p>${{ formatNumber(data.sma_50) }}</p>&ndash;&gt;-->
<!--&lt;!&ndash;            </div>&ndash;&gt;-->
<!--&lt;!&ndash;          </div>&ndash;&gt;-->
<!--&lt;!&ndash;        </div>&ndash;&gt;-->
<!--&lt;!&ndash;      </div>&ndash;&gt;-->
<!--&lt;!&ndash;    </CardContent>&ndash;&gt;-->
<!--&lt;!&ndash;  </Card>&ndash;&gt;-->
<!--&lt;!&ndash;</template>&ndash;&gt;-->

<!--&lt;!&ndash;<script setup>&ndash;&gt;-->
<!--&lt;!&ndash;import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card'&ndash;&gt;-->
<!--&lt;!&ndash;import { Progress } from '@/components/ui/progress'&ndash;&gt;-->

<!--&lt;!&ndash;defineProps({&ndash;&gt;-->
<!--&lt;!&ndash;  data: {&ndash;&gt;-->
<!--&lt;!&ndash;    type: Object,&ndash;&gt;-->
<!--&lt;!&ndash;    default: () => ({})&ndash;&gt;-->
<!--&lt;!&ndash;  }&ndash;&gt;-->
<!--&lt;!&ndash;})&ndash;&gt;-->

<!--&lt;!&ndash;const formatNumber = (value) => {&ndash;&gt;-->
<!--&lt;!&ndash;  return value?.toFixed(2) || '0.00'&ndash;&gt;-->
<!--&lt;!&ndash;}&ndash;&gt;-->

<!--&lt;!&ndash;const getRSIColor = (value) => {&ndash;&gt;-->
<!--&lt;!&ndash;  if (value > 70) return 'text-red-500'&ndash;&gt;-->
<!--&lt;!&ndash;  if (value < 30) return 'text-green-500'&ndash;&gt;-->
<!--&lt;!&ndash;  return 'text-blue-500'&ndash;&gt;-->
<!--&lt;!&ndash;}&ndash;&gt;-->

<!--&lt;!&ndash;const getRSISignal = (value) => {&ndash;&gt;-->
<!--&lt;!&ndash;  if (value > 70) return 'Overbought'&ndash;&gt;-->
<!--&lt;!&ndash;  if (value < 30) return 'Oversold'&ndash;&gt;-->
<!--&lt;!&ndash;  return 'Neutral'&ndash;&gt;-->
<!--&lt;!&ndash;}&ndash;&gt;-->

<!--&lt;!&ndash;const getMACDColor = (macd, signal) => {&ndash;&gt;-->
<!--&lt;!&ndash;  if (macd > signal) return 'text-green-500'&ndash;&gt;-->
<!--&lt;!&ndash;  if (macd < signal) return 'text-red-500'&ndash;&gt;-->
<!--&lt;!&ndash;  return 'text-blue-500'&ndash;&gt;-->
<!--&lt;!&ndash;}&ndash;&gt;-->

<!--&lt;!&ndash;const getMACDProgress = (macd) => {&ndash;&gt;-->
<!--&lt;!&ndash;  return Math.abs(macd) * 10&ndash;&gt;-->
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
<!--            <Progress-->
<!--              :value="data.rsi"-->
<!--              class="h-2"-->
<!--              :class="getRSIColor(data.rsi)"-->
<!--            />-->
<!--          </div>-->
<!--          <p class="text-sm text-muted-foreground mt-1">-->
<!--            {{ getRSISignal(data.rsi) }}-->
<!--          </p>-->
<!--        </div>-->

<!--        &lt;!&ndash; MACD &ndash;&gt;-->
<!--        <div v-if="data?.macd != null" class="border-b pb-2">-->
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

<!--        &lt;!&ndash; Moving Averages &ndash;&gt;-->
<!--        <div v-if="data?.sma_20 != null" class="border-b pb-2">-->
<!--          <div class="flex justify-between items-center">-->
<!--            <span class="font-medium">Moving Averages</span>-->
<!--          </div>-->
<!--          <div class="grid grid-cols-2 gap-2 mt-1">-->
<!--            <div>-->
<!--              <span class="text-muted-foreground text-sm">SMA20</span>-->
<!--              <p class="font-medium">${{ formatNumber(data.sma_20) }}</p>-->
<!--            </div>-->
<!--            <div v-if="data?.sma_50 != null">-->
<!--              <span class="text-muted-foreground text-sm">SMA50</span>-->
<!--              <p class="font-medium">${{ formatNumber(data.sma_50) }}</p>-->
<!--            </div>-->
<!--          </div>-->
<!--        </div>-->

<!--        &lt;!&ndash; Bollinger Bands &ndash;&gt;-->
<!--        <div v-if="data?.bb_middle != null" class="pt-2">-->
<!--          <div class="flex justify-between items-center">-->
<!--            <span class="font-medium">Bollinger Bands</span>-->
<!--          </div>-->
<!--          <div class="grid grid-cols-3 gap-2 mt-1">-->
<!--            <div>-->
<!--              <span class="text-muted-foreground text-sm">Upper</span>-->
<!--              <p class="font-medium">${{ formatNumber(data.bb_upper) }}</p>-->
<!--            </div>-->
<!--            <div>-->
<!--              <span class="text-muted-foreground text-sm">Middle</span>-->
<!--              <p class="font-medium">${{ formatNumber(data.bb_middle) }}</p>-->
<!--            </div>-->
<!--            <div>-->
<!--              <span class="text-muted-foreground text-sm">Lower</span>-->
<!--              <p class="font-medium">${{ formatNumber(data.bb_lower) }}</p>-->
<!--            </div>-->
<!--          </div>-->
<!--        </div>-->

<!--        &lt;!&ndash; No Data Message &ndash;&gt;-->
<!--        <div v-if="!hasAnyIndicator" class="text-muted-foreground text-center py-4">-->
<!--          No technical indicators available-->
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

<!--const hasAnyIndicator = computed(() => {-->
<!--  return props.data && Object.keys(props.data).some(key =>-->
<!--    props.data[key] != null && !isNaN(props.data[key])-->
<!--  )-->
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
<!--  if (value > 70) return 'Overbought - Consider Selling'-->
<!--  if (value < 30) return 'Oversold - Consider Buying'-->
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
      <div class="space-y-6">
        <!-- RSI Indikator -->
        <div v-if="data?.rsi" class="border-b pb-4">
          <div class="flex justify-between items-center mb-1">
            <span class="font-medium">RSI</span>
            <span :class="getRSIColor(data.rsi)">
              {{ formatNumber(data.rsi) }}
            </span>
          </div>
          <div class="relative h-2 mb-1">
            <div class="absolute w-full h-full bg-muted rounded-full"></div>
            <div
              class="absolute h-full rounded-full transition-all duration-300"
              :class="getRSIBarColor(data.rsi)"
              :style="{ width: `${Math.min(100, data.rsi)}%` }"
            ></div>
            <!-- Markierungen für Overbought/Oversold -->
            <div class="absolute h-full w-px bg-muted-foreground/30" style="left: 30%"></div>
            <div class="absolute h-full w-px bg-muted-foreground/30" style="left: 70%"></div>
          </div>
          <p class="text-sm text-muted-foreground mt-1">
            {{ getRSISignal(data.rsi) }}
          </p>
        </div>

        <!-- MACD Indikator -->
        <div v-if="data?.macd != null" class="border-b pb-4">
          <div class="flex justify-between items-center mb-1">
            <span class="font-medium">MACD</span>
            <span :class="getMACDColor(data.macd, data.macd_signal)">
              {{ formatNumber(data.macd) }}
            </span>
          </div>
          <div class="relative h-2 mb-1">
            <div class="absolute w-full h-full bg-muted rounded-full"></div>
            <div
              class="absolute h-full rounded-full transition-all duration-300"
              :class="getMACDBarColor(data.macd, data.macd_signal)"
              :style="{
                width: `${getMACDBarWidth(data.macd)}%`,
                left: data.macd < 0 ? 'auto' : '50%',
                right: data.macd < 0 ? '50%' : 'auto'
              }"
            ></div>
            <!-- Mittellinie -->
            <div class="absolute h-full w-px bg-muted-foreground/50" style="left: 50%"></div>
          </div>
          <div class="flex justify-between text-sm text-muted-foreground mt-1">
            <span>Signal: {{ formatNumber(data.macd_signal) }}</span>
            <span>{{ getMACDSignal(data.macd, data.macd_signal) }}</span>
          </div>
        </div>

        <!-- Moving Averages -->
        <div v-if="data?.sma_20 != null" class="pt-2">
          <div class="flex justify-between items-center mb-3">
            <span class="font-medium">Moving Averages</span>
          </div>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <span class="text-sm text-muted-foreground">SMA20</span>
              <p class="font-medium">${{ formatNumber(data.sma_20) }}</p>
            </div>
            <div v-if="data?.sma_50 != null">
              <span class="text-sm text-muted-foreground">SMA50</span>
              <p class="font-medium">${{ formatNumber(data.sma_50) }}</p>
            </div>
          </div>
        </div>

        <div v-if="!hasAnyIndicator" class="text-muted-foreground text-center py-8">
          <AlertCircle class="h-6 w-6 mx-auto mb-2 opacity-50" />
          <p>No technical indicators available</p>
        </div>
      </div>
    </CardContent>
  </Card>
</template>

<script setup>
import { computed } from 'vue'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card'
import { AlertCircle } from 'lucide-vue-next'

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

// RSI Funktionen
const getRSIColor = (value) => {
  if (value > 70) return 'text-destructive font-medium'
  if (value < 30) return 'text-green-500 font-medium'
  return 'text-blue-500 font-medium'
}

const getRSIBarColor = (value) => {
  if (value > 70) return 'bg-destructive/90'
  if (value < 30) return 'bg-green-500/90'
  return 'bg-blue-500/90'
}

const getRSISignal = (value) => {
  if (value > 70) return 'Overbought - Consider Selling'
  if (value < 30) return 'Oversold - Consider Buying'
  return 'Neutral'
}

// MACD Funktionen
const getMACDColor = (macd, signal) => {
  if (macd > signal) return 'text-green-500 font-medium'
  if (macd < signal) return 'text-destructive font-medium'
  return 'text-blue-500 font-medium'
}

const getMACDBarColor = (macd, signal) => {
  if (macd > signal) return 'bg-green-500/90'
  if (macd < signal) return 'bg-destructive/90'
  return 'bg-blue-500/90'
}

const getMACDBarWidth = (macd) => {
  // Konvertiert den MACD-Wert in eine Prozentbreite
  const maxWidth = 45 // Max 45% auf jeder Seite
  const absValue = Math.abs(macd)
  return Math.min(maxWidth, absValue * 20) // Skalierungsfaktor von 20
}

const getMACDSignal = (macd, signal) => {
  if (macd > signal) return 'Bullish'
  if (macd < signal) return 'Bearish'
  return 'Neutral'
}
</script>
