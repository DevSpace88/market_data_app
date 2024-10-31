<!--<template>-->
<!--  <Card>-->
<!--    <CardHeader>-->
<!--      <CardTitle>Trading Signals</CardTitle>-->
<!--    </CardHeader>-->
<!--    <CardContent>-->
<!--      <div class="space-y-4">-->
<!--        <div v-for="signal in signals" :key="signal.indicator"-->
<!--             class="p-3 rounded-lg border">-->
<!--          <div class="flex justify-between items-start">-->
<!--            <div>-->
<!--              <div class="flex items-center gap-2">-->
<!--                <Badge :variant="signal.type === 'BUY' ? 'default' : 'destructive'">-->
<!--                  {{ signal.type }}-->
<!--                </Badge>-->
<!--                <span class="font-medium">{{ signal.indicator }}</span>-->
<!--              </div>-->
<!--              <p class="text-sm text-muted-foreground mt-1">-->
<!--                {{ signal.reason }}-->
<!--              </p>-->
<!--            </div>-->
<!--            <Badge variant="outline">{{ signal.strength }}</Badge>-->
<!--          </div>-->
<!--        </div>-->
<!--        <div v-if="!signals.length" class="text-muted-foreground text-center py-4">-->
<!--          No active signals-->
<!--        </div>-->
<!--      </div>-->
<!--    </CardContent>-->
<!--  </Card>-->
<!--</template>-->

<!--<script setup>-->
<!--import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card'-->
<!--import { Badge } from '@/components/ui/badge'-->

<!--defineProps({-->
<!--  signals: {-->
<!--    type: Array,-->
<!--    default: () => []-->
<!--  }-->
<!--})-->
<!--</script>-->


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
                 class="p-3 rounded-lg border">
              <div class="flex justify-between items-start">
                <div>
                  <div class="flex items-center gap-2">
                    <Badge :variant="signal.type === 'BUY' ? 'default' : 'destructive'">
                      {{ signal.type }}
                    </Badge>
                    <span class="font-medium">{{ signal.indicator }}</span>
                  </div>
                  <p class="text-sm text-muted-foreground mt-1">
                    {{ signal.reason }}
                  </p>
                </div>
                <Badge variant="outline">{{ signal.strength }}</Badge>
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
</script>