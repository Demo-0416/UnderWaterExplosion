<template>
  <div class="login-bg">
      <vue-particles id="tsparticles" :particlesInit="particlesInit" :particlesLoaded="particlesLoaded" :options="data.options" />
      <div class="login-card" >
             <el-row style="width: 100%;background-color: blue;margin: 0;padding: 0px;">
                <el-col :span="12"><el-link id='denglu' style='border-bottom:3px sel-linkd #FFA00A;' onmouseover='onMouseOver()' onclick="changePage('login')" >登录</el-link></el-col>
                <el-col :span="12"><el-link id='zhuce' onmouseover='onMouseOver()' onclick="changePage('register')" >注册</el-link></el-col>
            </el-row>  
            
               
                
            
            <el-row style="width: 100%;height: 80%;display: flex;align-items: center;justify-content: center;padding: 0px;">
                <el-form ref="loginForm" :model="loginForm" label-width="80px" rules="rules" style="background-color: blue;width: 85%;height: 80%;margin: 0;padding: 0px; "> 
                    <el-form-item label="用户名">
                        <el-input v-model="loginForm.username" placeholder="请输入用户名"></el-input>
                    </el-form-item>
                    <el-form-item label="密码">
                        <el-input type="password" v-model="loginForm.password" placeholder="请输入密码"></el-input>
                    </el-form-item>
                  
                </el-form>
                <el-button type="primary" v-if="isLogin" @click="handleLogin" >登录</el-button>
                <el-button type="primary" v-else @click="handleRegister" >注册</el-button>
            </el-row>
      </div>
  </div>
</template>


<script setup>
import { loadFull } from "tsparticles"
import { ref } from "vue";

const isLogin=ref(true)

const loginForm = ref({
  username: "",
  password: "",
});
const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 1, max: 10, message: '用户名必须是 5-10位 的字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    {
      pattern: /^\S{1,15}$/,
      message: '密码必须是 6-15位 的非空字符',
      trigger: 'blur'
    }
  ],
}
const login = async () => {
  const valid=await form.value.validate()
  if(valid){
    const res = await userLoginService(formModel.value)
    console.log(res.data)
    const tokenString = res.data.data
    let user = JSON.parse(decodeURIComponent(escape(window.atob(tokenString.split('.')[1]))))
    ElMessage.success("登录成功")
    userStore.setToken(tokenString,formModel.value.userAccountId,formModel.value.userPassword,user.post_id)
    router.push('/')
  
  // try {
  //   const res = await axios.post("http://124.71.209.5:2345/login/1", formModel.value)
  //   if (res.data.code === 0) {
  //     ElMessage.success('登录成功')
  //     console.log(res.data)
  //     router.push('/')
  //   } else {
  //     ElMessage.error(res.data.message);
  //   }
  // } catch (error) {
  //   console.error('Error fetching orders:', error);
  // }
}
}
const data = ref({
  options: {
      fpsLimit: 100,
      interactivity: {
          events: {
              onClick: {
                  enable: true,
                  mode: "push",
              },
              onHover: {
                  enable: true,
                  mode: "grab",
              },
              resize: true,
          },
          modes: {
              bubble: {
                  distance: 400,
                  duration: 2,
                  opacity: 0.6,
                  size: 10,
              },
              push: {
                  quantity: 4,
              },
              repulse: {
                  distance: 200,
                  duration: 0.4,
              },
          },
      },
      particles: {
          color: {
              value: "#ffffff",
          },
          links: {
              color: "#ffffff",
              distance: 150,
              enable: true,
              opacity: 0.5,
              width: 1,
          },
          collisions: {
              enable: true,
          },
          move: {
              direction: "none",
              enable: true,
              outMode: "bounce",
              random: false,
              speed: 0.5,
              straight: false,
          },
          number: {
              density: {
                  enable: true,
                  value_area: 800,
              },
              value: 40,
          },
          opacity: {
              value: 0.5,
          },
          shape: {
              type: "circle",
          },
          size: {
              random: true,
              value: 3,
          },
      },
      detectRetina: true,
  },
})

// 粒子效果
const particlesInit = async (engine) => {
 await loadFull(engine)
}
const particlesLoaded = async (container) => {
 // console.log("Particles container loaded", container)
}
</script>
<style lang="less" scoped>
/**放置背景图片 */
.login-bg {
  width: 100%;
  height: 100%;
  background: url("/src/assets/star.jpg") no-repeat
      center;
  background-size: cover;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  overflow: hidden;
  position: relative;
}
.login-card {
  width: 380px;
  height: 320px;
  opacity: 0.7;
  background-color: #0a9cdb;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  border-radius: 10px;
  border: 2px solid transparent; /* 根据需要调整边框宽度 */  
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);
  padding: 0 0 0 0;

}
.el-button {
  width: 100%;
  height: 40px;
  line-height: 40px;
  text-align: center;
  color: #fff;
  background-color: #0a9cdb;
  border-radius: 0px;
  border: 0;
  cursor: pointer;
  transition: all 0.3s ease;
  &:hover {
    background-color: #ccc;
    color: #fff;
    opacity: 0.8;
  }

}
.el-form-item {
  margin-top: 45px;
}
.el-input {
  width: 100%;
  height: 34px;
  line-height: 34px;
  padding: 0 10px;
  font-size: 16px;
  transition: all 0.3s ease;
  &:focus {
    border-color: #0a9cdb;
    outline: none;
  }

}
</style>