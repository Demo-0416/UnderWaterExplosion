<template>
  <div> 
    <DragBall
      :distance-right="36"
      :distance-bottom="700"
      :is-scroll-hidden="false"
      :is-can-draggable="true"
      :z-index="50"
      value="悬浮球！"
    />
    <div class="card">
       
        <el-card shadow="always" class="box-card">
    <template #header>
      <div class="card-header">
         <el-avatar src="/favicon.ico" />
        <el-button class="button" text>切换用户</el-button>
      </div>
    </template>
      <el-table
    :data="tableData"
    style="width: 100%"
    :row-class-name="tableRowClassName"
  >
    <el-table-column prop="date" label="Date" width="180" />
    <el-table-column prop="name" label="Name" width="180" />
    <el-table-column prop="address" label="Status" />
  </el-table>
  </el-card>
  
    </div>
  </div>
    
    
</template>
<script lang="ts" setup>
import DragBall from '@/components/Dragball.vue'
interface User {
  date: string
  name: string
  address: string
}

const tableRowClassName = ({
  row,
  rowIndex,
}: {
  row: User
  rowIndex: number
}) => {
  if (rowIndex === 1) {
    return 'warning-row'
  } else if (rowIndex === 3) {
    return 'success-row'
  }
  return ''
}

const tableData: User[] = [
  {
    date: '2016-05-03',
    name: '试验一',
    address: '已处理',
  },
  {
    date: '2016-05-02',
    name: '试验二',
    address: '正在处理',
  },
  {
    date: '2016-05-04',
    name: '试验三',
    address: '已处理',
  },
  {
    date: '2016-05-01',
    name: '试验四',
    address: '未处理',
  },
]
</script>
<style>
.el-table .warning-row {
  --el-table-tr-bg-color: var(--el-color-warning-light-9);
}
.el-table .success-row {
  --el-table-tr-bg-color: var(--el-color-success-light-9);
}
.card {
     display: flex;
    justify-content: center;
    align-items: center
}
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.text {
  font-size: 14px;
}

.item {
  margin-bottom: 18px;
}

.box-card {
  width: 480px;
}
</style>