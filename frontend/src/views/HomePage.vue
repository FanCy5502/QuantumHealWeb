<template>
    <div class="home-container">
      <h2>上传肿瘤数据</h2>
      <input type="file" @change="handleFileUpload" accept=".xlsx" />
      <button @click="submitFile">上传</button>
      <p v-if="uploadMessage" :class="{'success': uploadSuccess, 'error': !uploadSuccess}">
        {{ uploadMessage }}
      </p>

      <h2>已上传的病例</h2>
    <table v-if="patients.length > 0">
      <thead>
        <tr>
          <th>患者 ID</th>
          <th>肿瘤大小 (体素数)</th>
          <th>上传时间</th>
          <th>操作</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="patient in patients" :key="patient.patient_id">
          <td>{{ patient.patient_id }}</td>
          <td>{{ patient.tumor_size }}</td>
          <td>{{ formatDate(patient.upload_timestamp) }}</td>
          <td>
            <button @click="viewPrediction(patient.patient_id)">查看预测结果</button>
            <button @click="viewClustering(patient.patient_id)">查看聚类结果</button>
          </td>
        </tr>
      </tbody>
    </table>
    <p v-else>暂无病例数据</p>
    </div>
  </template>
  
  <script>
  import axios from "axios";
  
  export default {
    data() {
      return {
        file: null, // 上传的文件
        uploadMessage: "",
        uploadSuccess: false,
        patients: [], // 存储已上传的病例数据
      };
    },
    mounted(){
      this.fetchPatientList();
    },
    methods: {
      handleFileUpload(event) {
        this.file = event.target.files[0];
      },
      async submitFile() {
        if (!this.file) {
          this.uploadMessage = "请选择一个文件";
          this.uploadSuccess = false;
          return;
        }
  
        let formData = new FormData();
        formData.append("file", this.file);
  
        try {
          let response = await axios.post("/function/upload", formData, {
            headers: { "Content-Type": "multipart/form-data" },
          });
  
          if (response.data.success) {
            this.uploadMessage = response.data.message //"文件上传成功!";
            this.uploadSuccess = true;
          } else {
            this.uploadMessage = response.data.message;
            this.uploadSuccess = false;
          }
        } catch (error) {
          this.uploadMessage = "上传失败：" + (error.response?.data?.message || error.message);
          this.uploadSuccess = false;
        }
      },

      async fetchPatientList() {
        try {
          let response = await axios.get("/function/get_patient_list");
          if (response.data.success) {
            this.patients = response.data.patients;
          }
        } catch (error) {
          console.error("获取病例列表失败", error);
        }
      },

      formatDate(timestamp) {
        const date = new Date(timestamp);
        return date.toLocaleString();
      },
      viewPrediction(patient_id) {
        this.$router.push(`/prediction/${patient_id}`);
      },
      viewClustering(patient_id) {
        this.$router.push(`/clustering/${patient_id}`);
      }
    },
  };
  </script>
  
  <style scoped>
.home-container {
  max-width: 600px;
  margin: auto;
  padding: 20px;
  text-align: center;
}
input {
  display: block;
  margin: 10px auto;
}
button {
  padding: 8px 12px;
  margin: 5px;
  background-color: #007bff;
  color: white;
  border: none;
  cursor: pointer;
  border-radius: 4px;
}
button:hover {
  background-color: #0056b3;
}
.success {
  color: green;
}
.error {
  color: red;
}
table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
}
th, td {
  border: 1px solid #ddd;
  padding: 8px;
}
th {
  background-color: #f4f4f4;
}
</style>