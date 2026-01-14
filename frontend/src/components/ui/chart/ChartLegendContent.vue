<script setup lang="ts">
import { inject, computed } from 'vue'
import type { ChartConfig } from './utils'

const props = defineProps<{
  config?: ChartConfig
}>()

const injectConfig = inject<ChartConfig>('chart-config', {})
const config = computed(() => props.config || injectConfig)

const legendItems = computed(() => {
  const cfg = config.value
  return Object.entries(cfg).map(([key, item]) => ({
    name: key,
    label: item?.label || key,
    color: item?.color || 'var(--chart-1)'
  }))
})
</script>

<template>
  <div class="flex flex-wrap items-center justify-center gap-4">
    <div
      v-for="item in legendItems"
      :key="item.name"
      class="flex items-center gap-1.5"
    >
      <span
        class="h-2 w-2 shrink-0 rounded-[2px]"
        :style="{ backgroundColor: item.color }"
      />
      <span class="text-muted-foreground text-sm">{{ item.label }}</span>
    </div>
  </div>
</template>
