<<template>
    <div class="common-layout">
        <el-container>
          <el-aside width="22%" style="">Aside</el-aside>
          
            <!-- <el-header style="background-color: #b3c0d1;">Header</el-header> -->
            <el-main width="50%" >Main</el-main>
         
          <!-- <el-aside width="22%" style="background-color: #d9ecff;margin-right: 2.5%; border-radius: 12px;">Aside</el-aside> -->
        </el-container>
        </div>
</template>

<script setup>

</script>

<style lang="scss" scoped>
.el-aside {
  background-color: #d9ecff;margin-left: 2.5%; border-radius: 12px;
}
.el-main {
  background-color: #e9eef3;margin: 50px 2.3%; border-radius: 12px;
}
</style>