<!--&lt;!&ndash;<template>&ndash;&gt;-->
<!--&lt;!&ndash;  <div class="bg-card rounded-lg shadow p-4">&ndash;&gt;-->
<!--&lt;!&ndash;    <div class="h-[500px]" ref="chartRef"></div>&ndash;&gt;-->
<!--&lt;!&ndash;  </div>&ndash;&gt;-->
<!--&lt;!&ndash;</template>&ndash;&gt;-->

<!--&lt;!&ndash;<script setup>&ndash;&gt;-->
<!--&lt;!&ndash;import { ref, onMounted, watch, onUnmounted } from 'vue'&ndash;&gt;-->
<!--&lt;!&ndash;import * as echarts from 'echarts'&ndash;&gt;-->

<!--&lt;!&ndash;const props = defineProps({&ndash;&gt;-->
<!--&lt;!&ndash;  data: {&ndash;&gt;-->
<!--&lt;!&ndash;    type: Array,&ndash;&gt;-->
<!--&lt;!&ndash;    default: () => []&ndash;&gt;-->
<!--&lt;!&ndash;  },&ndash;&gt;-->
<!--&lt;!&ndash;  indicators: {&ndash;&gt;-->
<!--&lt;!&ndash;    type: Array,&ndash;&gt;-->
<!--&lt;!&ndash;    default: () => []&ndash;&gt;-->
<!--&lt;!&ndash;  },&ndash;&gt;-->
<!--&lt;!&ndash;  technicalData: {  // Dies haben wir vorher nicht definiert&ndash;&gt;-->
<!--&lt;!&ndash;    type: Object,&ndash;&gt;-->
<!--&lt;!&ndash;    default: () => ({})&ndash;&gt;-->
<!--&lt;!&ndash;  }&ndash;&gt;-->
<!--&lt;!&ndash;})&ndash;&gt;-->

<!--&lt;!&ndash;const chartRef = ref(null)&ndash;&gt;-->
<!--&lt;!&ndash;const chart = ref(null)&ndash;&gt;-->

<!--&lt;!&ndash;const formatVolume = (value) => {&ndash;&gt;-->
<!--&lt;!&ndash;  if (value >= 1000000) return `${(value / 1000000).toFixed(1)}M`&ndash;&gt;-->
<!--&lt;!&ndash;  if (value >= 1000) return `${(value / 1000).toFixed(1)}K`&ndash;&gt;-->
<!--&lt;!&ndash;  return value.toString()&ndash;&gt;-->
<!--&lt;!&ndash;}&ndash;&gt;-->

<!--&lt;!&ndash;const getIndicatorColor = (indicator) => {&ndash;&gt;-->
<!--&lt;!&ndash;  const colors = {&ndash;&gt;-->
<!--&lt;!&ndash;    sma_20: '#7cb5ec',&ndash;&gt;-->
<!--&lt;!&ndash;    sma_50: '#434348',&ndash;&gt;-->
<!--&lt;!&ndash;    bb_upper: '#90ed7d',&ndash;&gt;-->
<!--&lt;!&ndash;    bb_middle: '#8085e9',&ndash;&gt;-->
<!--&lt;!&ndash;    bb_lower: '#90ed7d',&ndash;&gt;-->
<!--&lt;!&ndash;    rsi: '#f45b5b',&ndash;&gt;-->
<!--&lt;!&ndash;    macd: '#2196F3',&ndash;&gt;-->
<!--&lt;!&ndash;    'macd_signal': '#FF5722'&ndash;&gt;-->
<!--&lt;!&ndash;  }&ndash;&gt;-->
<!--&lt;!&ndash;  return colors[indicator.toLowerCase()] || '#000000'&ndash;&gt;-->
<!--&lt;!&ndash;}&ndash;&gt;-->

<!--&lt;!&ndash;const calculateMAValues = (data, period) => {&ndash;&gt;-->
<!--&lt;!&ndash;  return data.map((item, index) => {&ndash;&gt;-->
<!--&lt;!&ndash;    if (index < period - 1) return null&ndash;&gt;-->
<!--&lt;!&ndash;    const slice = data.slice(index - period + 1, index + 1)&ndash;&gt;-->
<!--&lt;!&ndash;    const sum = slice.reduce((acc, val) => acc + val.close, 0)&ndash;&gt;-->
<!--&lt;!&ndash;    return {&ndash;&gt;-->
<!--&lt;!&ndash;      name: item.timestamp,&ndash;&gt;-->
<!--&lt;!&ndash;      value: [&ndash;&gt;-->
<!--&lt;!&ndash;        new Date(item.timestamp).getTime(),&ndash;&gt;-->
<!--&lt;!&ndash;        sum / period&ndash;&gt;-->
<!--&lt;!&ndash;      ]&ndash;&gt;-->
<!--&lt;!&ndash;    }&ndash;&gt;-->
<!--&lt;!&ndash;  }).filter(item => item !== null)&ndash;&gt;-->
<!--&lt;!&ndash;}&ndash;&gt;-->

<!--&lt;!&ndash;const initChart = () => {&ndash;&gt;-->
<!--&lt;!&ndash;  if (!chartRef.value) return&ndash;&gt;-->
<!--&lt;!&ndash;  chart.value = echarts.init(chartRef.value)&ndash;&gt;-->
<!--&lt;!&ndash;  updateChart()&ndash;&gt;-->
<!--&lt;!&ndash;}&ndash;&gt;-->

