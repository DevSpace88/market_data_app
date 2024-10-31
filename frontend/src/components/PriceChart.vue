<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;<template>&ndash;&gt;&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;  <div class="bg-card rounded-lg shadow p-4">&ndash;&gt;&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;    <div class="h-[500px]" ref="chartRef"></div>&ndash;&gt;&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;  </div>&ndash;&gt;&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;</template>&ndash;&gt;&ndash;&gt;&ndash;&gt;-->

<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;<script setup>&ndash;&gt;&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;import {ref, onMounted, watch, onUnmounted} from 'vue'&ndash;&gt;&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;import * as echarts from 'echarts'&ndash;&gt;&ndash;&gt;&ndash;&gt;-->

<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;// const props = defineProps({&ndash;&gt;&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;//   data: {&ndash;&gt;&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;//     type: Array,&ndash;&gt;&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;//     default: () => []&ndash;&gt;&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;//   },&ndash;&gt;&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;//   indicators: {&ndash;&gt;&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;//     type: Array,&ndash;&gt;&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;//     default: () => []&ndash;&gt;&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;//   }&ndash;&gt;&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;// })&ndash;&gt;&ndash;&gt;&ndash;&gt;-->

<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;const props = defineProps({&ndash;&gt;&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;  data: {&ndash;&gt;&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;    type: Array,&ndash;&gt;&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;    default: () => []&ndash;&gt;&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;  },&ndash;&gt;&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;  indicators: {&ndash;&gt;&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;    type: Array,&ndash;&gt;&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;    default: () => []&ndash;&gt;&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;  },&ndash;&gt;&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;  indicatorData: {&ndash;&gt;&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;    type: Function,&ndash;&gt;&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;    required: true&ndash;&gt;&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;  }&ndash;&gt;&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;})&ndash;&gt;&ndash;&gt;&ndash;&gt;-->


<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;const chartRef = ref(null)&ndash;&gt;&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;const chart = ref(null)&ndash;&gt;&ndash;&gt;&ndash;&gt;-->

<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;const initChart = () => {&ndash;&gt;&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;  if (!chartRef.value) return&ndash;&gt;&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;  chart.value = echarts.init(chartRef.value)&ndash;&gt;&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;  updateChart()&ndash;&gt;&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;}&ndash;&gt;&ndash;&gt;&ndash;&gt;-->

