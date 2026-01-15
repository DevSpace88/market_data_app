<template>
  <Card>
    <CardHeader>
      <CardTitle class="flex items-center justify-between">
        <span>Master Investment Score</span>
        <Badge v-if="data" :variant="getRecommendationVariant(data.recommendation)">
          {{ data.recommendation.replace('_', ' ') }}
        </Badge>
      </CardTitle>
    </CardHeader>
    <CardContent>
      <div v-if="loading && !data" class="py-8 text-center text-muted-foreground">
        <Loader2 class="h-6 w-6 animate-spin mx-auto mb-2" />
        Calculating master score...
      </div>

      <div v-else-if="data" class="space-y-6">
        <!-- Main Score Display -->
        <div class="flex items-center justify-center py-6">
          <div class="relative">
            <!-- Circular Progress -->
            <svg class="w-40 h-40 transform -rotate-90">
              <circle
                cx="80"
                cy="80"
                r="70"
                fill="none"
                stroke="currentColor"
                stroke-width="12"
                class="text-muted opacity-20"
              />
              <circle
                cx="80"
                cy="80"
                r="70"
                fill="none"
                :stroke="getScoreColor(data.master_score)"
                stroke-width="12"
                stroke-linecap="round"
                :stroke-dasharray="circumference"
                :stroke-dashoffset="circumference - (data.master_score / 100) * circumference"
                class="transition-all duration-500"
              />
            </svg>
            <!-- Score in Center -->
            <div class="absolute inset-0 flex flex-col items-center justify-center">
              <span class="text-4xl font-bold" :class="getScoreColorClass(data.master_score)">
                {{ Math.round(data.master_score) }}
              </span>
              <span class="text-xs text-muted-foreground">out of 100</span>
            </div>
          </div>
        </div>

        <!-- Confidence -->
        <div class="flex items-center justify-center gap-2">
          <span class="text-sm text-muted-foreground">Confidence:</span>
          <Badge :variant="data.confidence === 'HIGH' ? 'default' : 'secondary'">
            {{ data.confidence }}
          </Badge>
        </div>

        <!-- Detailed Breakdown (if enabled) -->
        <div v-if="detailed" class="space-y-4 pt-4 border-t">
          <h4 class="text-sm font-medium">Score Breakdown</h4>

          <!-- Short-term -->
          <div class="space-y-2">
            <div class="flex items-center justify-between text-sm">
              <span>{{ data.breakdown.short_term.label }}</span>
              <span class="font-medium">{{ Math.round(data.breakdown.short_term.score) }}/100</span>
            </div>
            <Progress :model-value="data.breakdown.short_term.score" class="h-2" />
            <div class="text-xs text-muted-foreground">
              Weight: {{ Math.round(data.breakdown.short_term.weight * 100) }}%
            </div>
          </div>

          <!-- Medium-term -->
          <div class="space-y-2">
            <div class="flex items-center justify-between text-sm">
              <span>{{ data.breakdown.medium_term.label }}</span>
              <span class="font-medium">{{ Math.round(data.breakdown.medium_term.score) }}/100</span>
            </div>
            <Progress :model-value="data.breakdown.medium_term.score" class="h-2" />
            <div class="text-xs text-muted-foreground">
              Weight: {{ Math.round(data.breakdown.medium_term.weight * 100) }}%
            </div>
          </div>

          <!-- Long-term -->
          <div class="space-y-2">
            <div class="flex items-center justify-between text-sm">
              <span>{{ data.breakdown.long_term.label }}</span>
              <span class="font-medium">{{ Math.round(data.breakdown.long_term.score) }}/100</span>
            </div>
            <Progress :model-value="data.breakdown.long_term.score" class="h-2" />
            <div class="text-xs text-muted-foreground">
              Weight: {{ Math.round(data.breakdown.long_term.weight * 100) }}%
            </div>
          </div>

          <!-- Risk -->
          <div class="space-y-2">
            <div class="flex items-center justify-between text-sm">
              <span>{{ data.breakdown.risk.label }}</span>
              <span class="font-medium">{{ Math.round(data.breakdown.risk.score) }}/100</span>
            </div>
            <Progress :model-value="data.breakdown.risk.score" class="h-2" />
            <div class="text-xs text-muted-foreground">
              Weight: {{ Math.round(data.breakdown.risk.weight * 100) }}%
            </div>
          </div>

          <!-- Top Factors -->
          <div v-if="data.top_factors.length > 0" class="pt-4 border-t">
            <h4 class="text-sm font-medium mb-3">Top Contributing Factors</h4>
            <div class="space-y-2">
              <div
                v-for="factor in data.top_factors"
                :key="factor.name"
                class="flex items-center justify-between text-sm p-2 rounded-md bg-muted/50"
              >
                <span>{{ factor.name }}</span>
                <div class="flex items-center gap-2">
                  <Badge :variant="factor.contribution > 0 ? 'default' : 'destructive'">
                    {{ factor.contribution > 0 ? '+' : '' }}{{ factor.contribution }}
                  </Badge>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div v-else class="py-8 text-center text-muted-foreground">
        No score data available
      </div>
    </CardContent>
  </Card>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { Loader2 } from 'lucide-vue-next'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Progress } from '@/components/ui/progress'
import type { MasterScoreData } from '@/composables/useInvestmentEngine'

interface Props {
  data: MasterScoreData | null
  loading: boolean
  detailed?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  detailed: false
})

const circumference = 2 * Math.PI * 70 // 2 * π * r

const getScoreColor = (score: number) => {
  if (score >= 80) return '#22c55e' // green
  if (score >= 60) return '#84cc16' // lime
  if (score >= 40) return '#eab308' // yellow
  if (score >= 20) return '#f97316' // orange
  return '#ef4444' // red
}

const getScoreColorClass = (score: number) => {
  if (score >= 80) return 'text-green-600 dark:text-green-400'
  if (score >= 60) return 'text-lime-600 dark:text-lime-400'
  if (score >= 40) return 'text-yellow-600 dark:text-yellow-400'
  if (score >= 20) return 'text-orange-600 dark:text-orange-400'
  return 'text-red-600 dark:text-red-400'
}

const getRecommendationVariant = (recommendation: string) => {
  const variants = {
    STRONG_BUY: 'default',
    BUY: 'default',
    HOLD: 'secondary',
    SELL: 'destructive',
    STRONG_SELL: 'destructive'
  }
  return variants[recommendation] || 'secondary'
}
</script>
