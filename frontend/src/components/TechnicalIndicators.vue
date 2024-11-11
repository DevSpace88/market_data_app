<!--<template>-->
<!--  <Card>-->
<!--    <CardHeader>-->
<!--      <CardTitle>Technical Indicators</CardTitle>-->
<!--    </CardHeader>-->
<!--    <CardContent>-->
<!--      <div class="space-y-6">-->
<!--        &lt;!&ndash; RSI Indikator &ndash;&gt;-->
<!--        <div v-if="data?.rsi" class="border-b pb-4">-->
<!--          <div class="flex justify-between items-center mb-1">-->
<!--            <span class="font-medium">RSI</span>-->
<!--            <span :class="getRSIColor(data.rsi)">-->
<!--              {{ formatNumber(data.rsi) }}-->
<!--            </span>-->
<!--          </div>-->
<!--          <div class="relative h-2 mb-1">-->
<!--            <div class="absolute w-full h-full bg-muted rounded-full"></div>-->
<!--            <div-->
<!--              class="absolute h-full rounded-full transition-all duration-300"-->
<!--              :class="getRSIBarColor(data.rsi)"-->
<!--              :style="{ width: `${Math.min(100, data.rsi)}%` }"-->
<!--            ></div>-->
<!--            &lt;!&ndash; Markierungen für Overbought/Oversold &ndash;&gt;-->
<!--            <div class="absolute h-full w-px bg-muted-foreground/30" style="left: 30%"></div>-->
<!--            <div class="absolute h-full w-px bg-muted-foreground/30" style="left: 70%"></div>-->
<!--          </div>-->
<!--          <p class="text-sm text-muted-foreground mt-1">-->
<!--            {{ getRSISignal(data.rsi) }}-->
<!--          </p>-->
<!--        </div>-->

<!--        &lt;!&ndash; MACD Indikator &ndash;&gt;-->
<!--        <div v-if="data?.macd != null" class="border-b pb-4">-->
<!--          <div class="flex justify-between items-center mb-1">-->
<!--            <span class="font-medium">MACD</span>-->
<!--            <span :class="getMACDColor(data.macd, data.macd_signal)">-->
<!--              {{ formatNumber(data.macd) }}-->
<!--            </span>-->
<!--          </div>-->
<!--          <div class="relative h-2 mb-1">-->
<!--            <div class="absolute w-full h-full bg-muted rounded-full"></div>-->
<!--            <div-->
<!--              class="absolute h-full rounded-full transition-all duration-300"-->
<!--              :class="getMACDBarColor(data.macd, data.macd_signal)"-->
<!--              :style="{-->
<!--                width: `${getMACDBarWidth(data.macd)}%`,-->
<!--                left: data.macd < 0 ? 'auto' : '50%',-->
<!--                right: data.macd < 0 ? '50%' : 'auto'-->
<!--              }"-->
<!--            ></div>-->
<!--            &lt;!&ndash; Mittellinie &ndash;&gt;-->
<!--            <div class="absolute h-full w-px bg-muted-foreground/50" style="left: 50%"></div>-->
<!--          </div>-->
<!--          <div class="flex justify-between text-sm text-muted-foreground mt-1">-->
<!--            <span>Signal: {{ formatNumber(data.macd_signal) }}</span>-->
<!--            <span>{{ getMACDSignal(data.macd, data.macd_signal) }}</span>-->
<!--          </div>-->
<!--        </div>-->

<!--        &lt;!&ndash; Moving Averages &ndash;&gt;-->
<!--        <div v-if="data?.sma_20 != null" class="pt-2">-->
<!--          <div class="flex justify-between items-center mb-3">-->
<!--            <span class="font-medium">Moving Averages</span>-->
<!--          </div>-->
<!--          <div class="grid grid-cols-2 gap-4">-->
<!--            <div>-->
<!--              <span class="text-sm text-muted-foreground">SMA20</span>-->
<!--              <p class="font-medium">${{ formatNumber(data.sma_20) }}</p>-->
<!--            </div>-->
<!--            <div v-if="data?.sma_50 != null">-->
<!--              <span class="text-sm text-muted-foreground">SMA50</span>-->
<!--              <p class="font-medium">${{ formatNumber(data.sma_50) }}</p>-->
<!--            </div>-->
<!--          </div>-->
<!--        </div>-->

<!--        <div v-if="!hasAnyIndicator" class="text-muted-foreground text-center py-8">-->
<!--          <AlertCircle class="h-6 w-6 mx-auto mb-2 opacity-50" />-->
<!--          <p>No technical indicators available</p>-->
<!--        </div>-->
<!--      </div>-->
<!--    </CardContent>-->
<!--  </Card>-->
<!--</template>-->

<!--<script setup>-->
<!--import { computed } from 'vue'-->
<!--import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card'-->
<!--import { AlertCircle } from 'lucide-vue-next'-->

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

<!--// RSI Funktionen-->
<!--const getRSIColor = (value) => {-->
<!--  if (value > 70) return 'text-destructive font-medium'-->
<!--  if (value < 30) return 'text-green-500 font-medium'-->
<!--  return 'text-blue-500 font-medium'-->
<!--}-->

<!--const getRSIBarColor = (value) => {-->
<!--  if (value > 70) return 'bg-destructive/90'-->
<!--  if (value < 30) return 'bg-green-500/90'-->
<!--  return 'bg-blue-500/90'-->
<!--}-->

<!--const getRSISignal = (value) => {-->
<!--  if (value > 70) return 'Overbought - Consider Selling'-->
<!--  if (value < 30) return 'Oversold - Consider Buying'-->
<!--  return 'Neutral'-->
<!--}-->

<!--// MACD Funktionen-->
<!--const getMACDColor = (macd, signal) => {-->
<!--  if (macd > signal) return 'text-green-500 font-medium'-->
<!--  if (macd < signal) return 'text-destructive font-medium'-->
<!--  return 'text-blue-500 font-medium'-->
<!--}-->

<!--const getMACDBarColor = (macd, signal) => {-->
<!--  if (macd > signal) return 'bg-green-500/90'-->
<!--  if (macd < signal) return 'bg-destructive/90'-->
<!--  return 'bg-blue-500/90'-->
<!--}-->

<!--const getMACDBarWidth = (macd) => {-->
<!--  // Konvertiert den MACD-Wert in eine Prozentbreite-->
<!--  const maxWidth = 45 // Max 45% auf jeder Seite-->
<!--  const absValue = Math.abs(macd)-->
<!--  return Math.min(maxWidth, absValue * 20) // Skalierungsfaktor von 20-->
<!--}-->

<!--const getMACDSignal = (macd, signal) => {-->
<!--  if (macd > signal) return 'Bullish'-->
<!--  if (macd < signal) return 'Bearish'-->
<!--  return 'Neutral'-->
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
              <p class="font-medium">{{ currencySymbol }}{{ formatNumber(data.sma_20) }}</p>
            </div>
            <div v-if="data?.sma_50 != null">
              <span class="text-sm text-muted-foreground">SMA50</span>
              <p class="font-medium">{{ currencySymbol }}{{ formatNumber(data.sma_50) }}</p>
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
import { useMarketStore } from '@/stores/market'

const marketStore = useMarketStore()

const props = defineProps({
  data: {
    type: Object,
    default: () => ({})
  },
  currency: {
    type: String,
    default: 'USD'
  },
  currencySymbol: {
    type: String,
    default: '$'
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