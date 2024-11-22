<!--<template>-->
<!--  <div class="bg-card rounded-lg shadow p-6">-->
<!--    <div class="mb-4 flex gap-2">-->
<!--      <Button-->
<!--        v-for="indicator in indicators"-->
<!--        :key="indicator.name"-->
<!--        variant="outline"-->
<!--        size="sm"-->
<!--        :class="{ 'bg-primary/10': indicator.active }"-->
<!--        @click="toggleIndicator(indicator)"-->
<!--      >-->
<!--        {{ indicator.name }}-->
<!--      </Button>-->
<!--    </div>-->
<!--    <div id="chart-container" ref="chartRef" class="h-[700px]"></div>-->
<!--  </div>-->
<!--</template>-->

<!--<script setup>-->
<!--import { ref, onMounted, watch, onUnmounted } from 'vue'-->
<!--import { createChart } from 'lightweight-charts'-->
<!--import { Button } from '@/components/ui/button'-->

<!--const props = defineProps({-->
<!--  data: {-->
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
<!--const candlestickSeries = ref(null)-->
<!--const series = ref({})-->

<!--const indicators = ref([-->
<!--  { name: 'MA20', active: true, color: '#2196F3' },-->
<!--  { name: 'MA50', active: true, color: '#FF9800' },-->
<!--  { name: 'BB Upper', active: true, color: '#4CAF50' },-->
<!--  { name: 'BB Lower', active: true, color: '#4CAF50' }-->
<!--])-->

<!--const initChart = () => {-->
<!--  const chartOptions = {-->
<!--    layout: {-->
<!--      textColor: 'black',-->
<!--      background: { type: 'solid', color: 'white' }-->
<!--    },-->
<!--    grid: {-->
<!--      vertLines: { color: '#e6e6e6' },-->
<!--      horzLines: { color: '#e6e6e6' }-->
<!--    },-->
<!--    crosshair: {-->
<!--      mode: 1,-->
<!--      vertLine: {-->
<!--        color: '#2962FF',-->
<!--        width: 0.5,-->
<!--        style: 1,-->
<!--        visible: true,-->
<!--        labelVisible: true-->
<!--      },-->
<!--      horzLine: {-->
<!--        color: '#2962FF',-->
<!--        width: 0.5,-->
<!--        style: 1,-->
<!--        visible: true,-->
<!--        labelVisible: true-->
<!--      }-->
<!--    }-->
<!--  }-->

<!--  chart.value = createChart(chartRef.value, chartOptions)-->

<!--  // Candlestick Series-->
<!--  candlestickSeries.value = chart.value.addCandlestickSeries({-->
<!--    upColor: '#26a69a',-->
<!--    downColor: '#ef5350',-->
<!--    borderVisible: false,-->
<!--    wickUpColor: '#26a69a',-->
<!--    wickDownColor: '#ef5350'-->
<!--  })-->

<!--  // Initialize Technical Indicators-->
<!--  series.value = {-->
<!--    MA20: chart.value.addLineSeries({-->
<!--      color: '#2196F3',-->
<!--      lineWidth: 1,-->
<!--      visible: true-->
<!--    }),-->
<!--    MA50: chart.value.addLineSeries({-->
<!--      color: '#FF9800',-->
<!--      lineWidth: 1,-->
<!--      visible: true-->
<!--    }),-->
<!--    'BB Upper': chart.value.addLineSeries({-->
<!--      color: '#4CAF50',-->
<!--      lineWidth: 1,-->
<!--      lineStyle: 1, // Dashed-->
<!--      visible: true-->
<!--    }),-->
<!--    'BB Lower': chart.value.addLineSeries({-->
<!--      color: '#4CAF50',-->
<!--      lineWidth: 1,-->
<!--      lineStyle: 1, // Dashed-->
<!--      visible: true-->
<!--    })-->
<!--  }-->

<!--  updateChartData()-->
<!--}-->

<!--const calculateMA = (data, period) => {-->
<!--  return data.map((item, index) => {-->
<!--    if (index < period - 1) return null-->
<!--    const slice = data.slice(index - period + 1, index + 1)-->
<!--    const sum = slice.reduce((acc, val) => acc + val.close, 0)-->
<!--    return {-->
<!--      time: new Date(item.timestamp).getTime() / 1000,-->
<!--      value: sum / period-->
<!--    }-->
<!--  }).filter(item => item !== null)-->
<!--}-->

<!--const toggleIndicator = (indicator) => {-->
<!--  indicator.active = !indicator.active-->
<!--  if (series.value[indicator.name]) {-->
<!--    series.value[indicator.name].applyOptions({-->
<!--      visible: indicator.active-->
<!--    })-->
<!--  }-->
<!--}-->

<!--const updateChartData = () => {-->
<!--  if (!chart.value || !props.data.length) return-->

<!--  // Update Candlesticks-->
<!--  const candleData = props.data.map(item => ({-->
<!--    time: new Date(item.timestamp).getTime() / 1000,-->
<!--    open: item.open,-->
<!--    high: item.high,-->
<!--    low: item.low,-->
<!--    close: item.close-->
<!--  }))-->
<!--  candlestickSeries.value.setData(candleData)-->

<!--  // Update MA20-->
<!--  const ma20Data = calculateMA(props.data, 20)-->
<!--  series.value['MA20'].setData(ma20Data)-->

<!--  // Update MA50-->
<!--  const ma50Data = calculateMA(props.data, 50)-->
<!--  series.value['MA50'].setData(ma50Data)-->

<!--  // Update Bollinger Bands-->
<!--  const bbData = props.data.map(item => {-->
<!--    const timestamp = new Date(item.timestamp).getTime() / 1000-->
<!--    return {-->
<!--      upper: {-->
<!--        time: timestamp,-->
<!--        value: props.technicalData?.historical?.[item.timestamp]?.bb_upper ||-->
<!--               props.technicalData?.current?.bb_upper-->
<!--      },-->
<!--      lower: {-->
<!--        time: timestamp,-->
<!--        value: props.technicalData?.historical?.[item.timestamp]?.bb_lower ||-->
<!--               props.technicalData?.current?.bb_lower-->
<!--      }-->
<!--    }-->
<!--  })-->

<!--  series.value['BB Upper'].setData(bbData.map(d => d.upper).filter(item => item.value !== undefined))-->
<!--  series.value['BB Lower'].setData(bbData.map(d => d.lower).filter(item => item.value !== undefined))-->

<!--  chart.value.timeScale().fitContent()-->
<!--}-->

<!--onMounted(() => {-->
<!--  initChart()-->
<!--})-->

<!--watch(() => props.data, () => {-->
<!--  updateChartData()-->
<!--}, { deep: true })-->

<!--watch(() => props.technicalData, () => {-->
<!--  updateChartData()-->
<!--}, { deep: true })-->

<!--onUnmounted(() => {-->
<!--  if (chart.value) {-->
<!--    chart.value.remove()-->
<!--  }-->
<!--})-->
<!--</script>-->


<template>
  <div class="bg-card rounded-lg shadow p-6">
    <div class="mb-4 flex gap-2">
      <Button
        v-for="indicator in indicators"
        :key="indicator.name"
        variant="outline"
        size="sm"
        :class="{ 'bg-primary/10': indicator.active }"
        @click="toggleIndicator(indicator)"
      >
        {{ indicator.name }}
      </Button>
    </div>
    <div
      id="chart-container"
      ref="chartRef"
      class="w-full sm:h-[500px] md:h-[700px] lg:h-[900px]"
    ></div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, onUnmounted, computed } from 'vue'
import { createChart } from 'lightweight-charts'
import { Button } from '@/components/ui/button'
import { useThemeStore } from '@/stores/theme'  // Importiere den Theme-Store

const props = defineProps({
  data: {
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
const candlestickSeries = ref(null)
const series = ref({})

const indicators = ref([
  { name: 'MA20', active: true, color: '#2196F3' },
  { name: 'MA50', active: true, color: '#FF9800' },
  { name: 'BB Upper', active: true, color: '#4CAF50' },
  { name: 'BB Lower', active: true, color: '#4CAF50' }
])

const themeStore = useThemeStore() // Verwende den Theme-Store
const isDark = computed(() => themeStore.isDark) // Reaktive Variable für das aktuelle Theme

const initChart = () => {
  const chartOptions = {
    layout: {
      textColor: isDark.value ? 'white' : 'black',
      background: { type: 'solid', color: isDark.value ? 'black' : 'white' }
    },
    grid: {
      vertLines: { color: isDark.value ? '#444444' : '#e6e6e6' },
      horzLines: { color: isDark.value ? '#444444' : '#e6e6e6' }
    },
    crosshair: {
      mode: 1,
      vertLine: {
        color: '#2962FF',
        width: 0.5,
        style: 1,
        visible: true,
        labelVisible: true
      },
      horzLine: {
        color: '#2962FF',
        width: 0.5,
        style: 1,
        visible: true,
        labelVisible: true
      }
    }
  }

  chart.value = createChart(chartRef.value, chartOptions)

  // Candlestick Series
  candlestickSeries.value = chart.value.addCandlestickSeries({
    upColor: '#26a69a',
    downColor: '#ef5350',
    borderVisible: false,
    wickUpColor: '#26a69a',
    wickDownColor: '#ef5350'
  })

  // Initialize Technical Indicators
  series.value = {
    MA20: chart.value.addLineSeries({
      color: '#2196F3',
      lineWidth: 1,
      visible: true
    }),
    MA50: chart.value.addLineSeries({
      color: '#FF9800',
      lineWidth: 1,
      visible: true
    }),
    'BB Upper': chart.value.addLineSeries({
      color: '#4CAF50',
      lineWidth: 1,
      lineStyle: 1, // Dashed
      visible: true
    }),
    'BB Lower': chart.value.addLineSeries({
      color: '#4CAF50',
      lineWidth: 1,
      lineStyle: 1, // Dashed
      visible: true
    })
  }

  updateChartData()
}

// Funktion zur Berechnung des gleitenden Durchschnitts
const calculateMA = (data, period) => {
  return data.map((item, index) => {
    if (index < period - 1) return null
    const slice = data.slice(index - period + 1, index + 1)
    const sum = slice.reduce((acc, val) => acc + val.close, 0)
    return {
      time: new Date(item.timestamp).getTime() / 1000,
      value: sum / period
    }
  }).filter(item => item !== null)
}

// Indikator umschalten
const toggleIndicator = (indicator) => {
  indicator.active = !indicator.active
  if (series.value[indicator.name]) {
    series.value[indicator.name].applyOptions({
      visible: indicator.active
    })
  }
}

// Chart-Daten aktualisieren
const updateChartData = () => {
  if (!chart.value || !props.data.length) return

  // Update Candlesticks
  const candleData = props.data.map(item => ({
    time: new Date(item.timestamp).getTime() / 1000,
    open: item.open,
    high: item.high,
    low: item.low,
    close: item.close
  }))
  candlestickSeries.value.setData(candleData)

  // Update MA20
  const ma20Data = calculateMA(props.data, 20)
  series.value['MA20'].setData(ma20Data)

  // Update MA50
  const ma50Data = calculateMA(props.data, 50)
  series.value['MA50'].setData(ma50Data)

  // Update Bollinger Bands
  const bbData = props.data.map(item => {
    const timestamp = new Date(item.timestamp).getTime() / 1000
    return {
      upper: {
        time: timestamp,
        value: props.technicalData?.historical?.[item.timestamp]?.bb_upper ||
               props.technicalData?.current?.bb_upper
      },
      lower: {
        time: timestamp,
        value: props.technicalData?.historical?.[item.timestamp]?.bb_lower ||
               props.technicalData?.current?.bb_lower
      }
    }
  })

  series.value['BB Upper'].setData(bbData.map(d => d.upper).filter(item => item.value !== undefined))
  series.value['BB Lower'].setData(bbData.map(d => d.lower).filter(item => item.value !== undefined))

  chart.value.timeScale().fitContent()
}

// Überwachung von Theme-Änderungen
watch(isDark, (newVal) => {
  const newOptions = {
    layout: {
      textColor: newVal ? 'white' : 'black',
      background: { type: 'solid', color: newVal ? 'black' : 'white' }
    },
    grid: {
      vertLines: { color: newVal ? '#444444' : '#e6e6e6' },
      horzLines: { color: newVal ? '#444444' : '#e6e6e6' }
    }
  }
  chart.value.applyOptions(newOptions) // Wenden Sie die neuen Optionen an
})

// Initialisieren des Charts
onMounted(() => {
  initChart()
})

// Überwachen von Datenänderungen
watch(() => props.data, () => {
  updateChartData()
}, { deep: true })

watch(() => props.technicalData, () => {
  updateChartData()
}, { deep: true })

// Aufräumen bei der Zerstörung der Komponente
onUnmounted(() => {
  if (chart.value) {
    chart.value.remove()
  }
})
</script>
