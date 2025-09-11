<!--<template>-->
<!--  <Card>-->
<!--    <CardHeader>-->
<!--      <CardTitle>{{ t('symbolAnalysis.technicalIndicators') }}</CardTitle>-->
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
      <CardTitle>{{ t('symbolAnalysis.technicalIndicators') }}</CardTitle>
    </CardHeader>
    <CardContent>
      <div class="space-y-6">
        <!-- RSI Indikator -->
        <div v-if="data?.rsi" class="border-b pb-4">
          <div class="flex justify-between items-center mb-1">
            <div class="flex items-center gap-2">
              <span class="font-medium">RSI</span>
              <div class="group relative">
                <Info class="h-4 w-4 text-muted-foreground cursor-help" />
                <div class="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 px-3 py-2 bg-popover text-popover-foreground text-xs rounded-md shadow-lg opacity-0 group-hover:opacity-100 transition-opacity duration-200 w-64 z-10">
                  Relative Strength Index (0-100). Über 70 = überkauft, unter 30 = überverkauft. Misst Momentum der Preisbewegungen.
                </div>
              </div>
            </div>
            <div class="text-right">
              <span :class="getRSIColor(data.rsi)" class="text-lg font-bold">
                {{ formatNumber(data.rsi) }}
              </span>
              <div class="text-xs text-muted-foreground">
                {{ getRSISignal(data.rsi) }}
              </div>
            </div>
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
        </div>

        <!-- MACD Indikator -->
        <div v-if="data?.macd != null" class="border-b pb-4">
          <div class="flex justify-between items-center mb-1">
            <div class="flex items-center gap-2">
              <span class="font-medium">MACD</span>
              <div class="group relative">
                <Info class="h-4 w-4 text-muted-foreground cursor-help" />
                <div class="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 px-3 py-2 bg-popover text-popover-foreground text-xs rounded-md shadow-lg opacity-0 group-hover:opacity-100 transition-opacity duration-200 w-64 z-10">
                  Moving Average Convergence Divergence. Differenz zwischen 12- und 26-Tage EMA. Positive Werte = bullisch, negative = bärisch.
                </div>
              </div>
            </div>
            <div class="text-right">
              <span :class="getMACDColor(data.macd, data.macd_signal)" class="text-lg font-bold">
                {{ formatNumber(data.macd) }}
              </span>
              <div class="text-xs text-muted-foreground">
                Signal: {{ formatNumber(data.macd_signal) }}
              </div>
            </div>
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
          <div class="text-sm text-muted-foreground mt-1">
            {{ getMACDSignal(data.macd, data.macd_signal) }}
          </div>
        </div>

        <!-- Moving Averages -->
        <div v-if="data?.sma_20 != null" class="pt-2">
          <div class="flex justify-between items-center mb-3">
            <div class="flex items-center gap-2">
              <span class="font-medium">Moving Averages</span>
              <div class="group relative">
                <Info class="h-4 w-4 text-muted-foreground cursor-help" />
                <div class="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 px-3 py-2 bg-popover text-popover-foreground text-xs rounded-md shadow-lg opacity-0 group-hover:opacity-100 transition-opacity duration-200 w-64 z-10">
                  Gleitende Durchschnitte glätten Preisschwankungen. SMA = Simple, EMA = Exponential (reagiert schneller auf Änderungen).
                </div>
              </div>
            </div>
          </div>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <div class="flex items-center gap-2 mb-1">
                <span class="text-sm text-muted-foreground">SMA20</span>
                <div class="text-xs text-muted-foreground">
                  {{ currentPrice > data.sma_20 ? '↑' : '↓' }} {{ formatNumber(Math.abs(((currentPrice - data.sma_20) / data.sma_20) * 100)) }}%
                </div>
              </div>
              <p class="font-medium text-lg">{{ currencySymbol }}{{ formatNumber(data.sma_20) }}</p>
            </div>
            <div v-if="data?.sma_50 != null">
              <div class="flex items-center gap-2 mb-1">
                <span class="text-sm text-muted-foreground">SMA50</span>
                <div class="text-xs text-muted-foreground">
                  {{ currentPrice > data.sma_50 ? '↑' : '↓' }} {{ formatNumber(Math.abs(((currentPrice - data.sma_50) / data.sma_50) * 100)) }}%
                </div>
              </div>
              <p class="font-medium text-lg">{{ currencySymbol }}{{ formatNumber(data.sma_50) }}</p>
            </div>
            <div v-if="data?.sma_200 != null">
              <div class="flex items-center gap-2 mb-1">
                <span class="text-sm text-muted-foreground">SMA200</span>
                <div class="text-xs text-muted-foreground">
                  {{ currentPrice > data.sma_200 ? '↑' : '↓' }} {{ formatNumber(Math.abs(((currentPrice - data.sma_200) / data.sma_200) * 100)) }}%
                </div>
              </div>
              <p class="font-medium text-lg">{{ currencySymbol }}{{ formatNumber(data.sma_200) }}</p>
            </div>
            <div v-if="data?.ema_12 != null">
              <div class="flex items-center gap-2 mb-1">
                <span class="text-sm text-muted-foreground">EMA12</span>
                <div class="text-xs text-muted-foreground">
                  {{ currentPrice > data.ema_12 ? '↑' : '↓' }} {{ formatNumber(Math.abs(((currentPrice - data.ema_12) / data.ema_12) * 100)) }}%
                </div>
              </div>
              <p class="font-medium text-lg">{{ currencySymbol }}{{ formatNumber(data.ema_12) }}</p>
            </div>
          </div>
        </div>

        <!-- Stochastic Oscillator -->
        <div v-if="data?.stoch_k != null" class="border-b pb-4">
          <div class="flex justify-between items-center mb-1">
            <div class="flex items-center gap-2">
              <span class="font-medium">Stochastic</span>
              <div class="group relative">
                <Info class="h-4 w-4 text-muted-foreground cursor-help" />
                <div class="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 px-3 py-2 bg-popover text-popover-foreground text-xs rounded-md shadow-lg opacity-0 group-hover:opacity-100 transition-opacity duration-200 w-64 z-10">
                  Vergleicht Schlusskurs mit 14-Tage Range. K% = %K, D% = 3-Tage Durchschnitt. Über 80 = überkauft, unter 20 = überverkauft.
                </div>
              </div>
            </div>
            <div class="text-right">
              <div class="flex gap-2">
                <span :class="getStochColor(data.stoch_k)" class="text-lg font-bold">{{ formatNumber(data.stoch_k) }}%</span>
                <span class="text-muted-foreground">/</span>
                <span class="text-muted-foreground">{{ formatNumber(data.stoch_d) }}%</span>
              </div>
              <div class="text-xs text-muted-foreground">
                {{ getStochSignal(data.stoch_k, data.stoch_d) }}
              </div>
            </div>
          </div>
          <div class="relative h-2 mb-1">
            <div class="absolute w-full h-full bg-muted rounded-full"></div>
            <div
              class="absolute h-full rounded-full transition-all duration-300"
              :class="getStochBarColor(data.stoch_k)"
              :style="{ width: `${Math.min(100, data.stoch_k)}%` }"
            ></div>
            <div class="absolute h-full w-px bg-muted-foreground/30" style="left: 20%"></div>
            <div class="absolute h-full w-px bg-muted-foreground/30" style="left: 80%"></div>
          </div>
        </div>

        <!-- Williams %R -->
        <div v-if="data?.williams_r != null" class="border-b pb-4">
          <div class="flex justify-between items-center mb-1">
            <div class="flex items-center gap-2">
              <span class="font-medium">Williams %R</span>
              <div class="group relative">
                <Info class="h-4 w-4 text-muted-foreground cursor-help" />
                <div class="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 px-3 py-2 bg-popover text-popover-foreground text-xs rounded-md shadow-lg opacity-0 group-hover:opacity-100 transition-opacity duration-200 w-64 z-10">
                  Momentum-Oszillator (-100 bis 0). Über -20 = überkauft, unter -80 = überverkauft. Ähnlich wie Stochastic, aber mit negativen Werten.
                </div>
              </div>
            </div>
            <div class="text-right">
              <span :class="getWilliamsColor(data.williams_r)" class="text-lg font-bold">
                {{ formatNumber(data.williams_r) }}%
              </span>
              <div class="text-xs text-muted-foreground">
                {{ getWilliamsSignal(data.williams_r) }}
              </div>
            </div>
          </div>
          <div class="relative h-2 mb-1">
            <div class="absolute w-full h-full bg-muted rounded-full"></div>
            <div
              class="absolute h-full rounded-full transition-all duration-300"
              :class="getWilliamsBarColor(data.williams_r)"
              :style="{ width: `${Math.min(100, Math.abs(data.williams_r))}%` }"
            ></div>
            <div class="absolute h-full w-px bg-muted-foreground/30" style="left: 20%"></div>
            <div class="absolute h-full w-px bg-muted-foreground/30" style="left: 80%"></div>
          </div>
        </div>

        <!-- CCI -->
        <div v-if="data?.cci != null" class="border-b pb-4">
          <div class="flex justify-between items-center mb-1">
            <div class="flex items-center gap-2">
              <span class="font-medium">CCI</span>
              <div class="group relative">
                <Info class="h-4 w-4 text-muted-foreground cursor-help" />
                <div class="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 px-3 py-2 bg-popover text-popover-foreground text-xs rounded-md shadow-lg opacity-0 group-hover:opacity-100 transition-opacity duration-200 w-64 z-10">
                  Commodity Channel Index misst Abweichung vom typischen Preis. Über +100 = überkauft, unter -100 = überverkauft. Unbegrenzte Skala.
                </div>
              </div>
            </div>
            <div class="text-right">
              <span :class="getCCIColor(data.cci)" class="text-lg font-bold">
                {{ formatNumber(data.cci) }}
              </span>
              <div class="text-xs text-muted-foreground">
                {{ getCCISignal(data.cci) }}
              </div>
            </div>
          </div>
          <div class="relative h-2 mb-1">
            <div class="absolute w-full h-full bg-muted rounded-full"></div>
            <div
              class="absolute h-full rounded-full transition-all duration-300"
              :class="getCCIBarColor(data.cci)"
              :style="{ width: `${Math.min(100, Math.abs(data.cci) / 2)}%` }"
            ></div>
            <div class="absolute h-full w-px bg-muted-foreground/30" style="left: 25%"></div>
            <div class="absolute h-full w-px bg-muted-foreground/30" style="left: 75%"></div>
          </div>
        </div>

        <!-- ADX -->
        <div v-if="data?.adx != null" class="border-b pb-4">
          <div class="flex justify-between items-center mb-1">
            <div class="flex items-center gap-2">
              <span class="font-medium">ADX</span>
              <div class="group relative">
                <Info class="h-4 w-4 text-muted-foreground cursor-help" />
                <div class="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 px-3 py-2 bg-popover text-popover-foreground text-xs rounded-md shadow-lg opacity-0 group-hover:opacity-100 transition-opacity duration-200 w-64 z-10">
                  Average Directional Index misst Trendstärke (0-100). Über 25 = starker Trend, unter 20 = schwacher Trend. +DI/-DI zeigen Trendrichtung.
                </div>
              </div>
            </div>
            <div class="text-right">
              <span :class="getADXColor(data.adx)" class="text-lg font-bold">
                {{ formatNumber(data.adx) }}
              </span>
              <div class="text-xs text-muted-foreground">
                {{ data.adx > 25 ? 'Starker Trend' : data.adx > 20 ? 'Moderater Trend' : 'Schwacher Trend' }}
              </div>
            </div>
          </div>
          <div class="relative h-2 mb-1">
            <div class="absolute w-full h-full bg-muted rounded-full"></div>
            <div
              class="absolute h-full rounded-full transition-all duration-300"
              :class="getADXBarColor(data.adx)"
              :style="{ width: `${Math.min(100, data.adx)}%` }"
            ></div>
            <div class="absolute h-full w-px bg-muted-foreground/30" style="left: 25%"></div>
            <div class="absolute h-full w-px bg-muted-foreground/30" style="left: 50%"></div>
          </div>
          <div class="flex justify-between text-sm text-muted-foreground mt-1">
            <span>+DI: {{ formatNumber(data.plus_di) }} ({{ data.plus_di > data.minus_di ? '↑' : '↓' }})</span>
            <span>-DI: {{ formatNumber(data.minus_di) }} ({{ data.minus_di > data.plus_di ? '↑' : '↓' }})</span>
          </div>
        </div>

        <!-- Bollinger Bands -->
        <div v-if="data?.bb_upper != null" class="border-b pb-4">
          <div class="flex justify-between items-center mb-3">
            <div class="flex items-center gap-2">
              <span class="font-medium">Bollinger Bands</span>
              <div class="group relative">
                <Info class="h-4 w-4 text-muted-foreground cursor-help" />
                <div class="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 px-3 py-2 bg-popover text-popover-foreground text-xs rounded-md shadow-lg opacity-0 group-hover:opacity-100 transition-opacity duration-200 w-64 z-10">
                  Volatilitäts-Indikator mit 3 Linien: SMA20 ± 2 Standardabweichungen. Preis nahe oberer Band = überkauft, nahe unterer Band = überverkauft.
                </div>
              </div>
            </div>
            <div class="text-right">
              <span class="text-lg font-bold">{{ formatNumber(data.bb_percent * 100) }}%</span>
              <div class="text-xs text-muted-foreground">
                Position in Band
              </div>
            </div>
          </div>
          <div class="space-y-2">
            <div class="flex justify-between items-center">
              <span class="text-sm text-muted-foreground">Upper Band</span>
              <div class="text-right">
                <span class="font-medium text-lg">{{ currencySymbol }}{{ formatNumber(data.bb_upper) }}</span>
                <div class="text-xs text-muted-foreground">
                  +{{ formatNumber(((data.bb_upper - currentPrice) / currentPrice) * 100) }}%
                </div>
              </div>
            </div>
            <div class="flex justify-between items-center">
              <span class="text-sm text-muted-foreground">Middle (SMA20)</span>
              <div class="text-right">
                <span class="font-medium text-lg">{{ currencySymbol }}{{ formatNumber(data.bb_middle) }}</span>
                <div class="text-xs text-muted-foreground">
                  {{ currentPrice > data.bb_middle ? '+' : '' }}{{ formatNumber(((currentPrice - data.bb_middle) / data.bb_middle) * 100) }}%
                </div>
              </div>
            </div>
            <div class="flex justify-between items-center">
              <span class="text-sm text-muted-foreground">Lower Band</span>
              <div class="text-right">
                <span class="font-medium text-lg">{{ currencySymbol }}{{ formatNumber(data.bb_lower) }}</span>
                <div class="text-xs text-muted-foreground">
                  {{ formatNumber(((currentPrice - data.bb_lower) / currentPrice) * 100) }}%
                </div>
              </div>
            </div>
            <div class="text-sm text-muted-foreground">
              Band Width: {{ formatNumber(data.bb_width * 100) }}% ({{ formatNumber((data.bb_upper - data.bb_lower) / currentPrice * 100) }}% vom Preis)
            </div>
          </div>
        </div>

        <!-- ATR -->
        <div v-if="data?.atr != null" class="pt-2">
          <div class="flex justify-between items-center mb-1">
            <div class="flex items-center gap-2">
              <span class="font-medium">ATR</span>
              <div class="group relative">
                <Info class="h-4 w-4 text-muted-foreground cursor-help" />
                <div class="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 px-3 py-2 bg-popover text-popover-foreground text-xs rounded-md shadow-lg opacity-0 group-hover:opacity-100 transition-opacity duration-200 w-64 z-10">
                  Average True Range misst Volatilität. Höhere Werte = mehr Volatilität. Wichtig für Stop-Loss und Position Sizing.
                </div>
              </div>
            </div>
            <div class="text-right">
              <span class="font-medium text-lg">{{ currencySymbol }}{{ formatNumber(data.atr) }}</span>
              <div class="text-xs text-muted-foreground">
                {{ formatNumber((data.atr / currentPrice) * 100) }}% Volatilität
              </div>
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
import { useI18n } from 'vue-i18n'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card'
import { AlertCircle, Info } from 'lucide-vue-next'
import { useMarketStore } from '@/stores/market'

