<template>
  <Card>
    <CardHeader>
      <CardTitle>Technical Patterns</CardTitle>
    </CardHeader>
    <CardContent>
      <div class="space-y-4">
        <div v-for="pattern in patterns" :key="pattern.type"
             class="p-3 rounded-lg border">
          <div class="flex justify-between items-start">
            <div>
              <h4 class="font-medium">{{ formatPatternType(pattern.type) }}</h4>
              <p class="text-sm text-muted-foreground">
                {{ formatPatternDescription(pattern.description) }}
              </p>
            </div>
            <Badge :variant="getConfidenceVariant(pattern.confidence)">
              {{ pattern.confidence }}%
            </Badge>
          </div>
        </div>
        <div v-if="!patterns.length" class="text-muted-foreground text-center py-4">
          No patterns detected
        </div>
      </div>
    </CardContent>
  </Card>
</template>

<script setup>
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'

defineProps({
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

const formatPatternDescription = (description) => {
  // Entfernt die Confidence aus der Beschreibung, da wir sie separat anzeigen
  return description.split('with')[0].trim()
}

const getConfidenceVariant = (confidence) => {
  if (confidence >= 80) return 'default'
  if (confidence >= 60) return 'secondary'
  return 'outline'
}
</script>