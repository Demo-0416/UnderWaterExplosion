<template>
  <div class="main-container">
    <el-button type="primary" @click="generateData">生成数据</el-button>
    <el-button type="primary" @click="fetchData">获取数据</el-button>

    <VueDraggableNext class="charts-container">
      <div v-for="(chart, index) in Strain_Charts" :key="chart.id" class="chart-item">
        
        <MyChart :chartOptions="chart.options" />

      </div>
    </VueDraggableNext>
    <VueDraggableNext class="charts-container">
      <div v-for="(chart, index) in Pressure_Charts" :key="chart.id" class="chart-item">
        
        <MyChart :chartOptions="chart.options" />

      </div>
    </VueDraggableNext>
    <VueDraggableNext class="charts-container">
      <div v-for="(chart, index) in Temperature_Charts" :key="chart.id" class="chart-item">
        
        <MyChart :chartOptions="chart.options" />

      </div>
    </VueDraggableNext>
    <VueDraggableNext class="charts-container">
      <div v-for="(chart, index) in Acc_Charts" :key="chart.id" class="chart-item">
        
        <MyChart :chartOptions="chart.options" />

      </div>
    </VueDraggableNext>
    <el-text>时序特征</el-text>
    <VueDraggableNext class="charts-container">
      <div v-for="(chart, index) in dir1charts" v-show="selected1Charts[index]" :key="chart.id" class="chart-item">

        <MyChart :chartOptions="chart.options" />

      </div>
    </VueDraggableNext>
   
  </div>
</template>

<script setup>
import { ref, defineProps, onMounted,watch } from 'vue';
import { VueDraggableNext } from 'vue-draggable-next';
import { ElMessage } from 'element-plus';
import MyChart from '@/components/Mychart.vue';
import * as echarts from 'echarts';
import axios from 'axios';




const Acceleration_data = ref([]);
const Acc_Charts = ref([]);

const Temperature_data = ref([]);
const Temperature_Charts = ref([]);

const Pressure_data = ref([]);
const Pressure_Charts = ref([]);

const Strain_data = ref([]);
const Strain_Charts = ref([]);
const props = defineProps({
  selected1Charts: {
    type: Array,
    required: true,
    default: () => [true, true]
  },
});

const dataZoomOpts1 = [
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
    brushSelect: true,
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
const generateData = () => {
  try {
    const response = axios.get('http://127.0.0.1:8000/data_management/stream_sensor_data')
    console.log(response);
  }
  catch (error) {
    console.error(error);
  }
}
const fetchData = async () => {
 
  try {
    const test_param = {
      Year: '2024',
      Exp_Name: 'test1',
    }
    console.log(test_param);
    // const response = await axios.get('http://127.0.0.1:8000/data_management/get_ori_data/',{
    //   params: test_param
    // });
    const response = await axios.get('http://127.0.0.1:8000/data_process/consume_sensor_data')
    console.log(response.data);
    Acceleration_data.value = response.data.data.Acceleration;
    Temperature_data.value = response.data.data.Temperature;
    Pressure_data.value = response.data.data.Pressure;
    Strain_data.value = response.data.data.Strain;
    ElMessage.success('获取数据成功');
  } catch (error) {
    console.error(error);
  }
  
};

onMounted(() => {
  // console.log(props.select1Chart);
 
  console.log(props.select1Charts);

});
 // 监听 Acceleration_data 的变化
watch(Acceleration_data, (newVal) => {
      Acc_Charts.value  = (() => {

const charts = [];
 for (let sensor_data of Acceleration_data.value) {
  console.log(sensor_data);
  const chart = {
    id: sensor_data.SensorId,
    options: {
      title: {
        text: sensor_data.Type, // 这里设置图表名
        left: 'center', // 标题位置
        top: 20, // 标题距离顶部距离
        textStyle: {
          color: '#333', // 字体颜色
          fontSize: 14 // 字体大小
        }
      },
      grid: {
      width: 'auto',
      height: 'auto',
      y: '10%'
    },
      tooltip: {},
      animation: false,
      toolbox: {
        show: true,
        feature: {
          dataView: { show: true, readOnly: true },
        //  magicType: { show: true, type: ['line', 'bar'] },
          restore: { show: true },
          saveAsImage: { show: true }
        }
      },
      xAxis: {
        type: 'value',
       
        name: '时间',
      },
      yAxis: {
        type: 'value',
        name: '加速度',
      },
      series: [{
        data: sensor_data.data.map(item => [item.Time, item.Value]),
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
      }],
      dataZoom: dataZoomOpts1,
    }
  };
  charts.push(chart);
}
return charts;
})();

});
 // 监听 Pressure_data 的变化
watch(Pressure_data, (newVal) => {
      Pressure_Charts.value  = (() => {

const charts = [];
 for (let sensor_data of Pressure_data.value) {
  console.log(sensor_data);
  const chart = {
    id: sensor_data.SensorId,
    options: {
      title: {
        text: sensor_data.Type, // 这里设置图表名
        left: 'center', // 标题位置
        top: 20, // 标题距离顶部距离
        textStyle: {
          color: '#333', // 字体颜色
          fontSize: 14 // 字体大小
        }
      },
      grid: {
      width: 'auto',
      height: 'auto',
      y: '10%'
    },
      tooltip: {},
      animation: false,
      toolbox: {
        show: true,
        feature: {
          dataView: { show: true, readOnly: true },
        //  magicType: { show: true, type: ['line', 'bar'] },
          restore: { show: true },
          saveAsImage: { show: true }
        }
      },
      xAxis: {
        type: 'value',
       
        name: '时间',
      },
      yAxis: {
        type: 'value',
        name: '加速度',
      },
      series: [{
        data: sensor_data.data.map(item => [item.Time, item.Value]),
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
      }],
      dataZoom: dataZoomOpts1,
    }
  };
  charts.push(chart);
}
return charts;
})();

});

 // 监听 Strain_data 的变化
watch(Strain_data, (newVal) => {
      Strain_Charts.value  = (() => {

const charts = [];
 for (let sensor_data of Strain_data.value) {
  console.log(sensor_data);
  const chart = {
    id: sensor_data.SensorId,
    options: {
      title: {
        text: sensor_data.Type, // 这里设置图表名
        left: 'center', // 标题位置
        top: 20, // 标题距离顶部距离
        textStyle: {
          color: '#333', // 字体颜色
          fontSize: 14 // 字体大小
        }
      },
      grid: {
      width: 'auto',
      height: 'auto',
      y: '10%'
    },
      tooltip: {},
      animation: false,
      toolbox: {
        show: true,
        feature: {
          dataView: { show: true, readOnly: true },
        //  magicType: { show: true, type: ['line', 'bar'] },
          restore: { show: true },
          saveAsImage: { show: true }
        }
      },
      xAxis: {
        type: 'value',
       
        name: '时间',
      },
      yAxis: {
        type: 'value',
        name: '加速度',
      },
      series: [{
        data: sensor_data.data.map(item => [item.Time, item.Value]),
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
      }],
      dataZoom: dataZoomOpts1,
    }
  };
  charts.push(chart);
}
return charts;
})();

});
 // 监听 Temperature_data
watch(Temperature_data, (newVal) => {
      Temperature_Charts.value  = (() => {

const charts = [];
 for (let sensor_data of Temperature_data.value) {
  console.log(sensor_data);
  const chart = {
    id: sensor_data.SensorId,
    options: {
      title: {
        text: sensor_data.Type, // 这里设置图表名
        left: 'center', // 标题位置
        top: 20, // 标题距离顶部距离
        textStyle: {
          color: '#333', // 字体颜色
          fontSize: 14 // 字体大小
        }
      },
      grid: {
      width: 'auto',
      height: 'auto',
      y: '10%'
    },
      tooltip: {},
      animation: false,
      toolbox: {
        show: true,
        feature: {
          dataView: { show: true, readOnly: true },
        //  magicType: { show: true, type: ['line', 'bar'] },
          restore: { show: true },
          saveAsImage: { show: true }
        }
      },
      xAxis: {
        type: 'value',
       
        name: '时间',
      },
      yAxis: {
        type: 'value',
        name: '加速度',
      },
      series: [{
        data: sensor_data.data.map(item => [item.Time, item.Value]),
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
      }],
      dataZoom: dataZoomOpts1,
    }
  };
  charts.push(chart);
}
return charts;
})();

});



const dataZoomOpts2 = [
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
  }]
