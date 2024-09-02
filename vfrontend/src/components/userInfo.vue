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
        <p>用户名: {{ userInfo.username }}</p>
      </div>
      <div class="operation">
        <div @click="changePassword">修改信息</div>
        <div @click="createExperiment">新建实验</div>
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
                <el-date-picker v-model="filters.dateRange" type="daterange" range-separator="至"
                  start-placeholder="开始日期" end-placeholder="结束日期" format="YYYY-MM-DD" />
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
        <el-table :data="filteredData" style="width: 100%">
          <el-table-column prop="name" label="实验名称" width="200"></el-table-column>
          <el-table-column prop="progress" label="实验进度" width="180"
            :cell-style="({ row }) => getCellStyle(row.progress)"></el-table-column>
          <el-table-column prop="time" label="时间" width="180"></el-table-column>
        </el-table>
      </el-card>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { Edit } from '@element-plus/icons-vue';

export default {
  components: {
    Edit,
  },
  setup() {
    const userInfo = ref({
      avatar: '',
      username: '',
    });

    const filters = ref({
      experimentName: '',
      dateRange: [],
    });

    const historyData = ref([]);
    const filteredData = ref([]);

    const fetchData = async () => {
      const avatarImage = new URL('../assets/avatar.jpg', import.meta.url).href;

      userInfo.value = {
        avatar: avatarImage,
        username: '实验用户',
      };

      historyData.value = [
        { id: 1, name: '实验A', progress: '预处理', time: '2024-08-01' },
        { id: 2, name: '实验B', progress: '原始数据', time: '2024-08-10' },
        { id: 3, name: '实验C', progress: '特征提取', time: '2024-08-15' },
        { id: 4, name: '实验D', progress: '预处理', time: '2024-08-20' },
      ];

      filteredData.value = historyData.value;
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
    const getCellStyle = (progress) => {
      switch (progress) {
        case '预处理':
          return { color: 'blue' };
        case '原始数据':
          return { color: 'green' };
        case '特征提取':
          return { color: 'red' };
        default:
          return {};
      }
    };

    const resetFilters = () => {
      filters.value = {
        experimentName: '',
        dateRange: [],
      };
      filteredData.value = historyData.value;
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
      fetchData();
    });

    return {
      userInfo,
      filters,
      historyData,
      filteredData,
      changePassword,
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
  margin: 50px 75px;
  width: 25%;
  background-color: rgba(255, 255, 255);
  border-radius: 15px;
  padding: 10px;
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
  background-color: rgba(255, 255, 255, 0.9);
  border-radius: 15px;
  padding: 2rem;
  overflow-y: auto;
  box-shadow: 0px 2px 4px 0px rgba(0, 0, 0, 0.4),
    0px 7px 13px -3px rgba(0, 0, 0, 0.3),
    0px -3px 0px 0px rgba(0, 0, 0, 0.2) inset;
}

.filter-card {
  margin-bottom: 1rem;
  padding: 20px;
}
</style>
