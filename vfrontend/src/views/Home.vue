<template>
  <!-- <div class="common-layout" :style="themeStyles"> -->
  <el-container>
    <el-header>
      <!-- <el-row style="background-color: #c8e0fa;">
        <el-col :span="6" :offset="9"
          style="height: 60px;display: flex;text-align: center;justify-content: center;align-items: center;font-size: 18px;font-weight: bold;color: #303133;letter-spacing: 10px;">数据分析系统</el-col>
      

      </el-row> -->
      <!--    <el-col :span="2" :offset="4" style="display: flex;align-items: center;font-size: 14px;">欢迎您，{{name}}</el-col>
          <el-col :span="1" :offset="2"><el-avatar :src="imgsrc" style="width: 48; margin-top: 2px;"
              :fit="fit" /></el-col> -->
    </el-header>
    <el-container>
      <el-aside width="200px">
        <!-- <NavList @update:checked1Charts="updateSelect1Charts" @update:checked2Charts="updateSelect2Charts"
          @update:checked3Charts="updateSelect3Charts" @update:checked4Charts="updateSelect4Charts" /> -->
        <!-- <Elmenu1/> -->
        <el-row style="">
          <el-col :span="20" :offset="2">
            <!-- <el-select v-model="value" >
              <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value"
                :disabled="item.disabled" />
              </el-select> -->
            <el-cascader style="width: 100%" v-model="value" :options="options" />
          </el-col>
        </el-row>
        <el-row style="">
          <el-col :span="20" :offset="2">
            <el-cascader style="width: 100%" v-model="sensor_value" :options="sensor_type_options"
              @change="fentch_ori_data" />
          </el-col>
        </el-row>
      </el-aside>
      <el-main>
        <div class="cont" v-if="isLoad">
          <div class="anim"></div>
        </div>
        <h4>原始数据</h4>
        <div class="charts-container" v-if="ori_chart_Opts && Object.keys(ori_chart_Opts).length">
          <MyChart :chartOptions="ori_chart_Opts" class="chart-item" />
        </div>
        <el-select v-model="algorithm_value" placeholder="请选择算法" style="width: 200px; margin-bottom: 10px">
          <el-option v-for="item in algorithm_options" :key="item.value" :label="item.label"
            :value="item.value" /></el-select>
        <br />
        <el-button @click="fentch_pre_data" style="margin-bottom: 15px">数据预处理</el-button>
        <br />
        <div class="charts-container" v-if="pre_chart_Opts && Object.keys(pre_chart_Opts).length">
          <MyChart :chartOptions="pre_chart_Opts" class="chart-item" />
        </div>
        <el-button @click="fentch_feature_data">提取数据特征</el-button>
        <div class="charts-container" v-if="feature_chart_Opts && Object.keys(feature_chart_Opts).length">
          <MyChart :chartOptions="feature_chart_Opts" class="chart-item" />
        </div>
      </el-main>
    </el-container>
  </el-container>
  <!-- </div> -->
</template>
<script setup>
/*
#cb3d90
*/

// import mymain from '@/components/Main.vue'
import { ref, onMounted, watch } from "vue";
import { ElMessage } from "element-plus";
import MyChart from "@/components/Mychart.vue";
import * as echarts from "echarts";
import axios from "axios";
import { useRoute } from "vue-router";
const route = useRoute();
const test_param = route.query.value;
const fit = ref("contain");
const dialogVisible = ref(true);
const isPre = ref(false);
const isFeature = ref(false);
const isOri = ref(true);

const isLoad = ref(false);

const value = ref(test_param);
const options = [
  {
    value: "2024",
    label: "2024",
    children: [
      {
        value: "test1",
        label: "试验1",
      },
      {
        value: "test2",
        label: "试验2",
      },
      {
        value: "test3",
        label: "试验3",
      },
      {
        value: "test4",
        label: "试验4",
      },
      {
        value: "test5",
        label: "试验5",
      },
    ],
  },
  {
    value: "2023",
    label: "2023",
    children: [
      {
        value: "test1",
        label: "试验1",
      },
      {
        value: "test2",
        label: "试验2",
      },
      {
        value: "test3",
        label: "试验3",
      },
      {
        value: "test4",
        label: "试验4",
      },
      {
        value: "test5",
        label: "试验5",
      },
    ],
  },
  {
    value: "2022",
    label: "2022",
    children: [
      {
        value: "test1",
        label: "试验1",
      },
      {
        value: "test2",
        label: "试验2",
      },
      {
        value: "test3",
        label: "试验3",
      },
      {
        value: "test4",
        label: "试验4",
      },
      {
        value: "test5",
        label: "试验5",
      },
    ],
  },
  {
    value: "2021",
    label: "2021",
    children: [
      {
        value: "test1",
        label: "试验1",
      },
      {
        value: "test2",
        label: "试验2",
      },
      {
        value: "test3",
        label: "试验3",
      },
      {
        value: "test4",
        label: "试验4",
      },
      {
        value: "test5",
        label: "试验5",
      },
    ],
  },
];

