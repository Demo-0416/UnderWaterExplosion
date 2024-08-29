<template>
    <div ref="chartRef" class="my-chart"></div>
  </template>
  
  <script setup>
  import { ref, onMounted, watch } from 'vue';
  import * as echarts from 'echarts';
  import { CanvasRenderer } from 'echarts/renderers';
  import { GridComponent, TooltipComponent } from 'echarts/components';
  import 'echarts-gl';
  
  echarts.use([CanvasRenderer, GridComponent, TooltipComponent]);
  
  const props = defineProps({
    chartOptions: {
      type: Object,
      required: true
    }
  });
  
  const chartRef = ref(null);
  let chartInstance = null;
  
  onMounted(() => {
    chartInstance = echarts.init(chartRef.value);
    chartInstance.setOption(props.chartOptions);
  
    window.addEventListener('resize', () => {
      chartInstance.resize();
    });
  
    watch(() => chartRef.value.innerHTML, () => {
      chartInstance.resize();
    });
  });
 
// 监听 chartOptions 的变化
watch(() => props.chartOptions, (newOptions) => {
  if (chartInstance) {
    chartInstance.setOption(newOptions);
  }
}, { deep: true });
  </script>
  
  <style scoped>
  .my-chart {
    width: 95%;
    height: 100%;
    margin-left: 5px;
  }
  </style>
  