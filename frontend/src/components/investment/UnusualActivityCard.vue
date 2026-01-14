<template>
  <Card>
    <CardHeader>
      <CardTitle>Unusual Activity Detection</CardTitle>
    </CardHeader>
    <CardContent>
      <div v-if="loading && !data" class="py-8 text-center text-muted-foreground">
        <Loader2 class="h-6 w-6 animate-spin mx-auto mb-2" />
        Scanning for unusual activity...
      </div>

      <div v-else-if="data" class="space-y-6">
        <!-- Warning if applicable -->
        <Alert v-if="data.warning" variant="default">
          <AlertTriangle class="h-4 w-4" />
          <AlertDescription>{{ data.warning }}</AlertDescription>
        </Alert>

        <!-- Overall Status -->
        <div class="flex items-center justify-between p-4 rounded-lg bg-muted/50">
          <div>
            <div class="text-sm text-muted-foreground">Overall Status</div>
            <div class="text-2xl font-bold mt-1" :class="getSeverityColorClass(data.overall_severity)">
              {{ data.overall_severity }}
            </div>
          </div>
          <div class="text-right">
            <div v-if="data.has_unusual_activity" class="text-3xl font-bold text-orange-600">
              {{ data.activities.length }}
            </div>
            <div class="text-xs text-muted-foreground mt-1">
              {{ data.has_unusual_activity ? 'activities detected' : 'no unusual activity' }}
            </div>
          </div>
        </div>

        <!-- Activities List -->
        <div v-if="data.has_unusual_activity && data.activities.length > 0" class="space-y-4">
          <h4 class="text-sm font-medium">Detected Activities</h4>

          <div
            v-for="(activity, idx) in data.activities"
            :key="idx"
            class="p-4 rounded-lg border"
            :class="getActivityBorderClass(activity.severity)"
          >
            <!-- Activity Header -->
            <div class="flex items-start justify-between mb-3">
              <div class="flex items-center gap-2">
                <Badge :variant="getActivityVariant(activity.type)">
                  {{ formatActivityType(activity.type) }}
                </Badge>
                <Badge :variant="getSeverityVariant(activity.severity)">
                  {{ activity.severity }}
                </Badge>
              </div>
              <div class="text-xs text-muted-foreground">
                {{ activity.confidence }}% confidence
              </div>
            </div>

            <!-- Activity Details -->
            <div class="space-y-2 text-sm">
              <!-- Volume Spike Details -->
              <div v-if="activity.type === 'VOLUME_SPIKE'" class="space-y-1">
                <div class="flex justify-between">
                  <span class="text-muted-foreground">Current Volume:</span>
                  <span class="font-medium">
                    {{ formatNumber(activity.details.current_volume) }}
                  </span>
                </div>
                <div class="flex justify-between">
                  <span class="text-muted-foreground">Average Volume:</span>
                  <span class="font-medium">
                    {{ formatNumber(activity.details.average_volume) }}
                  </span>
                </div>
                <div class="flex justify-between">
                  <span class="text-muted-foreground">Ratio:</span>
                  <span class="font-medium text-orange-600">
                    {{ activity.details.ratio }}x normal
                  </span>
                </div>
              </div>

              <!-- Price Anomaly Details -->
              <div v-if="activity.type === 'PRICE_ANOMALY'" class="space-y-1">
                <div class="flex justify-between">
                  <span class="text-muted-foreground">Current Price:</span>
                  <span class="font-medium">
                    ${{ formatNumber(activity.details.current_price) }}
                  </span>
                </div>
                <div class="flex justify-between">
                  <span class="text-muted-foreground">Average Price:</span>
                  <span class="font-medium">
                    ${{ formatNumber(activity.details.average_price) }}
                  </span>
                </div>
                <div class="flex justify-between">
                  <span class="text-muted-foreground">Daily Change:</span>
                  <span
                    class="font-medium"
                    :class="activity.details.daily_change_percent >= 0 ? 'text-green-600' : 'text-red-600'"
                  >
                    {{ activity.details.daily_change_percent >= 0 ? '+' : '' }}{{ activity.details.daily_change_percent }}%
                  </span>
                </div>
              </div>

              <!-- Deviation -->
              <div v-if="activity.details.deviation" class="pt-2 border-t">
                <div class="flex items-center gap-2 text-xs text-muted-foreground">
                  <ActivityIcon class="h-3 w-3" />
                  <span>{{ activity.details.deviation }}</span>
                </div>
              </div>

              <!-- Interpretation -->
              <div v-if="activity.interpretation" class="pt-2 border-t">
                <p class="text-xs text-muted-foreground">{{ activity.interpretation }}</p>
              </div>
            </div>

            <!-- Timestamp -->
            <div v-if="activity.timestamp" class="mt-3 text-xs text-muted-foreground">
              Detected: {{ new Date(activity.timestamp).toLocaleString() }}
            </div>
          </div>
        </div>

        <!-- No Activity State -->
        <div v-else class="text-center py-8 text-muted-foreground">
          <div class="inline-flex items-center justify-center w-12 h-12 rounded-full bg-green-100 dark:bg-green-900/20 mb-3">
            <CheckIcon class="h-6 w-6 text-green-600 dark:text-green-400" />
          </div>
          <p>No unusual activity detected</p>
          <p class="text-xs mt-1">Market appears normal</p>
        </div>

        <!-- Phase 2 Features Placeholder -->
        <div class="pt-4 border-t">
          <div class="flex items-center justify-between">
            <div>
              <h4 class="text-sm font-medium">Advanced Detection</h4>
              <p class="text-xs text-muted-foreground mt-1">
                Coming in Phase 2: Dark Pool & Options Flow analysis
              </p>
            </div>
            <Badge variant="secondary">Phase 2</Badge>
          </div>
        </div>
      </div>

      <div v-else class="py-8 text-center text-muted-foreground">
        No activity data available
      </div>
    </CardContent>
  </Card>
