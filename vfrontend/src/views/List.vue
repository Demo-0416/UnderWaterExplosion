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
        <div>
          <input type="file" @change="handleFileUpload" accept=".csv" style="display: none;" ref="fileInput" />
          <input type="text" v-model="expYear" placeholder="输入年份" />
          <input type="text" v-model="expName" placeholder="输入实验名称" />
          <div @click="triggerFileInput">上传CSV文件</div>
        </div>
        <div @click="logout">退出登录</div>
      </div>
    </div>

    <!-- 历史实验数据 -->
    <div class="history">
      <!-- 筛选器 -->
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
      <el-card>
        <h3>历史实验数据</h3>
        <el-row :gutter="20" class="experiment-list">
          <el-col :span="24" v-for="item in filteredData" :key="item.id">
            <el-card @click="handleItemClick(item)">
              <h3>{{ item.name }}</h3>
              <p><strong>进度:</strong> {{ item.progress }}</p>
              <p><strong>时间:</strong> {{ item.time }}</p>
            </el-card>
          </el-col>
        </el-row>
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
    const router = useRouter(); // 获取 router 实例
    const avatarImage = new URL('../assets/avatar.jpg', import.meta.url).href;
    const fileInput = ref(null);
    const expYear = ref('');
    const expName = ref('');
    
    const triggerFileInput = () => {
      fileInput.value.click();
    };

    const handleFileUpload = async (event) => {
      const file = event.target.files[0];
      if (file && file.type === 'text/csv') {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('year', expYear.value);
        formData.append('exp_name', expName.value);

        try {
          const response = await axios.post('http://127.0.0.1:8000/data_management/create_new_exp/', formData, {
            headers: {
              'Content-Type': 'multipart/form-data',
            },
          });

          if (response.data.code === '0') {
            // 上传成功后刷新数据
            await fetchData();
            alert('CSV 文件上传成功，数据已刷新！');
          } else {
            alert('上传失败，请检查输入内容并重试。');
          }
        } catch (error) {
          console.error('上传失败:', error);
          alert('CSV 文件上传失败，请重试。');
        }
      } else {
        alert('请上传有效的 CSV 文件');
      }
    };
    const userInfo = ref({
      avatar: avatarImage,
      username: 'kiarkira',
    });

    const filters = ref({
      experimentName: '',
      dateRange: [],
    });

    const historyData = ref([]);
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
      "time": "2025",
      "name": "test3",
      "progress": "原始数据"
    }]);

    const handleItemClick = (item) => {
      const value = ref([item.time, item.name]);
      router.push({
        path: '/',
        query: {
          year: value.value[0],
          experimentName: value.value[1],
        },
      });
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

    const filterData = () => {
      filteredData.value = historyData.value.filter((item) => {
        const matchName =
          !filters.value.experimentName ||
          item.name.includes(filters.value.experimentName);
        const matchDate =
          !filters.value.dateRange.length ||
          (item.time >= filters.value.dateRange[0] &&
            item.time <= filters.value.dateRange[1]);
        return matchName && matchDate;
      });
    };

    const resetFilters = async () => {
      try {
        await fetchData(); // 调用 fetchData 来刷新数据
      } catch (error) {
        console.error('Error resetting filters:', error);
      }
    };

    const changePassword = () => {
      alert('密码修改功能');
    };

    const createExperiment = () => {
      alert('新建实验功能');
    };

    const logout = () => {
      alert('退出登录功能');
    };

    onMounted(() => {
      fetchData(); // 页面加载时调用 fetchData 获取数据
    });

    return {
      userInfo,
      filters,
      historyData,
      filteredData,
      fileInput,
      expYear,
      expName,
      triggerFileInput,
      handleFileUpload,
      changePassword,
      handleItemClick,
      createExperiment,
      logout,
      filterData,
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
  overflow-y: auto;
}

.filter-card {
  margin-bottom: 1rem;
  padding: 20px;
}

.experiment-list {
  margin-top: 20px;
}

.el-card {
  padding: 20px;
  border-radius: 10px;
}
</style>
