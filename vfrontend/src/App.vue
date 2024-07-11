<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
 <div class="laybox">
   <router-view></router-view>
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