</template>

<script setup lang="ts">
import { CheckIcon, ActivityIcon, AlertTriangle } from 'lucide-vue-next'
import { Loader2 } from 'lucide-vue-next'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Alert, AlertDescription } from '@/components/ui/alert'
import type { UnusualActivityData } from '@/composables/useInvestmentEngine'

interface Props {
  data: UnusualActivityData | null
  loading: boolean
}

defineProps<Props>()

const formatNumber = (num: number | undefined) => {
  if (!num) return 'N/A'
  if (num >= 1000000) return (num / 1000000).toFixed(1) + 'M'
  if (num >= 1000) return (num / 1000).toFixed(1) + 'K'
  return num.toFixed(0)
}

const formatActivityType = (type: string) => {
  const types = {
    VOLUME_SPIKE: 'Volume Spike',
    PRICE_ANOMALY: 'Price Anomaly',
    OPTIONS_FLOW: 'Options Flow',
    DARK_POOL: 'Dark Pool'
  }
  return types[type] || type
}

const getSeverityColorClass = (severity: string) => {
  const classes = {
    NONE: 'text-gray-600 dark:text-gray-400',
    LOW: 'text-blue-600 dark:text-blue-400',
    MEDIUM: 'text-yellow-600 dark:text-yellow-400',
    HIGH: 'text-orange-600 dark:text-orange-400',
    EXTREME: 'text-red-600 dark:text-red-400'
  }
  return classes[severity] || 'text-gray-600'
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

const getActivityVariant = (type: string) => {
  const variants = {
    VOLUME_SPIKE: 'default',
    PRICE_ANOMALY: 'destructive',
    OPTIONS_FLOW: 'outline',
    DARK_POOL: 'secondary'
  }
  return variants[type] || 'secondary'
}

const getActivityBorderClass = (severity: string) => {
  const classes = {
    NONE: 'border-gray-200 dark:border-gray-800',
    LOW: 'border-blue-200 dark:border-blue-900',
    MEDIUM: 'border-yellow-200 dark:border-yellow-900',
    HIGH: 'border-orange-200 dark:border-orange-900',
    EXTREME: 'border-red-200 dark:border-red-900'
  }
  return classes[severity] || 'border-gray-200'
}
</script>
