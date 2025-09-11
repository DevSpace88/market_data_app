<template>
  <Card>
    <CardHeader>
      <CardTitle>Risk Metrics</CardTitle>
    </CardHeader>
    <CardContent>
      <div class="space-y-6">
        <!-- Overall Risk Score -->
        <div v-if="data?.overall_risk_score != null" class="border-b pb-4">
          <div class="flex justify-between items-center mb-2">
            <span class="font-medium">Overall Risk Score</span>
            <div class="flex items-center gap-2">
              <span :class="getRiskScoreColor(data.overall_risk_score)" class="text-2xl font-bold">
                {{ data.overall_risk_score }}
              </span>
              <Badge :variant="getRiskLevelVariant(data.risk_level)">
                {{ data.risk_level }}
              </Badge>
            </div>
          </div>
          <div class="relative h-3 bg-muted rounded-full">
            <div
              class="absolute h-full rounded-full transition-all duration-500"
              :class="getRiskScoreBarColor(data.overall_risk_score)"
              :style="{ width: `${data.overall_risk_score}%` }"
            ></div>
          </div>
        </div>

        <!-- Volatility Metrics -->
        <div v-if="hasVolatilityData" class="border-b pb-4">
          <h4 class="font-medium mb-3">Volatility</h4>
          <div class="grid grid-cols-2 gap-4">
            <div v-if="data?.historical_volatility_20d != null">
              <span class="text-sm text-muted-foreground">Historical Volatility (20d)</span>
              <p class="font-medium">{{ formatNumber(data.historical_volatility_20d) }}%</p>
            </div>
            <div v-if="data?.atr_percentage != null">
              <span class="text-sm text-muted-foreground">ATR Percentage</span>
              <p class="font-medium">{{ formatNumber(data.atr_percentage) }}%</p>
            </div>
            <div v-if="data?.bb_width_percentage != null">
              <span class="text-sm text-muted-foreground">BB Width</span>
              <p class="font-medium">{{ formatNumber(data.bb_width_percentage) }}%</p>
            </div>
          </div>
        </div>

        <!-- Drawdown Metrics -->
        <div v-if="hasDrawdownData" class="border-b pb-4">
          <h4 class="font-medium mb-3">Drawdown</h4>
          <div class="grid grid-cols-2 gap-4">
            <div v-if="data?.max_drawdown != null">
              <span class="text-sm text-muted-foreground">Max Drawdown</span>
              <p :class="getDrawdownColor(data.max_drawdown)" class="font-medium">
                {{ formatNumber(data.max_drawdown) }}%
              </p>
            </div>
            <div v-if="data?.current_drawdown != null">
              <span class="text-sm text-muted-foreground">Current Drawdown</span>
              <p :class="getDrawdownColor(data.current_drawdown)" class="font-medium">
                {{ formatNumber(data.current_drawdown) }}%
              </p>
            </div>
          </div>
        </div>

        <!-- Momentum Risk -->
        <div v-if="data?.rsi_risk || data?.trend_strength" class="border-b pb-4">
          <h4 class="font-medium mb-3">Momentum Risk</h4>
          <div class="space-y-2">
            <div v-if="data?.rsi_risk" class="flex justify-between items-center">
              <span class="text-sm text-muted-foreground">RSI Risk</span>
              <Badge :variant="getRSIRiskVariant(data.rsi_risk)">
                {{ data.rsi_risk }}
              </Badge>
            </div>
            <div v-if="data?.trend_strength" class="flex justify-between items-center">
              <span class="text-sm text-muted-foreground">Trend Strength</span>
              <Badge :variant="getTrendStrengthVariant(data.trend_strength)">
                {{ data.trend_strength }}
              </Badge>
            </div>
          </div>
        </div>

        <!-- Liquidity Metrics -->
        <div v-if="hasLiquidityData" class="border-b pb-4">
          <h4 class="font-medium mb-3">Liquidity</h4>
          <div class="grid grid-cols-2 gap-4">
            <div v-if="data?.avg_volume_20d != null">
              <span class="text-sm text-muted-foreground">Avg Volume (20d)</span>
              <p class="font-medium">{{ formatLargeNumber(data.avg_volume_20d) }}</p>
            </div>
            <div v-if="data?.volume_ratio != null">
              <span class="text-sm text-muted-foreground">Volume Ratio</span>
              <p :class="getVolumeRatioColor(data.volume_ratio)" class="font-medium">
                {{ formatNumber(data.volume_ratio) }}x
              </p>
            </div>
            <div v-if="data?.volume_volatility != null">
              <span class="text-sm text-muted-foreground">Volume Volatility</span>
              <p class="font-medium">{{ formatNumber(data.volume_volatility) }}</p>
            </div>
          </div>
        </div>

        <!-- Price Action Risk -->
        <div v-if="hasPriceActionData" class="border-b pb-4">
          <h4 class="font-medium mb-3">Price Action</h4>
          <div class="grid grid-cols-2 gap-4">
            <div v-if="data?.price_range_percentage != null">
              <span class="text-sm text-muted-foreground">Price Range (20d)</span>
              <p class="font-medium">{{ formatNumber(data.price_range_percentage) }}%</p>
            </div>
            <div v-if="data?.price_position_in_range != null">
              <span class="text-sm text-muted-foreground">Position in Range</span>
              <p class="font-medium">{{ formatNumber(data.price_position_in_range * 100) }}%</p>
            </div>
          </div>
        </div>

        <!-- Support/Resistance Risk -->
        <div v-if="hasSupportResistanceData" class="pb-4">
          <h4 class="font-medium mb-3">Support/Resistance</h4>
          <div class="grid grid-cols-2 gap-4">
            <div v-if="data?.distance_to_support != null">
              <span class="text-sm text-muted-foreground">Distance to Support</span>
              <p :class="getDistanceColor(data.distance_to_support)" class="font-medium">
                {{ formatNumber(data.distance_to_support) }}%
              </p>
            </div>
            <div v-if="data?.distance_to_resistance != null">
              <span class="text-sm text-muted-foreground">Distance to Resistance</span>
              <p :class="getDistanceColor(data.distance_to_resistance)" class="font-medium">
                {{ formatNumber(data.distance_to_resistance) }}%
              </p>
            </div>
          </div>
        </div>

        <div v-if="!hasAnyRiskData" class="text-muted-foreground text-center py-8">
          <AlertCircle class="h-6 w-6 mx-auto mb-2 opacity-50" />
          <p>No risk metrics available</p>
        </div>
      </div>
    </CardContent>
  </Card>
