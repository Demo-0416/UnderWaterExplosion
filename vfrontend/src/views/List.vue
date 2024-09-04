<template>
  <div class="background">
    <!-- 用户信息卡片 -->
    <div class="userinfo">
      <div class="title">
        <span>个人卡片</span>
        <el-icon>
          <Edit />
        </el-icon>
      </div>
      <div class="avatar_container">
        <img :src="userInfo.avatar" alt="avatar" class="avatar" />
      </div>
      <div class="info">
        用户名: {{ userInfo.username }}
      </div>
      <div class="operation">
        <div @click="generate">生成数据</div>
        <div @click="logout">3D演示</div>
      </div>
    </div>

    <!-- 历史实验数据 -->
    <div class="history">
      <el-card class="filter-card">
        <el-form :model="filters" label-width="100px">
          <el-row :gutter="20">
            <el-col :span="8">
              <el-form-item label="实验名称">
                <el-input v-model="filters.experimentName" placeholder="请输入实验名称"></el-input>
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item label="实验日期">
                <el-date-picker v-model="filters.dateRange" type="daterange" range-separator="至" start-placeholder="开始"
                  end-placeholder="结束" format="YYYY-MM-DD" />
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item>
                <el-button type="primary" @click="filterData">筛选</el-button>
                <el-button @click="resetFilters">重置</el-button>
              </el-form-item>
            </el-col>
          </el-row>
        </el-form>
      </el-card>

      <!-- 历史实验数据时间轴 -->
      <el-card style="padding-bottom: 20px;">
        <h3>历史实验数据</h3>
        <div style="  max-height: 50vh; overflow-y: auto; ">
          <el-row :gutter="20" class="experiment-list">
            <el-col :span="24" v-for="item in filteredData.slice().reverse()" :key="item.id">
              <el-card @click="item.loading ? null : handleItemClick(item)">
                <h3>{{ item.name }}</h3>
                <p v-if="item.loading"><strong>生成中...</strong></p>
                <el-progress v-if="item.loading" :percentage="item.progress" />
                <p v-else><strong>进度:</strong> {{ item.progress }}</p>
                <p><strong>时间:</strong> {{ item.time }}</p>
              </el-card>
            </el-col>
          </el-row>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { Edit } from '@element-plus/icons-vue';
import { useRouter } from 'vue-router';

