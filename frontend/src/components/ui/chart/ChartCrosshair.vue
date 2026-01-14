<script setup lang="ts">
import { inject } from 'vue'
import { VisCrosshair } from '@unovis/vue'
import type { ChartConfig } from './utils'

const props = defineProps<{
  template?: any
  color?: string | string[] | ((...args: unknown[]) => string)
}>()

const config = inject<ChartConfig>('chart-config')
</script>

<template>
  <VisCrosshair :template="template" :color="color" />
</template>
