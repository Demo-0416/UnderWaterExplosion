<template>
  <!-- <div class="common-layout" :style="themeStyles"> -->
  <el-container>
    <el-header>
      <el-row style="background-color: #c8e0fa;">
        <el-col :span="6" :offset="9"
          style="height: 60px;display: flex;text-align: center;justify-content: center;align-items: center;font-size: 18px;font-weight: bold;color: #303133;letter-spacing: 10px;">数据分析系统</el-col>
        <!-- <el-col :span="2" :offset="4" style="display: flex;align-items: center;font-size: 14px;">欢迎您，{{name}}</el-col>
          <el-col :span="1" :offset="2"><el-avatar :src="imgsrc" style="width: 48; margin-top: 2px;"
              :fit="fit" /></el-col> -->

      </el-row>

      <el-row style="margin-left: 6px;margin-top: 10px;margin-bottom: 10px;margin-right: 6px;">
        <el-col :span="4">
          <!-- <el-select v-model="value" >
            <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value"
              :disabled="item.disabled" />
            </el-select> -->
          <el-cascader style="width: 100%;" v-model="value" :options="options" @change="handleChange" />
        </el-col>
        <el-col :span="20"> <el-steps style="height:6px" :active="active" finish-status="success" simple>
            <el-step title="原始数据" :status="active === 1 ? 'success' : 'process'" @click="handleStepClick(1)" />
            <el-step title="预处理" :status="active === 2 ? 'success' : 'process'" @click="handleStepClick(2)" />
            <el-step title="特征提取" :status="active === 3 ? 'success' : 'process'" @click="handleStepClick(3)" />
          </el-steps>
        </el-col>
      </el-row>


    </el-header>
    <el-container>
      <el-aside width="180px">
        <NavList @update:checked1Charts="updateSelect1Charts" @update:checked2Charts="updateSelect2Charts"
          @update:checked3Charts="updateSelect3Charts" @update:checked4Charts="updateSelect4Charts" />
        <!-- <Elmenu1/> -->
      </el-aside>
      <el-main>
        <!-- <mymain :selected1Charts="selected1Charts" /> -->

        <!-- 原始数据 -->
        <div class="main-container" v-if="active == 1 ">
          <h3 v-if="dir1charts == true">温度</h3>
          <VueDraggableNext class="charts-container" v-if="dir1charts == true">
            <div v-for="(chart, index) in Ori_Temperature_Charts" :key="chart.id" class="chart-item">
              <MyChart :chartOptions="chart.options" />
            </div>
          </VueDraggableNext>
          
          <VueDraggableNext class="charts-container" v-if="dir2charts == true">
            <h3>应变</h3>
            <div v-for="(chart, index) in Ori_Strain_Charts" :key="chart.id" class="chart-item">
              <MyChart :chartOptions="chart.options" />
            </div>
          </VueDraggableNext>
          
          <VueDraggableNext class="charts-container"  v-if="dir3charts == true">
            <h3>自由场压力</h3>
            <div v-for="(chart, index) in Ori_Pressure_Charts" :key="chart.id" class="chart-item">
              <MyChart :chartOptions="chart.options" />
            </div>
          </VueDraggableNext>
          
          <VueDraggableNext class="charts-container"  v-if="dir4charts == true">
            <h3>加速度</h3>
            <div v-for="(chart, index) in Ori_Acc_Charts" :key="chart.id" class="chart-item">
              <MyChart :chartOptions="chart.options" />
            </div>
          </VueDraggableNext>
        </div>

        <!-- 数据预处理 -->
        <div class="main-container" v-else-if="active == 2">
          <VueDraggableNext class="charts-container" v-if="dir1charts == true">
            <h3>温度</h3>
            <div v-for="(chart, index) in Temperature_Charts" :key="chart.id" class="chart-item">
              <MyChart :chartOptions="chart.options" />
            </div>
          </VueDraggableNext>
          
          <VueDraggableNext class="charts-container" v-if="dir2charts == true">
            <h3>应变</h3>
            <div v-for="(chart, index) in Strain_Charts" :key="chart.id" class="chart-item">
              <MyChart :chartOptions="chart.options" />
            </div>
          </VueDraggableNext>
          
          <VueDraggableNext class="charts-container" v-if="dir3charts == true">
            <h3>自由场压力</h3>
            <div v-for="(chart, index) in Pressure_Charts" :key="chart.id" class="chart-item">
              <MyChart :chartOptions="chart.options" />
            </div>
          </VueDraggableNext>
          
          <VueDraggableNext class="charts-container" v-if="dir4charts == true">
            <h3>加速度</h3>
            <div v-for="(chart, index) in Acc_Charts" :key="chart.id" class="chart-item">
              <MyChart :chartOptions="chart.options" />
            </div>
          </VueDraggableNext>

        </div>

        <!-- 提取数据特征 -->
        <div class="main-container" v-else-if="active == 3">
          
        
        </div>

      </el-main>
    </el-container>
  </el-container>
  <!-- </div> -->
