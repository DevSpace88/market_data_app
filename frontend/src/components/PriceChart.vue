<template>
  <div class="bg-card rounded-lg shadow p-6">
    <div class="h-[700px]" ref="chartRef"></div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, onUnmounted, nextTick } from 'vue'
import * as echarts from 'echarts'

const INDICATOR_NAMES = {
  KLINE: 'Candlesticks',
  MA20: '20 MA',
  MA50: '50 MA',
  BB_UPPER: 'BB Top',
  BB_LOWER: 'BB Bot',
  VOLUME: 'Volume'
}

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
  [INDICATOR_NAMES.KLINE]: true,
  [INDICATOR_NAMES.MA20]: true,
  [INDICATOR_NAMES.MA50]: true,
  [INDICATOR_NAMES.BB_UPPER]: true,
  [INDICATOR_NAMES.BB_LOWER]: true,
  [INDICATOR_NAMES.VOLUME]: true
})

const formatVolume = (value) => {
  if (value >= 1000000) return `${(value / 1000000).toFixed(1)}M`
  if (value >= 1000) return `${(value / 1000).toFixed(1)}K`
  return value.toString()
}

const getIndicatorColor = (indicator) => {
  const colors = {
    [INDICATOR_NAMES.KLINE]: '#000000',
    [INDICATOR_NAMES.MA20]: '#2196F3',
    [INDICATOR_NAMES.MA50]: '#FF9800',
    [INDICATOR_NAMES.BB_UPPER]: '#4CAF50',
    [INDICATOR_NAMES.BB_LOWER]: '#4CAF50',
    [INDICATOR_NAMES.VOLUME]: '#888888'
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
      updateChart()
    }
  } catch (error) {
    console.error('Legend change error:', error)
  }
}

const getLegendData = () => [
  {
    name: INDICATOR_NAMES.KLINE,
    icon: 'path://M0,0 L0,10 M2,3 L2,7 M4,2 L4,8'
  },
  {
    name: INDICATOR_NAMES.MA20,
    icon: 'line'
  },
  {
    name: INDICATOR_NAMES.MA50,
    icon: 'line'
  },
  {
    name: INDICATOR_NAMES.BB_UPPER,
    icon: 'line'
  },
  {
    name: INDICATOR_NAMES.BB_LOWER,
    icon: 'line'
  },
  {
    name: INDICATOR_NAMES.VOLUME,
    icon: 'roundRect'
  }
]

