<!--<template>-->
<!--  <Card>-->
<!--    <CardHeader>-->
<!--      <CardTitle>AI Market Insights</CardTitle>-->
<!--    </CardHeader>-->
<!--    <CardContent>-->
<!--      <div v-if="analysis" class="space-y-6">-->
<!--        &lt;!&ndash; Market Sentiment &ndash;&gt;-->
<!--        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">-->
<!--          <div-->
<!--            class="p-4 rounded-lg border"-->
<!--            :class="getSentimentColor(analysis.sentiment)"-->
<!--          >-->
<!--            <h4 class="font-medium mb-2">Market Sentiment</h4>-->
<!--            <p class="text-sm">{{ analysis.sentiment_summary || formatSentiment(analysis.sentiment) }}</p>-->
<!--          </div>-->

<!--          <div class="p-4 bg-card rounded-lg border">-->
<!--            <h4 class="font-medium mb-2">Technical Overview</h4>-->
<!--            <p class="text-sm">{{ analysis.technical_analysis }}</p>-->
<!--          </div>-->
<!--        </div>-->

<!--        &lt;!&ndash; Key Insights &ndash;&gt;-->
<!--        <div>-->
<!--          <h4 class="font-medium mb-2">Key Insights</h4>-->
<!--          <div class="space-y-2">-->
<!--            <Alert v-for="(insight, index) in analysis.key_insights" :key="index">-->
<!--              <AlertDescription>{{ insight }}</AlertDescription>-->
<!--            </Alert>-->
<!--          </div>-->
<!--        </div>-->

<!--        &lt;!&ndash; Support & Resistance &ndash;&gt;-->
<!--        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">-->
<!--          <div>-->
<!--            <h4 class="font-medium mb-2">Support Levels</h4>-->
<!--            <ul class="space-y-1">-->
<!--              <li v-for="(level, index) in analysis.support_resistance?.support_levels"-->
<!--                  :key="index"-->
<!--                  class="text-sm text-muted-foreground flex items-center gap-2">-->
<!--                <ArrowRight class="h-4 w-4" />-->
<!--                <span>${{ formatNumber(level) }}</span>-->
<!--              </li>-->
<!--            </ul>-->
<!--          </div>-->
<!--          <div>-->
<!--            <h4 class="font-medium mb-2">Resistance Levels</h4>-->
<!--            <ul class="space-y-1">-->
<!--              <li v-for="(level, index) in analysis.support_resistance?.resistance_levels"-->
<!--                  :key="index"-->
<!--                  class="text-sm text-muted-foreground flex items-center gap-2">-->
<!--                <ArrowRight class="h-4 w-4" />-->
<!--                <span>${{ formatNumber(level) }}</span>-->
<!--              </li>-->
<!--            </ul>-->
<!--          </div>-->
<!--        </div>-->

<!--        &lt;!&ndash; Risk Factors &ndash;&gt;-->
<!--        <div>-->
<!--          <h4 class="font-medium mb-2">Risk Factors</h4>-->
<!--          <div class="grid gap-2">-->
<!--            <Alert variant="destructive" v-for="(risk, index) in analysis.risk_factors" :key="index">-->
<!--              <AlertDescription>{{ risk }}</AlertDescription>-->
<!--            </Alert>-->
<!--          </div>-->
<!--        </div>-->

<!--        &lt;!&ndash; Outlook &ndash;&gt;-->
<!--        <div v-if="analysis.short_term_outlook" class="border rounded-lg p-4">-->
<!--          <h4 class="font-medium mb-2">Short-term Outlook</h4>-->
<!--          <p class="text-sm">{{ analysis.short_term_outlook }}</p>-->
<!--        </div>-->
<!--      </div>-->

<!--      <div v-else class="py-8 text-center text-muted-foreground">-->
<!--        <Loader2 class="h-6 w-6 animate-spin mx-auto mb-2" />-->
<!--        Analyzing market data...-->
<!--      </div>-->
<!--    </CardContent>-->
<!--  </Card>-->
<!--</template>-->

<!--<script setup>-->
<!--import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card'-->
<!--import { Alert, AlertDescription } from '@/components/ui/alert'-->
<!--import { ArrowRight, Loader2 } from 'lucide-vue-next'-->

<!--const props = defineProps({-->
<!--  analysis: {-->
<!--    type: Object,-->
<!--    default: null-->
<!--  }-->
<!--})-->

<!--const formatNumber = (value) => {-->
<!--  return value?.toFixed(2) || '0.00'-->
<!--}-->

<!--const formatSentiment = (sentiment) => {-->
<!--  if (!sentiment) return 'Neutral'-->
<!--  return sentiment.charAt(0).toUpperCase() + sentiment.slice(1)-->
<!--}-->