</template>
<script setup>
import NavList from '@/components/NavList.vue';
// import mymain from '@/components/Main.vue'
import blue3 from '@/assets/blue3.webp'
import { ref, onMounted, watch } from 'vue';
import { VueDraggableNext } from 'vue-draggable-next';
import { ElMessage } from 'element-plus';
import MyChart from '@/components/Mychart.vue';
import * as echarts from 'echarts';
import axios from 'axios';
import { useRoute } from 'vue-router';

const route = useRoute();
const test_param = route.query.value;
const imgsrc = ref(blue3)
const fit = ref('contain')
const dialogVisible = ref(true)
const selected1Charts = ref([])
const dir1charts = ref([])
const selected2Charts = ref([])
const dir2charts = ref([])
const selected3Charts = ref([])
const dir3charts = ref([])
const selected4Charts = ref([])
const dir4charts = ref([])
const updateSelect1Charts = (checked1Charts) => {
  console.log(checked1Charts);
  selected1Charts.value = checked1Charts;
  dir1charts.value = checked1Charts.every(Boolean);
}
const updateSelect2Charts = (checked2Charts) => {
  selected2Charts.value = checked2Charts;
  dir2charts.value = checked2Charts.every(Boolean);
}
const updateSelect3Charts = (checked3Charts) => {
  selected3Charts.value = checked3Charts;
  dir3charts.value = checked3Charts.every(Boolean);
}
const updateSelect4Charts = (checked4Charts) => {
  selected4Charts.value = checked4Charts;
  dir4charts.value = checked4Charts.every(Boolean);
}

const value = ref(test_param);

const options = [
  {
    value: '2024',
    label: '2024',
    children: [{
      value: 'test1',
      label: '试验1',
    },
    {
      value: 'test2',
      label: '试验2',
    },
    {
      value: 'test3',
      label: '试验3',
    },
    {
      value: 'test4',
      label: '试验4',
    },
    {
      value: 'test5',
      label: '试验5',
    },]
  },
  {
    value: '2023',
    label: '2023',
    children: [{
      value: 'test1',
      label: '试验1',
    },
    {
      value: 'test2',
      label: '试验2',
    },
    {
      value: 'test3',
      label: '试验3',
    },
    {
      value: 'test4',
      label: '试验4',
    },
    {
      value: 'test5',
      label: '试验5',
    },]
  },
  {
    value: '2022',
    label: '2022',
    children: [{
      value: 'test1',
      label: '试验1',
    },
    {
      value: 'test2',
      label: '试验2',
    },
    {
      value: 'test3',
      label: '试验3',
    },
    {
      value: 'test4',
      label: '试验4',
    },
    {
      value: 'test5',
      label: '试验5',
    },]
  },
  {
    value: '2021',
    label: '2021',
    children: [{
      value: 'test1',
      label: '试验1',
    },
    {
      value: 'test2',
      label: '试验2',
    },
    {
      value: 'test3',
      label: '试验3',
    },
    {
      value: 'test4',
      label: '试验4',
    },
    {
      value: 'test5',
      label: '试验5',
    },]
  },
]
const active = ref(1);
const getOrder = (choice) => {
  console.log("choice", choice);
  if (choice == 1) {
    return ['A', 'B', 'C'];
  }
  if (choice == 2) {
    return ['B', 'C', 'A'];
  }
  if (choice == 3) {
    return ['C', 'A', 'B'];
  }
  return ['A', 'B', 'C'];
};
const handleStepClick = (index) => {
  active.value = index;
};

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

