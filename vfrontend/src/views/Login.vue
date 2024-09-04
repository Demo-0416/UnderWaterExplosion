<template>
  <div class="login-bg">
    <vue-particles id="tsparticles" :particlesInit="particlesInit" :particlesLoaded="particlesLoaded"
      :options="data.options" />
    <div class="login-card">
      <span/>
      <span/>
      <span/>
      <span/>
   

      <el-row style="margin-top: 5px;">
        <el-col :span="9" :offset="2"><el-button class="a-btn"
            :style="{ 'border-bottom': isActive === 'login' ? '2px solid #dbeec1' : 'none' }"
            @click="setActive('login')">登录</el-button> </el-col>
        <el-col :span="9" :offset="2"><el-button class="a-btn"
            :style="{ 'border-bottom': isActive === 'register' ? '2px solid #dbeec1' : 'none' }"
            @click="setActive('register')">注册</el-button></el-col>
      </el-row>

      <el-row style="width: 100%;height: 80%;display: flex;align-items: center;justify-content: center;padding: 0px;">
        <el-form class="login-form" ref="form" :model="loginForm"  rules="rules" v-if="isActive === 'login'"
          style="width: 85%;height: 80%;margin: 0;padding: 0px; ">
          <el-form-item  >
            <!-- <el-input v-model="loginForm.username" placeholder="User"></el-input> -->
            <input type="text" v-model="loginForm.username" placeholder="User"></input>
          </el-form-item>
          
          <el-form-item  >
            <!-- <el-input type="password" v-model="loginForm.password" placeholder="Password"></el-input> -->
            <input type="password" v-model="loginForm.password" placeholder="Password"></input>
          </el-form-item>
      
        </el-form>
        <el-form class="register-form" ref="form" :model="registerForm" :rules="rules" v-else
  style="width: 85%;height: 80%;margin: 0;padding: 0px; ">
  <el-form-item >
    <input type="text" v-model="registerForm.username" placeholder="User"/>
  </el-form-item>
  
  <el-form-item >
    <input type="password" v-model="registerForm.password1" placeholder="Password1"/>
  </el-form-item>
  <el-form-item >
    <input type="password" v-model="registerForm.password2" placeholder="Password2">
  </el-form-item>
  <el-form-item >
    <input type="text" v-model="registerForm.email" placeholder="Email">
  </el-form-item>
</el-form>
        <!-- <el-button class="btn" type="primary" v-if="isActive === 'login'" @click="$router.push('/')">登录</el-button> -->
        <button class="b-btn" type="primary" v-if="isActive === 'login'" @click="handleLogin">登录
       
        </button>
        <el-button class="b-btn" type="primary" v-else @click="handleRegister">注册</el-button>
      </el-row>
    </div>
  </div>
</template>


<script setup>
import { loadFull } from "tsparticles"
import { ref } from "vue";
import axios from "axios";
import { ElMessage, ElMessageBox } from 'element-plus'
import { reactive } from "vue";
// import router from "@/router";
import { useRouter } from 'vue-router';
const form = ref();

// 控制当前激活的按钮  
const isActive = ref('login');

// 切换激活状态的函数  
function setActive(type) {
  isActive.value = type;
}

const isLogin = ref(true)

const loginForm = reactive({
  username: "",
  password: "",
});

const registerForm = reactive({
  username: "d",
  password1: "",
  password2: "",
  email: "",
});

const router = useRouter();
const handleLogin = async () => {
  try {
    const res = await axios.post('http://127.0.0.1:8000/user_management/login/', loginForm, {
      headers: {
        'Content-Type': 'application/json'
      }}
    );

    console.log(loginForm);
    console.log(res.data);
    if (res.data.code == 0) {
      
      ElMessage({type: 'success', message: '登录成功'})
      router.push('/list')
      
    } else {
      ElMessage.error(res.data.state)
      
    }

  } catch (error) {
    console.log(error)
  }

}