const sensor_value = ref([,]);
const sensor_type_options = [
  {
    value: "Acceleration",
    label: "加速度",
    children: [
      { value: "0", label: "传感器 0" },
      { value: "4", label: "传感器 4" },
      { value: "8", label: "传感器 8" },
      { value: "12", label: "传感器 12" },
      { value: "16", label: "传感器 16" },
      { value: "20", label: "传感器 20" },
      { value: "24", label: "传感器 24" },
      { value: "28", label: "传感器 28" },
      { value: "32", label: "传感器 32" },
      { value: "36", label: "传感器 36" },
      { value: "40", label: "传感器 40" },
      { value: "44", label: "传感器 44" },
      { value: "48", label: "传感器 48" },
      { value: "52", label: "传感器 52" },
      { value: "56", label: "传感器 56" },
      { value: "60", label: "传感器 60" },
      { value: "64", label: "传感器 64" },
      { value: "68", label: "传感器 68" },
      { value: "72", label: "传感器 72" },
      { value: "76", label: "传感器 76" },
      { value: "80", label: "传感器 80" },
      { value: "84", label: "传感器 84" },
      { value: "88", label: "传感器 88" },
      { value: "92", label: "传感器 92" },
      { value: "96", label: "传感器 96" },
    ],
  },
  {
    value: "Strain",
    label: "应变",
    children: [
      { value: "1", label: "传感器 1" },
      { value: "5", label: "传感器 5" },
      { value: "9", label: "传感器 9" },
      { value: "13", label: "传感器 13" },
      { value: "17", label: "传感器 17" },
      { value: "21", label: "传感器 21" },
      { value: "25", label: "传感器 25" },
      { value: "29", label: "传感器 29" },
      { value: "33", label: "传感器 33" },
      { value: "37", label: "传感器 37" },
      { value: "41", label: "传感器 41" },
      { value: "45", label: "传感器 45" },
      { value: "49", label: "传感器 49" },
      { value: "53", label: "传感器 53" },
      { value: "57", label: "传感器 57" },
      { value: "61", label: "传感器 61" },
      { value: "65", label: "传感器 65" },
      { value: "69", label: "传感器 69" },
      { value: "73", label: "传感器 73" },
      { value: "77", label: "传感器 77" },
      { value: "81", label: "传感器 81" },
      { value: "85", label: "传感器 85" },
      { value: "89", label: "传感器 89" },
      { value: "93", label: "传感器 93" },
      { value: "97", label: "传感器 97" },
    ],
  },
  {
    value: "Temperature",
    label: "温度",
    children: [
      { value: "2", label: "传感器 2" },
      { value: "6", label: "传感器 6" },
      { value: "10", label: "传感器 10" },
      { value: "14", label: "传感器 14" },
      { value: "18", label: "传感器 18" },
      { value: "22", label: "传感器 22" },
      { value: "26", label: "传感器 26" },
      { value: "30", label: "传感器 30" },
      { value: "34", label: "传感器 34" },
      { value: "38", label: "传感器 38" },
      { value: "42", label: "传感器 42" },
      { value: "46", label: "传感器 46" },
      { value: "50", label: "传感器 50" },
      { value: "54", label: "传感器 54" },
      { value: "58", label: "传感器 58" },
      { value: "62", label: "传感器 62" },
      { value: "66", label: "传感器 66" },
      { value: "70", label: "传感器 70" },
      { value: "74", label: "传感器 74" },
      { value: "78", label: "传感器 78" },
      { value: "82", label: "传感器 82" },
      { value: "86", label: "传感器 86" },
      { value: "90", label: "传感器 90" },
      { value: "94", label: "传感器 94" },
      { value: "98", label: "传感器 98" },
    ],
  },
  {
    value: "Pressure",
    label: "压力",
    children: [
      { value: "3", label: "传感器 3" },
      { value: "7", label: "传感器 7" },
      { value: "11", label: "传感器 11" },
      { value: "15", label: "传感器 15" },
      { value: "19", label: "传感器 19" },
      { value: "23", label: "传感器 23" },
      { value: "27", label: "传感器 27" },
      { value: "31", label: "传感器 31" },
      { value: "35", label: "传感器 35" },
      { value: "39", label: "传感器 39" },
      { value: "43", label: "传感器 43" },
      { value: "47", label: "传感器 47" },
      { value: "51", label: "传感器 51" },
      { value: "55", label: "传感器 55" },
      { value: "59", label: "传感器 59" },
      { value: "63", label: "传感器 63" },
      { value: "67", label: "传感器 67" },
      { value: "71", label: "传感器 71" },
      { value: "75", label: "传感器 75" },
      { value: "79", label: "传感器 79" },
      { value: "83", label: "传感器 83" },
      { value: "87", label: "传感器 87" },
      { value: "91", label: "传感器 91" },
      { value: "95", label: "传感器 95" },
      { value: "99", label: "传感器 99" },
    ],
  },
];