<!--&lt;!&ndash;const updateChart = () => {&ndash;&gt;-->
<!--&lt;!&ndash;  if (!chart.value || !props.data.length) return&ndash;&gt;-->

<!--&lt;!&ndash;  console.log('Technical Data structure:', JSON.stringify(props.technicalData, null, 2))&ndash;&gt;-->
<!--&lt;!&ndash;  console.log('First data point structure:', JSON.stringify(props.data[0], null, 2))&ndash;&gt;-->

<!--&lt;!&ndash;  const priceData = props.data.map(item => ({&ndash;&gt;-->
<!--&lt;!&ndash;    name: new Date(item.timestamp).toISOString(),&ndash;&gt;-->
<!--&lt;!&ndash;    value: [&ndash;&gt;-->
<!--&lt;!&ndash;      new Date(item.timestamp).getTime(),&ndash;&gt;-->
<!--&lt;!&ndash;      Number(item.close),&ndash;&gt;-->
<!--&lt;!&ndash;      Number(item.open),&ndash;&gt;-->
<!--&lt;!&ndash;      Number(item.low),&ndash;&gt;-->
<!--&lt;!&ndash;      Number(item.high)&ndash;&gt;-->
<!--&lt;!&ndash;    ]&ndash;&gt;-->
<!--&lt;!&ndash;  }))&ndash;&gt;-->

<!--&lt;!&ndash;  const volumeData = props.data.map(item => ({&ndash;&gt;-->
<!--&lt;!&ndash;    name: new Date(item.timestamp).toISOString(),&ndash;&gt;-->
<!--&lt;!&ndash;    value: [&ndash;&gt;-->
<!--&lt;!&ndash;      new Date(item.timestamp).getTime(),&ndash;&gt;-->
<!--&lt;!&ndash;      Number(item.volume),&ndash;&gt;-->
<!--&lt;!&ndash;      Number(item.close) > Number(item.open) ? 1 : -1&ndash;&gt;-->
<!--&lt;!&ndash;    ]&ndash;&gt;-->
<!--&lt;!&ndash;  }))&ndash;&gt;-->

<!--&lt;!&ndash;  // MA Berechnungen&ndash;&gt;-->
<!--&lt;!&ndash;  const ma20Data = calculateMAValues(props.data, 20)&ndash;&gt;-->
<!--&lt;!&ndash;  const ma50Data = calculateMAValues(props.data, 50)&ndash;&gt;-->

<!--&lt;!&ndash;const getHistoricalIndicators = (indicator) => {&ndash;&gt;-->
<!--&lt;!&ndash;  return props.data.map((item, index) => [&ndash;&gt;-->
<!--&lt;!&ndash;    new Date(item.timestamp).getTime(),&ndash;&gt;-->
<!--&lt;!&ndash;    item[indicator] ||&ndash;&gt;-->
<!--&lt;!&ndash;    props.technicalData?.historical?.[item.timestamp]?.[indicator] ||&ndash;&gt;-->
<!--&lt;!&ndash;    null&ndash;&gt;-->
<!--&lt;!&ndash;  ]).filter(item => item[1] !== null)&ndash;&gt;-->
<!--&lt;!&ndash;}&ndash;&gt;-->

<!--&lt;!&ndash;// Bollinger Bands nur hinzufügen wenn current Werte existieren&ndash;&gt;-->
<!--&lt;!&ndash;const bbSeries = props.technicalData?.current ? ['bb_upper', 'bb_middle', 'bb_lower']&ndash;&gt;-->
<!--&lt;!&ndash;  .filter(band => props.technicalData.current[band] !== undefined)&ndash;&gt;-->
<!--&lt;!&ndash;  .map(band => ({&ndash;&gt;-->
<!--&lt;!&ndash;    name: band.toUpperCase(),&ndash;&gt;-->
<!--&lt;!&ndash;    type: 'line',&ndash;&gt;-->
<!--&lt;!&ndash;    data: props.data.map(item => [&ndash;&gt;-->
<!--&lt;!&ndash;      new Date(item.timestamp).getTime(),&ndash;&gt;-->
<!--&lt;!&ndash;      props.technicalData.current[band]  // Konstanter Wert für die ganze Linie&ndash;&gt;-->
<!--&lt;!&ndash;    ]),&ndash;&gt;-->
<!--&lt;!&ndash;    smooth: true,&ndash;&gt;-->
<!--&lt;!&ndash;    lineStyle: {&ndash;&gt;-->
<!--&lt;!&ndash;      opacity: 0.5,&ndash;&gt;-->
<!--&lt;!&ndash;      width: 1,&ndash;&gt;-->
<!--&lt;!&ndash;      type: 'dashed',&ndash;&gt;-->
<!--&lt;!&ndash;      color: getIndicatorColor(band)&ndash;&gt;-->
<!--&lt;!&ndash;    },&ndash;&gt;-->
<!--&lt;!&ndash;    symbol: 'none'&ndash;&gt;-->
<!--&lt;!&ndash;  })) : []&ndash;&gt;-->

<!--&lt;!&ndash;  const option = {&ndash;&gt;-->
<!--&lt;!&ndash;    animation: false,&ndash;&gt;-->
<!--&lt;!&ndash;    tooltip: {&ndash;&gt;-->
<!--&lt;!&ndash;      trigger: 'axis',&ndash;&gt;-->
<!--&lt;!&ndash;      axisPointer: {&ndash;&gt;-->
<!--&lt;!&ndash;        type: 'cross',&ndash;&gt;-->
<!--&lt;!&ndash;        label: {&ndash;&gt;-->
<!--&lt;!&ndash;          backgroundColor: '#1b1b1b'&ndash;&gt;-->
<!--&lt;!&ndash;        }&ndash;&gt;-->
<!--&lt;!&ndash;      },&ndash;&gt;-->
<!--&lt;!&ndash;      formatter: (params) => {&ndash;&gt;-->
<!--&lt;!&ndash;        const date = new Date(params[0].value[0]).toLocaleString()&ndash;&gt;-->
<!--&lt;!&ndash;        let result = `<div style="font-weight: bold; margin-bottom: 5px">${date}</div>`&ndash;&gt;-->

<!--&lt;!&ndash;        params.forEach(param => {&ndash;&gt;-->
<!--&lt;!&ndash;          if (param.seriesName === 'K-Line') {&ndash;&gt;-->
<!--&lt;!&ndash;            const [time, close, open, low, high] = param.value&ndash;&gt;-->
<!--&lt;!&ndash;            result += `<div style="margin: 5px 0">&ndash;&gt;-->
<!--&lt;!&ndash;              <div>Open: $${open.toFixed(2)}</div>&ndash;&gt;-->
<!--&lt;!&ndash;              <div>High: $${high.toFixed(2)}</div>&ndash;&gt;-->
<!--&lt;!&ndash;              <div>Low: $${low.toFixed(2)}</div>&ndash;&gt;-->
<!--&lt;!&ndash;              <div>Close: $${close.toFixed(2)}</div>&ndash;&gt;-->
<!--&lt;!&ndash;            </div>`&ndash;&gt;-->
<!--&lt;!&ndash;          } else if (param.seriesName === 'Volume') {&ndash;&gt;-->
<!--&lt;!&ndash;            result += `<div>${param.marker}Volume: ${formatVolume(param.value[1])}</div>`&ndash;&gt;-->
<!--&lt;!&ndash;          } else {&ndash;&gt;-->
<!--&lt;!&ndash;            result += `<div>${param.marker}${param.seriesName}: $${param.value[1]?.toFixed(2)}</div>`&ndash;&gt;-->
<!--&lt;!&ndash;          }&ndash;&gt;-->
<!--&lt;!&ndash;        })&ndash;&gt;-->
<!--&lt;!&ndash;        return result&ndash;&gt;-->
<!--&lt;!&ndash;      }&ndash;&gt;-->
<!--&lt;!&ndash;    },&ndash;&gt;-->
<!--&lt;!&ndash;    axisPointer: {&ndash;&gt;-->
<!--&lt;!&ndash;      link: { xAxisIndex: 'all' }&ndash;&gt;-->
<!--&lt;!&ndash;    },&ndash;&gt;-->
<!--&lt;!&ndash;    legend: {&ndash;&gt;-->
<!--&lt;!&ndash;      data: ['K-Line', 'MA20', 'MA50', 'BB_UPPER', 'BB_MIDDLE', 'BB_LOWER', 'Volume'],&ndash;&gt;-->
<!--&lt;!&ndash;      selected: {&ndash;&gt;-->
<!--&lt;!&ndash;        'Volume': true,&ndash;&gt;-->
<!--&lt;!&ndash;        'MA20': true,&ndash;&gt;-->
<!--&lt;!&ndash;        'MA50': true,&ndash;&gt;-->
<!--&lt;!&ndash;        'BB_UPPER': true,  // Auf true gesetzt&ndash;&gt;-->
<!--&lt;!&ndash;        'BB_MIDDLE': true, // Auf true gesetzt&ndash;&gt;-->
<!--&lt;!&ndash;        'BB_LOWER': true,  // Auf true gesetzt&ndash;&gt;-->
<!--&lt;!&ndash;        'K-Line': true&ndash;&gt;-->
<!--&lt;!&ndash;      }&ndash;&gt;-->
<!--&lt;!&ndash;    },&ndash;&gt;-->
<!--&lt;!&ndash;    grid: [{&ndash;&gt;-->
<!--&lt;!&ndash;      left: '10%',&ndash;&gt;-->
<!--&lt;!&ndash;      right: '10%',&ndash;&gt;-->
<!--&lt;!&ndash;      height: '60%'&ndash;&gt;-->
<!--&lt;!&ndash;    }, {&ndash;&gt;-->
<!--&lt;!&ndash;      left: '10%',&ndash;&gt;-->
<!--&lt;!&ndash;      right: '10%',&ndash;&gt;-->
<!--&lt;!&ndash;      top: '75%',&ndash;&gt;-->
<!--&lt;!&ndash;      height: '20%'&ndash;&gt;-->
<!--&lt;!&ndash;    }],&ndash;&gt;-->
<!--&lt;!&ndash;    xAxis: [{&ndash;&gt;-->
<!--&lt;!&ndash;      type: 'time',&ndash;&gt;-->
<!--&lt;!&ndash;      boundaryGap: false,&ndash;&gt;-->
<!--&lt;!&ndash;      axisLine: { onZero: false },&ndash;&gt;-->
<!--&lt;!&ndash;      splitLine: { show: false },&ndash;&gt;-->
<!--&lt;!&ndash;      min: 'dataMin',&ndash;&gt;-->
<!--&lt;!&ndash;      max: 'dataMax',&ndash;&gt;-->
<!--&lt;!&ndash;      axisLabel: {&ndash;&gt;-->
<!--&lt;!&ndash;        formatter: (value) => {&ndash;&gt;-->
<!--&lt;!&ndash;          return new Date(value).toLocaleDateString()&ndash;&gt;-->
<!--&lt;!&ndash;        }&ndash;&gt;-->
<!--&lt;!&ndash;      }&ndash;&gt;-->
<!--&lt;!&ndash;    }, {&ndash;&gt;-->
<!--&lt;!&ndash;      type: 'time',&ndash;&gt;-->
<!--&lt;!&ndash;      gridIndex: 1,&ndash;&gt;-->
<!--&lt;!&ndash;      boundaryGap: false,&ndash;&gt;-->
<!--&lt;!&ndash;      axisLine: { onZero: false },&ndash;&gt;-->
<!--&lt;!&ndash;      axisTick: { show: false },&ndash;&gt;-->
<!--&lt;!&ndash;      splitLine: { show: false },&ndash;&gt;-->
<!--&lt;!&ndash;      axisLabel: { show: false },&ndash;&gt;-->
<!--&lt;!&ndash;      min: 'dataMin',&ndash;&gt;-->
<!--&lt;!&ndash;      max: 'dataMax'&ndash;&gt;-->
<!--&lt;!&ndash;    }],&ndash;&gt;-->
<!--&lt;!&ndash;    yAxis: [{&ndash;&gt;-->
<!--&lt;!&ndash;      type: 'value',&ndash;&gt;-->
<!--&lt;!&ndash;      position: 'left',&ndash;&gt;-->
<!--&lt;!&ndash;      splitLine: { show: true },&ndash;&gt;-->
<!--&lt;!&ndash;      axisLabel: {&ndash;&gt;-->
<!--&lt;!&ndash;        formatter: (value) => `$${value.toFixed(2)}`,&ndash;&gt;-->
<!--&lt;!&ndash;        margin: 16&ndash;&gt;-->
<!--&lt;!&ndash;      }&ndash;&gt;-->
<!--&lt;!&ndash;    }, {&ndash;&gt;-->
<!--&lt;!&ndash;      gridIndex: 1,&ndash;&gt;-->
<!--&lt;!&ndash;      position: 'left',&ndash;&gt;-->
<!--&lt;!&ndash;      splitLine: { show: false },&ndash;&gt;-->
<!--&lt;!&ndash;      axisLabel: {&ndash;&gt;-->
<!--&lt;!&ndash;        formatter: formatVolume,&ndash;&gt;-->
<!--&lt;!&ndash;        margin: 16&ndash;&gt;-->
<!--&lt;!&ndash;      }&ndash;&gt;-->
<!--&lt;!&ndash;    }],&ndash;&gt;-->
<!--&lt;!&ndash;  dataZoom: [{&ndash;&gt;-->
<!--&lt;!&ndash;  type: 'inside',&ndash;&gt;-->
<!--&lt;!&ndash;  xAxisIndex: [0, 1],&ndash;&gt;-->
<!--&lt;!&ndash;  start: 0,&ndash;&gt;-->
<!--&lt;!&ndash;  end: 100,&ndash;&gt;-->
<!--&lt;!&ndash;  zoomLock: false&ndash;&gt;-->
<!--&lt;!&ndash;}, {&ndash;&gt;-->
<!--&lt;!&ndash;  show: true,&ndash;&gt;-->
<!--&lt;!&ndash;  xAxisIndex: [0, 1],&ndash;&gt;-->
<!--&lt;!&ndash;  type: 'slider',&ndash;&gt;-->
<!--&lt;!&ndash;  bottom: '0%',&ndash;&gt;-->
<!--&lt;!&ndash;  start: 0,&ndash;&gt;-->
<!--&lt;!&ndash;  end: 100,&ndash;&gt;-->
<!--&lt;!&ndash;  handleSize: 20,  // macht die Griffe größer&ndash;&gt;-->
<!--&lt;!&ndash;  handleStyle: {&ndash;&gt;-->
<!--&lt;!&ndash;    color: '#7AB8FF'&ndash;&gt;-->
<!--&lt;!&ndash;  }&ndash;&gt;-->
<!--&lt;!&ndash;}],&ndash;&gt;-->
<!--&lt;!&ndash;    series: [&ndash;&gt;-->
<!--&lt;!&ndash;  {&ndash;&gt;-->
<!--&lt;!&ndash;    name: 'K-Line',&ndash;&gt;-->
<!--&lt;!&ndash;    type: 'candlestick',&ndash;&gt;-->
<!--&lt;!&ndash;    data: priceData.map(item => item.value),&ndash;&gt;-->
<!--&lt;!&ndash;    itemStyle: {&ndash;&gt;-->
<!--&lt;!&ndash;      color: '#ef5350',&ndash;&gt;-->
<!--&lt;!&ndash;      color0: '#26a69a',&ndash;&gt;-->
<!--&lt;!&ndash;      borderColor: '#ef5350',&ndash;&gt;-->
<!--&lt;!&ndash;      borderColor0: '#26a69a'&ndash;&gt;-->
<!--&lt;!&ndash;    }&ndash;&gt;-->
<!--&lt;!&ndash;  },&ndash;&gt;-->
<!--&lt;!&ndash;  {&ndash;&gt;-->
<!--&lt;!&ndash;    name: 'MA20',&ndash;&gt;-->
<!--&lt;!&ndash;    type: 'line',&ndash;&gt;-->
<!--&lt;!&ndash;    data: ma20Data,&ndash;&gt;-->
<!--&lt;!&ndash;    smooth: true,&ndash;&gt;-->
<!--&lt;!&ndash;    lineStyle: {&ndash;&gt;-->
<!--&lt;!&ndash;      opacity: 0.5,&ndash;&gt;-->
<!--&lt;!&ndash;      width: 1.5,&ndash;&gt;-->
<!--&lt;!&ndash;      color: '#7cb5ec'&ndash;&gt;-->
<!--&lt;!&ndash;    },&ndash;&gt;-->
<!--&lt;!&ndash;    symbol: 'none'&ndash;&gt;-->
<!--&lt;!&ndash;  },&ndash;&gt;-->
<!--&lt;!&ndash;  {&ndash;&gt;-->
<!--&lt;!&ndash;    name: 'MA50',&ndash;&gt;-->
<!--&lt;!&ndash;    type: 'line',&ndash;&gt;-->
<!--&lt;!&ndash;    data: ma50Data,&ndash;&gt;-->
<!--&lt;!&ndash;    smooth: true,&ndash;&gt;-->
<!--&lt;!&ndash;    lineStyle: {&ndash;&gt;-->
<!--&lt;!&ndash;      opacity: 0.5,&ndash;&gt;-->
<!--&lt;!&ndash;      width: 1.5,&ndash;&gt;-->
<!--&lt;!&ndash;      color: '#434348'&ndash;&gt;-->
<!--&lt;!&ndash;    },&ndash;&gt;-->
<!--&lt;!&ndash;    symbol: 'none'&ndash;&gt;-->
<!--&lt;!&ndash;  },&ndash;&gt;-->
<!--&lt;!&ndash;  {&ndash;&gt;-->
<!--&lt;!&ndash;    name: 'Volume',&ndash;&gt;-->
<!--&lt;!&ndash;    type: 'bar',&ndash;&gt;-->
<!--&lt;!&ndash;    xAxisIndex: 1,&ndash;&gt;-->
<!--&lt;!&ndash;    yAxisIndex: 1,&ndash;&gt;-->
<!--&lt;!&ndash;    data: volumeData.map(item => ({&ndash;&gt;-->
<!--&lt;!&ndash;      value: [item.value[0], item.value[1]],&ndash;&gt;-->
<!--&lt;!&ndash;      itemStyle: {&ndash;&gt;-->
<!--&lt;!&ndash;        color: item.value[2] > 0 ? '#26a69a' : '#ef5350'&ndash;&gt;-->
<!--&lt;!&ndash;      }&ndash;&gt;-->
<!--&lt;!&ndash;    }))&ndash;&gt;-->
<!--&lt;!&ndash;  },&ndash;&gt;-->
<!--&lt;!&ndash;  ...bbSeries,&ndash;&gt;-->
<!--&lt;!&ndash;    ]&ndash;&gt;-->
<!--&lt;!&ndash;  }&ndash;&gt;-->

<!--&lt;!&ndash;  chart.value.setOption(option, true)&ndash;&gt;-->
<!--&lt;!&ndash;}&ndash;&gt;-->

