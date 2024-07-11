<template>
  <el-menu :default-active="activeIndex" class="el-menu-vertical-demo" @select="handleSelect" >
    <template v-for="submenu1 in menuItems" :key="submenu1.index">
      <el-submenu :index="submenu1.index">
        <template slot="title">
          <span>{{ submenu1.title }}</span>
        </template>
        <!-- <template v-for="2submenu in submenu1.children" :key="2submenu.index">
          <el-menu-item :index="2submenu.index"></el-menu-item>
        </template> -->
      </el-submenu>
    </template>
  </el-menu>
</template>

<script setup>
import { ref } from 'vue';


const activeIndex = ref('1');
const menuItems = ref([
  {
    index: '1',
    title: '导航一',
    icon: 'el-icon-s-unfold',
  },
  {
    index: '2',
    title: '导航二',
    icon: 'el-icon-s-unfold',
    children: [
      {
        index: '2-1',
        title: '子导航一',
      },
      {
        index: '2-2',
        title: '子导航二',
      },
    ],
  },
  // 更多菜单项...
]);

const handleSelect = (key, keyPath) => {
  console.log('select', key, keyPath);
  activeIndex.value = key;
};
</script>

<style scoped>
.el-menu-vertical-demo:not(.el-menu--collapse) {
  width: 200px;
  min-height: 400px;
}
</style>