const algorithm_value = ref("");
const algorithm_options = [
  {
    value: "移动平均滤波",
    label: "移动平均滤波",
  },
  {
    value: "卡尔曼滤波",
    label: "卡尔曼滤波",
  },
  {
    value: "Butterworth滤波",
    label: "Butterworth滤波",
  },
  {
    value: "小波变换",
    label: "小波变换",
  },
];

const dataZoomOpts1 = [
  {
    type: "slider", // 滑动条类型
    show: true, // 显示滑动条
    xAxisIndex: [0], // 控制X轴的缩放和滑动
    start: 0, // 数据窗口的起始百分比
    end: 100, // 数据窗口的结束百分比
    //bottom: 0, // 滑动条距离底部的距离
    textStyle: {
      color: "blue",
      fontSize: 12,
    },
    backgroundColor: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
      {
        offset: 0,
        color: "rgb(128, 255, 165)",
      },
      {
        offset: 1,
        color: "rgb(1, 191, 236)",
      },
    ]),
    dataBackground: {
      lineStyle: {
        color: "red",
        opacity: 0.62, //数据阴影的线条透明度
      },
      areaStyle: {
        color: "green",
        shadowBlur: 0,
        opacity: 0,
      },
    },
    borderRadius: 5,
    borderColor: "red",
    handleStyle: {
      borderColor: "red",
      borderWidth: 2,
    },
    brushSelect: true,
    brushStyle: {
      color: "#fff",
      borderColor: "blue",
    },
    emphasis: {
      handleStyle: {
        color: "red",
      },
      moveHandleStyle: {
        color: "red",
      },
    },
  },
  {
    type: "inside", // 内置的缩放控制器
    start: 0,
    end: 40,
  },
];

//原始数据
const ori_sensor_data = ref({});
const ori_chart_Opts = ref({});

//预处理数据
const pre_sensor_data = ref({});
const pre_chart_Opts = ref({});

//数据特征
const feature_sensor_data = ref({});
const feature_chart_Opts = ref({});

const test_Pre = () => {
  isLoad.value = true;
  setTimeout(() => {
    isLoad.value = false;
    pre_chart_Opts.value = {
      backgroundColor: '#f7f7f7', // 浅灰色背景
      title: {
        text: `Data: test_pre`
      },
      tooltip: {
        trigger: 'axis'
      },
      grid: {
        left: '3%',
        right: '4%',
        bottom: '12%',
        containLabel: true
      },
      xAxis: {
        type: 'value',
        boundaryGap: false,
      },
      yAxis: {
        type: 'value'
      },
      series: [{

        type: 'line',
        data: [[-1.2, 3], [-2.4, 7], [8.5, 6], [4.3, 5], [5.4, 5]],
        symbol: 'none',
        itemStyle: {
          color: '#' + (Math.floor(Math.random() * 16777215).toString(16)), // Random color
        },
        smooth: true // Smooth lines
      }],
      dataZoom: dataZoomOpts1
    };
  }, 1600);

}

