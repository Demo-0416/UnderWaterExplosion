<template>
    <div ref="chartRef" style="width: 100%; height: 600px;"></div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue';
  import * as echarts from 'echarts';
  import { CanvasRenderer } from 'echarts/renderers';
  import { GridComponent, TooltipComponent } from 'echarts/components';
  import 'echarts-gl';

  
  echarts.use([CanvasRenderer, GridComponent, TooltipComponent]);
  const chartRef = ref(null);
  
  // 假设你需要读取的两列数据的索引分别是0和1
  const columnIndex1 = 0;
  const columnIndex2 = 1;

  let chartInstance = null
  onMounted(async () => {
    const response = await fetch('./Acceleration_0.csv');
    const text = await response.text();
    const lines = text.trim().split('\n');
  
    // 跳过第一行数据名称
    const data = lines.slice(1).map(line => {
      const values = line.split(',');
      return {
        value1: parseFloat(values[0]), 
        value2: parseFloat(values[4]), 
      };
    });

    // 准备X轴数据，这里假设X轴数据是行号
    
    chartInstance = echarts.init(chartRef.value);
   
    const option = {
      title: {
        text: 'ECharts 示例'
      },
      tooltip: {
        trigger: 'axis'
      },
        grid: {  
          width: 'auto',
          height: 'auto', 
          y: '10%'  
        }, 
      xAxis: {
        type: 'value',
        name: '时间',
      },
      yAxis: {
        type: 'value',
        name: '加速度',
      },
      series: [
        {
          name: '数据1',
          type: 'line',
          smooth: true,
          data: data.map(item => [item.value1, item.value2]),  
        }
      ],
      dataZoom: [  
        {  
          type: 'slider', // 滑动条类型  
          show: true, // 显示滑动条  
          xAxisIndex: [0], // 控制X轴的缩放和滑动  
          start: 0, // 数据窗口的起始百分比  
          end: 40 // 数据窗口的结束百分比  
        },  
        {  
          type: 'inside', // 内置的缩放控制器  
          start: 0,  
          end: 40  
        }  
      ]  
    };
    
    const myChart = echarts.init(chartRef.value);
    chartInstance.setOption(option);
    myChart.setOption(option);
  });
  
  </script>