<!--const getSentimentColor = (sentiment) => {-->
<!--  if (!sentiment) return 'bg-card border'-->

<!--  switch (sentiment.toLowerCase()) {-->
<!--    case 'bullish':-->
<!--      return 'bg-green-50 dark:bg-green-950 border-green-200'-->
<!--    case 'bearish':-->
<!--      return 'bg-red-50 dark:bg-red-950 border-red-200'-->
<!--    case 'neutral':-->
<!--      return 'bg-blue-50 dark:bg-blue-950 border-blue-200'-->
<!--    default:-->
<!--      return 'bg-card border'-->
<!--  }-->
<!--}-->
<!--</script>-->


<template>
  <Card>
    <CardHeader>
      <CardTitle>AI Market Insights</CardTitle>
    </CardHeader>
    <CardContent>
      <div v-if="analysis" class="space-y-6">
        <!-- Market Sentiment -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div
            class="p-4 rounded-lg border"
            :class="getSentimentColor(analysis.sentiment)"
          >
            <h4 class="font-medium mb-2">Market Sentiment</h4>
            <p class="text-sm">{{ analysis.sentiment_summary || formatSentiment(analysis.sentiment) }}</p>
          </div>

          <div class="p-4 bg-card rounded-lg border">
            <h4 class="font-medium mb-2">Technical Overview</h4>
            <p class="text-sm">{{ analysis.technical_analysis }}</p>
          </div>
        </div>

        <!-- Key Insights -->
        <div>
          <h4 class="font-medium mb-2">Key Insights</h4>
          <div class="space-y-2">
            <Alert v-for="(insight, index) in uniqueInsights" :key="index">
              <AlertDescription>{{ insight }}</AlertDescription>
            </Alert>
          </div>
        </div>

        <!-- Support & Resistance -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <h4 class="font-medium mb-2">Support Levels</h4>
            <ul class="space-y-1">
              <li v-for="(level, index) in uniqueSupportLevels"
                  :key="index"
                  class="text-sm text-muted-foreground flex items-center gap-2">
                <ArrowRight class="h-4 w-4" />
                <span>${{ formatNumber(level) }}</span>
              </li>
            </ul>
          </div>
          <div>
            <h4 class="font-medium mb-2">Resistance Levels</h4>
            <ul class="space-y-1">
              <li v-for="(level, index) in uniqueResistanceLevels"
                  :key="index"
                  class="text-sm text-muted-foreground flex items-center gap-2">
                <ArrowRight class="h-4 w-4" />
                <span>${{ formatNumber(level) }}</span>
              </li>
            </ul>
          </div>
        </div>

        <!-- Risk Factors -->
        <div>
          <h4 class="font-medium mb-2">Risk Factors</h4>
          <div class="grid gap-2">
            <Alert variant="destructive" v-for="(risk, index) in uniqueRiskFactors" :key="index">
              <AlertDescription>{{ risk }}</AlertDescription>
            </Alert>
          </div>
        </div>

        <!-- Outlook -->
        <div v-if="analysis.short_term_outlook" class="border rounded-lg p-4">
          <h4 class="font-medium mb-2">Short-term Outlook</h4>
          <p class="text-sm">{{ analysis.short_term_outlook }}</p>
        </div>
      </div>

      <div v-else class="py-8 text-center text-muted-foreground">
        <Loader2 class="h-6 w-6 animate-spin mx-auto mb-2" />
        Analyzing market data...
      </div>
    </CardContent>
  </Card>
</template>

<script setup>
import { computed } from 'vue'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { ArrowRight, Loader2 } from 'lucide-vue-next'

const props = defineProps({
  analysis: {
    type: Object,
    default: null
  }
})

// Einzigartige Einsichten filtern
const uniqueInsights = computed(() => {
  return [...new Set(props.analysis?.key_insights || [])]
})

// Einzigartige Unterstützungslevel filtern
const uniqueSupportLevels = computed(() => {
  return [...new Set(props.analysis?.support_resistance?.support_levels || [])]
})

// Einzigartige Widerstandsebenen filtern
const uniqueResistanceLevels = computed(() => {
  return [...new Set(props.analysis?.support_resistance?.resistance_levels || [])]
})

// Einzigartige Risikofaktoren filtern
const uniqueRiskFactors = computed(() => {
  return [...new Set(props.analysis?.risk_factors || [])]
})

const formatNumber = (value) => {
  return value?.toFixed(2) || '0.00'
}

const formatSentiment = (sentiment) => {
  if (!sentiment) return 'Neutral'
  return sentiment.charAt(0).toUpperCase() + sentiment.slice(1)
}

const getSentimentColor = (sentiment) => {
  if (!sentiment) return 'bg-card border'

  switch (sentiment.toLowerCase()) {
    case 'bullish':
      return 'bg-green-50 dark:bg-green-950 border-green-200'
    case 'bearish':
      return 'bg-red-50 dark:bg-red-950 border-red-200'
    case 'neutral':
      return 'bg-blue-50 dark:bg-blue-950 border-blue-200'
    default:
      return 'bg-card border'
  }
}
</script>
