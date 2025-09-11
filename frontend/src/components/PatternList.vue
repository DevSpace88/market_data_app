<!--&lt;!&ndash;<template>&ndash;&gt;-->
<!--&lt;!&ndash;  <Card>&ndash;&gt;-->
<!--&lt;!&ndash;    <CardHeader>&ndash;&gt;-->
<!--&lt;!&ndash;      <CardTitle>Technical Patterns</CardTitle>&ndash;&gt;-->
<!--&lt;!&ndash;    </CardHeader>&ndash;&gt;-->
<!--&lt;!&ndash;    <CardContent>&ndash;&gt;-->
<!--&lt;!&ndash;      <div class="space-y-4">&ndash;&gt;-->
<!--&lt;!&ndash;        <div v-for="pattern in patterns" :key="pattern.type"&ndash;&gt;-->
<!--&lt;!&ndash;             class="p-3 rounded-lg border">&ndash;&gt;-->
<!--&lt;!&ndash;          <div class="flex justify-between items-start">&ndash;&gt;-->
<!--&lt;!&ndash;            <div>&ndash;&gt;-->
<!--&lt;!&ndash;              <h4 class="font-medium">{{ formatPatternType(pattern.type) }}</h4>&ndash;&gt;-->
<!--&lt;!&ndash;              <p class="text-sm text-muted-foreground">&ndash;&gt;-->
<!--&lt;!&ndash;                {{ formatPatternDescription(pattern.description) }}&ndash;&gt;-->
<!--&lt;!&ndash;              </p>&ndash;&gt;-->
<!--&lt;!&ndash;            </div>&ndash;&gt;-->
<!--&lt;!&ndash;            <Badge :variant="getConfidenceVariant(pattern.confidence)">&ndash;&gt;-->
<!--&lt;!&ndash;              {{ pattern.confidence }}%&ndash;&gt;-->
<!--&lt;!&ndash;            </Badge>&ndash;&gt;-->
<!--&lt;!&ndash;          </div>&ndash;&gt;-->
<!--&lt;!&ndash;        </div>&ndash;&gt;-->
<!--&lt;!&ndash;        <div v-if="!patterns.length" class="text-muted-foreground text-center py-4">&ndash;&gt;-->
<!--&lt;!&ndash;          No patterns detected&ndash;&gt;-->
<!--&lt;!&ndash;        </div>&ndash;&gt;-->
<!--&lt;!&ndash;      </div>&ndash;&gt;-->
<!--&lt;!&ndash;    </CardContent>&ndash;&gt;-->
<!--&lt;!&ndash;  </Card>&ndash;&gt;-->
<!--&lt;!&ndash;</template>&ndash;&gt;-->

<!--&lt;!&ndash;<script setup>&ndash;&gt;-->
<!--&lt;!&ndash;import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card'&ndash;&gt;-->
<!--&lt;!&ndash;import { Badge } from '@/components/ui/badge'&ndash;&gt;-->

<!--&lt;!&ndash;defineProps({&ndash;&gt;-->
<!--&lt;!&ndash;  patterns: {&ndash;&gt;-->
<!--&lt;!&ndash;    type: Array,&ndash;&gt;-->
<!--&lt;!&ndash;    default: () => []&ndash;&gt;-->
<!--&lt;!&ndash;  }&ndash;&gt;-->
<!--&lt;!&ndash;})&ndash;&gt;-->

<!--&lt;!&ndash;const formatPatternType = (type) => {&ndash;&gt;-->
<!--&lt;!&ndash;  // Konvertiert z.B. "RESISTANCE_TEST" zu "Resistance Test"&ndash;&gt;-->
<!--&lt;!&ndash;  return type&ndash;&gt;-->
<!--&lt;!&ndash;    .split('_')&ndash;&gt;-->
<!--&lt;!&ndash;    .map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())&ndash;&gt;-->
<!--&lt;!&ndash;    .join(' ')&ndash;&gt;-->
<!--&lt;!&ndash;}&ndash;&gt;-->