</template>

<script setup>
import { computed } from 'vue'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { AlertCircle } from 'lucide-vue-next'

const props = defineProps({
  data: {
    type: Object,
    default: () => ({})
  }
})

const hasAnyRiskData = computed(() => {
  return props.data && Object.keys(props.data).length > 0
})

const hasVolatilityData = computed(() => {
  return props.data?.historical_volatility_20d != null || 
         props.data?.atr_percentage != null || 
         props.data?.bb_width_percentage != null
})

const hasDrawdownData = computed(() => {
  return props.data?.max_drawdown != null || props.data?.current_drawdown != null
})

const hasLiquidityData = computed(() => {
  return props.data?.avg_volume_20d != null || 
         props.data?.volume_ratio != null || 
         props.data?.volume_volatility != null
})

const hasPriceActionData = computed(() => {
  return props.data?.price_range_percentage != null || 
         props.data?.price_position_in_range != null
})

const hasSupportResistanceData = computed(() => {
  return props.data?.distance_to_support != null || 
         props.data?.distance_to_resistance != null
})

const formatNumber = (value) => {
  return value?.toFixed(2) || '0.00'
}

const formatLargeNumber = (value) => {
  if (value >= 1e9) return (value / 1e9).toFixed(1) + 'B'
  if (value >= 1e6) return (value / 1e6).toFixed(1) + 'M'
  if (value >= 1e3) return (value / 1e3).toFixed(1) + 'K'
  return value?.toFixed(0) || '0'
}

const getRiskScoreColor = (score) => {
  if (score >= 80) return 'text-red-500'
  if (score >= 60) return 'text-orange-500'
  if (score >= 40) return 'text-yellow-500'
  if (score >= 20) return 'text-blue-500'
  return 'text-green-500'
}

const getRiskScoreBarColor = (score) => {
  if (score >= 80) return 'bg-red-500'
  if (score >= 60) return 'bg-orange-500'
  if (score >= 40) return 'bg-yellow-500'
  if (score >= 20) return 'bg-blue-500'
  return 'bg-green-500'
}

const getRiskLevelVariant = (level) => {
  switch (level) {
    case 'VERY_HIGH':
      return 'destructive'
    case 'HIGH':
      return 'destructive'
    case 'MEDIUM':
      return 'secondary'
    case 'LOW':
      return 'outline'
    case 'VERY_LOW':
      return 'outline'
    default:
      return 'outline'
  }
}

const getDrawdownColor = (value) => {
  const absValue = Math.abs(value)
  if (absValue >= 20) return 'text-red-500'
  if (absValue >= 15) return 'text-orange-500'
  if (absValue >= 10) return 'text-yellow-500'
  if (absValue >= 5) return 'text-blue-500'
  return 'text-green-500'
}

const getRSIRiskVariant = (risk) => {
  switch (risk) {
    case 'EXTREME_OVERBOUGHT':
    case 'EXTREME_OVERSOLD':
      return 'destructive'
    case 'OVERBOUGHT':
    case 'OVERSOLD':
      return 'secondary'
    case 'NEUTRAL':
      return 'outline'
    default:
      return 'outline'
  }
}

const getTrendStrengthVariant = (strength) => {
  switch (strength) {
    case 'VERY_STRONG':
      return 'default'
    case 'STRONG':
      return 'secondary'
    case 'MODERATE':
      return 'outline'
    case 'WEAK':
      return 'destructive'
    default:
      return 'outline'
  }
}

const getVolumeRatioColor = (ratio) => {
  if (ratio >= 2) return 'text-green-500'
  if (ratio >= 1.5) return 'text-blue-500'
  if (ratio >= 0.8) return 'text-yellow-500'
  return 'text-red-500'
}

const getDistanceColor = (distance) => {
  const absDistance = Math.abs(distance)
  if (absDistance <= 2) return 'text-red-500'
  if (absDistance <= 5) return 'text-orange-500'
  if (absDistance <= 10) return 'text-yellow-500'
  return 'text-green-500'
}
</script>
