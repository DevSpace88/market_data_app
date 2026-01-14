<script setup lang="ts">
import { provide, toRef, type HTMLAttributes } from 'vue'
import type { ChartConfig } from './utils'

const props = defineProps<{
  config: ChartConfig
  class?: HTMLAttributes['class']
  cursor?: boolean
}>()

provide('chart-config', props.config)
provide('chart-cursor', toRef(props, 'cursor'))

// Generate unique ID for chart
const id = `chart-${Math.random().toString(36).substr(2, 9)}`
provide('chart-id', id)
</script>

<template>
  <div :class="props.class">
    <slot />
  </div>
</template>
