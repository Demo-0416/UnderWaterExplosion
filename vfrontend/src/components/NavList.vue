<template>

  <el-row class="nav-list">
    <el-col :span="24">
      <el-menu class="mymenu" border-right="none" @open="handleOpen" @close="handleClose"
        popper-offset="10">
        <el-sub-menu index="1">
          <template #title>
            <el-checkbox v-model="dirchecked1" size="large"
            @click.stop="handleSubMenuCheck1" > 
            <el-icon class="my-icon"><FolderOpened /></el-icon><span>时序特征</span></el-checkbox> 
          </template>
          <el-menu-item index="1-1"><el-checkbox v-model="checked1_1" size="large"><el-icon><DocumentRemove /></el-icon>峰值</el-checkbox></el-menu-item>
          <el-menu-item index="1-2"><el-checkbox v-model="checked1_2" size="large"><el-icon><DocumentRemove /></el-icon>最小值</el-checkbox></el-menu-item>
        </el-sub-menu>
        <el-sub-menu index="2">
          <template #title>
            <el-checkbox v-model="dirchecked2" size="large" @click.stop="handleSubMenuCheck2"> <el-icon class="my-icon"><FolderOpened /></el-icon>
              <span>自由场压力</span></el-checkbox>
          </template>
          <el-menu-item index="2-1"><el-checkbox v-model="checked2_1" size="large"><el-icon><DocumentRemove /></el-icon>峰值</el-checkbox></el-menu-item>
          <el-menu-item index="2-2"><el-checkbox v-model="checked2_2" size="large"><el-icon><DocumentRemove /></el-icon>时间常数</el-checkbox></el-menu-item>
          <el-menu-item index="2-3"><el-checkbox v-model="checked2_3" size="large"><el-icon><DocumentRemove /></el-icon>比冲击波能</el-checkbox></el-menu-item>
          <el-menu-item index="2-4"><el-checkbox v-model="checked2_4" size="large"><el-icon><DocumentRemove /></el-icon>比气泡能</el-checkbox></el-menu-item>
        </el-sub-menu>
        <el-sub-menu index="3">
          <template #title>
            <el-checkbox v-model="dirchecked3" size="large" @click.stop="handleSubMenuCheck3"> <el-icon class="my-icon"><FolderOpened /></el-icon>
              <span>应变数据</span></el-checkbox>
          </template>
          <el-menu-item index="3-1"><el-checkbox v-model="checked3_1" size="large"><el-icon><DocumentRemove /></el-icon>塑性应变值</el-checkbox></el-menu-item>
          <el-menu-item index="3-2"><el-checkbox v-model="checked3_2" size="large"><el-icon><DocumentRemove /></el-icon>峰值</el-checkbox></el-menu-item>
          <el-menu-item index="3-3"><el-checkbox v-model="checked3_3" size="large"><el-icon><DocumentRemove /></el-icon>最大值</el-checkbox></el-menu-item>
        </el-sub-menu>
        <el-sub-menu index="4">
          <template #title>
            <el-checkbox v-model="dirchecked4" size="large" @click.stop="handleSubMenuCheck4"> <el-icon class="my-icon"><FolderOpened /></el-icon>
              <span>加速度数据</span></el-checkbox>
          </template>
          <el-menu-item index="4-1"><el-checkbox v-model="checked4_1" size="large"><el-icon><DocumentRemove /></el-icon>统计值计算</el-checkbox></el-menu-item>
          <el-menu-item index="4-2"><el-checkbox v-model="checked4_2" size="large"><el-icon><DocumentRemove /></el-icon>冲击值计算</el-checkbox></el-menu-item>
        </el-sub-menu>

      </el-menu>
    </el-col>
  </el-row>
</template>

<script setup>
import { FolderOpened,DocumentRemove } from '@element-plus/icons-vue';
import { ref } from 'vue'

const dirchecked1 = ref(false)
const dirchecked2 = ref(false)
const dirchecked3 = ref(false)
const dirchecked4 = ref(false)

const checked1_1 = ref(false)
const checked1_2 = ref(false)
const checked2_1 = ref(false)
const checked2_2 = ref(false)
const checked2_3 = ref(false)
const checked2_4 = ref(false)
const checked3_1 = ref(false)
const checked3_2 = ref(false)
const checked3_3 = ref(false)
const checked4_1 = ref(false)
const checked4_2 = ref(false)
const handleOpen = (key, keyPath) => {
  console.log(key, keyPath);
};

const handleClose = (key, keyPath) => {
  console.log(key, keyPath);
};
const handleSubMenuCheck1 = () => {
  checked1_1.value = !dirchecked1.value;
  checked1_2.value = !dirchecked1.value;
}
const handleSubMenuCheck2 = () => {
  checked2_1.value = !dirchecked2.value;
  checked2_2.value = !dirchecked2.value;
  checked2_3.value = !dirchecked2.value;
  checked2_4.value = !dirchecked2.value;
}
const handleSubMenuCheck3 = () => {
  checked3_1.value = !dirchecked3.value;
  checked3_2.value = !dirchecked3.value;
  checked3_3.value = !dirchecked3.value;
}
const handleSubMenuCheck4 = () => {
  checked4_1.value = !dirchecked4.value;
  checked4_2.value = !dirchecked4.value;
}

</script>

<style scoped>
.el-menu {
  width: 200px;
  display: flex;  
  position: fixed;
  flex-direction: column;
  height: 100%;
  background-color: var(--header-bg-color,'#fff');
  color: var(--text-color,'blue');
  
}


.el-menu-item {
  display: flex;
  align-items: center;

}
.el-icon {
 color: #848e93;
}
</style>