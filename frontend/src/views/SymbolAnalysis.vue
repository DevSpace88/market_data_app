<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <h2 class="text-3xl font-bold">{{ symbol }}</h2>
      <Badge>Loading...</Badge>
    </div>

    <Card>
      <CardHeader>
        <CardTitle>Market Data</CardTitle>
        <CardDescription>
          Analyzing {{ symbol }}...
        </CardDescription>
      </CardHeader>
      <CardContent>
        <p class="text-muted-foreground">
          Loading market data and analysis...
        </p>
      </CardContent>
    </Card>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'

const route = useRoute()
const symbol = computed(() => route.params.symbol)
</script>