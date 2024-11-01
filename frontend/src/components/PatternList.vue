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
            <div>
              <div class="flex items-center gap-2">
                <h4 class="font-medium">{{ pattern.type }}</h4>
                <Badge :variant="getConfidenceVariant(pattern.confidence)">
                  {{ pattern.confidence }}%
                </Badge>
              </div>
              <p class="text-sm text-muted-foreground mt-1">
                {{ pattern.description }}
              </p>
            </div>
            <div class="text-sm text-muted-foreground">
              {{ formatTimestamp(pattern.timestamp) }}
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

</script>