//原始数据
const Ori_Acceleration_data = ref([]);
const Ori_Acc_Charts = ref([]);

const Ori_Temperature_data = ref([]);
const Ori_Temperature_Charts = ref([]);

const Ori_Pressure_data = ref([]);
const Ori_Pressure_Charts = ref([]);

const Ori_Strain_data = ref([]);
const Ori_Strain_Charts = ref([]);


//预处理数据
const Acceleration_data = ref([]);
const Acc_Charts = ref([]);

const Temperature_data = ref([]);
const Temperature_Charts = ref([]);

const Pressure_data = ref([]);
const Pressure_Charts = ref([]);

const Strain_data = ref([]);
const Strain_Charts = ref([]);

//数据特征
const Feature_Acceleration_data = ref([]);
const Feature_Acc_Charts = ref([]);

const Feature_Temperature_data = ref([]);
const Feature_Temperature_Charts = ref([]);

const Feature_Pressure_data = ref([]);
const Feature_Pressure_Charts = ref([]);

const Feature_Strain_data = ref([]);
const Feature_Strain_Charts = ref([]);



const fetchData = async () => {
  const order = getOrder(active.value);
  console.log(order);


  console.log(test_param);
  try {
    for (const letter of order) {
      let response;
      switch (letter) {
        case 'A':
          try {
            const ori_param = {
              Year: value.value[0],
              Exp_Name: value.value[1],
              state: '原始数据',
            }
            const response = await axios.get('http://127.0.0.1:8000/data_management/get_data/', {
              params:  {
              Year: value.value[0],
              Exp_Name: value.value[1],
              state: '原始数据',
            }
            });
            if (response.data.code == 0) {
              Ori_Acceleration_data.value = response.data.data.Acceleration;
              Ori_Temperature_data.value = response.data.data.Temperature;
              Ori_Pressure_data.value = response.data.data.Pressure;
              Ori_Strain_data.value = response.data.data.Strain;
              ElMessage.success('获取数据成功');
            } else {
              ElMessage.error(response.data.message);
            }
          } catch (error) {
            ElMessage.error(error);
          }
          break;
        case 'B':
          try {
            const pre_param = {
              Year: value.value[0],
              Exp_Name: value.value[1],
              state: '预处理数据',
            }
            const response = await axios.get('http://127.0.0.1:8000/data_management/get_data/', {
              params: pre_param
            });
            if (response.data.code == 0) {
              Acceleration_data.value = response.data.data.Acceleration;
              Temperature_data.value = response.data.data.Temperature;
              Pressure_data.value = response.data.data.Pressure;
              Strain_data.value = response.data.data.Strain;
              ElMessage.success('获取数据成功');
            } else {
              ElMessage.error(response.data.message);
            }
          } catch (error) {
            ElMessage.error(error);
          }
          break;
        case 'C':
        try {
            const feature_param = {
              Year: value.value[0],
              Exp_Name: value.value[1],
              state: '特征提取',
            }
            const response = await axios.get('http://127.0.0.1:8000/data_management/get_data/', {
              params: feature_param
            });
            if (response.data.code == 0) {
              console.log(response.data.data);
              ElMessage.success('获取数据成功');
            } else {
              ElMessage.error(response.data.message);
            }
          } catch (error) {
            ElMessage.error(error);
          }
          break;
      }
    }
  } catch (error) {
    console.error('请求失败:', error);
  }
};

watch(() => value.value, (newVal) => {
  fetchData();
});

onMounted(() => {
  // console.log(props.select1Chart);
  fetchData();
});

