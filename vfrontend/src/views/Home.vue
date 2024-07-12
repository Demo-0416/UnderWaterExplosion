<template>
  <div class="common-layout" :style="themeStyles">
    <el-container>
      <el-header >
        <el-row style="background-color: #c8e0fa;">
          <el-col :span="6" :offset="9"
            style="display: flex;text-align: center;justify-content: center;align-items: center;font-size: 16px;font-weight: bold;color: #303133;">数据分析系统</el-col>
          <el-col :span="2" :offset="4" style="display: flex;align-items: center;font-size: 14px;">欢迎您，{{name}}</el-col>
          <el-col :span="1" :offset="2"><el-avatar :src="imgsrc" style="width: 48; margin-top: 2px;"
              :fit="fit" /></el-col>
          
        </el-row>
        
         <el-row style="margin-left: 6px;margin-top: 10px;margin-bottom: 10px;margin-right: 6px;">
           <el-col :span="4" ><el-select v-model="value" >
            <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value"
              :disabled="item.disabled" />
          </el-select></el-col>
           <el-col :span="20" > <el-steps  style="height:6px" :active="active" finish-status="success" simple>
            <el-step title="原始数据" :status="active === 1 ? 'success' : 'process'" @click="handleStepClick(1)" />
            <el-step title="预处理" :status="active === 2 ? 'success' : 'process'" @click="handleStepClick(2)" />
            <el-step title="特征提取" :status="active === 3 ? 'success' : 'process'" @click="handleStepClick(3)" />
          </el-steps>
        </el-col>
         </el-row>
          
         
      </el-header>
      <el-container>
        <el-aside width="180px">
          <NavList @update:checked1Charts="updateSelect1Charts" />
          <!-- <Elmenu1/> -->
        </el-aside>
        <el-main>
          <mymain :selected1Charts="selected1Charts" />
          <!-- <el-dialog title="提示" v-model="dialogVisible" width="30%" :before-close="handleClose"></el-dialog> -->
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>
<script setup>
import NavList from '@/components/NavList.vue';
import Elmenu1 from '@/components/Elmenu1.vue'
import TopHeader from '@/components/Header.vue'
import mymain from '@/components/Main.vue'
import blue3 from '@/assets/blue3.webp'
import { ref, reactive } from 'vue'

const imgsrc = ref(blue3)
const fit = ref('contain')
const dialogVisible = ref(true)
const selected1Charts = ref([])
const updateSelect1Charts = (checked1Charts) => {
  console.log(checked1Charts);
  selected1Charts.value = checked1Charts;

}

const value = ref('option1')
const options = [
  {
    value: '试验1',
    label: '试验1',
  },
  {
    value: '试验2',
    label: '试验2',
  },
  {
    value: '试验3',
    label: '试验3',
  },
  {
    value: '试验4',
    label: '试验4',
  },
  {
    value: '试验5',
    label: '试验5',
  },
]
const active = ref(1);
  const handleStepClick = (index) => {  

    active.value = index;

  };
</script>
<style scoped>


.common-layout {
  height: 100%;
  overflow: hidden;
}

.el-container {
  height: 100%;
  direction: vertical;
}

header {
  width: 100%;
  background-color: #c7c8cbd5;
  padding: 0;
  height: 100PX;
  border-bottom: 0.5px solid #dcdfe6;
}

aside {
  display: block;
  border-right: 1px solid #dcdfe6;
}

main {
  display: block;
  padding: 0 0 0 1px;

}


/**.main {
  position: absolute;
  background-color: black;
  left: 275px;
  top: 70px;
  right: 20px;
}*/
</style>