const test_Feature = () => {

  feature_chart_Opts.value = {
    backgroundColor: "#f7f7f7", // 浅灰色背景
    title: {
      text: `Data: test_pre`,
    },
    tooltip: {
      trigger: "axis",
    },
    grid: {
      left: "3%",
      right: "4%",
      bottom: "12%",
      containLabel: true,
    },
    xAxis: {
      type: "category",
      data: ["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"],
      boundaryGap: false,
    },
    yAxis: {},
    series: [
      {
        type: "bar",
        data: [5, 20, 36, 10, 10, 20],
        symbol: "none",
        itemStyle: {
          color: "#" + Math.floor(Math.random() * 16777215).toString(16), // Random color
        },
      },
    ],
    // dataZoom: dataZoomOpts1
  };
};

const fentch_ori_data = async () => {
  try {
    const ori_param = {
      Year: value.value[0],
      Exp_Name: value.value[1],
      state: "ori",
      SensorID: sensor_value.value[1],
    };
    const response = await axios.get(
      "http://127.0.0.1:8000/data_management/get_data",
      {
        params: ori_param,
      }
    );
    if (response.data.code == 0) {
      ori_sensor_data.value = response.data.data;
      ori_chart_Opts.value = {
        backgroundColor: "#f7f7f7", // 浅灰色背景
        title: {
          text: `Data: ${value.value[1]} 传感器 ${sensor_value.value[1]}`,
        },
        tooltip: {
          trigger: "axis",
        },
        toolbox: {
          show: true,
          feature: {
            dataView: { show: true, readOnly: true },
            //  magicType: { show: true, type: ['line', 'bar'] },
            restore: { show: true },
            saveAsImage: { show: true },
          },
        },
        grid: {
          left: "3%",
          right: "4%",
          bottom: "12%",
          containLabel: true,
        },
        xAxis: {
          type: "value",
          name: "时间",
          boundaryGap: false,
        },
        yAxis: {
          type: "value",
          name: value.value[0],
        },
        series: [
          {
            type: "line",
            data: ori_sensor_data.value.data.sort((a, b) => {
              if (a[0] < b[0]) {
                return -1; // a 应该在 b 之前
              }
              if (a[0] > b[0]) {
                return 1; // b 应该在 a 之前
              }
              return 0; // a 和 b 相等，顺序不变
            }),
            symbol: "none",
            itemStyle: {
              color: "#" + Math.floor(Math.random() * 16777215).toString(16), // Random color
            },
            smooth: true, // Smooth lines
          },
        ],
        dataZoom: dataZoomOpts1,
      };
    } else {
      ElMessage.error(response.data.message);
    }
  } catch (error) {
    console.error("Error fetching ori_data:", error);
  }
};

const fentch_pre_data = async () => {
  try {
    const pre_param = {
      Year: value.value[0],
      Exp_Name: value.value[1],
      state: "pre",
      SensorID: sensor_value.value[1],
    };
    const response = await axios.get(
      "http://127.0.0.1:8000/data_management/get_data",
      { params: pre_param }
    );
    if (response.data.code == 0) {
      pre_sensor_data.value = response.data.data;
      isLoad.value = true;
      setTimeout(() => {
        isLoad.value = false;
      }, 1600);
      pre_chart_Opts.value = {
        backgroundColor: '#f7f7f7', // 浅灰色背景
        title: {
          text: `Data: ${value.value[1]} 传感器 ${sensor_value.value[1]}`,
        },
        tooltip: {
          trigger: "axis",
        },
        toolbox: {
          show: true,
          feature: {
            dataView: { show: true, readOnly: true },
            //  magicType: { show: true, type: ['line', 'bar'] },
            restore: { show: true },
            saveAsImage: { show: true },
          },
        },
        grid: {
          left: "3%",
          right: "4%",
          bottom: "12%",
          containLabel: true,
        },
        xAxis: {
          type: "value",
          name: "时间",
          boundaryGap: false,
        },
        yAxis: {
          type: "value",
          name: value.value[0],
        },
        series: [
          {
            type: "line",
            data: pre_sensor_data.value.data.sort((a, b) => {
              if (a[0] < b[0]) {
                return -1; // a 应该在 b 之前
              }
              if (a[0] > b[0]) {
                return 1; // b 应该在 a 之前
              }
              return 0; // a 和 b 相等，顺序不变
            }),
            symbol: "none",
            itemStyle: {
              color: "#" + Math.floor(Math.random() * 16777215).toString(16), // Random color
            },
            smooth: true, // Smooth lines
          },
        ],
        dataZoom: dataZoomOpts1,
      };
    } else {
      ElMessage.error(response.data.message);
    }
  } catch (error) {
    console.error("Error fetching ori_data:", error);
  }
};

