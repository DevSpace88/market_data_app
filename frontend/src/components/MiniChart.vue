<template>
  <div class="w-full h-full relative">
    <svg 
      :width="width" 
      :height="height" 
      class="w-full h-full"
      viewBox="0 0 64 32"
    >
      <defs>
        <linearGradient :id="gradientId" x1="0%" y1="0%" x2="0%" y2="100%">
          <stop 
            offset="0%" 
            :stop-color="isPositive ? '#10b981' : '#ef4444'"
            stop-opacity="0.3"
          />
          <stop 
            offset="100%" 
            :stop-color="isPositive ? '#10b981' : '#ef4444'"
            stop-opacity="0"
          />
        </linearGradient>
      </defs>
      
      <!-- Chart line -->
      <polyline
        :points="chartPoints"
        :stroke="isPositive ? '#10b981' : '#ef4444'"
        stroke-width="1.5"
        fill="none"
        stroke-linecap="round"
        stroke-linejoin="round"
      />
      
      <!-- Area under the curve -->
      <polygon
        :points="areaPoints"
        :fill="`url(#${gradientId})`"
      />
    </svg>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  data: {
    type: Array,
    required: true
  },
  isPositive: {
    type: Boolean,
    default: true
  },
  width: {
    type: Number,
    default: 64
  },
  height: {
    type: Number,
    default: 32
  }
})

const gradientId = computed(() => `gradient-${Math.random().toString(36).substr(2, 9)}`)

const chartPoints = computed(() => {
  if (!props.data || props.data.length < 2) return ''
  
  const min = Math.min(...props.data)
  const max = Math.max(...props.data)
  const range = max - min || 1
  
  const points = props.data.map((value, index) => {
    const x = (index / (props.data.length - 1)) * props.width
    const y = props.height - ((value - min) / range) * props.height
    return `${x},${y}`
  })
  
  return points.join(' ')
})

const areaPoints = computed(() => {
  if (!props.data || props.data.length < 2) return ''
  
  const min = Math.min(...props.data)
  const max = Math.max(...props.data)
  const range = max - min || 1
  
  const chartPoints = props.data.map((value, index) => {
    const x = (index / (props.data.length - 1)) * props.width
    const y = props.height - ((value - min) / range) * props.height
    return `${x},${y}`
  })
  
  // Add bottom corners for the area
  const firstPoint = chartPoints[0]
  const lastPoint = chartPoints[chartPoints.length - 1]
  const firstX = firstPoint.split(',')[0]
  const lastX = lastPoint.split(',')[0]
  
  return `${firstX},${props.height} ${chartPoints.join(' ')} ${lastX},${props.height}`
})
</script>
