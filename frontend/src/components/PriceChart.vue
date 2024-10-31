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
  },
  technicalData: {
    type: Object,
    default: () => ({})
  }
})

const chartRef = ref(null)
const chart = ref(null)

const formatVolume = (value) => {
  if (value >= 1000000) return `${(value / 1000000).toFixed(1)}M`
  if (value >= 1000) return `${(value / 1000).toFixed(1)}K`
  return value.toString()
}

const getIndicatorColor = (indicator) => {
  const colors = {
    sma_20: '#7cb5ec',
    sma_50: '#434348',
    bb_upper: '#90ed7d',
    bb_middle: '#8085e9',
    bb_lower: '#90ed7d'
  }
  return colors[indicator] || '#000000'
}

const initChart = () => {
  if (!chartRef.value) return
  chart.value = echarts.init(chartRef.value)
  updateChart()
}

const updateChart = () => {
  if (!chart.value || !props.data.length) return

  console.log('Updating chart with data:', {
    dataPoints: props.data.length,
    indicators: props.indicators,
    technicalData: props.technicalData
  })

  // Daten für den Hauptchart
  const priceData = props.data.map(item => ({
    name: new Date(item.timestamp).toISOString(),
    value: [
      new Date(item.timestamp).getTime(),
      Number(item.close)
    ]
  }))

  const volumeData = props.data.map(item => ({
    name: new Date(item.timestamp).toISOString(),
    value: [
      new Date(item.timestamp).getTime(),
      Number(item.volume)
    ]
  }))

  // Technische Indikatoren vorbereiten
  const indicatorSeries = []
  if (props.technicalData && props.indicators.length > 0) {
    // Für jeden Indikator einen konstanten Wert über den gesamten Zeitraum erstellen
    props.indicators.forEach(indicator => {
      const value = props.technicalData[indicator]
      if (value !== undefined) {
        const indicatorData = props.data.map(item => ({
          name: new Date(item.timestamp).toISOString(),
          value: [
            new Date(item.timestamp).getTime(),
            value
          ]
        }))

        indicatorSeries.push({
          name: indicator.toUpperCase(),
          type: 'line',
          smooth: true,
          showSymbol: false,
          data: indicatorData,
          lineStyle: {
            width: 1,
            color: getIndicatorColor(indicator),
            type: 'dashed'
          }
        })
      }
    })
  }

  const option = {
    animation: false,
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'cross' },
      formatter: (params) => {
        const date = new Date(params[0].value[0]).toLocaleString()
        let result = `<div>${date}</div>`
        params.forEach(param => {
          const value = param.seriesName === 'Volume'
            ? formatVolume(param.value[1])
            : `$${param.value[1].toFixed(2)}`
          result += `<div>${param.marker}${param.seriesName}: ${value}</div>`
        })
        return result
      }
    },
    legend: {
      data: ['Price', 'Volume', ...props.indicators.map(i => i.toUpperCase())],
      selected: {
        'Volume': true,
        ...props.indicators.reduce((acc, curr) => ({...acc, [curr.toUpperCase()]: true}), {})
      }
    },
    grid: [{
      left: '3%',
      right: '3%',
      height: '60%'
    }, {
      left: '3%',
      right: '3%',
      top: '75%',
      height: '20%'
    }],
    xAxis: [{
      type: 'time',
      boundaryGap: false,
      axisLine: { onZero: false },
      splitLine: { show: false },
      min: 'dataMin',
      max: 'dataMax',
      axisLabel: {
        formatter: (value) => {
          return new Date(value).toLocaleDateString()
        }
      }
    }, {
      type: 'time',
      gridIndex: 1,
      boundaryGap: false,
      axisLine: { onZero: false },
      axisTick: { show: false },
      splitLine: { show: false },
      axisLabel: { show: false },
      min: 'dataMin',
      max: 'dataMax'
    }],
    yAxis: [{
      type: 'value',
      position: 'right',
      splitLine: { show: false },
      axisLabel: {
        formatter: (value) => `$${value.toFixed(2)}`
      }
    }, {
      gridIndex: 1,
      position: 'right',
      splitLine: { show: false },
      axisLabel: {
        formatter: formatVolume
      }
    }],
    dataZoom: [{
      type: 'inside',
      xAxisIndex: [0, 1],
      start: 0,
      end: 100
    }, {
      show: true,
      xAxisIndex: [0, 1],
      type: 'slider',
      bottom: '0%',
      start: 0,
      end: 100
    }],
    series: [
      {
        name: 'Price',
        type: 'line',
        data: priceData,
        smooth: true,
        showSymbol: false,
        lineStyle: {
          width: 1.5,
          color: '#2196F3'
        }
      },
      ...indicatorSeries,
      {
        name: 'Volume',
        type: 'bar',
        xAxisIndex: 1,
        yAxisIndex: 1,
        data: volumeData,
        itemStyle: {
          color: '#E0E0E0'
        }
      }
    ]
  }

  chart.value.setOption(option, true)
}

onMounted(() => {
  initChart()
  window.addEventListener('resize', () => chart.value?.resize())
})

watch(() => props.data, updateChart, { deep: true })
watch(() => props.indicators, updateChart)
watch(() => props.technicalData, updateChart, { deep: true })

onUnmounted(() => {
  window.removeEventListener('resize', () => chart.value?.resize())
  chart.value?.dispose()
})
</script>