const dir1charts = ref([
  {
    id: 1, options: {
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
          dataView: { show: true, readOnly: true },
          magicType: { show: true, type: ['line', 'bar'] },
          restore: { show: true },
          saveAsImage: { show: true }
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
    }
  },
  {
    id: 2, name: 'Chart 2', options: {
      tooltip: {},
      animation: false,
      toolbox: {
        show: true,
        feature: {
          dataView: { show: true, readOnly: true },
          magicType: { show: true, type: ['line', 'bar', 'tiled'] },
          restore: { show: true },
          saveAsImage: { show: true }
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

    }
  },
  {
    id: 3, name: 'Chart 3', options: {
      tooltip: {},
      animation: false,
      toolbox: {
        show: true,
        feature: {
          dataView: { show: true, readOnly: true },
          magicType: { show: true, type: ['line', 'bar'] },
          restore: { show: true },
          saveAsImage: { show: true }
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

    }
  },
  {
    id: 4, name: 'Chart 3', options: {
      tooltip: {},
      animation: false,
      toolbox: {
        show: true,
        feature: {
          dataView: { show: true, readOnly: true },
          magicType: { show: true, type: ['line', 'bar'] },
          restore: { show: true },
          saveAsImage: { show: true }
        }
      },
      grid: {
        width: 'auto',
        height: 'auto',
        y: '10%'
      },
      xAxis: {
        type: 'value',

      },
      yAxis: {
        type: 'value',
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
        type: 'line',
        stack: 'all', // 堆叠图的设置
        areaStyle: {},// 面积图的设置
        data: [1, 2, 3, 4, 5], // 线的数据

        data: [
          // 这里的数据应该是一个二维数组，表示不同时间和频率下的强度  
          [0, 1],
          [1, 2],
          [2, 6],
          [3, 4],
          [4, 3],
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

    }
  },
]);


const onDragEnd = () => {
 const test_data = [[-1.2,3],[-2.4,7],[8.5,6],[4.3,5],[5.4,5]];
};


</script>

<style scoped>
.charts-container {
  display: flex;
  /* 启用Flexbox */
  flex-wrap: wrap;
  /* 允许子元素换行 */
  justify-content: flex-start;
  /* 水平对齐方式，这里是从左到右 */
  margin-bottom: 30px;
}

.chart-item {
  flex: 1 1 48%;
  /* 一行最多放置两个图表 */
  margin-left: 1%;
  /* 图表之间的间距 */
  max-width: 49%;
  /* 图表的宽度 */
  height: 560px;
  /* 设置图表高度 */
  border: 0.5px solid #ccc;
  /* 图表的边框 */
  border-radius: 5px;
  /* 图表的圆角 */
  /*box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); /* 图表的阴影 */
  padding-bottom: 20px;

}


@media (max-width: 600px) {
  .chart-item {
    /* 在非常小的屏幕上图表占据整行 */
    flex: 1 1 100%;
    /* 可能需要调整高度或其他样式以适应全宽显示 */
  }
}
</style>