<!--&lt;!&ndash;onMounted(() => {&ndash;&gt;-->
<!--&lt;!&ndash;  initChart()&ndash;&gt;-->
<!--&lt;!&ndash;  window.addEventListener('resize', () => chart.value?.resize())&ndash;&gt;-->
<!--&lt;!&ndash;})&ndash;&gt;-->

<!--&lt;!&ndash;watch(() => props.data, updateChart, { deep: true })&ndash;&gt;-->
<!--&lt;!&ndash;watch(() => props.indicators, updateChart)&ndash;&gt;-->

<!--&lt;!&ndash;onUnmounted(() => {&ndash;&gt;-->
<!--&lt;!&ndash;  window.removeEventListener('resize', () => chart.value?.resize())&ndash;&gt;-->
<!--&lt;!&ndash;  chart.value?.dispose()&ndash;&gt;-->
<!--&lt;!&ndash;})&ndash;&gt;-->
<!--&lt;!&ndash;</script>&ndash;&gt;-->


<!--<template>-->
<!--  <div class="bg-card rounded-lg shadow p-4">-->
<!--    <div class="h-[700px]" ref="chartRef"></div>-->
<!--  </div>-->
<!--</template>-->

<!--<script setup>-->
<!--import { ref, onMounted, watch, onUnmounted } from 'vue'-->
<!--import * as echarts from 'echarts'-->

