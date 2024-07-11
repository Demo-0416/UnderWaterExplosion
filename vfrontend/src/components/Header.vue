<template>

    <el-row class="mb">
        <el-col :span="10" :offset="1">  <el-button @click="selectCsvFile" color="#307af2">选择文件</el-button> <el-text v-if="!selectedFileName">未选择文件</el-text>
            <el-text v-else>{{ selectedFileName }}</el-text></el-col>
        <el-col :span="6" :offset="3">  <el-button  class="uploadbutton" @click="uploadFile" :disabled="!selectedFile">开始数据仿真</el-button></el-col>
    </el-row>
    
       
        
    
</template>

<script setup>
import { ref } from 'vue';

// 响应式变量来存储选择的文件  
const selectedFile = ref(null);
const selectedFileName = ref('');

// 选择文件的方法  
function selectCsvFile() {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = '.csv, .xlsx, .xls'; // 限制只能选择CSV .XLs .XLSX文件  
    input.onchange = e => {
        if (e.target.files && e.target.files[0]) {
            selectedFile.value = e.target.files[0];
            selectedFileName.value = e.target.files[0].name;
        }
    };
    input.click();
}

// 上传文件到后端的方法  
function uploadFile() {
    if (!selectedFile.value) {
        alert('请选择文件！');
        return;
    }

    const formData = new FormData();
    formData.append('file', selectedFile.value);

    //API端点来处理文件上传  
    fetch('YOUR_BACKEND_ENDPOINT', {
        method: 'POST',
        body: formData,
    })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
        })
        .catch((error) => {
            console.error('Error:', error);
        });
}  
</script>

<style scoped>
.mb {
    /*background-color: blue;*/
    width: 380px;
    display: flex;
    justify-content: start-end;
   }
   
.el-text{
    font-size: 13px;
   
}
.uploadbutton:hover {  
    background-color: ; /* 例如：'#409EFF'（天蓝色更深的色调） */  
  }   
    
</style>