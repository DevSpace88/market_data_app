<template>
  <Card>
    <CardHeader>
      <CardTitle>Signal Performance Tracking</CardTitle>
    </CardHeader>
    <CardContent>
      <div v-if="loading && !data" class="py-8 text-center text-muted-foreground">
        <Loader2 class="h-6 w-6 animate-spin mx-auto mb-2" />
        Loading performance data...
      </div>

      <div v-else-if="data" class="space-y-6">
        <!-- Message if applicable -->
        <Alert v-if="data.message" variant="default">
          <InfoIcon class="h-4 w-4" />
          <AlertDescription>{{ data.message }}</AlertDescription>
        </Alert>

        <!-- Overall Performance -->
        <div class="space-y-4">
          <h4 class="text-sm font-medium">Overall Performance</h4>

          <div class="grid gap-4 md:grid-cols-3">
            <!-- Win Rate -->
            <div class="p-4 rounded-lg bg-muted/50">
              <div class="text-xs text-muted-foreground mb-1">Win Rate</div>
              <div class="text-3xl font-bold" :class="getWinRateColorClass(data.overall.win_rate)">
                {{ data.overall.win_rate }}%
              </div>
              <div class="text-xs text-muted-foreground mt-2">
                {{ data.overall.profitable_signals }} of {{ data.overall.total_signals }} signals
              </div>
            </div>

            <!-- Avg Return -->
            <div class="p-4 rounded-lg bg-muted/50">
              <div class="text-xs text-muted-foreground mb-1">Avg Return</div>
              <div
                class="text-3xl font-bold"
                :class="data.overall.avg_return_percent >= 0 ? 'text-green-600' : 'text-red-600'"
              >
                {{ data.overall.avg_return_percent >= 0 ? '+' : '' }}{{ data.overall.avg_return_percent }}%
              </div>
              <div class="text-xs text-muted-foreground mt-2">
                per signal
              </div>
            </div>

            <!-- vs Benchmark -->
            <div class="p-4 rounded-lg bg-muted/50">
              <div class="text-xs text-muted-foreground mb-1">vs Benchmark</div>
              <div
                class="text-3xl font-bold"
                :class="data.overall.avg_excess_return_percent >= 0 ? 'text-green-600' : 'text-red-600'"
              >
                {{ data.overall.avg_excess_return_percent >= 0 ? '+' : '' }}{{ data.overall.avg_excess_return_percent }}%
              </div>
              <div class="text-xs text-muted-foreground mt-2">
                excess return
              </div>
            </div>
          </div>
        </div>

        <!-- By Signal Type -->
        <div v-if="Object.keys(data.by_signal_type).length > 0" class="space-y-3 pt-4 border-t">
          <h4 class="text-sm font-medium">Performance by Signal Type</h4>
          <div class="space-y-2">
            <div
              v-for="(perf, type) in data.by_signal_type"
              :key="type"
              class="flex items-center justify-between p-3 rounded-md bg-muted/50"
            >
              <div class="flex items-center gap-3">
                <Badge :variant="type === 'BUY' ? 'default' : type === 'SELL' ? 'destructive' : 'secondary'">
                  {{ type }}
                </Badge>
                <span class="text-sm text-muted-foreground">{{ perf.count }} signals</span>
              </div>
              <div class="text-right">
                <div class="font-medium" :class="getWinRateColorClass(perf.win_rate)">
                  {{ perf.win_rate }}% win rate
                </div>
                <div class="text-xs text-muted-foreground">
                  avg: {{ perf.avg_return >= 0 ? '+' : '' }}{{ perf.avg_return }}%
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- By Timeframe -->
        <div v-if="Object.keys(data.by_timeframe).length > 0" class="space-y-3 pt-4 border-t">
          <h4 class="text-sm font-medium">Performance by Timeframe</h4>
          <div class="space-y-2">
            <div
              v-for="(perf, timeframe) in data.by_timeframe"
              :key="timeframe"
              class="flex items-center justify-between p-3 rounded-md bg-muted/50"
            >
              <div class="flex items-center gap-3">
                <Badge variant="outline">
                  {{ timeframe }}
                </Badge>
                <span class="text-sm text-muted-foreground">{{ perf.count }} signals</span>
              </div>
              <div class="text-right">
                <div class="font-medium" :class="getWinRateColorClass(perf.win_rate)">
                  {{ perf.win_rate }}% win rate
                </div>
                <div class="text-xs text-muted-foreground">
                  avg: {{ perf.avg_return >= 0 ? '+' : '' }}{{ perf.avg_return }}%
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Benchmark Comparison -->
        <div class="space-y-3 pt-4 border-t">
          <h4 class="text-sm font-medium">Benchmark Comparison</h4>
          <div class="grid gap-4 md:grid-cols-2">
            <div class="p-3 rounded-md bg-muted/50">
              <div class="text-xs text-muted-foreground mb-1">Outperformed</div>
              <div class="text-2xl font-bold text-green-600">
                {{ data.vs_benchmark.outperformed }}
              </div>
            </div>
            <div class="p-3 rounded-md bg-muted/50">
              <div class="text-xs text-muted-foreground mb-1">Beat Rate</div>
              <div
                class="text-2xl font-bold"
                :class="data.vs_benchmark.beat_rate >= 50 ? 'text-green-600' : 'text-red-600'"
              >
                {{ data.vs_benchmark.beat_rate }}%
              </div>
            </div>
          </div>
        </div>

        <!-- Last Updated -->
        <div class="text-xs text-center text-muted-foreground pt-4 border-t">
          Last updated: {{ new Date(data.timestamp).toLocaleString() }}
        </div>
      </div>

      <!-- No Data State -->
      <div v-else class="py-8 text-center text-muted-foreground">
        <div class="inline-flex items-center justify-center w-12 h-12 rounded-full bg-yellow-100 dark:bg-yellow-900/20 mb-3">
          <ClockIcon class="h-6 w-6 text-yellow-600 dark:text-yellow-400" />
        </div>
        <p>No performance data yet</p>
        <p class="text-xs mt-1">Signals need time to be evaluated</p>
      </div>
    </CardContent>
  </Card>
</template>

<script setup lang="ts">
import { InfoIcon, ClockIcon } from 'lucide-vue-next'
import { Loader2 } from 'lucide-vue-next'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Alert, AlertDescription } from '@/components/ui/alert'
import type { SignalPerformanceData } from '@/composables/useInvestmentEngine'

interface Props {
  data: SignalPerformanceData | null
  loading: boolean
}

defineProps<Props>()

const getWinRateColorClass = (winRate: number) => {
  if (winRate >= 70) return 'text-green-600 dark:text-green-400'
  if (winRate >= 55) return 'text-lime-600 dark:text-lime-400'
  if (winRate >= 45) return 'text-yellow-600 dark:text-yellow-400'
  return 'text-red-600 dark:text-red-400'
}
</script>
