<script setup>
// import { RouterLink, RouterView } from 'vue-router'
import loadnewfile from './components/loadnewfile.vue';
import List from './views/List.vue';
import Login from './views/Login.vue';
</script>

<template>
 <div class="laybox">
   <router-view></router-view>
      <!-- <loadnewfile></loadnewfile> -->
       <!-- <list></List> -->
         <!-- <login></Login> -->
 </div>
</template>



<style scoped>

.laybox {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
}


</style>
