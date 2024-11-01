<template>
  <div class="bg-card rounded-lg shadow p-4">
    <div class="h-[700px]" ref="chartRef"></div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, onUnmounted, nextTick } from 'vue'
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
const isInitialized = ref(false)
const selectedIndicators = ref({
  'K-Line': true,
  'Volume': true,
  'MA20': true,
  'MA50': true,
  'BB_UPPER': true,
  'BB_MIDDLE': true,
  'BB_LOWER': true
})

const formatVolume = (value) => {
  if (value >= 1000000) return `${(value / 1000000).toFixed(1)}M`
  if (value >= 1000) return `${(value / 1000).toFixed(1)}K`
  return value.toString()
}

const getIndicatorColor = (indicator) => {
  const colors = {
    'K-Line': '#000000',
    'MA20': '#2196F3',
    'MA50': '#FF9800',
    'BB_UPPER': '#4CAF50',
    'BB_MIDDLE': '#9C27B0',
    'BB_LOWER': '#4CAF50',
    'Volume': '#888888'
  }
  return colors[indicator] || '#000000'
}

const calculateMAValues = (data, period) => {
  if (!data || data.length < period) return []

  return data.map((item, index) => {
    if (index < period - 1) return null
    const slice = data.slice(index - period + 1, index + 1)
    const sum = slice.reduce((acc, val) => acc + val.close, 0)
    return [
      new Date(item.timestamp).getTime(),
      sum / period
    ]
  }).filter(item => item !== null)
}

const handleLegendSelectChanged = async (params) => {
  try {
    const { name, selected } = params
    selectedIndicators.value[name] = selected[name]

    if (chart.value && isInitialized.value) {
      await nextTick()
      const option = chart.value.getOption()
      const seriesIndex = option.series.findIndex(s => s.name === name)

      if (seriesIndex !== -1) {
        option.series[seriesIndex].show = selected[name]
        chart.value.setOption(option, {
          replaceMerge: ['series']
        })
      }
    }
  } catch (error) {
    console.error('Legend change error:', error)
  }
}

const initChart = async () => {
  try {
    if (!chartRef.value) return

    // Cleanup altes Chart
    if (chart.value) {
      chart.value.off('legendselectchanged', handleLegendSelectChanged)
      chart.value.dispose()
      chart.value = null
    }

    // Warten auf DOM-Update
    await nextTick()

    // Chart initialisieren
    chart.value = echarts.init(chartRef.value)
    chart.value.on('legendselectchanged', handleLegendSelectChanged)

    // Warten auf Chart-Initialisierung
    await nextTick()
    isInitialized.value = true

    // Erstes Update
    await updateChart()

  } catch (error) {
    console.error('Chart initialization error:', error)
    isInitialized.value = false
  }
}

