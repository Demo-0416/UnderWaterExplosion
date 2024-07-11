<template>
    <div class="main-container">
      <el-steps style="max-width: 600px" :active="active" finish-status="success" simple>
        <el-step title="Step 1" :status="active === 1 ? 'success' : 'process'" @click="handleStepClick(1)" />
        <el-step title="Step 2" :status="active === 2 ? 'success' : 'process'" @click="handleStepClick(2)" />
        <el-step title="Step 3" :status="active === 3 ? 'success' : 'process'" @click="handleStepClick(3)" />
      </el-steps>

      <el-text>时序特征</el-text>
      <VueDraggableNext  class="charts-container">
        <div v-for="(chart, index) in dir1charts" :key="chart.id" class="chart-item">
          
            <MyChart v-if="selected1Charts[index]" :chartOptions="chart.options" />
         
        </div> 
      </VueDraggableNext>
      <el-text>自由场压力</el-text>
      <VueDraggableNext  class="charts-container">
        <div v-for="(chart, index) in dir1charts" :key="chart.id" class="chart-item">
          <MyChart :chartOptions="chart.options"></MyChart>
        </div> 
      </VueDraggableNext>
    </div>
  </template>
  
  <script setup>
  import { ref,defineProps,onMounted } from 'vue';
  import { VueDraggableNext } from 'vue-draggable-next';

  import MyChart from '@/components/Mychart.vue';

  const active = ref(1);
  const handleStepClick = (index) => {  

    active.value = index;

  };
  const props = defineProps({
    selected1Charts: {
      type: Array,  
      required: true,
      default: () => [true,true]
    },
  });
  const dir1charts = ref([
    { id: 1, options:  {
      title: {
        text: '峰值', // 这里设置图表名
        left: 'center', // 标题位置
        top: 20, // 标题距离顶部距离
        textStyle: {
          color: '#333', // 字体颜色
          fontSize: 14 // 字体大小
        }
      },
      tooltip: {},  
      animation: false,
      toolbox: {  
        show: true,  
        feature: {  
            dataView: {show: true, readOnly: true},  
            magicType: {show: true, type: ['line', 'bar']},  
            restore: {show: true},  
            saveAsImage: {show: true}  
        }  
    },  
        xAxis3D: {
          type: 'category',
          data: ['一', '二', '三', '四', '五']
        },
        yAxis3D: {
          type: 'value'
        },
        zAxis3D: {
          type: 'value'
        },
        grid3D: {
          width: 'auto',
          height: 'auto',
          depth: '80%',
          viewControl: {
              // 视角控制
          }
        },
        series: [{
          type: 'bar3D',
          data: [[1, 2, 3], [2, 3, 4], [3, 4, 5], [4, 5, 6], [5, 6, 7]],
          // 其他配置项
        }]
      } },
    { id: 2, name: 'Chart 2', options: {  
        tooltip: {},  
        animation: false,
        toolbox: {  
        show: true,  
        feature: {  
            dataView: {show: true, readOnly: true},  
            magicType: {show: true, type: ['line', 'bar', 'tiled']},  
            restore: {show: true},  
            saveAsImage: {show: true}  
        }  
    },  
        grid: {  
          width: 'auto',
          height: 'auto', 
          y: '10%'  
        },  
        xAxis: {  
          type: 'category',  
          data: ['Time 1', 'Time 2', 'Time 3', 'Time 4', 'Time 5'] // 时间轴  
        },  
        yAxis: {  
          type: 'category',  
          data: ['Freq 1', 'Freq 2', 'Freq 3', 'Freq 4', 'Freq 5'] // 频率轴  
        },  
        visualMap: {  
          min: 0,  
          max: 100,  
          calculable: true,  
          orient: 'horizontal',  
          left: 'center',  
          bottom: '0%'  
        },  
        series: [{  
          name: 'Spectrogram',  
          type: 'heatmap',  
          data: [  
            // 这里的数据应该是一个二维数组，表示不同时间和频率下的强度  
            [5, 1, 0, 0, 0],  
            [0, 2, 0, 39, 10],  
            [0, 0, 0, 0, 0],  
            [0, 0, 0, 0, 0],  
            [0, 0, 0, 0, 0]  
          ],  
          label: {  
            show: true  
          },  
          emphasis: {  
            itemStyle: {  
              shadowBlur: 10,  
              shadowColor: 'rgba(0, 0, 0, 0.5)'  
            }  
          }  
        }],
          
      } },
      { id: 3, name: 'Chart 3', options: {  
        tooltip: {},  
        animation: false,
        toolbox: {  
        show: true,  
        feature: {  
            dataView: {show: true, readOnly: true},  
            magicType: {show: true, type: ['line', 'bar']},  
            restore: {show: true},  
            saveAsImage: {show: true}  
        }  
    },  
        grid: {  
          width: 'auto',
          height: 'auto', 
          y: '10%'  
        },  
        xAxis: {  
          type: 'category',  
          data: ['Time 1', 'Time 2', 'Time 3', 'Time 4', 'Time 5'] // 时间轴  
        },  
        yAxis: {  
          type: 'category',  
          data: ['Freq 1', 'Freq 2', 'Freq 3', 'Freq 4', 'Freq 5'] // 频率轴  
        },  
        visualMap: {  
          min: 0,  
          max: 100,  
          calculable: true,  
          orient: 'horizontal',  
          left: 'center',  
          bottom: '0%'  
        },  
        series: [{  
          name: 'Spectrogram',  
          type: 'heatmap',  
          data: [  
            // 这里的数据应该是一个二维数组，表示不同时间和频率下的强度  
            [5, 1, 0, 0, 0],  
            [0, 2, 0, 39, 10],  
            [0, 0, 0, 0, 0],  
            [0, 0, 0, 0, 0],  
            [0, 0, 0, 0, 0]  
          ],  
          label: {  
            show: true  
          },  
          emphasis: {  
            itemStyle: {  
              shadowBlur: 10,  
              shadowColor: 'rgba(0, 0, 0, 0.5)'  
            }  
          }  
        }],
          
      } },
    { id: 4, name: 'Chart 3', options: {  
        tooltip: {},  
        animation: false,
        toolbox: {  
        show: true,  
        feature: {  
            dataView: {show: true, readOnly: true},  
            magicType: {show: true, type: ['line', 'bar']},  
            restore: {show: true},  
            saveAsImage: {show: true}  
        }  
    },  
        grid: {  
          width: 'auto',
          height: 'auto', 
          y: '10%'  
        },  
        xAxis: {  
          type: 'category',  
          data: ['Time 1', 'Time 2', 'Time 3', 'Time 4', 'Time 5'] // 时间轴  
        },  
        yAxis: {  
          type: 'category',  
          data: ['Freq 1', 'Freq 2', 'Freq 3', 'Freq 4', 'Freq 5'] // 频率轴  
        },  
        visualMap: {  
          min: 0,  
          max: 100,  
          calculable: true,  
          orient: 'horizontal',  
          left: 'center',  
          bottom: '0%'  
        },  
        series: [{  
          name: 'Spectrogram',  
          type: 'heatmap',  
          data: [  
            // 这里的数据应该是一个二维数组，表示不同时间和频率下的强度  
            [5, 1, 0, 0, 0],  
            [0, 2, 0, 39, 10],  
            [0, 0, 0, 0, 0],  
            [0, 0, 0, 0, 0],  
            [0, 0, 0, 0, 0]  
          ],  
          label: {  
            show: true  
          },  
          emphasis: {  
            itemStyle: {  
              shadowBlur: 10,  
              shadowColor: 'rgba(0, 0, 0, 0.5)'  
            }  
          }  
        }],
          
      } },
  ]);
  
  const onDragEnd = () => {

  };  
  onMounted(() => {
    console.log(props.select1Chart);

  });
 
  </script>
  
  <style scoped>
  .charts-container {  
    display: flex; /* 启用Flexbox */  
    flex-wrap: wrap; /* 允许子元素换行 */  
    justify-content: flex-start; /* 水平对齐方式，这里是从左到右 */  
    margin-bottom: 30px;
  } 
  
  .chart-item {
    flex: 1 1 33.33%; /* 一行最多放置三个图表 */
    max-width: 33.33%; /* 图表的宽度 */
    height: 350px; /* 设置图表高度 */
  }


@media (max-width: 600px) {  
  .chart-item {  
      /* 在非常小的屏幕上图表占据整行 */  
      flex: 1 1 100%;  
      /* 可能需要调整高度或其他样式以适应全宽显示 */  
  }  }
  </style>
  