<!--const props = defineProps({-->
<!--  data: {-->
<!--    type: Array,-->
<!--    default: () => []-->
<!--  },-->
<!--  indicators: {-->
<!--    type: Array,-->
<!--    default: () => []-->
<!--  },-->
<!--  technicalData: {-->
<!--    type: Object,-->
<!--    default: () => ({})-->
<!--  }-->
<!--})-->

<!--const chartRef = ref(null)-->
<!--const chart = ref(null)-->

<!--const formatVolume = (value) => {-->
<!--  if (value >= 1000000) return `${(value / 1000000).toFixed(1)}M`-->
<!--  if (value >= 1000) return `${(value / 1000).toFixed(1)}K`-->
<!--  return value.toString()-->
<!--}-->

<!--const getIndicatorColor = (indicator) => {-->
<!--  const colors = {-->
<!--    sma_20: '#7cb5ec',-->
<!--    sma_50: '#434348',-->
<!--    bb_upper: '#90ed7d',-->
<!--    bb_middle: '#8085e9',-->
<!--    bb_lower: '#90ed7d',-->
<!--    rsi: '#f45b5b',-->
<!--    macd: '#2196F3',-->
<!--    'macd_signal': '#FF5722'-->
<!--  }-->
<!--  return colors[indicator.toLowerCase()] || '#000000'-->
<!--}-->

