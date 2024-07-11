
<template>
  <div class="common-layout" :style="themeStyles">
    <el-container>
      <el-header>
        <!-- <el-row>
          <el-col :span="12" style="margin-top: 6px;"><TopHeader/></el-col>
          <el-col :span="1" :offset="11"><el-avatar :src="imgsrc" style="width: 48; margin-top: 2px;" :fit="fit"/></el-col>
        </el-row> -->
      </el-header>
      <el-container>
        <el-aside width="200px">
          <!-- <NavList @update:checked1Charts="updateSelect1Charts"/> -->
           <Elmenu1/>
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
// import NavList from '@/components/NavList.vue';
import Elmenu1 from '@/components/Elmenu1.vue'
import TopHeader from '@/components/Header.vue'
import mymain from '@/components/Main.vue'
import blue3 from '@/assets/blue3.webp'
import { ref,reactive } from 'vue'

const imgsrc = ref(blue3)
const fit = ref('contain')
const dialogVisible = ref(true)
const selected1Charts = ref([])
const updateSelect1Charts = (checked1Charts) => {
   console.log(checked1Charts);
   selected1Charts.value=checked1Charts;
  
}
</script>
<style scoped>
::-webkit-scrollbar {
  width: 0 !important;
}
::-webkit-scrollbar {
  width: 0 !important;height: 0;
}
.common-layout{
  height: 100vh;
}
.el-container{
  height: 100%;
  direction: vertical;
}
header{
  width: 100%;
  background-color: #ccc;
  padding: auto;
  height: 48PX;
  border-bottom: 0.5px solid #dcdfe6;
}
aside{
 display: block;
}

main{
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
