<template>
  <div class="container">
    <!-- 左侧：招聘信息列表 -->
    <div class="left">
      <h1>招聘信息列表</h1>
      <div id="job-list">
        <div v-for="job in jobs" :key="job.id" class="job-container">
          <a :href="job.job_card_link" target="_blank">
            <div>
              <span class="job-title">{{ job.title }}</span>
              <span class="salary">({{ job.salary_min }}-{{ job.salary_max }}元/天)</span>
            </div>
            <div class="job-keywords">
              <span v-for="(keyword, index) in job.key_words" :key="index" class="keyword">
                {{ keyword }}
              </span>
            </div>
            <div class="job-detail">
              <span class="job-label">通勤时间:</span> {{ job.duration_hours_minutes }}
              <span class="job-label">通勤费用:</span> {{ job.cost }}元
            </div>
            <div class="job-detail">
              <span class="job-label">到岗要求:</span> {{ job.internship_days }} 天/周 {{ job.internship_months }} 个月
            </div>
            <div class="job-detail">
              <span class="job-label">地址:</span> {{ job.address }}
            </div>
          </a>
        </div>
      </div>
    </div>

    <!-- 右侧：图表 -->
    <div class="right">
      <div class="keyword-filter">
        <h3>选择关键词筛选：</h3>
        <form @submit.prevent="filterJobs">
          <div class="keywords-container">
            <label v-for="(keyword, index) in all_keywords" :key="index" class="keyword-label">
              <input type="checkbox" :value="keyword" v-model="selected_keywords" class="keyword-checkbox" />
              <span class="keyword-text">{{ keyword }}</span>
            </label>
          </div>
          <!-- 筛选按钮 -->
          <button type="submit" class="filter-button">筛选</button>
        </form>
      </div>
      <h1>关键词频率分析</h1>
      <div class="chart-container" id="pie-chart"></div>
      <div class="chart-container" id="bar-chart"></div>
      <h1>关键词对应的平均薪资</h1>
      <div class="chart-container" id="salary-bar-chart"></div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import * as echarts from 'echarts'; // 引入 ECharts

