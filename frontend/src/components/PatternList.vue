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
              <h4 class="font-medium">{{ pattern.type }}</h4>
              <p class="text-sm text-muted-foreground">
                {{ pattern.description }}
              </p>
            </div>
            <Badge>{{ (pattern.confidence * 100).toFixed(0) }}%</Badge>
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
</script>