<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;const updateChart = () => {&ndash;&gt;&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;  if (!chart.value || !props.data) return&ndash;&gt;&ndash;&gt;&ndash;&gt;-->

<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;  const option = {&ndash;&gt;&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;    tooltip: {&ndash;&gt;&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;      trigger: 'axis',&ndash;&gt;&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;      axisPointer: {type: 'cross'}&ndash;&gt;&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;    },&ndash;&gt;&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;    legend: {&ndash;&gt;&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;      data: ['Price', 'Volume', ...props.indicators]&ndash;&gt;&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;    },&ndash;&gt;&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;    grid: {&ndash;&gt;&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;      left: '3%',&ndash;&gt;&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;      right: '3%',&ndash;&gt;&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;      bottom: '15%'&ndash;&gt;&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;    },&ndash;&gt;&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;    xAxis: {&ndash;&gt;&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;      type: 'time',&ndash;&gt;&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;      boundaryGap: false,&ndash;&gt;&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;      min: props.data.length ? props.data[0].timestamp : null,&ndash;&gt;&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;      max: props.data.length ? props.data[props.data.length - 1].timestamp : null,&ndash;&gt;&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;    },&ndash;&gt;&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;    yAxis: [&ndash;&gt;&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;      {&ndash;&gt;&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;        type: 'value',&ndash;&gt;&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;        name: 'Price',&ndash;&gt;&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;        position: 'left'&ndash;&gt;&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;      },&ndash;&gt;&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;      {&ndash;&gt;&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;        type: 'value',&ndash;&gt;&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;        name: 'Volume',&ndash;&gt;&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;        position: 'right'&ndash;&gt;&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;      }&ndash;&gt;&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;    ],&ndash;&gt;&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;    // series: [&ndash;&gt;&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;    //   {&ndash;&gt;&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;    //     name: 'Price',&ndash;&gt;&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;    //     type: 'line',&ndash;&gt;&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;    //     data: props.data.map(item => [item.timestamp, item.close]),&ndash;&gt;&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;    //     smooth: true&ndash;&gt;&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;    //   },&ndash;&gt;&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;    //   {&ndash;&gt;&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;    //     name: 'Volume',&ndash;&gt;&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;    //     type: 'bar',&ndash;&gt;&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;    //     yAxisIndex: 1,&ndash;&gt;&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;    //     data: props.data.map(item => [item.timestamp, item.volume])&ndash;&gt;&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;    //   },&ndash;&gt;&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;    //   ...props.indicators.map(indicator => ({&ndash;&gt;&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;    //     name: indicator,&ndash;&gt;&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;    //     type: 'line',&ndash;&gt;&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;    //     smooth: true,&ndash;&gt;&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;    //     data: props.data.map(item => [item.timestamp, item[indicator.toLowerCase()]])&ndash;&gt;&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;    //   }))&ndash;&gt;&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;    // ]&ndash;&gt;&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;    series: [&ndash;&gt;&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;      {&ndash;&gt;&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;        name: 'Price',&ndash;&gt;&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;        type: 'line',&ndash;&gt;&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;        data: props.data.map(item => [item.timestamp, item.close]),&ndash;&gt;&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;        smooth: true&ndash;&gt;&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;      },&ndash;&gt;&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;      {&ndash;&gt;&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;        name: 'Volume',&ndash;&gt;&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;        type: 'bar',&ndash;&gt;&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;        yAxisIndex: 1,&ndash;&gt;&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;        data: props.data.map(item => [item.timestamp, item.volume])&ndash;&gt;&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;      },&ndash;&gt;&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;      ...props.indicators.map(indicator => ({&ndash;&gt;&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;        name: indicator,&ndash;&gt;&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;        type: 'line',&ndash;&gt;&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;        smooth: true,&ndash;&gt;&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;        data: props.indicatorData(indicator)&ndash;&gt;&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;      }))&ndash;&gt;&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;    ]&ndash;&gt;&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;  }&ndash;&gt;&ndash;&gt;&ndash;&gt;-->

<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;  chart.value.setOption(option)&ndash;&gt;&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;}&ndash;&gt;&ndash;&gt;&ndash;&gt;-->

<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;onMounted(initChart)&ndash;&gt;&ndash;&gt;&ndash;&gt;-->

<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;// watch(() => props.data, updateChart, { deep: true })&ndash;&gt;&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;watch(() => props.data, updateChart, {immediate: true, deep: true})&ndash;&gt;&ndash;&gt;&ndash;&gt;-->

<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;watch(() => props.indicators, updateChart)&ndash;&gt;&ndash;&gt;&ndash;&gt;-->


<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;onUnmounted(() => {&ndash;&gt;&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;  if (chart.value) {&ndash;&gt;&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;    chart.value.dispose()&ndash;&gt;&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;  }&ndash;&gt;&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;})&ndash;&gt;&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;&lt;!&ndash;</script>&ndash;&gt;&ndash;&gt;&ndash;&gt;-->



<!--&lt;!&ndash;&lt;!&ndash;<template>&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;  <div class="bg-card rounded-lg shadow p-4">&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;    <div class="h-[500px]" ref="chartRef"></div>&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;  </div>&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;</template>&ndash;&gt;&ndash;&gt;-->

<!--&lt;!&ndash;&lt;!&ndash;<script setup>&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;import { ref, onMounted, watch, onUnmounted } from 'vue'&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;import * as echarts from 'echarts'&ndash;&gt;&ndash;&gt;-->

<!--&lt;!&ndash;&lt;!&ndash;const props = defineProps({&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;  data: {&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;    type: Array,&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;    default: () => []&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;  },&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;  indicators: {&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;    type: Array,&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;    default: () => []&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;  },&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;  indicatorData: {&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;    type: Object,&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;    default: () => ({})&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;  }&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;})&ndash;&gt;&ndash;&gt;-->

<!--&lt;!&ndash;&lt;!&ndash;const chartRef = ref(null)&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;const chart = ref(null)&ndash;&gt;&ndash;&gt;-->

<!--&lt;!&ndash;&lt;!&ndash;const formatIndicatorLines = () => {&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;  if (!props.indicatorData?.historical) return []&ndash;&gt;&ndash;&gt;-->

<!--&lt;!&ndash;&lt;!&ndash;  return props.indicators.map(indicator => ({&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;    name: indicator,&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;    type: 'line',&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;    smooth: true,&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;    data: props.data.map(item => [&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;      item.timestamp,&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;      props.indicatorData.historical[item.timestamp]?.[indicator]&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;    ]).filter(point => point[1] !== null && point[1] !== undefined),&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;    lineStyle: {&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;      opacity: 0.7&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;    }&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;  }))&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;}&ndash;&gt;&ndash;&gt;-->

<!--&lt;!&ndash;&lt;!&ndash;const updateChart = () => {&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;  if (!chart.value || !props.data?.length) return&ndash;&gt;&ndash;&gt;-->

<!--&lt;!&ndash;&lt;!&ndash;  const option = {&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;    tooltip: {&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;      trigger: 'axis',&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;      axisPointer: { type: 'cross' }&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;    },&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;    legend: {&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;      data: ['Price', 'Volume', ...props.indicators],&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;      top: 0&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;    },&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;    grid: {&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;      left: '3%',&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;      right: '3%',&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;      bottom: '15%',&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;      containLabel: true&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;    },&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;    xAxis: {&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;      type: 'time',&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;      boundaryGap: false&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;    },&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;    yAxis: [&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;      {&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;        type: 'value',&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;        name: 'Price',&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;        position: 'left',&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;        axisLine: { show: true },&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;        axisLabel: { formatter: '${value}' }&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;      },&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;      {&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;        type: 'value',&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;        name: 'Volume',&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;        position: 'right',&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;        axisLine: { show: true }&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;      }&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;    ],&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;    series: [&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;      {&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;        name: 'Price',&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;        type: 'line',&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;        data: props.data.map(item => [item.timestamp, item.close]),&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;        smooth: true,&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;        lineStyle: { width: 2 }&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;      },&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;      {&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;        name: 'Volume',&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;        type: 'bar',&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;        yAxisIndex: 1,&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;        data: props.data.map(item => [item.timestamp, item.volume])&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;      },&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;      ...formatIndicatorLines()&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;    ],&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;    dataZoom: [&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;      {&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;        type: 'inside',&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;        start: 0,&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;        end: 100&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;      },&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;      {&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;        show: true,&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;        type: 'slider',&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;        bottom: 0,&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;        start: 0,&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;        end: 100&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;      }&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;    ]&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;  }&ndash;&gt;&ndash;&gt;-->

<!--&lt;!&ndash;&lt;!&ndash;  chart.value.setOption(option, true)&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;}&ndash;&gt;&ndash;&gt;-->

<!--&lt;!&ndash;&lt;!&ndash;onMounted(() => {&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;  if (!chartRef.value) return&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;  chart.value = echarts.init(chartRef.value)&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;  updateChart()&ndash;&gt;&ndash;&gt;-->

<!--&lt;!&ndash;&lt;!&ndash;  window.addEventListener('resize', () => {&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;    chart.value?.resize()&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;  })&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;})&ndash;&gt;&ndash;&gt;-->

<!--&lt;!&ndash;&lt;!&ndash;watch([() => props.data, () => props.indicators], updateChart, { deep: true })&ndash;&gt;&ndash;&gt;-->

<!--&lt;!&ndash;&lt;!&ndash;onUnmounted(() => {&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;  if (chart.value) {&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;    chart.value.dispose()&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;  }&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;})&ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;&lt;!&ndash;</script>&ndash;&gt;&ndash;&gt;-->


<!--&lt;!&ndash;<template>&ndash;&gt;-->
<!--&lt;!&ndash;  <Card class="w-full">&ndash;&gt;-->
<!--&lt;!&ndash;    <CardHeader>&ndash;&gt;-->
<!--&lt;!&ndash;      <CardTitle>{{ symbol }} Price Chart</CardTitle>&ndash;&gt;-->
<!--&lt;!&ndash;      <CardDescription>&ndash;&gt;-->
<!--&lt;!&ndash;        Live price and volume data with technical indicators&ndash;&gt;-->
<!--&lt;!&ndash;      </CardDescription>&ndash;&gt;-->
<!--&lt;!&ndash;    </CardHeader>&ndash;&gt;-->
<!--&lt;!&ndash;    <CardContent>&ndash;&gt;-->
<!--&lt;!&ndash;      <div class="h-[500px]">&ndash;&gt;-->
<!--&lt;!&ndash;        <ResponsiveContainer width="100%" height="100%">&ndash;&gt;-->
<!--&lt;!&ndash;          <ComposedChart :data="chartData">&ndash;&gt;-->
<!--&lt;!&ndash;            &lt;!&ndash; Price Line &ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;            <Line&ndash;&gt;-->
<!--&lt;!&ndash;              type="monotone"&ndash;&gt;-->
<!--&lt;!&ndash;              dataKey="close"&ndash;&gt;-->
<!--&lt;!&ndash;              :stroke="'#8884d8'"&ndash;&gt;-->
<!--&lt;!&ndash;              name="Price"&ndash;&gt;-->
<!--&lt;!&ndash;              yAxisId="price"&ndash;&gt;-->
<!--&lt;!&ndash;            />&ndash;&gt;-->

<!--&lt;!&ndash;            &lt;!&ndash; Technical Indicators &ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;            <Line&ndash;&gt;-->
<!--&lt;!&ndash;              v-for="indicator in indicators"&ndash;&gt;-->
<!--&lt;!&ndash;              :key="indicator"&ndash;&gt;-->
<!--&lt;!&ndash;              type="monotone"&ndash;&gt;-->
<!--&lt;!&ndash;              :dataKey="indicator"&ndash;&gt;-->
<!--&lt;!&ndash;              :stroke="getIndicatorColor(indicator)"&ndash;&gt;-->
<!--&lt;!&ndash;              :name="indicator"&ndash;&gt;-->
<!--&lt;!&ndash;              yAxisId="price"&ndash;&gt;-->
<!--&lt;!&ndash;              :dot="false"&ndash;&gt;-->
<!--&lt;!&ndash;              strokeDasharray="3 3"&ndash;&gt;-->
<!--&lt;!&ndash;            />&ndash;&gt;-->

<!--&lt;!&ndash;            &lt;!&ndash; Volume Bars &ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;            <Bar&ndash;&gt;-->
<!--&lt;!&ndash;              dataKey="volume"&ndash;&gt;-->
<!--&lt;!&ndash;              :fill="'#82ca9d'"&ndash;&gt;-->
<!--&lt;!&ndash;              yAxisId="volume"&ndash;&gt;-->
<!--&lt;!&ndash;              name="Volume"&ndash;&gt;-->
<!--&lt;!&ndash;              :opacity="0.5"&ndash;&gt;-->
<!--&lt;!&ndash;            />&ndash;&gt;-->

<!--&lt;!&ndash;            &lt;!&ndash; Axes &ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;            <XAxis&ndash;&gt;-->
<!--&lt;!&ndash;              dataKey="timestamp"&ndash;&gt;-->
<!--&lt;!&ndash;              scale="time"&ndash;&gt;-->
<!--&lt;!&ndash;              type="number"&ndash;&gt;-->
<!--&lt;!&ndash;              :domain="['auto', 'auto']"&ndash;&gt;-->
<!--&lt;!&ndash;              :tickFormatter="formatXAxis"&ndash;&gt;-->
<!--&lt;!&ndash;            />&ndash;&gt;-->
<!--&lt;!&ndash;            <YAxis&ndash;&gt;-->
<!--&lt;!&ndash;              yAxisId="price"&ndash;&gt;-->
<!--&lt;!&ndash;              orientation="right"&ndash;&gt;-->
<!--&lt;!&ndash;              :tickFormatter="formatPrice"&ndash;&gt;-->
<!--&lt;!&ndash;            />&ndash;&gt;-->
<!--&lt;!&ndash;            <YAxis&ndash;&gt;-->
<!--&lt;!&ndash;              yAxisId="volume"&ndash;&gt;-->
<!--&lt;!&ndash;              orientation="left"&ndash;&gt;-->
<!--&lt;!&ndash;              :tickFormatter="formatVolume"&ndash;&gt;-->
<!--&lt;!&ndash;            />&ndash;&gt;-->

<!--&lt;!&ndash;            &lt;!&ndash; Additional Features &ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;            <Tooltip :content="renderTooltip" />&ndash;&gt;-->
<!--&lt;!&ndash;            <Legend />&ndash;&gt;-->
<!--&lt;!&ndash;            <CartesianGrid strokeDasharray="3 3" />&ndash;&gt;-->
<!--&lt;!&ndash;            <Brush dataKey="timestamp" :height="30" :stroke="'#8884d8'" />&ndash;&gt;-->
<!--&lt;!&ndash;          </ComposedChart>&ndash;&gt;-->
<!--&lt;!&ndash;        </ResponsiveContainer>&ndash;&gt;-->
<!--&lt;!&ndash;      </div>&ndash;&gt;-->
<!--&lt;!&ndash;    </CardContent>&ndash;&gt;-->
<!--&lt;!&ndash;  </Card>&ndash;&gt;-->
<!--&lt;!&ndash;</template>&ndash;&gt;-->

<!--&lt;!&ndash;<script setup>&ndash;&gt;-->
<!--&lt;!&ndash;import { computed } from 'vue'&ndash;&gt;-->
<!--&lt;!&ndash;import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ui/card'&ndash;&gt;-->
<!--&lt;!&ndash;import {&ndash;&gt;-->
<!--&lt;!&ndash;  ResponsiveContainer,&ndash;&gt;-->
<!--&lt;!&ndash;  ComposedChart,&ndash;&gt;-->
<!--&lt;!&ndash;  Line,&ndash;&gt;-->
<!--&lt;!&ndash;  Bar,&ndash;&gt;-->
<!--&lt;!&ndash;  XAxis,&ndash;&gt;-->
<!--&lt;!&ndash;  YAxis,&ndash;&gt;-->
<!--&lt;!&ndash;  Tooltip,&ndash;&gt;-->
<!--&lt;!&ndash;  Legend,&ndash;&gt;-->
<!--&lt;!&ndash;  CartesianGrid,&ndash;&gt;-->
<!--&lt;!&ndash;  Brush&ndash;&gt;-->
<!--&lt;!&ndash;} from 'recharts'&ndash;&gt;-->

<!--&lt;!&ndash;const props = defineProps({&ndash;&gt;-->
<!--&lt;!&ndash;  data: {&ndash;&gt;-->
<!--&lt;!&ndash;    type: Array,&ndash;&gt;-->
<!--&lt;!&ndash;    default: () => []&ndash;&gt;-->
<!--&lt;!&ndash;  },&ndash;&gt;-->
<!--&lt;!&ndash;  indicators: {&ndash;&gt;-->
<!--&lt;!&ndash;    type: Array,&ndash;&gt;-->
<!--&lt;!&ndash;    default: () => []&ndash;&gt;-->
<!--&lt;!&ndash;  },&ndash;&gt;-->
<!--&lt;!&ndash;  indicatorData: {&ndash;&gt;-->
<!--&lt;!&ndash;    type: Object,&ndash;&gt;-->
<!--&lt;!&ndash;    default: () => ({})&ndash;&gt;-->
<!--&lt;!&ndash;  },&ndash;&gt;-->
<!--&lt;!&ndash;  symbol: {&ndash;&gt;-->
<!--&lt;!&ndash;    type: String,&ndash;&gt;-->
<!--&lt;!&ndash;    required: true&ndash;&gt;-->
<!--&lt;!&ndash;  }&ndash;&gt;-->
<!--&lt;!&ndash;})&ndash;&gt;-->

<!--&lt;!&ndash;const chartData = computed(() => {&ndash;&gt;-->
<!--&lt;!&ndash;  return props.data.map(item => {&ndash;&gt;-->
<!--&lt;!&ndash;    const dataPoint = {&ndash;&gt;-->
<!--&lt;!&ndash;      timestamp: new Date(item.timestamp).getTime(),&ndash;&gt;-->
<!--&lt;!&ndash;      close: item.close,&ndash;&gt;-->
<!--&lt;!&ndash;      volume: item.volume || 0&ndash;&gt;-->
<!--&lt;!&ndash;    }&ndash;&gt;-->

<!--&lt;!&ndash;    props.indicators.forEach(indicator => {&ndash;&gt;-->
<!--&lt;!&ndash;      if (props.indicatorData?.historical?.[item.timestamp]?.[indicator]) {&ndash;&gt;-->
<!--&lt;!&ndash;        dataPoint[indicator] = props.indicatorData.historical[item.timestamp][indicator]&ndash;&gt;-->
<!--&lt;!&ndash;      }&ndash;&gt;-->
<!--&lt;!&ndash;    })&ndash;&gt;-->

<!--&lt;!&ndash;    return dataPoint&ndash;&gt;-->
<!--&lt;!&ndash;  })&ndash;&gt;-->
<!--&lt;!&ndash;})&ndash;&gt;-->

<!--&lt;!&ndash;const indicatorColors = {&ndash;&gt;-->
<!--&lt;!&ndash;  sma_20: '#2196F3',&ndash;&gt;-->
<!--&lt;!&ndash;  sma_50: '#FF9800',&ndash;&gt;-->
<!--&lt;!&ndash;  bb_upper: '#4CAF50',&ndash;&gt;-->
<!--&lt;!&ndash;  bb_lower: '#4CAF50',&ndash;&gt;-->
<!--&lt;!&ndash;  bb_middle: '#4CAF50',&ndash;&gt;-->
<!--&lt;!&ndash;  rsi: '#E91E63',&ndash;&gt;-->
<!--&lt;!&ndash;  macd: '#9C27B0'&ndash;&gt;-->
<!--&lt;!&ndash;}&ndash;&gt;-->

<!--&lt;!&ndash;const getIndicatorColor = (indicator) => {&ndash;&gt;-->
<!--&lt;!&ndash;  return indicatorColors[indicator] || '#666666'&ndash;&gt;-->
<!--&lt;!&ndash;}&ndash;&gt;-->

<!--&lt;!&ndash;const formatXAxis = (timestamp) => {&ndash;&gt;-->
<!--&lt;!&ndash;  return new Date(timestamp).toLocaleDateString()&ndash;&gt;-->
<!--&lt;!&ndash;}&ndash;&gt;-->

<!--&lt;!&ndash;const formatPrice = (value) => {&ndash;&gt;-->
<!--&lt;!&ndash;  return `$${value.toFixed(2)}`&ndash;&gt;-->
<!--&lt;!&ndash;}&ndash;&gt;-->

<!--&lt;!&ndash;const formatVolume = (value) => {&ndash;&gt;-->
<!--&lt;!&ndash;  if (value >= 1000000) return `${(value / 1000000).toFixed(1)}M`&ndash;&gt;-->
<!--&lt;!&ndash;  if (value >= 1000) return `${(value / 1000).toFixed(1)}K`&ndash;&gt;-->
<!--&lt;!&ndash;  return value.toString()&ndash;&gt;-->
<!--&lt;!&ndash;}&ndash;&gt;-->

<!--&lt;!&ndash;const renderTooltip = (props) => {&ndash;&gt;-->
<!--&lt;!&ndash;  if (!props.active || !props.payload) return null&ndash;&gt;-->

<!--&lt;!&ndash;  return (&ndash;&gt;-->
<!--&lt;!&ndash;    `<div class="bg-card border rounded-lg p-2 shadow-lg">&ndash;&gt;-->
<!--&lt;!&ndash;      <p class="font-medium">${new Date(props.label).toLocaleString()}</p>&ndash;&gt;-->
<!--&lt;!&ndash;      ${props.payload.map(entry => `&ndash;&gt;-->
<!--&lt;!&ndash;        <p style="color: ${entry.color}">&ndash;&gt;-->
<!--&lt;!&ndash;          ${entry.name}: ${entry.name === 'Volume' ? formatVolume(entry.value) : formatPrice(entry.value)}&ndash;&gt;-->
<!--&lt;!&ndash;        </p>&ndash;&gt;-->
<!--&lt;!&ndash;      `).join('')}&ndash;&gt;-->
<!--&lt;!&ndash;    </div>`&ndash;&gt;-->
<!--&lt;!&ndash;  )&ndash;&gt;-->
<!--&lt;!&ndash;}&ndash;&gt;-->
<!--&lt;!&ndash;</script>&ndash;&gt;-->

<!--&lt;!&ndash;<style scoped>&ndash;&gt;-->
<!--&lt;!&ndash;.recharts-cartesian-grid-horizontal line,&ndash;&gt;-->
<!--&lt;!&ndash;.recharts-cartesian-grid-vertical line {&ndash;&gt;-->
<!--&lt;!&ndash;  stroke: var(&#45;&#45;border);&ndash;&gt;-->
<!--&lt;!&ndash;}&ndash;&gt;-->

<!--&lt;!&ndash;.recharts-text {&ndash;&gt;-->
<!--&lt;!&ndash;  fill: var(&#45;&#45;foreground);&ndash;&gt;-->
<!--&lt;!&ndash;}&ndash;&gt;-->

<!--&lt;!&ndash;.recharts-legend-item-text {&ndash;&gt;-->
<!--&lt;!&ndash;  color: var(&#45;&#45;foreground) !important;&ndash;&gt;-->
<!--&lt;!&ndash;}&ndash;&gt;-->
<!--&lt;!&ndash;</style>&ndash;&gt;-->

<!--<template>-->
<!--  <Card class="w-full">-->
<!--    <CardHeader>-->
<!--      <CardTitle>Price Chart</CardTitle>-->
<!--      <CardDescription>-->
<!--        {{ symbol }} - {{ timeframe }} Chart-->
<!--      </CardDescription>-->
<!--    </CardHeader>-->
<!--    <CardContent>-->
<!--      <div class="h-[600px] w-full">-->
<!--        <ResponsiveContainer width="100%" height="100%">-->
<!--          <ComposedChart :data="formattedData">-->
<!--            <defs>-->
<!--              <linearGradient id="colorVolume" x1="0" y1="0" x2="0" y2="1">-->
<!--                <stop offset="5%" stop-color="#82ca9d" :stop-opacity="0.8" />-->
<!--                <stop offset="95%" stop-color="#82ca9d" :stop-opacity="0.1" />-->
<!--              </linearGradient>-->
<!--            </defs>-->

<!--            <XAxis-->
<!--              dataKey="date"-->
<!--              :tickFormatter="formatDate"-->
<!--              :minTickGap="30"-->
<!--            />-->
<!--            <YAxis-->
<!--              yAxisId="price"-->
<!--              :domain="['auto', 'auto']"-->
<!--              :tickFormatter="formatPrice"-->
<!--              orientation="right"-->
<!--            />-->
<!--            <YAxis-->
<!--              yAxisId="volume"-->
<!--              orientation="left"-->
<!--              :tickFormatter="formatVolume"-->
<!--            />-->
<!--            <Tooltip :content="CustomTooltip" />-->
<!--            <Legend />-->
<!--            <CartesianGrid strokeDasharray="3 3" :opacity="0.5" />-->

<!--            <Area-->
<!--              type="monotone"-->
<!--              dataKey="volume"-->
<!--              yAxisId="volume"-->
<!--              fill="url(#colorVolume)"-->
<!--              stroke="#82ca9d"-->
<!--              :opacity="0.5"-->
<!--            />-->

<!--            <Line-->
<!--              type="linear"-->
<!--              dataKey="close"-->
<!--              stroke="#8884d8"-->
<!--              yAxisId="price"-->
<!--              :dot="false"-->
<!--            />-->

<!--            <Line-->
<!--              v-for="indicator in indicators"-->
<!--              :key="indicator"-->
<!--              type="linear"-->
<!--              :dataKey="indicator"-->
<!--              :stroke="getIndicatorColor(indicator)"-->
<!--              strokeDasharray="3 3"-->
<!--              yAxisId="price"-->
<!--              :dot="false"-->
<!--            />-->
<!--          </ComposedChart>-->
<!--        </ResponsiveContainer>-->
<!--      </div>-->
<!--    </CardContent>-->
<!--  </Card>-->
<!--</template>-->

<!--<script setup>-->
<!--import { computed } from 'vue'-->
<!--import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ui/card'-->
<!--import {-->
<!--  ResponsiveContainer,-->
<!--  ComposedChart,-->
<!--  Line,-->
<!--  Area,-->
<!--  XAxis,-->
<!--  YAxis,-->
<!--  CartesianGrid,-->
<!--  Tooltip,-->
<!--  Legend-->
<!--} from 'recharts'-->

<!--const props = defineProps({-->
<!--  data: {-->
<!--    type: Array,-->
<!--    default: () => []-->
<!--  },-->
<!--  indicators: {-->
<!--    type: Array,-->
<!--    default: () => []-->
<!--  },-->
<!--  indicatorData: {-->
<!--    type: Object,-->
<!--    default: () => ({})-->
<!--  },-->
<!--  symbol: {-->
<!--    type: String,-->
<!--    required: true-->
<!--  },-->
<!--  timeframe: {-->
<!--    type: String,-->
<!--    default: '1D'-->
<!--  }-->
<!--})-->

<!--const formattedData = computed(() => {-->
<!--  return props.data.map(item => {-->
<!--    const point = {-->
<!--      date: new Date(item.timestamp),-->
<!--      close: item.close,-->
<!--      volume: item.volume || 0-->
<!--    }-->

<!--    // Add indicators-->
<!--    props.indicators.forEach(indicator => {-->
<!--      if (props.indicatorData?.historical?.[item.timestamp]?.[indicator]) {-->
<!--        point[indicator] = props.indicatorData.historical[item.timestamp][indicator]-->
<!--      }-->
<!--    })-->

<!--    return point-->
<!--  })-->
<!--})-->

<!--const indicatorColors = {-->
<!--  sma_20: '#2196F3',-->
<!--  sma_50: '#FF9800',-->
<!--  bb_upper: '#4CAF50',-->
<!--  bb_lower: '#4CAF50',-->
<!--  bb_middle: '#4CAF50',-->
<!--  rsi: '#E91E63',-->
<!--  macd: '#9C27B0'-->
<!--}-->

<!--const formatDate = (date) => {-->
<!--  return new Date(date).toLocaleDateString()-->
<!--}-->

<!--const formatPrice = (value) => {-->
<!--  return `$${value.toFixed(2)}`-->
<!--}-->

<!--const formatVolume = (value) => {-->
<!--  if (value >= 1_000_000) return `${(value / 1_000_000).toFixed(1)}M`-->
<!--  if (value >= 1_000) return `${(value / 1_000).toFixed(1)}K`-->
<!--  return value.toString()-->
<!--}-->

<!--const getIndicatorColor = (indicator) => {-->
<!--  return indicatorColors[indicator] || '#666666'-->
<!--}-->

<!--const CustomTooltip = (props) => {-->
<!--  if (!props.active || !props.payload?.length) return null-->

<!--  return `-->
<!--    <div class="bg-card border rounded p-2 shadow">-->
<!--      <p class="font-medium">${formatDate(props.label)}</p>-->
<!--      ${props.payload.map(entry => `-->
<!--        <p style="color: ${entry.color}">-->
<!--          ${entry.name}: ${entry.name === 'Volume' ?-->
<!--            formatVolume(entry.value) :-->
<!--            formatPrice(entry.value)}-->
<!--        </p>-->
<!--      `).join('')}-->
<!--    </div>-->
<!--  `-->
<!--}-->
<!--</script>-->


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