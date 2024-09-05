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
      <div class="info">用户名: {{ userInfo.username }}</div>
      <div class="operation">
        <div @click="openGenerateDialog" :class="{ disabled: generating }">
          生成数据
        </div>
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
      <el-card style="padding-bottom: 20px">
        <h3>历史实验数据</h3>
        <div style="max-height: 50vh; overflow-y: auto">
          <el-row :gutter="20" class="experiment-list">
            <el-col :span="24" v-for="(item, index) in filteredData.slice().reverse()" :key="item.id">
              <el-card :class="{ clickable: canClick(item, index) }"
                @click="canClick(item, index) ? handleItemClick(item) : null">
                <h3>{{ item.name }}</h3>
                <p><strong>进度:</strong> {{ item.progress }}</p>
                <p><strong>时间:</strong> {{ item.time }}</p>
                <el-button v-if="isLastOri(item, index)" @click="openPreprocessDialog(item)">进行预处理</el-button>
              </el-card>
            </el-col>
          </el-row>
        </div>
      </el-card>
    </div>

    <!-- 生成数据 Dialog -->
    <el-dialog v-model="generateDialogVisible" title="生成数据" width="30%">
      <el-form :model="newData">
        <el-form-item label="实验名称">
          <el-input v-model="newData.name" placeholder="请输入实验名称"></el-input>
        </el-form-item>
        <el-form-item label="实验年份">
          <el-input v-model="newData.year" placeholder="请输入实验年份"></el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="generateDialogVisible = false">取消</el-button>
        <el-button v-loading.fullscreen.lock="fullscreenLoading" type="primary" @click="generate">确认</el-button>
      </template>
    </el-dialog>

    <!-- 预处理 Dialog -->
    <el-dialog v-model="preprocessDialogVisible" title="选择预处理方式" width="30%">
      <el-radio-group v-model="selectedPreprocess">
        <el-radio :label="1">预处理方法 1</el-radio>
        <el-radio :label="2">预处理方法 2</el-radio>
        <el-radio :label="3">预处理方法 3</el-radio>
        <el-radio :label="4">预处理方法 4</el-radio>
      </el-radio-group>
      <template #footer>
        <el-button @click="preprocessDialogVisible = false">取消</el-button>
        <el-button v-loading.fullscreen.lock="fullscreenLoading" type="primary" @click="preprocess">确认</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, onMounted } from "vue";
import axios from "axios";
import { Edit } from "@element-plus/icons-vue";
import { useRouter } from "vue-router";

export default {
  components: {
    Edit,
  },
  setup() {
    const fullscreenLoading = ref(false);
    const router = useRouter();
    const userInfo = ref({
      avatar: new URL("../assets/avatar.jpg", import.meta.url).href,
      username: "kiarkira",
    });

    const filters = ref({
      experimentName: "",
      dateRange: [],
    });

    const historyData = ref([]);
    const filteredData = ref([]);

    const generating = ref(false);

    // 生成数据 Dialog
    const generateDialogVisible = ref(false);
    const newData = ref({
      name: "",
      year: "",
    });

    // 预处理 Dialog
    const preprocessDialogVisible = ref(false);
    const selectedPreprocess = ref(null);
    const selectedItem = ref(null); // 当前选择预处理的实验

    const fetchData = async () => {
      try {
        const response = await axios.get(
          "http://127.0.0.1:8000/data_management/get_history/"
        );
        if (response.data.code === "0") {
          historyData.value = response.data.data.map((item) => ({
            id: item.exp_name,
            name: item.exp_name,
            progress: item.status,
            time: item.year,
          }));
          filteredData.value = historyData.value;
        } else {
          console.error("Failed to fetch history data");
        }
      } catch (error) {
        console.error("Error fetching history data:", error);
      }
    };

    const openGenerateDialog = () => {
      generateDialogVisible.value = true;
    };

    const generate = async () => {
      if (!newData.value.name || !newData.value.year) {
        ElMessage.error('请填写完整的实验名称和年份');
        return;
      }

      generating.value = true;
      fullscreenLoading.value = true;

      try {
        const response = await axios.post(
          "http://127.0.0.1:8000/data_management/stream_sensor_data/",
          {
            Exp_name: newData.value.name,
            Year: newData.value.year,
          }
        );

        if (response.status === 200) {
          generateDialogVisible.value = false;
          fullscreenLoading.value = false;
          await fetchData();
          ElMessage.success('数据生成成功');
        } else {
          console.error("Failed to generate data");
          ElMessage.error(`生成数据失败: ${response.data.message || '未知错误'}`);
        }
      } catch (error) {
        console.error("Error generating data:", error);
        ElMessage.error(`生成数据错误: ${error.message}`);
      } finally {
        generating.value = false;
        fullscreenLoading.value = false;
      }
    };

    const canClick = (item, index) => {
      if (item.progress !== "ori") {
        return true;
      }
      return false;
    };

    const isLastOri = (item, index) => {
      const lastOriIndex = filteredData.value
        .slice()
        .reverse()
        .findIndex((item) => item.progress === "ori");
      return index === lastOriIndex;
    };

    const openPreprocessDialog = (item) => {
      selectedItem.value = item;
      preprocessDialogVisible.value = true;
    };

    const preprocess = async () => {
      if (!selectedPreprocess.value) {
        ElMessage.error('请选择预处理方法');
        return;
      }
      fullscreenLoading.value = true;
      try {
        const response = await axios.post(
          "http://127.0.0.1:8000/data_process/consume_sensor_data/",
          {
            Exp_name: selectedItem.value.name,
            Year: selectedItem.value.time,
            Code: selectedPreprocess.value,
          }
        );

        if (response.status === 200) {
          preprocessDialogVisible.value = false;
          fullscreenLoading.value = false;
          await fetchData();
          ElMessage.success('预处理成功');
        } else {
          console.error("Failed to preprocess data");
          ElMessage.error(`预处理失败: ${response.data.message || '未知错误'}`);
        }
      } catch (error) {
        console.error("Error preprocessing data:", error);
        ElMessage.error(`预处理错误: ${error.message}`);
      } finally {
        fullscreenLoading.value = false;
      }
    };

    const handleItemClick = (item) => {
      router.push({
        path: "/detail",
        query: {
          value: [item.time, item.name],
        },
      });
    };

    const filterData = () => {
      filteredData.value = historyData.value.filter((item) => {
        const matchName =
          !filters.value.experimentName ||
          item.name.includes(filters.value.experimentName);

        const matchDate =
          !filters.value.dateRange.length ||
          (new Date(item.time) >= new Date(filters.value.dateRange[0]) &&
            new Date(item.time) <= new Date(filters.value.dateRange[1]));

        return matchName && matchDate;
      });
    };

    const resetFilters = async () => {
      await fetchData();
    };

    onMounted(() => {
      fetchData();
    });

    return {
      fullscreenLoading,
      userInfo,
      filters,
      historyData,
      filteredData,
      generateDialogVisible,
      preprocessDialogVisible,
      newData,
      selectedPreprocess,
      generate,
      preprocess,
      canClick,
      isLastOri,
      openGenerateDialog,
      openPreprocessDialog,
      handleItemClick,
      filterData,
      resetFilters,
      generating,
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
  background: url("../assets/star.jpg") no-repeat center center;
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

.clickable {
  cursor: pointer;
}

.disabled {
  pointer-events: none;
  opacity: 0.5;
}
</style>