const { t } = useI18n()
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
  },
  currentPrice: {
    type: Number,
    default: 0
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

// Stochastic functions
const getStochColor = (value) => {
  if (value > 80) return 'text-destructive font-medium'
  if (value < 20) return 'text-green-500 font-medium'
  return 'text-blue-500 font-medium'
}

const getStochBarColor = (value) => {
  if (value > 80) return 'bg-destructive/90'
  if (value < 20) return 'bg-green-500/90'
  return 'bg-blue-500/90'
}

const getStochSignal = (k, d) => {
  if (k < 20 && d < 20 && k > d) return 'Oversold - Bullish Crossover'
  if (k > 80 && d > 80 && k < d) return 'Overbought - Bearish Crossover'
  if (k > 80) return 'Overbought - Consider Selling'
  if (k < 20) return 'Oversold - Consider Buying'
  return 'Neutral'
}

// Williams %R functions
const getWilliamsColor = (value) => {
  if (value > -20) return 'text-destructive font-medium'
  if (value < -80) return 'text-green-500 font-medium'
  return 'text-blue-500 font-medium'
}

const getWilliamsBarColor = (value) => {
  if (value > -20) return 'bg-destructive/90'
  if (value < -80) return 'bg-green-500/90'
  return 'bg-blue-500/90'
}

const getWilliamsSignal = (value) => {
  if (value > -20) return 'Overbought - Consider Selling'
  if (value < -80) return 'Oversold - Consider Buying'
  return 'Neutral'
}

// CCI functions
const getCCIColor = (value) => {
  if (value > 100) return 'text-destructive font-medium'
  if (value < -100) return 'text-green-500 font-medium'
  return 'text-blue-500 font-medium'
}

const getCCIBarColor = (value) => {
  if (value > 100) return 'bg-destructive/90'
  if (value < -100) return 'bg-green-500/90'
  return 'bg-blue-500/90'
}

const getCCISignal = (value) => {
  if (value > 100) return 'Overbought - Consider Selling'
  if (value < -100) return 'Oversold - Consider Buying'
  return 'Neutral'
}

// ADX functions
const getADXColor = (value) => {
  if (value > 50) return 'text-green-500 font-medium'
  if (value > 25) return 'text-blue-500 font-medium'
  if (value > 15) return 'text-yellow-500 font-medium'
  return 'text-muted-foreground font-medium'
}

const getADXBarColor = (value) => {
  if (value > 50) return 'bg-green-500/90'
  if (value > 25) return 'bg-blue-500/90'
  if (value > 15) return 'bg-yellow-500/90'
  return 'bg-muted/90'
}
</script>