export default {
  data() {
    return {
      jobs: [],
      all_keywords: [],
      selected_keywords: [],
      pie_html: '', // 饼图 HTML（暂不使用）
      bar_html: '', // 频率柱状图的 HTML（废弃，改用 JSON 数据渲染）
      salary_bar_html: '', // 平均薪资柱状图的 HTML（废弃，改用 JSON 数据渲染）
      pieChart: null, // 存储频率玫瑰饼图实例
      barChart: null, // 存储频率柱状图实例
      salaryBarChart: null, // 存储平均薪资柱状图实例
    };
  },
  methods: {
    // 从后端获取数据
    async fetchData() {
      try {
        const response = await axios.get('/job', {
          params: { keywords: this.selected_keywords },
        });
        this.jobs = response.data.jobs;
        this.all_keywords = response.data.all_keywords;

        // 使用后端返回的 JSON 数据渲染图表
        this.renderPieChart(JSON.parse(response.data.pie_html)); // 渲染关键词频率饼图
        this.renderBarChart(JSON.parse(response.data.bar_html)); // 渲染关键词频率柱状图
        this.renderSalaryBarChart(JSON.parse(response.data.salary_bar_html)); // 渲染平均薪资柱状图
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    },

    // 渲染关键词频率饼图
    renderPieChart(pieChartData) {
      const chartDom = document.getElementById('pie-chart'); // 获取饼图容器
      if (!this.pieChart) {
        // 初始化 ECharts 实例
        this.pieChart = echarts.init(chartDom);
      }
      this.pieChart.setOption(pieChartData); // 设置图表数据
    },

    // 渲染关键词频率柱状图
    renderBarChart(barChartData) {
      const chartDom = document.getElementById('bar-chart'); // 获取柱状图容器
      if (!this.barChart) {
        // 初始化 ECharts 实例
        this.barChart = echarts.init(chartDom);
      }
      this.barChart.setOption(barChartData); // 设置图表数据
    },

    // 渲染关键词平均薪资柱状图
    renderSalaryBarChart(salaryBarChartData) {
      const chartDom = document.getElementById('salary-bar-chart'); // 获取柱状图容器
      if (!this.salaryBarChart) {
        // 初始化 ECharts 实例
        this.salaryBarChart = echarts.init(chartDom);
      }
      this.salaryBarChart.setOption(salaryBarChartData); // 设置图表数据
    },

    // 点击筛选按钮时重新加载数据和渲染图表
    filterJobs() {
      this.fetchData();
    },
  },
  mounted() {
    this.fetchData(); // 初次加载数据
  },
};
</script>


<style scoped>
  body {
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 0;
    display: flex;
    flex-direction: row;
    height: 100vh; /* 页面高度固定为视窗高度 */
  }

  .container {
    display: flex;
    flex: 1;
    overflow: hidden; /* 防止页面整体滚动 */
  }

  .left, .right {
    height: 100%; /* 区域高度占满页面 */
    overflow-y: auto; /* 启用垂直滚动 */
    padding: 20px;
  }

  .left {
    flex: 5; /* 左侧宽度比例 */
    background-color: #f9f9f9;
  }

  .right {
    flex: 5; /* 右侧宽度比例 */
    background-color: #fff;
    border-left: 2px solid #ccc;
  }

  .job-container {
    border: 2px solid #ccc;
    border-radius: 10px;
    background: #fff;
    box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
    padding: 20px; /* 增大内边距 */
    margin-bottom: 20px; /* 增大间距 */
  }

  .job-title {
    font-size: 1.6em; /* 增大标题字体 */
    font-weight: bold;
    margin-bottom: 8px;
  }

  .salary {
    color: #e7643c;
    font-weight: bold;
    font-size: 1.4em; /* 增大薪资字体 */
  }

  .job-keywords {
    font-size: 1.1em; /* 关键词字体加大 */
    color: #757373;
    margin-bottom: 15px;
  }

  .keyword {
    background-color: #e1f0f6; /* 浅灰色背景 */
    padding: 6px 12px; /* 内边距 */
    margin-right: 10px; /* 关键词之间的间距 */
    border-radius: 5px; /* 圆角 */
    display: inline-block; /* 使关键词在同一行显示 */
    font-size: 15px; /* 字体大小 */
  }

  .job-detail {
    margin-top: 12px;
    font-size: 1.1em;
    color: #333;
  }

  .job-detail span.job-label {
    font-weight: bold;
    color: #333;
  }

  .chart-container {
    width: 100%; /* 图表宽度自适应 */
    height: 450px; /* 图表高度固定 */
    margin-bottom: 28px; /* 增大图表间距 */
    padding: 15px;
    border: 1px solid #ddd;
    background-color: #fafafa;
    overflow: visible; /* 确保文字显示完整 */
  }

  .keyword-filter {
    width: 100%;
    margin-bottom: 25px;
  }

  .keywords-container {
    display: flex;
    flex-wrap: wrap; /* 自动换行 */
    gap: 1px; /* 每个复选框之间的间隔 */
  }

  .keywords-container label {
    width: calc(25% - 10px); /* 每行最多显示 4 个关键词，减去间隔 */
    margin-bottom: 10px;
    font-size: 15px;
  }

  a {
    color: #000000;
    text-decoration: none;
  }
  .keyword-filter {
    margin-bottom: 30px;
    padding: 20px;
    background-color: #f7f7f7;
    border-radius: 8px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  }

  h3 {
    font-size: 1.6em;
    margin-bottom: 15px;
    font-weight: bold;
    color: #333;
  }

  .keywords-container {
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
    margin-bottom: 20px;
  }

  .keyword-label {
    display: flex;
    align-items: center;
    font-size: 1.1em;
    color: #555;
  }

  .keyword-checkbox {
    margin-right: 8px;
    accent-color: #4CAF50; /* 使用绿色作为复选框的颜色 */
  }

  .keyword-text {
    font-size: 1.1em;
  }

  .filter-button {
    background-color: #4CAF50;
    color: white;
    font-size: 1.2em;
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    transition: background-color 0.3s ease;
  }

  .filter-button:hover {
    background-color: #45a049;
  }

  .filter-button:active {
    background-color: #388e3c;
  }
  
</style>
