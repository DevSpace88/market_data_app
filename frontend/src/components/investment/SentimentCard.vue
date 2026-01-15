<template>
  <Card>
    <CardHeader>
      <CardTitle>Sentiment Analysis</CardTitle>
    </CardHeader>
    <CardContent>
      <div v-if="loading && !data" class="py-8 text-center text-muted-foreground">
        <Loader2 class="h-6 w-6 animate-spin mx-auto mb-2" />
        Analyzing sentiment...
      </div>

      <div v-else-if="data" class="space-y-6">
        <!-- Warning if applicable -->
        <Alert v-if="data.warning" variant="default">
          <InfoIcon class="h-4 w-4" />
          <AlertDescription>{{ data.warning }}</AlertDescription>
        </Alert>

        <!-- Overall Sentiment -->
        <div class="flex items-center justify-between p-4 rounded-lg bg-muted/50">
          <div>
            <div class="text-sm text-muted-foreground">Overall Sentiment</div>
            <div class="text-2xl font-bold mt-1" :class="getSentimentColorClass(data.sentiment_score)">
              {{ data.sentiment_label }}
            </div>
          </div>
          <div class="text-right">
            <div class="text-3xl font-bold" :class="getSentimentColorClass(data.sentiment_score)">
              {{ data.sentiment_score > 0 ? '+' : '' }}{{ data.sentiment_score }}
            </div>
            <div class="text-xs text-muted-foreground mt-1">
              {{ data.confidence }} confidence
            </div>
          </div>
        </div>

        <!-- Sentiment Meter -->
        <div class="space-y-2">
          <div class="flex justify-between text-sm">
            <span class="text-red-500">Bearish</span>
            <span class="text-yellow-500">Neutral</span>
            <span class="text-green-500">Bullish</span>
          </div>
          <div class="relative h-3 rounded-full bg-gradient-to-r from-red-500 via-yellow-500 to-green-500">
            <div
              class="absolute w-4 h-4 bg-white border-2 border-gray-900 rounded-full top-1/2 -translate-y-1/2 transition-all"
              :style="{ left: `calc(${((data.sentiment_score + 100) / 200) * 100}% - 8px)` }"
            />
          </div>
        </div>

        <!-- News Breakdown -->
        <div v-if="data.breakdown.news" class="space-y-3 pt-4 border-t">
          <h4 class="text-sm font-medium">News Analysis</h4>
          <div class="grid grid-cols-3 gap-4">
            <div class="text-center">
              <div class="text-2xl font-bold text-green-600">{{ data.breakdown.news.positive }}</div>
              <div class="text-xs text-muted-foreground">Positive</div>
            </div>
            <div class="text-center">
              <div class="text-2xl font-bold text-yellow-600">{{ data.breakdown.news.neutral }}</div>
              <div class="text-xs text-muted-foreground">Neutral</div>
            </div>
            <div class="text-center">
              <div class="text-2xl font-bold text-red-600">{{ data.breakdown.news.negative }}</div>
              <div class="text-xs text-muted-foreground">Negative</div>
            </div>
          </div>
          <div class="text-xs text-center text-muted-foreground">
            {{ data.breakdown.news.count }} articles analyzed from {{ data.data_sources }}
          </div>
        </div>

        <!-- Top Headlines -->
        <div v-if="data.top_headlines.length > 0" class="space-y-3 pt-4 border-t">
          <h4 class="text-sm font-medium">Top Headlines</h4>
          <div class="space-y-2">
            <div
              v-for="(headline, idx) in data.top_headlines"
              :key="idx"
              class="flex items-center gap-2 p-3 rounded-md bg-muted/50"
            >
              <div class="flex-1 min-w-0">
                <a
                  :href="headline.link"
                  target="_blank"
                  rel="noopener noreferrer"
                  class="text-sm line-clamp-2 hover:underline"
                >
                  {{ headline.title }}
                </a>
                <div class="flex items-center gap-2 mt-2">
                  <Badge variant="outline" size="sm">
                    {{ headline.sentiment_contribution }}
                  </Badge>
                  <span v-if="headline.timestamp" class="text-xs text-muted-foreground">
                    {{ new Date(headline.timestamp).toLocaleDateString() }}
                  </span>
                </div>
              </div>
              <Button
                as="a"
                :href="headline.link"
                target="_blank"
                rel="noopener noreferrer"
                size="sm"
                variant="ghost"
              >
                <ExternalLinkIcon class="h-4 w-4" />
              </Button>
            </div>
          </div>
        </div>

        <!-- Social Buzz (Phase 2 placeholder) -->
        <div class="pt-4 border-t">
          <div class="flex items-center justify-between">
            <div>
              <h4 class="text-sm font-medium">Social Buzz</h4>
              <p class="text-xs text-muted-foreground mt-1">
                Coming in Phase 2: Twitter/X & Reddit integration
              </p>
            </div>
            <Badge variant="secondary">Phase 2</Badge>
          </div>
        </div>

        <!-- Price Correlation (Phase 2 placeholder) -->
        <div v-if="data.price_correlation === null" class="pt-4 border-t">
          <div class="flex items-center justify-between">
            <div>
              <h4 class="text-sm font-medium">Price Correlation</h4>
              <p class="text-xs text-muted-foreground mt-1">
                Coming soon: Compare sentiment with price movement
              </p>
            </div>
            <Badge variant="secondary">Soon</Badge>
          </div>
        </div>
      </div>

      <div v-else class="py-8 text-center text-muted-foreground">
        No sentiment data available
      </div>
    </CardContent>
  </Card>
</template>

<script setup lang="ts">
import { InfoIcon, ExternalLinkIcon } from 'lucide-vue-next'
import { Loader2 } from 'lucide-vue-next'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Alert, AlertDescription } from '@/components/ui/alert'
import type { SentimentData } from '@/composables/useInvestmentEngine'

interface Props {
  data: SentimentData | null
  loading: boolean
}

defineProps<Props>()

const getSentimentColorClass = (score: number) => {
  if (score >= 60) return 'text-green-600 dark:text-green-400'
  if (score >= 30) return 'text-lime-600 dark:text-lime-400'
  if (score >= -30) return 'text-yellow-600 dark:text-yellow-400'
  if (score >= -60) return 'text-orange-600 dark:text-orange-400'
  return 'text-red-600 dark:text-red-400'
}
</script>