<!--const calculateMAValues = (data, period) => {-->
<!--  return data.map((item, index) => {-->
<!--    if (index < period - 1) return null-->
<!--    const slice = data.slice(index - period + 1, index + 1)-->
<!--    const sum = slice.reduce((acc, val) => acc + val.close, 0)-->
<!--    return {-->
<!--      name: item.timestamp,-->
<!--      value: [-->
<!--        new Date(item.timestamp).getTime(),-->
<!--        sum / period-->
<!--      ]-->
<!--    }-->
<!--  }).filter(item => item !== null)-->
<!--}-->

<!--const initChart = () => {-->
<!--  if (!chartRef.value) return-->
<!--  chart.value = echarts.init(chartRef.value)-->
<!--  updateChart()-->

<!--  // Doppelklick zum Reset-->
<!--  chartRef.value.addEventListener('dblclick', () => {-->
<!--    chart.value.dispatchAction({-->
<!--      type: 'dataZoom',-->
<!--      start: 50,-->
<!--      end: 100-->
<!--    })-->
<!--  })-->
<!--}-->

<!--const updateChart = () => {-->
<!--  if (!chart.value || !props.data.length) return-->

<!--  console.log('Technical Data structure:', JSON.stringify(props.technicalData, null, 2))-->
<!--  console.log('First data point structure:', JSON.stringify(props.data[0], null, 2))-->

<!--  const priceData = props.data.map(item => ({-->
<!--    name: new Date(item.timestamp).toISOString(),-->
<!--    value: [-->
<!--      new Date(item.timestamp).getTime(),-->
<!--      Number(item.close),-->
<!--      Number(item.open),-->
<!--      Number(item.low),-->
<!--      Number(item.high)-->
<!--    ]-->
<!--  }))-->

<!--  const volumeData = props.data.map(item => ({-->
<!--    name: new Date(item.timestamp).toISOString(),-->
<!--    value: [-->
<!--      new Date(item.timestamp).getTime(),-->
<!--      Number(item.volume),-->
<!--      Number(item.close) > Number(item.open) ? 1 : -1-->
<!--    ]-->
<!--  }))-->

<!--  // MA Berechnungen-->
<!--  const ma20Data = calculateMAValues(props.data, 20)-->
<!--  const ma50Data = calculateMAValues(props.data, 50)-->

<!--  const getHistoricalIndicators = (indicator) => {-->
<!--    return props.data.map((item, index) => [-->
<!--      new Date(item.timestamp).getTime(),-->
<!--      item[indicator] ||-->
<!--      props.technicalData?.historical?.[item.timestamp]?.[indicator] ||-->
<!--      null-->
<!--    ]).filter(item => item[1] !== null)-->
<!--  }-->

<!--  // Bollinger Bands nur hinzufügen wenn current Werte existieren-->
<!--  const bbSeries = props.technicalData?.current ? ['bb_upper', 'bb_middle', 'bb_lower']-->
<!--    .filter(band => props.technicalData.current[band] !== undefined)-->
<!--    .map(band => ({-->
<!--      name: band.toUpperCase(),-->
<!--      type: 'line',-->
<!--      data: props.data.map(item => [-->
<!--        new Date(item.timestamp).getTime(),-->
<!--        props.technicalData.current[band]  // Konstanter Wert für die ganze Linie-->
<!--      ]),-->
<!--      smooth: true,-->
<!--      lineStyle: {-->
<!--        opacity: 0.5,-->
<!--        width: 1,-->
<!--        type: 'dashed',-->
<!--        color: getIndicatorColor(band)-->
<!--      },-->
<!--      symbol: 'none'-->
<!--    })) : []-->

<!--  const option = {-->
<!--    animation: false,-->
<!--    tooltip: {-->
<!--      trigger: 'axis',-->
<!--      axisPointer: {-->
<!--        type: 'cross',-->
<!--        label: {-->
<!--          backgroundColor: '#1b1b1b'-->
<!--        }-->
<!--      },-->
<!--      formatter: (params) => {-->
<!--        const date = new Date(params[0].value[0]).toLocaleString()-->
<!--        let result = `<div style="font-weight: bold; margin-bottom: 5px">${date}</div>`-->

<!--        params.forEach(param => {-->
<!--          if (param.seriesName === 'K-Line') {-->
<!--            const [time, close, open, low, high] = param.value-->
<!--            result += `<div style="margin: 5px 0">-->
<!--              <div>Open: $${open.toFixed(2)}</div>-->
<!--              <div>High: $${high.toFixed(2)}</div>-->
<!--              <div>Low: $${low.toFixed(2)}</div>-->
<!--              <div>Close: $${close.toFixed(2)}</div>-->
<!--            </div>`-->
<!--          } else if (param.seriesName === 'Volume') {-->
<!--            result += `<div>${param.marker}Volume: ${formatVolume(param.value[1])}</div>`-->
<!--          } else {-->
<!--            result += `<div>${param.marker}${param.seriesName}: $${param.value[1]?.toFixed(2)}</div>`-->
<!--          }-->
<!--        })-->
<!--        return result-->
<!--      }-->
<!--    },-->
<!--    axisPointer: {-->
<!--      link: { xAxisIndex: 'all' }-->
<!--    },-->
<!--    legend: {-->
<!--      data: ['K-Line', 'MA20', 'MA50', 'BB_UPPER', 'BB_MIDDLE', 'BB_LOWER', 'Volume'],-->
<!--      selected: {-->
<!--        'Volume': true,-->
<!--        'MA20': true,-->
<!--        'MA50': true,-->
<!--        'BB_UPPER': true,-->
<!--        'BB_MIDDLE': true,-->
<!--        'BB_LOWER': true,-->
<!--        'K-Line': true-->
<!--      }-->
<!--    },-->
<!--    toolbox: {-->
<!--      feature: {-->
<!--        dataZoom: {-->
<!--          yAxisIndex: false,-->
<!--          title: {-->
<!--            zoom: 'Zoom',-->
<!--            back: 'Reset'-->
<!--          }-->
<!--        },-->
<!--        restore: { show: true }-->
<!--      },-->
<!--      right: 30,-->
<!--      top: 10-->
<!--    },-->
<!--    grid: [{-->
<!--      left: '10%',-->
<!--      right: '10%',-->
<!--      height: '70%',-->
<!--      top: '5%'-->
<!--    }, {-->
<!--      left: '10%',-->
<!--      right: '10%',-->
<!--      top: '80%',-->
<!--      height: '15%'-->
<!--    }],-->
<!--    xAxis: [{-->
<!--      type: 'time',-->
<!--      boundaryGap: false,-->
<!--      axisLine: { onZero: false },-->
<!--      splitLine: { show: false },-->
<!--      min: 'dataMin',-->
<!--      max: 'dataMax',-->
<!--      axisLabel: {-->
<!--        formatter: (value) => {-->
<!--          return new Date(value).toLocaleDateString()-->
<!--        }-->
<!--      }-->
<!--    }, {-->
<!--      type: 'time',-->
<!--      gridIndex: 1,-->
<!--      boundaryGap: false,-->
<!--      axisLine: { onZero: false },-->
<!--      axisTick: { show: false },-->
<!--      splitLine: { show: false },-->
<!--      axisLabel: { show: false },-->
<!--      min: 'dataMin',-->
<!--      max: 'dataMax'-->
<!--    }],-->
<!--    yAxis: [{-->
<!--      type: 'value',-->
<!--      position: 'left',-->
<!--      splitLine: { show: true },-->
<!--      axisLabel: {-->
<!--        formatter: (value) => `$${value.toFixed(2)}`,-->
<!--        margin: 16-->
<!--      }-->
<!--    }, {-->
<!--      gridIndex: 1,-->
<!--      position: 'left',-->
<!--      splitLine: { show: false },-->
<!--      axisLabel: {-->
<!--        formatter: formatVolume,-->
<!--        margin: 16-->
<!--      }-->
<!--    }],-->
<!--    dataZoom: [{-->
<!--      type: 'inside',-->
<!--      xAxisIndex: [0, 1],-->
<!--      start: 50,-->
<!--      end: 100,-->
<!--      zoomOnMouseWheel: true,-->
<!--      moveOnMouseMove: true,-->
<!--      moveOnMouseWheel: true,-->
<!--      preventDefaultMouseMove: true-->
<!--    }, {-->
<!--      show: true,-->
<!--      xAxisIndex: [0, 1],-->
<!--      type: 'slider',-->
<!--      bottom: '0%',-->
<!--      height: 20,-->
<!--      start: 50,-->
<!--      end: 100,-->
<!--      handleSize: 20,-->
<!--      handleStyle: {-->
<!--        color: '#7AB8FF'-->
<!--      }-->
<!--    }],-->
<!--    series: [-->
<!--      {-->
<!--        name: 'K-Line',-->
<!--        type: 'candlestick',-->
<!--        data: priceData.map(item => item.value),-->
<!--        itemStyle: {-->
<!--          color: '#ef5350',-->
<!--          color0: '#26a69a',-->
<!--          borderColor: '#ef5350',-->
<!--          borderColor0: '#26a69a'-->
<!--        }-->
<!--      },-->
<!--      {-->
<!--        name: 'MA20',-->
<!--        type: 'line',-->
<!--        data: ma20Data,-->
<!--        smooth: true,-->
<!--        lineStyle: {-->
<!--          opacity: 0.5,-->
<!--          width: 1.5,-->
<!--          color: '#7cb5ec'-->
<!--        },-->
<!--        symbol: 'none'-->
<!--      },-->
<!--      {-->
<!--        name: 'MA50',-->
<!--        type: 'line',-->
<!--        data: ma50Data,-->
<!--        smooth: true,-->
<!--        lineStyle: {-->
<!--          opacity: 0.5,-->
<!--          width: 1.5,-->
<!--          color: '#434348'-->
<!--        },-->
<!--        symbol: 'none'-->
<!--      },-->
<!--      {-->
<!--        name: 'Volume',-->
<!--        type: 'bar',-->
<!--        xAxisIndex: 1,-->
<!--        yAxisIndex: 1,-->
<!--        data: volumeData.map(item => ({-->
<!--          value: [item.value[0], item.value[1]],-->
<!--          itemStyle: {-->
<!--            color: item.value[2] > 0 ? '#26a69a' : '#ef5350'-->
<!--          }-->
<!--        }))-->
<!--      },-->
<!--      ...bbSeries-->
<!--    ]-->
<!--  }-->

<!--  chart.value.setOption(option, true)-->
<!--}-->

