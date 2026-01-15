<template>
  <div class="space-y-6">
    <!-- Overview Tab -->
    <div v-if="activeTab === 'overview'" class="space-y-6">
      <!-- Master Score Hero -->
      <MasterScoreCard
        :data="decisionData?.master_score"
        :loading="isLoading"
      />

      <!-- Quick Summary Grid -->
      <div class="grid gap-4 md:grid-cols-3">
        <Card>
          <CardHeader class="pb-3">
            <CardTitle class="text-sm font-medium">Sentiment</CardTitle>
          </CardHeader>
          <CardContent>
            <div v-if="decisionData?.sentiment" class="space-y-2">
              <div class="flex items-center gap-2">
                <span
                  class="text-2xl font-bold"
                  :class="getSentimentColorClass(decisionData.sentiment.sentiment_score)"
                >
                  {{ decisionData.sentiment.sentiment_label }}
                </span>
              </div>
              <div class="text-xs text-muted-foreground">
                Score: {{ decisionData.sentiment.sentiment_score }}
              </div>
            </div>
            <div v-else class="text-sm text-muted-foreground">
              No sentiment data available
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader class="pb-3">
            <CardTitle class="text-sm font-medium">Unusual Activity</CardTitle>
          </CardHeader>
          <CardContent>
            <div v-if="decisionData?.unusual_activity" class="space-y-2">
              <div class="flex items-center gap-2">
                <Badge
                  :variant="getSeverityVariant(decisionData.unusual_activity.overall_severity)"
                >
                  {{ decisionData.unusual_activity.overall_severity }}
                </Badge>
                <span v-if="decisionData.unusual_activity.has_unusual_activity" class="text-xs text-muted-foreground">
                  {{ decisionData.unusual_activity.activities.length }} detected
                </span>
              </div>
              <div v-if="!decisionData.unusual_activity.has_unusual_activity" class="text-xs text-muted-foreground">
                No unusual activity
              </div>
            </div>
            <div v-else class="text-sm text-muted-foreground">
              No activity data available
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader class="pb-3">
            <CardTitle class="text-sm font-medium">Signal Accuracy</CardTitle>
          </CardHeader>
          <CardContent>
            <div v-if="decisionData?.signal_performance" class="space-y-2">
              <div class="flex items-center gap-2">
                <span
                  class="text-2xl font-bold"
                  :class="getWinRateColorClass(decisionData.signal_performance.overall.win_rate)"
                >
                  {{ decisionData.signal_performance.overall.win_rate }}%
                </span>
                <span class="text-xs text-muted-foreground">win rate</span>
              </div>
              <div class="text-xs text-muted-foreground">
                {{ decisionData.signal_performance.overall.total_signals }} signals tracked
              </div>
            </div>
            <div v-else class="text-sm text-muted-foreground">
              No performance data yet
            </div>
          </CardContent>
        </Card>
      </div>
    </div>

    <!-- Technical Tab -->
    <div v-if="activeTab === 'technical'">
      <MasterScoreCard
        :data="decisionData?.master_score"
        :loading="isLoading"
        :detailed="true"
      />
    </div>

    <!-- Sentiment Tab -->
    <div v-if="activeTab === 'sentiment'">
      <SentimentCard
        :data="decisionData?.sentiment"
        :loading="isLoading"
      />
    </div>

    <!-- Activity Tab -->
    <div v-if="activeTab === 'activity'">
      <UnusualActivityCard
        :data="decisionData?.unusual_activity"
        :loading="isLoading"
      />
    </div>

    <!-- Performance Tab -->
    <div v-if="activeTab === 'performance'">
      <SignalPerformanceCard
        :data="decisionData?.signal_performance"
        :loading="isLoading"
      />
    </div>

    <!-- Tab Navigation -->
    <Tabs v-model="activeTab" class="w-full">
      <TabsList class="grid w-full grid-cols-5">
        <TabsTrigger value="overview">
          Overview
        </TabsTrigger>
        <TabsTrigger value="technical">
          Technical
        </TabsTrigger>
        <TabsTrigger value="sentiment">
          Sentiment
        </TabsTrigger>
        <TabsTrigger value="activity">
          Activity
        </TabsTrigger>
        <TabsTrigger value="performance">
          Performance
        </TabsTrigger>
      </TabsList>
    </Tabs>

    <!-- Data Quality Badge -->
    <div class="flex items-center justify-between text-xs text-muted-foreground">
      <span>Data Quality: {{ decisionData?.data_quality || 'N/A' }}</span>
      <span v-if="decisionData?.generated_at">
        Updated: {{ new Date(decisionData.generated_at).toLocaleTimeString() }}
      </span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { Tabs, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import MasterScoreCard from './MasterScoreCard.vue'
import SentimentCard from './SentimentCard.vue'
import UnusualActivityCard from './UnusualActivityCard.vue'
import SignalPerformanceCard from './SignalPerformanceCard.vue'
import type { InvestmentDecisionData } from '@/composables/useInvestmentEngine'

interface Props {
  decisionData: InvestmentDecisionData | null
  isLoading: boolean
}

const props = defineProps<Props>()

const activeTab = ref('overview')

const getSentimentColorClass = (score: number) => {
  if (score >= 60) return 'text-green-600 dark:text-green-400'
  if (score >= 30) return 'text-lime-600 dark:text-lime-400'
  if (score >= -30) return 'text-yellow-600 dark:text-yellow-400'
  if (score >= -60) return 'text-orange-600 dark:text-orange-400'
  return 'text-red-600 dark:text-red-400'
}

const getSeverityVariant = (severity: string) => {
  const variants = {
    NONE: 'secondary',
    LOW: 'default',
    MEDIUM: 'outline',
    HIGH: 'default',
    EXTREME: 'destructive'
  }
  return variants[severity] || 'secondary'
}

const getWinRateColorClass = (winRate: number) => {
  if (winRate >= 70) return 'text-green-600 dark:text-green-400'
  if (winRate >= 55) return 'text-lime-600 dark:text-lime-400'
  if (winRate >= 45) return 'text-yellow-600 dark:text-yellow-400'
  return 'text-red-600 dark:text-red-400'
}
</script>