const updateChart = async () => {
  try {
    if (!chart.value || !props.data.length || !isInitialized.value) return

    const priceData = props.data.map(item => ([
      new Date(item.timestamp).getTime(),
      Number(item.open),
      Number(item.close),
      Number(item.low),
      Number(item.high)
    ]))

    const volumeData = props.data.map(item => ([
      new Date(item.timestamp).getTime(),
      Number(item.volume),
      Number(item.close) > Number(item.open) ? 1 : -1
    ]))

    const ma20Data = calculateMAValues(props.data, 20)
    const ma50Data = calculateMAValues(props.data, 50)

    const bbSeries = ['BB_UPPER', 'BB_MIDDLE', 'BB_LOWER'].map(band => ({
      name: band,
      type: 'line',
      show: selectedIndicators.value[band],
      data: props.data.map(item => {
        const value = props.technicalData?.historical?.[item.timestamp]?.[band.toLowerCase()]
        return value ? [
          new Date(item.timestamp).getTime(),
          value
        ] : null
      }).filter(item => item !== null),
      smooth: true,
      lineStyle: {
        opacity: 0.8,
        width: 2,
        type: 'dashed',
        color: getIndicatorColor(band)
      },
      symbol: 'none'
    }))

    const option = {
      animation: false,
      legend: {
        show: true,
        top: 10,
        left: 10,
        itemGap: 20,
        selectedMode: 'multiple',
        selected: selectedIndicators.value,
        data: [
          { name: 'K-Line', icon: 'roundRect' },
          { name: 'MA20', icon: 'line' },
          { name: 'MA50', icon: 'line' },
          { name: 'BB_UPPER', icon: 'line' },
          { name: 'BB_MIDDLE', icon: 'line' },
          { name: 'BB_LOWER', icon: 'line' },
          { name: 'Volume', icon: 'roundRect' }
        ],
        textStyle: {
          fontSize: 12,
          color: '#333'
        }
      },
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'cross'
        }
      },
      grid: [{
        left: '10%',
        right: '3%',
        height: '70%',
        top: '8%'
      }, {
        left: '10%',
        right: '3%',
        top: '82%',
        height: '12%'
      }],
      xAxis: [{
        type: 'time',
        boundaryGap: false,
        axisLine: { onZero: false },
        splitLine: { show: false },
        min: 'dataMin',
        max: 'dataMax'
      }, {
        type: 'time',
        gridIndex: 1,
        boundaryGap: false,
        axisLine: { onZero: false },
        axisTick: { show: false },
        splitLine: { show: false },
        axisLabel: { show: false }
      }],
      yAxis: [{
        scale: true,
        splitLine: { show: true },
        position: 'left',
        axisLabel: {
          formatter: (value) => `$${value.toFixed(2)}`
        }
      }, {
        scale: true,
        gridIndex: 1,
        splitNumber: 2,
        position: 'left',
        axisLabel: {
          formatter: formatVolume
        }
      }],
      series: [
        {
          name: 'K-Line',
          type: 'candlestick',
          data: priceData,
          show: selectedIndicators.value['K-Line'],
          itemStyle: {
            color: '#ef5350',
            color0: '#26a69a',
            borderColor: '#ef5350',
            borderColor0: '#26a69a'
          }
        },
        {
          name: 'MA20',
          type: 'line',
          data: ma20Data,
          show: selectedIndicators.value['MA20'],
          smooth: true,
          lineStyle: {
            opacity: 0.8,
            width: 2,
            color: getIndicatorColor('MA20')
          },
          symbol: 'none'
        },
        {
          name: 'MA50',
          type: 'line',
          data: ma50Data,
          show: selectedIndicators.value['MA50'],
          smooth: true,
          lineStyle: {
            opacity: 0.8,
            width: 2,
            color: getIndicatorColor('MA50')
          },
          symbol: 'none'
        },
        ...bbSeries,
        {
          name: 'Volume',
          type: 'bar',
          xAxisIndex: 1,
          yAxisIndex: 1,
          data: volumeData,
          show: selectedIndicators.value['Volume'],
          itemStyle: {
            color: params => params.value[2] > 0 ? '#26a69a' : '#ef5350'
          }
        }
      ]
    }

    await nextTick()
    chart.value.setOption(option, {
      replaceMerge: ['series'],
      lazyUpdate: true
    })

  } catch (error) {
    console.error('Chart update error:', error)
  }
}

// Verzögertes Resize-Handling
let resizeTimeout
const handleResize = () => {
  if (resizeTimeout) clearTimeout(resizeTimeout)
  resizeTimeout = setTimeout(() => {
    if (chart.value && isInitialized.value) {
      chart.value.resize()
    }
  }, 100)
}

onMounted(async () => {
  await initChart()
  window.addEventListener('resize', handleResize)
})

// Watchers
watch(() => props.data, async () => {
  if (isInitialized.value) {
    await updateChart()
  }
}, { deep: true })

watch(() => props.technicalData, async () => {
  if (isInitialized.value) {
    await updateChart()
  }
}, { deep: true })

watch(selectedIndicators, async () => {
  if (isInitialized.value) {
    await updateChart()
  }
}, { deep: true })

onUnmounted(() => {
  if (resizeTimeout) {
    clearTimeout(resizeTimeout)
  }

  if (chart.value) {
    chart.value.off('legendselectchanged', handleLegendSelectChanged)
    chart.value.dispose()
    chart.value = null
  }

  window.removeEventListener('resize', handleResize)
})
</script>