<!--onMounted(() => {-->
<!--  initChart()-->
<!--  window.addEventListener('resize', () => chart.value?.resize())-->
<!--})-->

<!--watch(() => props.data, updateChart, { deep: true })-->
<!--watch(() => props.indicators, updateChart)-->

<!--onUnmounted(() => {-->
<!--  window.removeEventListener('resize', () => chart.value?.resize())-->
<!--  chart.value?.dispose()-->
<!--})-->
<!--</script>-->


<template>
  <div class="bg-card rounded-lg shadow p-4">
    <div class="h-[700px]" ref="chartRef"></div>
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
    bb_lower: '#90ed7d',
    rsi: '#f45b5b',
    macd: '#2196F3',
    'macd_signal': '#FF5722'
  }
  return colors[indicator.toLowerCase()] || '#000000'
}

const calculateMAValues = (data, period) => {
  return data.map((item, index) => {
    if (index < period - 1) return null
    const slice = data.slice(index - period + 1, index + 1)
    const sum = slice.reduce((acc, val) => acc + val.close, 0)
    return {
      name: item.timestamp,
      value: [
        new Date(item.timestamp).getTime(),
        sum / period
      ]
    }
  }).filter(item => item !== null)
}

const initChart = () => {
  if (!chartRef.value) return
  chart.value = echarts.init(chartRef.value)
  updateChart()
}