<!--&lt;!&ndash;const formatPatternDescription = (description) => {&ndash;&gt;-->
<!--&lt;!&ndash;  // Entfernt die Confidence aus der Beschreibung, da wir sie separat anzeigen&ndash;&gt;-->
<!--&lt;!&ndash;  return description.split('with')[0].trim()&ndash;&gt;-->
<!--&lt;!&ndash;}&ndash;&gt;-->

<!--&lt;!&ndash;const getConfidenceVariant = (confidence) => {&ndash;&gt;-->
<!--&lt;!&ndash;  if (confidence >= 80) return 'default'&ndash;&gt;-->
<!--&lt;!&ndash;  if (confidence >= 60) return 'secondary'&ndash;&gt;-->
<!--&lt;!&ndash;  return 'outline'&ndash;&gt;-->
<!--&lt;!&ndash;}&ndash;&gt;-->
<!--&lt;!&ndash;</script>&ndash;&gt;-->


<!--<template>-->
<!--  <Card>-->
<!--    <CardHeader>-->
<!--      <CardTitle>Technical Patterns</CardTitle>-->
<!--    </CardHeader>-->
<!--    <CardContent>-->
<!--      <div class="space-y-4">-->
<!--        <div v-for="pattern in sortedPatterns" :key="pattern.type"-->
<!--             class="p-4 rounded-lg border hover:bg-muted/50 transition-colors">-->
<!--          <div class="flex justify-between items-start">-->
<!--            <div>-->
<!--              <div class="flex items-center gap-2">-->
<!--                <h4 class="font-medium">{{ pattern.type }}</h4>-->
<!--                <Badge :variant="getConfidenceVariant(pattern.confidence)">-->
<!--                  {{ pattern.confidence }}%-->
<!--                </Badge>-->
<!--              </div>-->
<!--              <p class="text-sm text-muted-foreground mt-1">-->
<!--                {{ pattern.description }}-->
<!--              </p>-->
<!--            </div>-->
<!--            <div class="text-sm text-muted-foreground">-->
<!--              {{ formatTimestamp(pattern.timestamp) }}-->
<!--            </div>-->
<!--          </div>-->
<!--        </div>-->
<!--        <div v-if="!patterns.length" class="text-muted-foreground text-center py-8">-->
<!--          <AlertCircle class="h-6 w-6 mx-auto mb-2 opacity-50" />-->
<!--          <p>No patterns detected in current timeframe</p>-->
<!--        </div>-->
<!--      </div>-->
<!--    </CardContent>-->
<!--  </Card>-->
<!--</template>-->

<!--<script setup>-->
<!--import { computed } from 'vue'-->
<!--import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card'-->
<!--import { Badge } from '@/components/ui/badge'-->
<!--import { AlertCircle } from 'lucide-vue-next'-->

<!--const props = defineProps({-->
<!--  patterns: {-->
<!--    type: Array,-->
<!--    default: () => []-->
<!--  }-->
<!--})-->

<!--const sortedPatterns = computed(() => {-->
<!--  return [...props.patterns].sort((a, b) => b.confidence - a.confidence)-->
<!--})-->

<!--const getConfidenceVariant = (confidence) => {-->
<!--  if (confidence >= 80) return 'default'-->
<!--  if (confidence >= 65) return 'secondary'-->
<!--  if (confidence >= 50) return 'warning'-->
<!--  return 'destructive'-->
<!--}-->

<!--const formatTimestamp = (timestamp) => {-->
<!--  if (!timestamp) return ''-->
<!--  return new Date(timestamp).toLocaleTimeString()-->
<!--}-->
<!--</script>-->


