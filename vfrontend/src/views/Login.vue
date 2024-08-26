<template>
  <div class="login-bg">
    <vue-particles id="tsparticles" :particlesInit="particlesInit" :particlesLoaded="particlesLoaded"
      :options="data.options" />
    <div class="login-card">
      <!-- <el-row style="width: 100%;margin: 0;padding: 0px;">
                <el-col :span="12"><el-link id='denglu' onmouseover='onMouseOver()' onclick="changePage('login')" >登录</el-link></el-col>
                <el-col :span="12"><el-link id='zhuce' onmouseover='onMouseOver()' onclick="changePage('register')" >注册</el-link></el-col>
            </el-row>   -->

      <el-row style="margin-top: 5px;">
        <el-col :span="9" :offset="2"><el-button class="a-btn"
            :style="{ 'border-bottom': isActive === 'login' ? '2px solid #dbeec1' : 'none' }"
            @click="setActive('login')">登录</el-button> </el-col>
        <el-col :span="9" :offset="2"><el-button class="a-btn"
            :style="{ 'border-bottom': isActive === 'register' ? '2px solid #dbeec1' : 'none' }"
            @click="setActive('register')">注册</el-button></el-col>
      </el-row>

      <el-row style="width: 100%;height: 70%;display: flex;align-items: center;justify-content: center;padding: 0px;">
        <el-form ref="form" :model="loginForm" label-width="20px" rules="rules"
          style="width: 85%;height: 80%;margin: 0;padding: 0px; ">
          <el-form-item  prop="account">
            <el-input v-model="loginForm.account" placeholder="User"></el-input>
          </el-form-item>
          <el-form-item  prop="password">
            <el-input type="password" v-model="loginForm.password" placeholder="Password"></el-input>
          </el-form-item>

        </el-form>
        <!-- <el-button class="btn" type="primary" v-if="isActive === 'login'" @click="$router.push('/')">登录</el-button> -->
        <el-button class="b-btn" type="primary" v-if="isActive === 'login'" @click="handleLogin">登录</el-button>
        <el-button class="b-btn" type="primary" v-else @click="handleRegister">注册</el-button>
      </el-row>
    </div>
  </div>
</template>


<script setup>
import { loadFull } from "tsparticles"
import { ref } from "vue";
import axios from "axios";

const form = ref();

// 控制当前激活的按钮  
const isActive = ref('login');

// 切换激活状态的函数  
function setActive(type) {
  isActive.value = type;
}

const isLogin = ref(true)

const loginForm = ref({
  account: "a",
  password: "",
});

const handleLogin = async () => {
  try {
    const res = await axios.post('http://127.0.0.1:8000/api/login', loginForm.value)
    console.log(res.data)
    if (res.data.error_code === 0) {
      
      ElMessage.success("登录成功")
    } else {
      ElMessage.error(res.data.msg)
    }

  } catch (error) {
    console.log(error)
  }

}
//const rules = {
//  account: [
//    { required: true, message: '请输入用户名', trigger: 'blur' },
//    { min: 1, max: 10, message: '用户名必须是 5-10位 的字符', trigger: 'blur' }
//  ],
//  password: [
//    { required: true, message: '请输入密码', trigger: 'blur' },
//    {
//      pattern: /^\S{1,15}$/,
//      message: '密码必须是 6-15位 的非空字符',
//      trigger: 'blur'
//    }
//  ],
//}
//const login = async () => {
//  const valid = await form.value.validate()
//  if (valid) {
//    const res = await userLoginService(formModel.value)
//    console.log(res.data)
//    const tokenString = res.data.data
//    let user = JSON.parse(decodeURIComponent(escape(window.atob(tokenString.split('.')[1]))))
//    ElMessage.success("登录成功")
//    userStore.setToken(tokenString, formModel.value.userAccountId, formModel.value.userPassword, user.post_id)
//    router.push('/')
//
//    // try {
//    //   const res = await axios.post("http://124.71.209.5:2345/login/1", formModel.value)
//    //   if (res.data.code === 0) {
//    //     ElMessage.success('登录成功')
//    //     console.log(res.data)
//    //     router.push('/')
//    //   } else {
//    //     ElMessage.error(res.data.message);
//    //   }
//    // } catch (error) {
//    //   console.error('Error fetching orders:', error);
//    // }
//  }
//}
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
        value: "#d8f5ff",
      },
      links: {
        color: "#ffffff",
        distance: 150,
        enable: true,
        opacity: 0.25,
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
        speed: 0.2,
        straight: false,
      },
      number: {
        density: {
          enable: true,
          value_area: 800,
        },
        value: 60,
      },
      opacity: {
        value: 0.95,
      },
      shape: {
        type: "circle",
      },
      size: {
        random: false,
        value: 1.2,
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
  background: url("/src/assets/star.jpg") no-repeat center;
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
  height: 285px;
  opacity: 1;
//  filter: blur(0.5px);

  background-color: #0a9cdb;
  background-color: #fff;

  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  border-radius: 10px;
  border: 2px solid transparent;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);
  padding: 0 0 0 0;
}

.login-register-container {
  display: flex;
  gap: 20px;
  /* 按钮之间的间隔 */
}

.a-btn {
  width: 100%;
  border: none;
  border-radius: 0px;
 // border-bottom:  #0a9cdb;
  border-bottom:2px solid ;
  text-align: center;
  height: 40px;
  font-family: 'Courier New', Courier, monospace;
  &:active {
    border: none;

  }

  &:hover {
    background-color: #fff;
  }
}




.b-btn {
  width: 50%;
  height: 40px;
  margin-top: 16px;
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