const handleRegister = async() => {
  try {
    // const testform = {
    //   username: "test_username45",
    //   password1: "test_password",
    //   password2: "test_password",
    //   email: "2240829627@qq.com"
    // };
    const res = await axios.post('http://127.0.0.1:8000/user_management/register/', registerForm)
    console.log(registerForm)
   console.log(res.data)
 
    if (res.data.code == 0) {
      ElMessage.success("注册成功")
    } else {
      ElMessage.error(res.data.state)
    }
}
catch (error) {
  console.log(error)
}
}
//const rules = {
//  username: [
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
//    userStore.setToken(tokenString, formModel.value.userusernameId, formModel.value.userPassword, user.post_id)
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
          value_area: 1000,
        },
        value: 100,
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
  width: 25%;
  height: 45%;
  opacity: 1;
//  filter: blur(0.5px);


background-color: #0c1622;

  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  //border-radius: 10px;
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
  background: transparent;
  font-family: 'Courier New', Courier, monospace;
  &:active {
    border: none;

  }

  &:hover {
    background-color: transparent;
  }
}




.b-btn {
  width: 50%;
  height: 40px;
  margin-top: 16px;
  line-height: 40px;
  text-align: center;
  color: #03e9f4;
  background-color: #ccc;
  border-radius: 0px;
  border: 0;
  cursor: pointer;
  transition: all 0.3s ease;

  &:hover {
    border-radius: 5px;
			color: #fff;
			background: #03e9f4;
			box-shadow: 0 0 5px 0 #03e9f4,
				0 0 25px 0 #03e9f4,
				0 0 50px 0 #03e9f4,
				0 0 100px 0 #03e9f4;
			transition: all 1s linear;
  }

}
.el-form {

  /*display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;*/
  
}
.login-form .el-form-item {
  
  margin-top: 18%;
  border-bottom:2px solid #fff; 
}

.register-form .el-form-item {
  margin-top: 3.5%;
  border-bottom:2px solid #fff; 
}
 .el-form-item input {
  width: 100%;
  height: 34px;
  line-height: 34px;
  padding: 0 0px 0 0px;
  font-size: 16px;
  color: white;
  border: none;

  background: transparent;
  outline: none;
  box-sizing: border-box;
/*   &:focus {
     border: 0;
     background: transparent;
     outline: none;
   }
  &:hover {
    border: 0;
    background: transparent;
    outline: none;
  }*/
  &:-webkit-autofill {
    box-shadow: 0 0 0px 1000px #0c1622 inset;
    -webkit-text-fill-color: #fff;
    border: none;
    
  } 
 }

/*.el-input {
 width: 100%;
 height: 34px;
 line-height: 34px;
 padding: 0 0px;
 font-size: 16px;
 border: none;
 background: transparent;
 outline: none;
  &:focus {
    border-color: #0a9cdb;
    outline: none;
  }

}*/

.login-card>span {
  position: absolute;
}

.login-card>span:nth-child(1) {
  width: 100%;
  height: 2px;
  background: -webkit-linear-gradient(left, transparent, #03e9f4);
  left: -100%;
  top: 0px;
  animation: line1 1s  linear infinite;
}

@keyframes line1 {

  50%,
  100% {
    left: 100%;
  }
}

.login-card>span:nth-child(2) {
  width: 2px;
  height: 100%;
  background: -webkit-linear-gradient(top, transparent, #03e9f4);
  right: 0px;
  top: -100%;
  animation: line2 1s 0.15s linear infinite;
}

@keyframes line2 {

  50%,
  100% {
    top: 100%;
  }
}

.login-card>span:nth-child(3) {
  width: 100%;
  height: 2px;
  background: -webkit-linear-gradient(left, #03e9f4, transparent);
  left: 100%;
  bottom: 0px;
  animation: line3 1s 0.3s linear infinite;
}

@keyframes line3 {

  50%,
  100% {
    left: -100%;
  }
}

.login-card>span:nth-child(4) {
  width: 2px;
  height: 100%;
  background: -webkit-linear-gradient(top, transparent, #03e9f4);
  left: 0px;
  top: 100%;
  animation: line4 1s 0.5s linear infinite;
}

@keyframes line4 {

  50%,
  100% {
    top: -100%;
  }
}

</style>