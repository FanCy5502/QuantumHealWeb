<template>
    <div class="login-container">
        <el-card class="login-card" shadow="hover">
            <el-container class="login-title">
                <img src="../assets/img/logo.jpg" class="logo">
                <h1>量子智疗平台注册</h1>
            </el-container>
            <el-form :model="form" :rules="rules" label-width="100px">

                <!-- 用户名 -->
                <el-form-item label="用户名" prop="username">
                    <el-input v-model="form.username" placeholder="请输入用户名">
                        <template #prefix>
                            <!-- <el-icon><user /></el-icon> -->
                        </template>
                    </el-input>
                </el-form-item>

                <!-- 密码 -->
                <el-form-item label="密码" prop="password">
                    <el-input v-model="form.password" placeholder="请输入密码" show-password>
                        <template #prefix>
                            <!-- <el-icon><lock /></el-icon> -->
                        </template>
                    </el-input>
                </el-form-item>

                <!-- 确认密码 -->
                <el-form-item label="确认密码" prop="c_password">
                    <el-input v-model="form.c_password" placeholder="请再次输入密码" show-password>
                        <template #prefix>
                            <!-- <el-icon><lock /></el-icon> -->
                        </template>
                    </el-input>
                </el-form-item>

                <!-- 登录和注册按钮 -->
                <el-form-item>
                    <el-row :gutter="0">
                        <el-col :span="12">
                            <el-button type="default" @click="handleRegister" plain block>
                                注册
                            </el-button>
                        </el-col>
                        <el-col :span="12">
                            <el-button type="default" @click="handleLogin" plain block>
                                已有帐号，前往登录
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
// import { User, Lock } from "@element-plus/icons-vue";

export default {
    name: "Register-Form",
    // components: {
    //   user: User,
    //   lock: Lock,
    // },
    setup() {
        const form = reactive({
            username: "",
            password: "",
            c_password: "",
            // captcha: "",
        });
        const rules = {
            username: [{ required: true, message: "请输入用户名", trigger: "blur" }],
            password: [{ required: true, message: "请输入密码", trigger: "blur" }],
            c_password: [{ required: true, message: "请确认密码", trigger: "blur" }],
        };

        const handleRegister = () => {
            if (form.password != form.c_password) { ElMessage.error("密码不一致！注册失败"); }
            else {
                try {
                    axios.post("/auth/register", form).then((res) => {
                        console.log(res.data.message);
                        if (res.data.success == true) {
                            ElMessage.success({
                                message: "注册成功", duration: 1200,
                                onClose: () => {
                                    const Url = window.location.href.replace(/\/register$/, "/login");
                                    window.location.href = Url;
                                }
                            });
                        } else {
                            ElMessage.error(res.data.message || "注册失败");
                        }
                    })
                } catch (error) {
                    ElMessage.error(error.message || "请求出错");
                }
            }

        };
        const handleLogin = () => {
            try {
                const Url = window.location.href.replace(/\/register$/, "/login");
                window.location.href = Url;
            } catch (error) {
                ElMessage.error(error.message || "请求出错");
            }
        };
        return {
            form,
            rules,
            // loading,
            // captchaSrc,
            // refreshCaptcha,
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