const initChart = async () => {
  try {
    if (!chartRef.value) return

    if (chart.value) {
      chart.value.off('legendselectchanged', handleLegendSelectChanged)
      chart.value.dispose()
      chart.value = null
    }

    await nextTick()

    chart.value = echarts.init(chartRef.value)
    chart.value.on('legendselectchanged', handleLegendSelectChanged)

    await nextTick()
    isInitialized.value = true

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

    // const bbSeries = [
    //   { name: INDICATOR_NAMES.BB_UPPER, key: 'bb_upper' },
    //   { name: INDICATOR_NAMES.BB_LOWER, key: 'bb_lower' }
    // ].map(({ name, key }) => ({
    //   name,
    //   type: 'line',
    //   data: props.data.map(item => {
    //     const value = props.technicalData?.historical?.[item.timestamp]?.[key]
    //     return value ? [
    //       new Date(item.timestamp).getTime(),
    //       value
    //     ] : null
    //   }).filter(item => item !== null),
    //   show: selectedIndicators.value[name],
    //   smooth: true,
    //   lineStyle: {
    //     opacity: 0.8,
    //     width: 2,
    //     type: 'dashed',
    //     color: getIndicatorColor(name)
    //   },
    //   symbol: 'none'
    // }))

//   const bbSeries = ['BB_UPPER', 'BB_LOWER'].map(band => {
//   const indicatorKey = band === 'BB_UPPER' ? 'bb_upper' : 'bb_lower'
//   return {
//     name: INDICATOR_NAMES[band],
//     type: 'line',
//     data: props.data.map(item => {
//       // Versuche zuerst historical data, dann current
//       let value = props.technicalData?.historical?.[item.timestamp]?.[indicatorKey]
//       if (value === undefined) {
//         value = props.technicalData?.current?.[indicatorKey]
//       }
//       return [
//         new Date(item.timestamp).getTime(),
//         value
//       ]
//     }).filter(item => item[1] !== undefined),
//     smooth: true,
//     lineStyle: {
//       opacity: 0.8,
//       width: 2,
//       type: 'dashed',
//       color: getIndicatorColor(band)
//     },
//     symbol: 'none',
//     z: 1  // Legt die Bollinger Bands unter die Kerzen
//   }
// })


    const bbSeries = ['BB_UPPER', 'BB_LOWER'].map(band => {
  const indicatorKey = band === 'BB_UPPER' ? 'bb_upper' : 'bb_lower';
  return {
    name: INDICATOR_NAMES[band],
    type: 'line',
    data: props.data.map(item => {
      let value = props.technicalData?.historical?.[item.timestamp]?.[indicatorKey];
      if (value === undefined) {
        value = props.technicalData?.current?.[indicatorKey];
      }
      console.log(`Bollinger Band (${band}) for timestamp ${item.timestamp}: `, value);
      return [
        new Date(item.timestamp).getTime(),
        value
      ];
    }).filter(item => item[1] !== undefined),
    smooth: true,
    lineStyle: {
      opacity: 0.8,
      width: 2,
      type: 'dashed',
      color: getIndicatorColor(band)
    },
    symbol: 'none',
    z: 1
  };
});

    const option = {
      animation: false,
      legend: {
        show: true,
        top: '2%',
        left: 'center',
        itemGap: 25,
        itemWidth: 25,
        itemHeight: 14,
        textStyle: {
          fontSize: 12,
          color: '#333',
          fontWeight: 500
        },
        selected: selectedIndicators.value,
        data: getLegendData(),
        emphasis: {
          textStyle: {
            fontWeight: 'bold'
          }
        },
        selectedMode: true
      },
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'cross'
        }
      },
      grid: [{
        left: '6%',
        right: '6%',
        height: '70%',
        top: '12%',
        containLabel: true
      }, {
        left: '6%',
        right: '6%',
        top: '82%',
        height: '12%',
        containLabel: true
      }],
      xAxis: [{
        type: 'time',
        boundaryGap: false,
        axisLine: { onZero: false },
        splitLine: { show: false },
        min: 'dataMin',
        max: 'dataMax',
        axisLabel: {
          formatter: value => new Date(value).toLocaleDateString(),
          hideOverlap: true
        }
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
        splitLine: {
          show: true,
          lineStyle: {
            color: '#f0f0f0'
          }
        },
        position: 'right',
        axisLabel: {
          formatter: value => `$${value.toFixed(2)}`,
          inside: false,
          margin: 10
        }
      }, {
        scale: true,
        gridIndex: 1,
        splitNumber: 2,
        position: 'right',
        axisLabel: {
          formatter: formatVolume,
          inside: false,
          margin: 10
        }
      }],
      series: [
        {
          name: INDICATOR_NAMES.KLINE,
          type: 'candlestick',
          data: priceData,
          show: selectedIndicators.value[INDICATOR_NAMES.KLINE],
          itemStyle: {
            color: '#ef5350',
            color0: '#26a69a',
            borderColor: '#ef5350',
            borderColor0: '#26a69a'
          }
        },
        {
          name: INDICATOR_NAMES.MA20,
          type: 'line',
          data: ma20Data,
          show: selectedIndicators.value[INDICATOR_NAMES.MA20],
          smooth: true,
          lineStyle: {
            opacity: 0.8,
            width: 2,
            color: getIndicatorColor(INDICATOR_NAMES.MA20)
          },
          symbol: 'none'
        },
        {
          name: INDICATOR_NAMES.MA50,
          type: 'line',
          data: ma50Data,
          show: selectedIndicators.value[INDICATOR_NAMES.MA50],
          smooth: true,
          lineStyle: {
            opacity: 0.8,
            width: 2,
            color: getIndicatorColor(INDICATOR_NAMES.MA50)
          },
          symbol: 'none'
        },
        ...bbSeries,
        {
          name: INDICATOR_NAMES.VOLUME,
          type: 'bar',
          xAxisIndex: 1,
          yAxisIndex: 1,
          data: volumeData,
          show: selectedIndicators.value[INDICATOR_NAMES.VOLUME],
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
