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
          <el-menu-item index="1-1"><el-checkbox v-model="checked1Charts[0]" size="large" @change="funk"><el-icon><DocumentRemove /></el-icon>峰值</el-checkbox></el-menu-item>
          <el-menu-item index="1-2"><el-checkbox v-model="checked1Charts[1]" size="large"><el-icon><DocumentRemove /></el-icon>最小值</el-checkbox></el-menu-item>
        </el-sub-menu>
        <el-sub-menu index="2">
          <template #title>
            <el-checkbox v-model="dirchecked2" size="large" @click.stop="handleSubMenuCheck2"> <el-icon class="my-icon"><FolderOpened /></el-icon>
              <span>自由场压力</span></el-checkbox>
          </template>
          <el-menu-item index="2-1"><el-checkbox v-model="checked2Charts[0]" size="large"><el-icon><DocumentRemove /></el-icon>峰值</el-checkbox></el-menu-item>
          <el-menu-item index="2-2"><el-checkbox v-model="checked2Charts[1]" size="large"><el-icon><DocumentRemove /></el-icon>时间常数</el-checkbox></el-menu-item>
          <el-menu-item index="2-3"><el-checkbox v-model="checked2Charts[2]" size="large"><el-icon><DocumentRemove /></el-icon>比冲击波能</el-checkbox></el-menu-item>
          <el-menu-item index="2-4"><el-checkbox v-model="checked2Charts[3]" size="large"><el-icon><DocumentRemove /></el-icon>比气泡能</el-checkbox></el-menu-item>
        </el-sub-menu>
        <el-sub-menu index="3">
          <template #title>
            <el-checkbox v-model="dirchecked3" size="large" @click.stop="handleSubMenuCheck3"> <el-icon class="my-icon"><FolderOpened /></el-icon>
              <span>应变数据</span></el-checkbox>
          </template>
          <el-menu-item index="3-1"><el-checkbox v-model="checked3Charts[0]" size="large"><el-icon><DocumentRemove /></el-icon>塑性应变值</el-checkbox></el-menu-item>
          <el-menu-item index="3-2"><el-checkbox v-model="checked3Charts[1]" size="large"><el-icon><DocumentRemove /></el-icon>峰值</el-checkbox></el-menu-item>
          <el-menu-item index="3-3"><el-checkbox v-model="checked3Charts[2]" size="large"><el-icon><DocumentRemove /></el-icon>最大值</el-checkbox></el-menu-item>
        </el-sub-menu>
        <el-sub-menu index="4">
          <template #title>
            <el-checkbox v-model="dirchecked4" size="large" @click.stop="handleSubMenuCheck4"> <el-icon class="my-icon"><FolderOpened /></el-icon>
              <span>加速度数据</span></el-checkbox>
          </template>
          <el-menu-item index="4-1"><el-checkbox v-model="checked4Charts[0]" size="large"><el-icon><DocumentRemove /></el-icon>统计值计算</el-checkbox></el-menu-item>
          <el-menu-item index="4-2"><el-checkbox v-model="checked4Charts[1]" size="large"><el-icon><DocumentRemove /></el-icon>冲击值计算</el-checkbox></el-menu-item>
        </el-sub-menu>
       
      </el-menu>
      <!-- <el-image style="position:fixed;top: 500px; left: 0;width: 200px; height: 200px" :src="imgsrc" :fit="fit" /> -->
    </el-col>
  </el-row>
</template>

<script setup>
import { FolderOpened,DocumentRemove } from '@element-plus/icons-vue';
import { ref,reactive,defineEmits,watch } from 'vue'

const emit = defineEmits(['update:checked1Charts','update:checked2Charts','update:checked3Charts','update:checked4Charts']);  


const dirchecked1 = ref(true)
const dirchecked2 = ref(true)
const dirchecked3 = ref(true)
const dirchecked4 = ref(true)

const checked1Charts =reactive([true,true])
const checked2Charts =reactive([true,true,true,true,])
const checked3Charts =reactive([true,true,true,true,])
const checked4Charts =reactive([true,true,true,true,])

const handleOpen = (key, keyPath) => {
  console.log(key, keyPath);
};

const handleClose = (key, keyPath) => {
  console.log(key, keyPath);
};
const handleSubMenuCheck1 = () => {
  checked1Charts[0] = !dirchecked1.value;
  checked1Charts[1] = !dirchecked1.value;
}

const handleSubMenuCheck2 = () => {
  checked2Charts[0] = !dirchecked2.value;
  checked2Charts[1] = !dirchecked2.value;
  checked2Charts[2] = !dirchecked2.value;
  checked2Charts[3] = !dirchecked2.value;
}
const handleSubMenuCheck3 = () => {
  checked3Charts[0] = !dirchecked3.value;
  checked3Charts[1] = !dirchecked3.value;
  checked3Charts[2] = !dirchecked3.value;
}
const handleSubMenuCheck4 = () => {
  checked4Charts[0] = !dirchecked4.value;
  checked4Charts[1] = !dirchecked4.value;
}
watch(checked1Charts, () => {  
  console.log('asdad:  ',checked1Charts);
  emit('update:checked1Charts',checked1Charts);  
 }, {  

  deep: true, 
  immediate: true 
});  
// watch(() => checked1Charts, () => {
//   console.log('dadad  ',checked1Charts);
//   emit('update:checked1Charts', checked1Charts);
// });

const funk = () => {
  console.log('funk,checked1Charts:  ',checked1Charts);
}
</script>

<style scoped>

.el-menu {
  width: 200px;
  display: flex;  

  flex-direction: column;
  height: 100vh;
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