<template>  
    <el-submenu :index="menu.index">  
      <template #title>{{ menu.title }}</template>  
      <el-checkbox-group v-model="localCheckedKeys" @change="handleChange">  
        <el-checkbox  
          v-for="item in menu.groups"  
          :key="item.index"  
          :label="item.index"  
        >{{ item.label }}</el-checkbox>  
      </el-checkbox-group>  
    </el-submenu>  
  </template>  
    
  <script setup>  
  import { defineProps, defineEmits, ref, computed,watch } from 'vue';  
    
  const props = defineProps({  
    menu: {  
      type: Object,  
      required: true,  
    },  
    modelValue: { // 假设我们使用 modelValue 作为 v-model 绑定的 prop  
      type: Array,  
      default: () => [],  
    },  
  });  
    
  const emit = defineEmits(['update:modelValue']);  
    
  const localCheckedKeys = ref([]);  
    
  // 监听 modelValue 的变化，并更新 localCheckedKeys  
  watch(() => props.modelValue, (newValue) => {  
    localCheckedKeys.value = newValue;  
  });  
    
  // 当复选框的值变化时，通知父组件  
  function handleChange(newCheckedKeys) {  
    emit('update:modelValue', newCheckedKeys);  
  }  
  </script>