export default {
  components: {
    Edit,
  },
  setup() {
    const router = useRouter();
    const userInfo = ref({
      avatar: new URL('../assets/avatar.jpg', import.meta.url).href,
      username: 'kiarkira',
    });

    const filters = ref({
      experimentName: '',
      dateRange: [],
    });

    const historyData = ref([{
      "time": "2024",
      "name": "test2",
      "progress": "原始数据"
    },
    {
      "time": "2024",
      "name": "test5",
      "progress": "原始数据"
    },
    {
      "time": "2024",
      "name": "test5",
      "progress": "原始数据"
    },
    {
      "time": "2024",
      "name": "test5",
      "progress": "原始数据"
    },
    {
      "time": "2024",
      "name": "test5",
      "progress": "原始数据"
    },
    {
      "time": "2024",
      "name": "test5",
      "progress": "原始数据"
    },
    {
      "time": "2025",
      "name": "test3",
      "progress": "原始数据"
    }]);
    const filteredData = ref([{
      "time": "2024",
      "name": "test2",
      "progress": "原始数据"
    },
    {
      "time": "2024",
      "name": "test5",
      "progress": "原始数据"
    },
    {
      "time": "2024",
      "name": "test5",
      "progress": "原始数据"
    },
    {
      "time": "2024",
      "name": "test5",
      "progress": "原始数据"
    },
    {
      "time": "2024",
      "name": "test5",
      "progress": "原始数据"
    },
    {
      "time": "2024",
      "name": "test5",
      "progress": "原始数据"
    },
    {
      "time": "2025",
      "name": "test3",
      "progress": "原始数据"
    }]);

    const handleItemClick = (item) => {
      if (!item.loading) {
        router.push({
          path: '/detail',
          query: {
            value: [item.time, item.name],
          },
        });
      }
    };

    const fetchData = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:8000/data_management/get_history/');
        if (response.data.code === '0') {
          historyData.value = response.data.data.map(item => ({
            id: item.exp_name, // 根据实际需要设置合适的 id
            name: item.exp_name,
            progress: item.status,
            time: item.year, // 这里假设 year 是时间字段
          }));
          filteredData.value = historyData.value;
        } else {
          console.error('Failed to fetch history data');
        }
      } catch (error) {
        console.error('Error fetching history data:', error);
      }
    };

    const generate = async () => {
      // 创建一个新数据对象，包含进度条信息和不可点击状态
      const newItem = {
        id: Date.now(), // 使用时间戳作为临时 ID
        name: '新实验数据', // 你可以根据实际需求设置名字
        progress: '正在生成...',
        time: new Date().toISOString().split('T')[0], // 当前日期
        clickable: false, // 初始化为不可点击状态
      };

      // 将新数据添加到历史数据列表的顶部
      historyData.value.push(newItem);
      filteredData.value = historyData.value;

      try {
        // 调用后端的 stream_sensor_data 接口
        const response = await axios.post('http://127.0.0.1:8000/data_management/stream_sensor_data/', {
          // 根据接口要求传递参数
          Year: '2024', // 传递年份参数
          Exp_name: 'experiment_1', // 传递实验名称参数
        });

        // 如果请求成功，更新新数据的状态
        if (response.status === 200 && response.data.status === 'streaming started') {
          // 查找刚添加的这个新数据
          const item = historyData.value.find(item => item.id === newItem.id);
          if (item) {
            // 更新其状态为可点击，并移除进度条信息
            item.progress = '生成完成';
            item.clickable = true;
            filteredData.value = historyData.value;
          }
        }
      } catch (error) {
        console.error('生成数据失败:', error);
        // 可以添加错误处理逻辑，比如移除该条数据或显示错误信息
      }
    };


    const resetFilters = async () => {
      await fetchData();
    };

    onMounted(() => {
      fetchData();
    });

    return {
      userInfo,
      filters,
      historyData,
      filteredData,
      handleItemClick,
      generate,
      resetFilters,
    };
  },
};
</script>

<style scoped>
.background {
  display: flex;
  justify-content: space-between;
  width: 100vw;
  height: 100vh;
  background: url('../assets/star.jpg') no-repeat center center;
  background-size: cover;
}

.title {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 48px;
  line-height: 48px;
  padding-left: 4%;
  border-bottom: 1px solid #ebebeb;
  font-size: 15px;
  font-weight: 700;
  color: #666;
}

.userinfo {
  height: 45vh;
  margin: 50px 75px;
  width: 25%;
  background-color: rgba(255, 255, 255);
  border-radius: 15px;
  padding: 10px;
}

.info {
  padding: 20px;
}

.avatar_container {
  padding-top: 20px;
  text-align: center;
}

.avatar {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  margin-bottom: 1rem;
}

.operation {
  display: flex;
  flex-direction: column;
  gap: 10px;
  cursor: pointer;
}

.operation div {
  padding: 8px;
  text-align: center;
  border-radius: 5px;
  background-color: #f0f0f0;
  transition: background-color 0.3s;
}

.operation div:hover {
  background-color: #dcdcdc;
}

.history {
  width: 75%;
  margin: 50px 75px;
  margin-left: 0;
  background-color: rgba(255, 255, 255);
  border-radius: 15px;
  padding: 2rem;
}

.filter-card {
  margin-bottom: 1rem;
  padding: 20px;
}

.experiment-list {
  width: 100%;
  margin-top: 20px;
  overflow-y: auto;
}

.el-card {
  padding: 20px;
  border-radius: 10px;
}
</style>