const updateChart = () => {
  if (!chart.value || !props.data.length) return

  console.log('Technical Data structure:', JSON.stringify(props.technicalData, null, 2))
  console.log('First data point structure:', JSON.stringify(props.data[0], null, 2))

  const priceData = props.data.map(item => ({
    name: new Date(item.timestamp).toISOString(),
    value: [
      new Date(item.timestamp).getTime(),
      Number(item.close),
      Number(item.open),
      Number(item.low),
      Number(item.high)
    ]
  }))

  const volumeData = props.data.map(item => ({
    name: new Date(item.timestamp).toISOString(),
    value: [
      new Date(item.timestamp).getTime(),
      Number(item.volume),
      Number(item.close) > Number(item.open) ? 1 : -1
    ]
  }))

  // MA Berechnungen
  const ma20Data = calculateMAValues(props.data, 20)
  const ma50Data = calculateMAValues(props.data, 50)

  const getHistoricalIndicators = (indicator) => {
    return props.data.map((item, index) => [
      new Date(item.timestamp).getTime(),
      item[indicator] ||
      props.technicalData?.historical?.[item.timestamp]?.[indicator] ||
      null
    ]).filter(item => item[1] !== null)
  }

  // Bollinger Bands nur hinzufügen wenn current Werte existieren
  const bbSeries = props.technicalData?.current ? ['bb_upper', 'bb_middle', 'bb_lower']
    .filter(band => props.technicalData.current[band] !== undefined)
    .map(band => ({
      name: band.toUpperCase(),
      type: 'line',
      data: props.data.map(item => [
        new Date(item.timestamp).getTime(),
        props.technicalData.current[band]  // Konstanter Wert für die ganze Linie
      ]),
      smooth: true,
      lineStyle: {
        opacity: 0.5,
        width: 1,
        type: 'dashed',
        color: getIndicatorColor(band)
      },
      symbol: 'none'
    })) : []

  const option = {
    animation: false,
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'cross',
        label: {
          backgroundColor: '#1b1b1b'
        }
      },
      formatter: (params) => {
        const date = new Date(params[0].value[0]).toLocaleString()
        let result = `<div style="font-weight: bold; margin-bottom: 5px">${date}</div>`

        params.forEach(param => {
          if (param.seriesName === 'K-Line') {
            const [time, close, open, low, high] = param.value
            result += `<div style="margin: 5px 0">
              <div>Open: $${open.toFixed(2)}</div>
              <div>High: $${high.toFixed(2)}</div>
              <div>Low: $${low.toFixed(2)}</div>
              <div>Close: $${close.toFixed(2)}</div>
            </div>`
          } else if (param.seriesName === 'Volume') {
            result += `<div>${param.marker}Volume: ${formatVolume(param.value[1])}</div>`
          } else {
            result += `<div>${param.marker}${param.seriesName}: $${param.value[1]?.toFixed(2)}</div>`
          }
        })
        return result
      }
    },
    axisPointer: {
      link: { xAxisIndex: 'all' }
    },
    legend: {
      data: ['K-Line', 'MA20', 'MA50', 'BB_UPPER', 'BB_MIDDLE', 'BB_LOWER', 'Volume'],
      selected: {
        'Volume': true,
        'MA20': true,
        'MA50': true,
        'BB_UPPER': true,
        'BB_MIDDLE': true,
        'BB_LOWER': true,
        'K-Line': true
      }
    },
    grid: [{
      left: '10%',
      right: '10%',
      height: '70%',
      top: '5%'
    }, {
      left: '10%',
      right: '10%',
      top: '80%',
      height: '15%'
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
      position: 'left',
      splitLine: { show: true },
      axisLabel: {
        formatter: (value) => `$${value.toFixed(2)}`,
        margin: 16
      }
    }, {
      gridIndex: 1,
      position: 'left',
      splitLine: { show: false },
      axisLabel: {
        formatter: formatVolume,
        margin: 16
      }
    }],
    dataZoom: [{
      type: 'inside',
      xAxisIndex: [0, 1],
      start: 0,
      end: 100,
      minValueSpan: 3600 * 24 * 1000 * 3  // Minimum 3 Tage
    }, {
      show: true,
      xAxisIndex: [0, 1],
      type: 'slider',
      bottom: '0%',
      start: 0,
      end: 100,
      height: 20,
      handleSize: 20,
      handleStyle: {
        color: '#7AB8FF'
      }
    }],
    series: [
      {
        name: 'K-Line',
        type: 'candlestick',
        data: priceData.map(item => item.value),
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
        smooth: true,
        lineStyle: {
          opacity: 0.5,
          width: 1.5,
          color: '#7cb5ec'
        },
        symbol: 'none'
      },
      {
        name: 'MA50',
        type: 'line',
        data: ma50Data,
        smooth: true,
        lineStyle: {
          opacity: 0.5,
          width: 1.5,
          color: '#434348'
        },
        symbol: 'none'
      },
      {
        name: 'Volume',
        type: 'bar',
        xAxisIndex: 1,
        yAxisIndex: 1,
        data: volumeData.map(item => ({
          value: [item.value[0], item.value[1]],
          itemStyle: {
            color: item.value[2] > 0 ? '#26a69a' : '#ef5350'
          }
        }))
      },
      ...bbSeries
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

onUnmounted(() => {
  window.removeEventListener('resize', () => chart.value?.resize())
  chart.value?.dispose()
})
</script>