import type { Component } from 'vue'

export type ChartConfig = {
  [key: string]: {
    label?: string
    icon?: Component
    color?: string
  }
}

export type ChartTooltipContentProps = {
  title?: string
  data?: Record<string, unknown>
  labelFormatter?: (value: unknown, index: number) => string
  valueFormatter?: (value: unknown, name: string) => string
  indicator?: 'line' | 'dot' | 'dashed'
  config?: ChartConfig
}

export function componentToString(
  config: ChartConfig,
  component: Component,
  props: ChartTooltipContentProps
) {
  return {
    title: props.title || '',
    config,
    labelFormatter: props.labelFormatter || ((v: unknown) => String(v)),
    valueFormatter: props.valueFormatter || ((v: unknown) => String(v))
  }
}
