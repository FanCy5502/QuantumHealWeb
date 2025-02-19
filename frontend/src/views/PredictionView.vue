<template>
    <div>
      <h2>预测结果 3D 可视化</h2>
      <div class="charts-container">
        <div>
          <h3>放疗前</h3>
          <div ref="chartBefore" class="chart"></div>
        </div>
        <div>
          <h3>放疗后（预测值）</h3>
          <div ref="chartAfter" class="chart"></div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { onMounted, ref } from "vue";
  import { useRoute } from "vue-router";
  import * as echarts from "echarts";
  
  export default {
    setup() {
      const route = useRoute();
      const chartBefore = ref(null);
      const chartAfter = ref(null);
  
      onMounted(() => {
        Promise.all([
          fetch(`/result/view_prediction/${route.params.patient_id}?pre=1`).then(res => res.json()), // 放疗前
          fetch(`/result/view_prediction/${route.params.patient_id}?pre=0`).then(res => res.json())  // 放疗后
        ]).then(([beforeData, afterData]) => {
          if (beforeData.success && afterData.success) {
            renderChart(chartBefore.value, beforeData.data, "rgba(255, 165, 0, 0.8)"); // 橙色点（放疗前）
            renderChart(chartAfter.value, afterData.data, "rgba(0, 255, 0, 0.8)");   // 绿色点（放疗后）
          }
        });
      });
  
      function renderChart(container, points, color) {
        const myChart = echarts.init(container);
        myChart.setOption({
          tooltip: {},
          xAxis3D: { type: "value" },
          yAxis3D: { type: "value" },
          zAxis3D: { type: "value" },
          grid3D: {},
          series: [
            {
              type: "scatter3D",
              data: points,
              symbolSize: 4,
              itemStyle: { color }
            }
          ]
        });
      }
  
      return { chartBefore, chartAfter };
    }
  };
  </script>
  
  <style scoped>
  .charts-container {
    display: flex;
    justify-content: space-around;
    align-items: center;
  }
  .chart {
    width: 400px;
    height: 400px;
  }
  </style>
  