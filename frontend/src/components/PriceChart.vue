<template>
  <div class="bg-card rounded-lg shadow p-4">
    <div class="h-[500px]" ref="chartRef"></div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, onUnmounted } from 'vue'
import * as echarts from 'echarts'

const props = defineProps({
  data: {
    type: Array,
    default: () => []
  },
  indicators: {
    type: Array,
    default: () => []
  }
})

const chartRef = ref(null)
const chart = ref(null)

const initChart = () => {
  if (!chartRef.value) return
  chart.value = echarts.init(chartRef.value)
  updateChart()
}

const updateChart = () => {
  if (!chart.value || !props.data) return

  const option = {
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'cross' }
    },
    legend: {
      data: ['Price', 'Volume', ...props.indicators]
    },
    grid: {
      left: '3%',
      right: '3%',
      bottom: '15%'
    },
    xAxis: {
      type: 'time',
      boundaryGap: false
    },
    yAxis: [
      {
        type: 'value',
        name: 'Price',
        position: 'left'
      },
      {
        type: 'value',
        name: 'Volume',
        position: 'right'
      }
    ],
    series: [
      {
        name: 'Price',
        type: 'line',
        data: props.data.map(item => [item.timestamp, item.close]),
        smooth: true
      },
      {
        name: 'Volume',
        type: 'bar',
        yAxisIndex: 1,
        data: props.data.map(item => [item.timestamp, item.volume])
      },
      ...props.indicators.map(indicator => ({
        name: indicator,
        type: 'line',
        smooth: true,
        data: props.data.map(item => [item.timestamp, item[indicator.toLowerCase()]])
      }))
    ]
  }

  chart.value.setOption(option)
}

onMounted(initChart)

watch(() => props.data, updateChart, { deep: true })
watch(() => props.indicators, updateChart)

onUnmounted(() => {
  if (chart.value) {
    chart.value.dispose()
  }
})
</script>