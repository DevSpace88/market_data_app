<template>
  <Card>
    <CardHeader>
      <CardTitle>Trading Signals</CardTitle>
    </CardHeader>
    <CardContent>
      <div class="space-y-4">
        <!-- Gruppiert nach Zeitrahmen -->
        <div v-for="timeframe in ['short', 'medium', 'long']" :key="timeframe">
          <h4 class="font-medium mb-2">{{ formatTimeframe(timeframe) }}</h4>
          <div class="space-y-2">
            <div v-for="signal in filterSignalsByTimeframe(signals, timeframe)"
                 :key="signal.indicator"
                 class="p-3 rounded-lg border hover:bg-muted/50 transition-colors">
              <div class="flex justify-between items-start">
                <div class="flex-1">
                  <div class="flex items-center gap-2 mb-2">
                    <Badge :variant="getSignalTypeVariant(signal.type)">
                      {{ signal.type }}
                    </Badge>
                    <Badge :variant="getStrengthVariant(signal.strength)" class="text-xs">
                      {{ signal.strength }}
                    </Badge>
                    <span class="font-medium text-sm">{{ signal.indicator }}</span>
                  </div>
                  <p class="text-sm text-muted-foreground">
                    {{ signal.reason }}
                  </p>
                  <div class="flex items-center gap-2 mt-2">
                    <span class="text-xs text-muted-foreground">{{ formatTimeframe(timeframe) }}</span>
                    <div class="w-2 h-2 rounded-full" :class="getSignalColor(signal.type)"></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div v-if="!signals.length" class="text-muted-foreground text-center py-4">
          No active signals
        </div>
      </div>
    </CardContent>
  </Card>
</template>

<script setup>
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'

const props = defineProps({
  signals: {
    type: Array,
    default: () => []
  }
})

const formatTimeframe = (timeframe) => {
  const formats = {
    short: 'Short-term Signals (Minutes to Hours)',
    medium: 'Medium-term Signals (Days to Weeks)',
    long: 'Long-term Signals (Weeks to Months)'
  }
  return formats[timeframe]
}

const filterSignalsByTimeframe = (signals, timeframe) => {
  return signals.filter(signal => signal.timeframe === timeframe)
}

const getSignalTypeVariant = (type) => {
  switch (type) {
    case 'BUY':
      return 'default'
    case 'SELL':
      return 'destructive'
    case 'HOLD':
      return 'secondary'
    default:
      return 'outline'
  }
}

const getStrengthVariant = (strength) => {
  switch (strength) {
    case 'VERY_STRONG':
      return 'default'
    case 'STRONG':
      return 'secondary'
    case 'MEDIUM':
      return 'outline'
    case 'WEAK':
      return 'outline'
    default:
      return 'outline'
  }
}

const getSignalColor = (type) => {
  switch (type) {
    case 'BUY':
      return 'bg-green-500'
    case 'SELL':
      return 'bg-red-500'
    case 'HOLD':
      return 'bg-yellow-500'
    default:
      return 'bg-gray-500'
  }
}
</script>