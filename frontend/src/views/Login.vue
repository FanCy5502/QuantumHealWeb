<template>
    <div class="login-container">
      <el-card class="login-card" shadow="hover">
        <el-container class="login-title">
          <img src="../assets/img/logo.jpg" class="logo">
          <h1>量子智疗平台登录</h1>
        </el-container>
        <el-form :model="form" :rules="rules" label-width="100px">
  
          <!-- 用户名 -->
          <el-form-item label="用户名" prop="username">
            <el-input v-model="form.username" placeholder="请输入用户名">
              <template #prefix>
              </template>
            </el-input>
          </el-form-item>
  
          <!-- 密码 -->
          <el-form-item label="密码" prop="password">
            <el-input v-model="form.password" placeholder="请输入密码" show-password>
              <template #prefix>
              </template>
            </el-input>
          </el-form-item>
          <!-- 登录和注册按钮 -->
          <el-form-item>
            <el-row :gutter="0">
              <el-col :span="12">
                <el-button type="default" @click="handleLogin" plain block>
                  登录
                </el-button>
              </el-col>
              <el-col :span="12">
                <el-button type="default" @click="handleRegister" plain block>
                  没有账号，前往注册
                </el-button>
              </el-col>
            </el-row>
          </el-form-item>
        </el-form>
      </el-card>
    </div>
  </template>
  
  <script>
  import { reactive } from "vue";
  import axios from "axios";
  import { ElMessage } from "element-plus";
  
  export default {
    name: "Login-Form",
    setup() {
      const form = reactive({
        username: "",
        password: "",
        // captcha: "",
      });
      const rules = {
        username: [{ required: true, message: "请输入用户名", trigger: "blur" }],
        password: [{ required: true, message: "请输入密码", trigger: "blur" }],
      };
      //登录页面
      const handleLogin = () => {   // 表单验证
        try {
            axios.post("/auth/login", form).then((res) => {
              console.log(res.data.message);
              if (res.data.success == true) {
                ElMessage.success({
                  message: "登录成功", duration: 500,
                  onClose: () => {
                    const Url = window.location.href.replace(/\/login$/, "/home");
                    window.location.href = Url;
                  }
                });
              } else {
                ElMessage.error(res.data.message || "登录失败");
              }
            })
        } catch (error) {
          ElMessage.error(error.message || "请求出错");
        }
      };
      // 注册跳转
      const handleRegister = () => {
        try {
          const Url = window.location.href.replace(/\/login$/, "/register");
          window.location.href = Url;
        } catch (error) {
          ElMessage.error(error.message || "请求出错");
        }
      };
  
      return {
        form,
        rules,
        handleLogin,
        handleRegister,
      };
    },
  };
  </script>
  
  <style scoped>
  .login-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    background: url('../assets/img/background.jpg');
    background-size: cover;
  }
  
  .login-card {
    width: 410px;
  }
  
  .login-title {
    width: 100%;
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
    margin-bottom: 15px;
    flex-grow: 0;
  }
  
  .login-title h1 {
    font-size: 22px;
    line-height: 22px;
    margin: 0;
    margin-left: 5px;
    font-weight: 500;
  }
  
  /* .captcha-img-container {
    text-align: center;
    cursor: pointer;
  } */
  .logo {
    width: 50px;
    height: 50px;
  }
  </style>
  