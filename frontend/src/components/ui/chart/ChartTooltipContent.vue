<script setup lang="ts">
import { inject, computed } from 'vue'
import { cn } from '@/lib/utils'
import type { ChartConfig } from './utils'

const props = defineProps<{
  data: Record<string, unknown>
  config?: ChartConfig
  labelFormatter?: (value: unknown, index: number) => string
  valueFormatter?: (value: unknown, name: string) => string
  indicator?: 'line' | 'dot' | 'dashed'
}>()

const config = inject<ChartConfig>('chart-config', {})

const items = computed(() => {
  if (!props.data) return []

  const keys = Object.keys(props.data).filter(key => key !== '0' && key !== 'data')
  return keys.map(key => {
    const item = props.config?.[key] || config[key] || {}
    const value = props.data[key]
    return {
      key,
      label: item?.label || key,
      color: item?.color || 'var(--chart-1)',
      value: props.valueFormatter ? props.valueFormatter(value, key) : String(value)
    }
  })
})

const label = computed(() => {
  const data = props.data
  if (props.labelFormatter && data) {
    const index = items.value.findIndex(item => item.key === '0')
    return props.labelFormatter(data, index)
  }
  return undefined
})
</script>

<template>
  <div
    :class="cn(
      'grid min-w-[8rem] items-start gap-1.5 rounded-lg border bg-popover px-2.5 py-1.5 text-xs shadow-xl',
      'sm:min-w-[12rem]'
    )"
  >
    <div v-if="label" class="text-muted-foreground font-medium">
      {{ label }}
    </div>
    <div class="grid gap-1.5">
      <div
        v-for="item in items"
        :key="item.key"
        class="flex items-center justify-between gap-2"
      >
        <div class="flex items-center gap-2">
          <span
            :class="cn(
              'h-2 w-2 shrink-0 rounded-[2px]',
              indicator === 'dashed' && 'border-2 border-[currentColor]'
            )"
            :style="{ backgroundColor: indicator !== 'dashed' ? item.color : undefined, borderColor: item.color }"
          />
          <span class="text-muted-foreground">{{ item.label }}</span>
        </div>
        <span class="font-mono font-medium tabular-nums">{{ item.value }}</span>
      </div>
    </div>
  </div>
</template>
