<template>
  <Card>
    <CardHeader>
      <div class="flex items-center gap-2">
        <CardTitle>{{ t('symbolAnalysis.technicalPatterns') }}</CardTitle>
        <div class="group relative">
          <Info class="h-4 w-4 text-muted-foreground cursor-help" />
          <div class="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 px-3 py-2 bg-popover text-popover-foreground text-xs rounded-md shadow-lg opacity-0 group-hover:opacity-100 transition-opacity duration-200 w-64 z-10">
            {{ t('patterns.info') }}
          </div>
        </div>
      </div>
    </CardHeader>
    <CardContent>
      <div class="space-y-4">

        <!-- Gruppiert nach Kategorien -->
        <div v-for="category in ['Candlestick', 'Chart', 'Trend', 'Volume', 'Support/Resistance']" :key="category">
          <h4 class="font-medium mb-2">{{ category }} Patterns</h4>
          <div class="space-y-2">
            <div v-for="pattern in filterPatternsByCategory(patterns, category)"
                 :key="pattern.type"
                 class="p-3 rounded-lg border hover:bg-muted/50 transition-colors">
              <div class="flex justify-between items-start">
                <div class="flex-1">
                  <div class="flex items-center gap-2 mb-2">
                    <Badge :variant="getPatternCategoryVariant(category)">
                      {{ category }}
                    </Badge>
                    <Badge :variant="getConfidenceVariant(pattern.confidence)" class="text-xs">
                      {{ pattern.confidence }}%
                    </Badge>
                    <span class="font-medium text-sm">{{ formatPatternType(pattern.type) }}</span>
                  </div>
                  <p class="text-sm text-muted-foreground">
                    {{ pattern.description }}
                  </p>
                  <div class="flex items-center gap-2 mt-2">
                    <span class="text-xs text-muted-foreground">{{ formatTimestamp(pattern.timestamp) }}</span>
                    <div class="w-2 h-2 rounded-full" :class="getPatternColor(pattern.type)"></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div v-if="!patterns.length" class="text-muted-foreground text-center py-4">
          <div class="mb-2">No patterns detected</div>
          <div class="text-xs text-muted-foreground">
            Patterns werden basierend auf technischen Indikatoren und Chart-Mustern erkannt.
          </div>
        </div>
      </div>
    </CardContent>
  </Card>
</template>

<script setup>
import { useI18n } from 'vue-i18n'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Info } from 'lucide-vue-next'

const { t } = useI18n()

const props = defineProps({
  patterns: {
    type: Array,
    default: () => []
  }
})

const formatPatternType = (type) => {
  // Konvertiert z.B. "RESISTANCE_TEST" zu "Resistance Test"
  return type
    .split('_')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
    .join(' ')
}

const formatTimestamp = (timestamp) => {
  if (!timestamp) return 'Unknown'
  const date = new Date(timestamp)
  return date.toLocaleDateString('de-DE', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const filterPatternsByCategory = (patterns, category) => {
  const categoryMap = {
    'Candlestick': ['Doji', 'Hammer', 'Shooting Star', 'Bullish Engulfing', 'Bearish Engulfing'],
    'Chart': ['Head and Shoulders', 'Double Top', 'Double Bottom', 'Ascending Triangle', 'Descending Triangle'],
    'Trend': ['Higher Highs/Lows', 'Lower Highs/Lows', 'Breakout'],
    'Volume': ['Volume Spike', 'Volume Divergence'],
    'Support/Resistance': ['Resistance Test', 'Support Test']
  }
  
  const categoryTypes = categoryMap[category] || []
  return patterns.filter(pattern => categoryTypes.includes(pattern.type))
}


const getPatternCategoryVariant = (category) => {
  switch (category) {
    case 'Candlestick':
      return 'default'
    case 'Chart':
      return 'secondary'
    case 'Trend':
      return 'outline'
    case 'Volume':
      return 'destructive'
    case 'Support/Resistance':
      return 'secondary'
    default:
      return 'outline'
  }
}

const getConfidenceVariant = (confidence) => {
  if (confidence >= 80) return 'default'
  if (confidence >= 60) return 'secondary'
  return 'outline'
}

const getPatternColor = (type) => {
  // Bullish patterns
  if (['Hammer', 'Bullish Engulfing', 'Ascending Triangle', 'Higher Highs/Lows', 'Breakout', 'Support Test'].includes(type)) {
    return 'bg-green-500'
  }
  // Bearish patterns
  if (['Shooting Star', 'Bearish Engulfing', 'Descending Triangle', 'Lower Highs/Lows', 'Resistance Test'].includes(type)) {
    return 'bg-red-500'
  }
  // Neutral patterns
  if (['Doji', 'Head and Shoulders', 'Double Top', 'Double Bottom', 'Volume Spike', 'Volume Divergence'].includes(type)) {
    return 'bg-yellow-500'
  }
  return 'bg-gray-500'
}
</script>