<template>
  <Card>
    <CardHeader>
      <CardTitle>Technical Patterns</CardTitle>
    </CardHeader>
    <CardContent>
      <div class="space-y-4">
        <div v-for="pattern in uniquePatterns" :key="pattern.type"
             class="p-4 rounded-lg border hover:bg-muted/50 transition-colors">
          <div class="flex justify-between items-start">
            <div class="flex-1">
              <div class="flex items-center gap-2 mb-2">
                <h4 class="font-medium">{{ pattern.type }}</h4>
                <Badge :variant="getConfidenceVariant(pattern.confidence)">
                  {{ pattern.confidence }}%
                </Badge>
                <Badge :variant="getPatternCategoryVariant(pattern.type)" class="text-xs">
                  {{ getPatternCategory(pattern.type) }}
                </Badge>
              </div>
              <p class="text-sm text-muted-foreground mb-2">
                {{ pattern.description }}
              </p>
              <div class="flex items-center gap-2">
                <div class="w-2 h-2 rounded-full" :class="getPatternColor(pattern.type)"></div>
                <span class="text-xs text-muted-foreground">{{ formatTimestamp(pattern.timestamp) }}</span>
              </div>
            </div>
          </div>
        </div>
        <div v-if="!patterns.length" class="text-muted-foreground text-center py-8">
          <AlertCircle class="h-6 w-6 mx-auto mb-2 opacity-50" />
          <p>No patterns detected in current timeframe</p>
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
  patterns: {
    type: Array,
    default: () => []
  }
})

const uniquePatterns = computed(() => {
  const seenTypes = new Set()
  return [...props.patterns]
    .sort((a, b) => b.confidence - a.confidence)
    .filter(pattern => {
      if (seenTypes.has(pattern.type)) {
        return false
      }
      seenTypes.add(pattern.type)
      return true
    })
})

const getConfidenceVariant = (confidence) => {
  if (confidence >= 80) return 'default'
  if (confidence >= 65) return 'secondary'
  if (confidence >= 50) return 'warning'
  return 'destructive'
}

// const formatTimestamp = (timestamp) => {
//   if (!timestamp) return ''
//   return new Date(timestamp).toLocaleTimeString()
// }

const formatTimestamp = (timestamp) => {
  if (!timestamp) return ''
  return new Date(timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false, timeZoneName: 'short' })
}

const getPatternCategory = (type) => {
  const categories = {
    // Candlestick Patterns
    'Doji': 'Candlestick',
    'Hammer': 'Candlestick',
    'Shooting Star': 'Candlestick',
    'Bullish Engulfing': 'Candlestick',
    'Bearish Engulfing': 'Candlestick',
    
    // Chart Patterns
    'Head and Shoulders': 'Chart',
    'Double Top': 'Chart',
    'Double Bottom': 'Chart',
    'Ascending Triangle': 'Chart',
    'Descending Triangle': 'Chart',
    
    // Trend Patterns
    'Higher Highs/Lows': 'Trend',
    'Lower Highs/Lows': 'Trend',
    'Breakout': 'Trend',
    
    // Volume Patterns
    'Volume Spike': 'Volume',
    'Volume Divergence': 'Volume',
    
    // Support/Resistance Patterns
    'Resistance Test': 'S/R',
    'Support Test': 'S/R'
  }
  return categories[type] || 'Pattern'
}

const getPatternCategoryVariant = (type) => {
  const category = getPatternCategory(type)
  switch (category) {
    case 'Candlestick':
      return 'default'
    case 'Chart':
      return 'secondary'
    case 'Trend':
      return 'outline'
    case 'Volume':
      return 'destructive'
    case 'S/R':
      return 'secondary'
    default:
      return 'outline'
  }
}

const getPatternColor = (type) => {
  const category = getPatternCategory(type)
  switch (category) {
    case 'Candlestick':
      return 'bg-blue-500'
    case 'Chart':
      return 'bg-purple-500'
    case 'Trend':
      return 'bg-green-500'
    case 'Volume':
      return 'bg-orange-500'
    case 'S/R':
      return 'bg-yellow-500'
    default:
      return 'bg-gray-500'
  }
}

</script>