/* 原始数据 */
// 监听 Ori_Acceleration_data 的变化
watch(Ori_Acceleration_data, (newVal) => {
  Ori_Acc_Charts.value = (() => {

    const charts = [];
    for (let sensor_data of Ori_Acceleration_data.value) {
      console.log(sensor_data);
      const chart = {
        id: sensor_data.SensorId,
        options: {
          title: {
            text: 'SensorId '+sensor_data.SensorId, // 这里设置图表名
            subtext: 'Position: '+sensor_data.Position,
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
            data: sensor_data.data,
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
// 监听 Ori_Pressure_data 的变化
watch(Ori_Pressure_data, (newVal) => {
  Ori_Pressure_Charts.value = (() => {

    const charts = [];
    for (let sensor_data of Ori_Pressure_data.value) {
      console.log(sensor_data);
      const chart = {
        id: sensor_data.SensorId,
        options: {
          title: {
            text: 'SensorId '+sensor_data.SensorId, // 这里设置图表名
            subtext: 'Position: '+sensor_data.Position,
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
            data: sensor_data.data,
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

// 监听 Ori_Strain_data 的变化
watch(Ori_Strain_data, (newVal) => {
  Ori_Strain_Charts.value = (() => {

    const charts = [];
    for (let sensor_data of Ori_Strain_data.value) {
      console.log(sensor_data);
      const chart = {
        id: sensor_data.SensorId,
        options: {
          title: {
            text: 'SensorId '+sensor_data.SensorId, // 这里设置图表名
            subtext: 'Position: '+sensor_data.Position,
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
            data: sensor_data.data,
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
// 监听 Ori_Temperature_data
watch(Ori_Temperature_data, (newVal) => {
  Ori_Temperature_Charts.value = (() => {

    const charts = [];
    for (let sensor_data of Ori_Temperature_data.value) {
      console.log(sensor_data);
      const chart = {
        id: sensor_data.SensorId,
        options: {
          title: {
            text: 'SensorId '+sensor_data.SensorId, // 这里设置图表名
            subtext: 'Position: '+sensor_data.Position,
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
            data: sensor_data.data,
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


/* 已处理数据 */
// 监听 Acceleration_data 的变化
watch(Acceleration_data, (newVal) => {
  Acc_Charts.value = (() => {

    const charts = [];
    for (let sensor_data of Acceleration_data.value) {
      console.log(sensor_data);
      const chart = {
        id: sensor_data.SensorId,
        options: {
          title: {
            text: 'SensorId '+sensor_data.SensorId, // 这里设置图表名
            subtext: 'Position: '+sensor_data.Position,
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
            data: sensor_data.data,
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
  Pressure_Charts.value = (() => {

    const charts = [];
    for (let sensor_data of Pressure_data.value) {
      console.log(sensor_data);
      const chart = {
        id: sensor_data.SensorId,
        options: {
          title: {
            text: 'SensorId '+sensor_data.SensorId, // 这里设置图表名
            subtext: 'Position: '+sensor_data.Position,
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
            data: sensor_data.data,
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
  Strain_Charts.value = (() => {

    const charts = [];
    for (let sensor_data of Strain_data.value) {
      console.log(sensor_data);
      const chart = {
        id: sensor_data.SensorId,
        options: {
          title: {
            text: 'SensorId '+sensor_data.SensorId, // 这里设置图表名
            subtext: 'Position: '+sensor_data.Position,
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
            data: sensor_data.data,
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
  Temperature_Charts.value = (() => {

    const charts = [];
    for (let sensor_data of Temperature_data.value) {
      console.log(sensor_data);
      const chart = {
        id: sensor_data.SensorId,
        options: {
          title: {
            text: 'SensorId '+sensor_data.SensorId, // 这里设置图表名
            subtext: 'Position: '+sensor_data.Position,
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
            data: sensor_data.data,
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


const onDragEnd = () => {
  const test_data = [[-1.2, 3], [-2.4, 7], [8.5, 6], [4.3, 5], [5.4, 5]];
};
</script>
<style scoped>
.el-container {
  height: 100%;
  direction: vertical;
  overflow-y: auto;
  overflow: hidden;
}

header {
  width: 100%;
  background-color: #c7c8cbd5;
  padding: 0;
  height: 125PX;
  border-bottom: 0.5px solid #dcdfe6;
}

aside {
  display: block;
  border-right: 1px solid #dcdfe6;
}

main {
  display: block;
  overflow-y: auto;
  padding: 0 0 0 1px;

}


/**.main {
  position: absolute;
  background-color: black;
  left: 275px;
  top: 70px;
  right: 20px;
}*/
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