const fentch_feature_data = async () => {
  try {
    const feature_param = {
      Year: value.value[0],
      Exp_Name: value.value[1],
      state: "fix",
      SensorID: sensor_value.value[1],
    };
    const response = await axios.get(
      "http://127.0.0.1:8000/data_management/get_data",
      { params: feature_param }
    );
    if (response.data.code == 0) {
      feature_sensor_data.value = response.data.data;
      feature_chart_Opts.value = {
        backgroundColor: "#f7f7f7", // 浅灰色背景
        title: {
          text: `Data: ${value.value[1]} 传感器 ${sensor_value.value[1]}`,
        },
        tooltip: {
          trigger: "axis",
        },
        toolbox: {
          show: true,
          feature: {
            dataView: { show: true, readOnly: true },
            //  magicType: { show: true, type: ['line', 'bar'] },
            restore: { show: true },
            saveAsImage: { show: true },
          },
        },
        grid: {
          left: "3%",
          right: "4%",
          bottom: "12%",
          containLabel: true,
        },
        xAxis: {
          type: "category",

          name: "特征",
          boundaryGap: false,
          data: ["Max", "Min", "Mean", "StdDev", "PeakToPeak"],
        },
        yAxis: {
          type: "value",
          name: value.value[0],
        },
        series: [
          {
            type: "bar",
            data: [
              feature_sensor_data.value.Max,
              feature_sensor_data.value.Min,
              feature_sensor_data.value.Mean,
              feature_sensor_data.value.StdDev,
              feature_sensor_data.value.PeakToPeak,
            ],
            symbol: "none",
            itemStyle: {
              color: "#" + Math.floor(Math.random() * 16777215).toString(16), // Random color
            },
          },
        ],
        dataZoom: dataZoomOpts1,
      };
    } else {
      ElMessage.error(response.data.message);
    }
  } catch (error) {
    console.error("Error fetching ori_data:", error);
  }
};

const onDragEnd = () => {
  const test_data = [
    [-1.2, 3],
    [-2.4, 7],
    [8.5, 6],
    [4.3, 5],
    [5.4, 5],
  ];
};
</script>
<style scoped>
.el-container {
  height: 100%;
  direction: vertical;
  overflow-y: auto;
  overflow: hidden;
}

.el-row {
  margin-top: 20px;
}

header {
  width: 100%;
  background-color: #c7c8cbd5;
  padding: 0;
  height: 15px;
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
  margin-bottom: 50px;
}

.chart-item {
  flex: 0 0 80%;

  margin-left: 1%;
  /* 图表之间的间距 */
  max-width: 80%;
  /* 图表的宽度 */
  height: 400px;
  /* 设置图表高度 */
  /* border: 0.5px solid #ccc;
  /* 图表的边框 */
  /* border-radius: 5px;
  /* 图表的圆角 */
  /*box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); /* 图表的阴影 */
  /* padding-bottom: 20px;*/
}

/*@media (max-width: 600px) {
  .chart-item {
 
    flex: 1 1 100%;
   
  }
}*/
.anim {
  position: absolute;
  top: 0;
  left: -100px;
  width: 480px;
  height: 30px;
  background-size: 30px 30px;
  /*添加条纹背景*/
  background-image: linear-gradient(-45deg,
      transparent 15px,
      transparent 8px,
      #ffe45c 9px,
      #ffe45c 20px,
      transparent 21px,
      transparent 36px,
      #ffe45c 37px);
  animation: load 1.6s 1 linear forwards;
}

.cont {
  width: 300px;
  height: 20px;
  position: absolute;
  /* 绝对定位 */
  top: 50%;
  /* 向下偏移50% */
  left: 50%;
  /* 向右偏移50% */
  transform: translate(-50%, -50%);
  /* 使用位移使其居中 */
  background-color: #ee6666;
  border-radius: 5px;
  overflow: hidden;
}

@keyframes load {
  0% {
    width: 0;
  }

  100% {
    width: 680px;
  }
}
</style>
