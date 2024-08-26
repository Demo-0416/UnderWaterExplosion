// src/untils/axios.js  
import axios from 'axios';  
  
// 创建一个 axios 实例  
const axiosInstance = axios.create({  
  baseURL: 'https://api.example.com', // 设置全局基址  
  // 你可以在这里添加其他 axios 配置  
  timeout: 1000,  
  headers: {'X-Custom-Header': 'foobar'}  
});  
  
export default axiosInstance;