import { createApp } from 'vue'
import App from './App.vue'
import router from './router/Router.js'
import ElementPlus from 'element-plus'
import  zhCn  from 'element-plus/dist/locale/zh-cn.mjs'
import axios from 'axios'
import 'element-plus/dist/index.css'


axios.defaults.baseURL = 'http://localhost:2025'; 
axios.defaults.headers.post['Content-Type'] = 'application/json';
axios.defaults.withCredentials = true;

const app=createApp(App)
app.use(ElementPlus,{
    locale:zhCn
})
app.use(router)
app.mount('#app')
