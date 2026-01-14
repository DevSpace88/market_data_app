<template>
  <Card class="pt-0">
    <CardHeader class="flex items-center gap-2 space-y-0 border-b py-5">
      <div class="grid flex-1 gap-1">
        <CardTitle>{{ symbol || t('symbolAnalysis.title') }}</CardTitle>
        <CardDescription v-if="timeframe">
          {{ t('symbolAnalysis.timeframe') }}: {{ timeframe }}
        </CardDescription>
      </div>
      <div class="flex items-center gap-2">
        <Button
          variant="outline"
          size="sm"
          :class="{ 'bg-primary/10': showMA20 }"
          @click="showMA20 = !showMA20"
        >
          MA 20
        </Button>
        <Button
          variant="outline"
          size="sm"
          :class="{ 'bg-primary/10': showMA50 }"
          @click="showMA50 = !showMA50"
        >
          MA 50
        </Button>
        <Button
          variant="outline"
          size="sm"
          :class="{ 'bg-primary/10': showBB }"
          @click="showBB = !showBB"
        >
          BB
        </Button>
      </div>
    </CardHeader>
    <CardContent class="px-2 pt-4 sm:px-6 sm:pt-6 pb-4">
      <ChartContainer :config="chartConfig" class="aspect-auto h-[400px] w-full">
        <VisXYContainer
          :data="chartData"
          :svg-defs="svgDefs"
          :margin="{ left: -10, right: 10, top: 10, bottom: 20 }"
        >
          <!-- Area fill for price -->
          <VisArea
            :x="(d: DataPoint) => d.date"
            :y="(d: DataPoint) => d.close"
            color="url(#fillPrice)"
          />

          <!-- Main price line -->
          <VisLine
            :x="(d: DataPoint) => d.date"
            :y="(d: DataPoint) => d.close"
            :color="chartConfig.price.color"
            :line-width="2"
          />

          <!-- MA 20 Line -->
          <VisLine
            v-if="showMA20"
            :x="(d: DataPoint) => d.date"
            :y="(d: DataPoint) => d.ma20"
            :color="chartConfig.ma20.color"
            :line-width="1.5"
          />

          <!-- MA 50 Line -->
          <VisLine
            v-if="showMA50"
            :x="(d: DataPoint) => d.date"
            :y="(d: DataPoint) => d.ma50"
            :color="chartConfig.ma50.color"
            :line-width="1.5"
          />

          <!-- Bollinger Bands -->
          <VisLine
            v-if="showBB"
            :x="(d: DataPoint) => d.date"
            :y="(d: DataPoint) => d.bb_upper"
            :color="chartConfig.bb.color"
            :line-width="1"
            :line-style="2"
          />
          <VisLine
            v-if="showBB"
            :x="(d: DataPoint) => d.date"
            :y="(d: DataPoint) => d.bb_lower"
            :color="chartConfig.bb.color"
            :line-width="1"
            :line-style="2"
          />

          <!-- X Axis -->
          <VisAxis
            type="x"
            :x="(d: DataPoint) => d.date"
            :tick-line="false"
            :domain-line="false"
            :grid-line="false"
            :num-ticks="6"
            :tick-format="(d: number) => {
              const date = new Date(d)
              return date.toLocaleDateString('en-US', {
                month: 'short',
                day: 'numeric'
              })
            }"
          />

          <!-- Y Axis -->
          <VisAxis
            type="y"
            :num-ticks="4"
            :tick-line="false"
            :domain-line="false"
            :tick-format="(d: number) => formatCurrency(d)"
          />

          <!-- Tooltip -->
          <VisTooltip>
            <template #default="{ data }">
              <div
                class="grid min-w-[8rem] items-start gap-1.5 rounded-lg border bg-popover px-2.5 py-1.5 text-xs shadow-xl"
              >
                <div class="text-muted-foreground font-medium">
                  {{ new Date(data.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' }) }}
                </div>
                <div class="flex items-center justify-between gap-2">
                  <span class="text-muted-foreground">{{ t('common.close') }}</span>
                  <span class="font-mono font-medium tabular-nums">{{ formatCurrency(data.close) }}</span>
                </div>
                <div v-if="data.ma20" class="flex items-center justify-between gap-2">
                  <span class="text-muted-foreground">MA 20</span>
                  <span class="font-mono font-medium tabular-nums">{{ formatCurrency(data.ma20) }}</span>
                </div>
                <div v-if="data.ma50" class="flex items-center justify-between gap-2">
                  <span class="text-muted-foreground">MA 50</span>
                  <span class="font-mono font-medium tabular-nums">{{ formatCurrency(data.ma50) }}</span>
                </div>
                <div v-if="data.bb_upper" class="flex items-center justify-between gap-2">
                  <span class="text-muted-foreground">BB Upper</span>
                  <span class="font-mono font-medium tabular-nums">{{ formatCurrency(data.bb_upper) }}</span>
                </div>
                <div v-if="data.bb_lower" class="flex items-center justify-between gap-2">
                  <span class="text-muted-foreground">BB Lower</span>
                  <span class="font-mono font-medium tabular-nums">{{ formatCurrency(data.bb_lower) }}</span>
                </div>
              </div>
            </template>
          </VisTooltip>
        </VisXYContainer>

        <!-- Legend -->
        <div class="flex flex-wrap items-center justify-center gap-4 pt-4">
          <div class="flex items-center gap-2">
            <span class="h-2 w-2 rounded-full" :style="{ backgroundColor: chartConfig.price.color }" />
            <span class="text-muted-foreground text-sm">{{ t('common.close') }}</span>
          </div>
          <div v-if="showMA20" class="flex items-center gap-2">
            <span class="h-2 w-2 rounded-full" :style="{ backgroundColor: chartConfig.ma20.color }" />
            <span class="text-muted-foreground text-sm">MA 20</span>
          </div>
          <div v-if="showMA50" class="flex items-center gap-2">
            <span class="h-2 w-2 rounded-full" :style="{ backgroundColor: chartConfig.ma50.color }" />
            <span class="text-muted-foreground text-sm">MA 50</span>
          </div>
          <div v-if="showBB" class="flex items-center gap-2">
            <span class="h-2 w-2 rounded-full border border-dashed" :style="{ backgroundColor: chartConfig.bb.color }" />
            <span class="text-muted-foreground text-sm">{{ t('indicators.bollinger') }}</span>
          </div>
        </div>
      </ChartContainer>
    </CardContent>
  </Card>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { VisArea, VisAxis, VisLine, VisXYContainer, VisTooltip } from '@unovis/vue'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import {
  ChartContainer,
  type ChartConfig
} from '@/components/ui/chart'

interface DataPoint {
  date: Date
  close: number
  ma20?: number
  ma50?: number
  bb_upper?: number
  bb_lower?: number
}

const props = defineProps<{
  data: Array<{
    timestamp: string
    open: number
    high: number
    low: number
    close: number
    volume?: number
  }>
  technicalData?: {
    current?: {
      sma_20?: number
      sma_50?: number
      sma_200?: number
      bb_upper?: number
      bb_lower?: number
      bb_middle?: number
    }
    historical?: {
      sma_20?: Record<string, number>
      sma_50?: Record<string, number>
      bb_upper?: Record<string, number>
      bb_lower?: Record<string, number>
      bb_middle?: Record<string, number>
    }
  }
  symbol?: string
  timeframe?: string
  currency?: string
  currencySymbol?: string
}>()

const { t } = useI18n()
const currencySymbol = props.currencySymbol || '$'

const showMA20 = ref(true)
const showMA50 = ref(true)
const showBB = ref(false) // Default off for less clutter

const chartConfig: ChartConfig = {
  price: {
    label: 'Price',
    color: 'var(--chart-1)'
  },
  ma20: {
    label: 'MA 20',
    color: 'var(--chart-2)'
  },
  ma50: {
    label: 'MA 50',
    color: 'var(--chart-3)'
  },
  bb: {
    label: 'Bollinger Bands',
    color: 'var(--chart-4)'
  }
}

const svgDefs = `
  <linearGradient id="fillPrice" x1="0" y1="0" x2="0" y2="1">
    <stop offset="5%" stop-color="var(--chart-1)" stop-opacity="0.5" />
    <stop offset="95%" stop-color="var(--chart-1)" stop-opacity="0" />
  </linearGradient>
`

const chartData = computed((): DataPoint[] => {
  if (!props.data?.length) return []

  const historical = props.technicalData?.historical || {}

  // Debug: log historical data
  if (historical.sma_20 && Object.keys(historical.sma_20).length > 0) {
    console.log('[PriceChart] Historical SMA20 data:', Object.keys(historical.sma_20).slice(0, 3), '...', Object.values(historical.sma_20).slice(0, 3))
  }

  return props.data.map(item => {
    const ts = Math.floor(new Date(item.timestamp).getTime() / 1000)
    const tsStr = String(ts)
    const ma20 = historical.sma_20?.[ts] ?? historical.sma_20?.[tsStr]
    const ma50 = historical.sma_50?.[ts] ?? historical.sma_50?.[tsStr]
    const bb_upper = historical.bb_upper?.[ts] ?? historical.bb_upper?.[tsStr]
    const bb_lower = historical.bb_lower?.[ts] ?? historical.bb_lower?.[tsStr]

    // Debug: log first match
    if (item === props.data[0]) {
      console.log('[PriceChart] First data point:', { ts, tsStr, ma20, ma50, bb_upper, bb_lower })
    }

    return {
      date: new Date(item.timestamp),
      close: item.close,
      ma20,
      ma50,
      bb_upper,
      bb_lower
    }
  }).filter(d => d.close !== undefined)
})

function formatCurrency(value: number): string {
  if (value >= 1000) {
    return `${currencySymbol}${value.toLocaleString('en-US', {
      minimumFractionDigits: 2,
      maximumFractionDigits: 2
    })}`
  }
  return `${currencySymbol}${value.toFixed(2)}`
}
</script>
