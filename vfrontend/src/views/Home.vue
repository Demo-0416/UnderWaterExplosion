<script setup>
import NavList from '@/components/NavList.vue';
import TopHeader from '@/components/Header.vue'
import mymain from '@/components/Main.vue'

</script>
<template>
  <div class="common-layout" :style="themeStyles">
    <el-container>
      <el-header>
          <TopHeader/>
      </el-header>
      <el-container>
        <el-aside width="200px">
          <NavList/>
        </el-aside>
        <el-main>
             <mymain/>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<style scoped>
.common-layout{
  height: 100vh;
}
.el-container{
  height: 100%;
  direction: vertical;
}
header{
  padding: auto;
  padding-top: 12px;
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
