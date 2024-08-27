<template>
  <div ref="chartRef" style="width: 100%; height: 400px;"></div>
  <div ref="chartRef1" style="width: 100%; height: 400px;"></div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import * as echarts from 'echarts';
import { CanvasRenderer } from 'echarts/renderers';
import { GridComponent, TooltipComponent } from 'echarts/components';
import 'echarts-gl';



echarts.use([CanvasRenderer, GridComponent, TooltipComponent]);
const chartRef = ref(null);

const chartRef1 = ref(null);

let chartInstance = null
let chartInstance1 = null
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
  chartInstance1 = echarts.init(chartRef1.value);

  const option = {
    animation: true, // 是否开启动画
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
        showSymbol: false,
        clip: true,
        color: '#45cc93',
        markLine: {
          symbol: ['none', 'none'],
          label: { show: true },
        },
        data: data.map(item => [item.value1, item.value2]),
      }
    ],
    dataZoom: [
      {
        type: 'slider', // 滑动条类型  
        show: true, // 显示滑动条  
        xAxisIndex: [0], // 控制X轴的缩放和滑动  
        start: 0, // 数据窗口的起始百分比  
        end: 40,// 数据窗口的结束百分比 
        textStyle: {
          color: 'blue',
          fontSize: 12,
        },
        backgroundColor: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          {
            offset: 0,
            color: 'rgb(128, 255, 165)'
          },
          {
            offset: 1,
            color: 'rgb(1, 191, 236)'
          }
        ]),
        dataBackground: {
          lineStyle: {
            color: 'red',

            opacity: 0.62, //数据阴影的线条透明度


          },
          areaStyle: {
            color: 'green',
            shadowBlur: 0,
            opacity: 0,
          },

        },
        borderRadius: 5,
        borderColor: 'red',


        handleStyle: {
          borderColor: 'red',
          borderWidth: 2,
        },



        brushSelect: false,
        brushStyle: {
          color: '#fff',
          borderColor: 'blue',
        },
        emphasis: {
          handleStyle: {
            color: 'red',
          },
          moveHandleStyle: {
            color: 'red',
          }
        }


      },
      {
        type: 'inside', // 内置的缩放控制器  
        start: 0,
        end: 40
      }
    ]
  };
  const option1 = {

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
        name: '数据2',
        type: 'line',
        smooth: true, // 是否平滑曲线
        showSymbol: false, // 是否显示标记点
        clip: true, // 是否裁剪
        stack: 'all', // 堆叠图的设置
        areaStyle: {

          opacity: 0.5, // 透明度
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
            offset: 0,
            color: 'rgba(255, 0.2)'
          }, {
            offset: 1,
            color: 'rgba(255, 0.2)'
          }]) // 渐变颜色 
          

          // color: 'rgba(255, 0.2)' // 单一颜色

        }, // 区域填充样式
        markLine: {
          symbol: ['none', 'none'],// 标记线的形状
          label: { show: true },
        },
        data: data.map(item => [item.value1, item.value2]),
      }
    ],
    dataZoom: [
      {
        type: 'slider', // 滑动条类型  
        show: true, // 显示滑动条  
        xAxisIndex: [0], // 控制X轴的缩放和滑动  
        start: 0, // 数据窗口的起始百分比  
        end: 40,// 数据窗口的结束百分比  
        dataBackground: {//数据阴影的样式。
          lineStyle: { color: '#b3dd98' },//阴影的线条样式
          areaStyle: { color: 'red' },//阴影的填充样式
        },
        backgroundcolor: new echarts.graphic.RadialGradient(0.3, 0.3, 0.8, 0.8, [{
          offset: 0,
          color: 'rgba(255, 0.8)'
        }, {
          offset: 1,
          color: 'rgba(255, 0.2)'


        }]), // 背景颜色
        selectedDataBackground: { // 选中范围的背景样式  
          lineStyle: {
            color: '#e3f3da' // 选中范围的边框颜色  
          },
          areaStyle: {
            color: '#d0d8e2' // 选中范围的填充颜色  
          }
        },

        moveHandleSize: 7,
        moveHandleStyle: {

          color: 'red', // 手柄的颜色  
          borderColor: '#5793f3', // 手柄边框的颜色  
          borderWidth: 1, // 手柄边框的宽度   
        },
        sliderStyle: {  
                backgroundColor: '#eceeef', // 滑块背景颜色  
                borderColor: '#a7b7cb', // 滑块边框颜色  
                fillerColor: '#d0d8e2', // 选中范围的填充颜色  
                handleStyle: { // 滑块手柄的样式  
                    color: '#1E90FF', // 手柄颜色  
                    borderColor: '#1E90FF', // 手柄边框颜色  
                    borderWidth: 2, // 手柄边框宽度  
                    shadowBlur: 10, // 阴影的模糊大小  
                    shadowColor: 'rgba(0, 0, 0, 0.5)' // 阴影颜色  
                }  
            },  
      },
      {
        type: 'inside', // 内置的缩放控制器  
        start: 0,
        end: 40
      }
    ]
  };
  chartInstance.setOption(option);
  chartInstance1.setOption(option1);



});

</script>