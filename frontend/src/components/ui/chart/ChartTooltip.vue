<script setup lang="ts">
import { inject, type Component } from 'vue'
import { VisTooltip } from '@unovis/vue'
import ChartTooltipContent from './ChartTooltipContent.vue'
import type { ChartConfig } from './utils'

const props = withDefaults(
  defineProps<{
    selector?: string
    index?: string
    customTooltip?: Component
    labelFormatter?: (value: unknown, index: number) => string
    valueFormatter?: (value: unknown, name: string) => string
  }>(),
  {
    selector: undefined,
    index: undefined,
  }
)

const config = inject<ChartConfig>('chart-config')
</script>

<template>
  <VisTooltip :selector="selector" :index="index">
    <template #default="data">
      <slot v-if="$slots.default" :data="data" />
      <component
        v-else-if="customTooltip"
        :is="customTooltip"
        :data="data"
      />
      <ChartTooltipContent
        v-else
        :data="data"
        :config="config"
        :label-formatter="labelFormatter"
        :value-formatter="valueFormatter"
      />
    </template>
  </VisTooltip>
</template>
