<template> 
  <div>
    <h2>预测结果 3D 可视化</h2>

    <!-- 显示后端返回的 JSON 数据，便于调试 -->
    <!-- <div class="debug-info">
      <h3>放疗前数据 (beforeData)</h3>
      <pre>{{ JSON.stringify(beforeData, null, 2) }}</pre>
      
      <h3>放疗后数据 (afterData)</h3>
      <pre>{{ JSON.stringify(afterData, null, 2) }}</pre>
    </div> -->

    <div class="charts-container">
      <p v-if="sendMessage" :class="{'success': Success, 'error': !Success}">
        {{ sendMessage }}
      </p>
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
import { onMounted, ref, nextTick } from "vue";
import { useRoute } from "vue-router";
import * as echarts from "echarts";
import "echarts-gl";
import axios from "axios"; 

export default {
  setup() {
    const route = useRoute();
    const chartBefore = ref(null);
    const chartAfter = ref(null);
    let myChartBefore = null;
    let myChartAfter = null;

    onMounted(() => {
      Promise.all([
        axios.get(`/result/view_prediction/${route.params.patient_id}?pre=1`),
        axios.get(`/result/view_prediction/${route.params.patient_id}?pre=0`),
      ])
      .then(([before, after]) => {
        if (!before.data.success || !before.data.data.length) {
          console.error("放疗前数据为空或格式错误:", before.data);
          return;
        }
        if (!after.data.success || !after.data.data.length) {
          console.error("放疗后数据为空或格式错误:", after.data);
          return;
        }

        nextTick(() => {
          if (chartBefore.value && chartAfter.value) {
            if (!myChartBefore) myChartBefore = echarts.init(chartBefore.value);
            if (!myChartAfter) myChartAfter = echarts.init(chartAfter.value);
            
            updateChart(myChartBefore, before.data.data);
            updateChart(myChartAfter, after.data.data);
          } else {
            console.error("ECharts 容器未找到");
          }
        });
      })
      .catch(error => console.error("获取预测数据出错:", error));
    });

    function updateChart(chartInstance, points) {
      if (!points || points.length === 0) {
        console.error("数据为空");
        return;
      }

      const xs = points.map(p => p[0]);
      const ys = points.map(p => p[1]);
      const zs = points.map(p => p[2]);
      const PETs = points.map(p => p[3]);

      const getRange = arr => arr.length > 0 ? [Math.min(...arr), Math.max(...arr)] : [0, 1];
      const [xMin, xMax] = getRange(xs);
      const [yMin, yMax] = getRange(ys);
      const [zMin, zMax] = getRange(zs);
      const [petMin, petMax] = getRange(PETs);

      chartInstance.setOption({
        tooltip: {
          formatter: params => params.value ? `X: ${params.value[0]}<br>Y: ${params.value[1]}<br>Z: ${params.value[2]}<br>PET: ${params.value[3]}` : "无数据"
        },
        xAxis3D: { type: "value", min: xMin, max: xMax, name: "X" },
        yAxis3D: { type: "value", min: yMin, max: yMax, name: "Y" },
        zAxis3D: { type: "value", min: zMin, max: zMax, name: "Z" },
        grid3D: { viewControl: { autoRotate: true, distance: 180 } },
        series: [{
          type: "scatter3D",
          data: points.map(([x, y, z, PETsparse]) => [x, y, z, PETsparse]),
          symbolSize: 5,
        }],
        visualMap: {
          show: true,
          dimension: 3,
          min: petMin,
          max: petMax,
          calculable: true,
          inRange: { color: ["blue", "green", "yellow", "red"] },
          text: ["高", "低"],
          left: "right",
          top: "center",
        },
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

.debug-info {
  background: #f4f4f4;
  padding: 10px;
  border: 1px solid #ccc;
  margin-bottom: 20px;
}
pre {
  white-space: pre-wrap;
  word-wrap: break-word;
  background: #fff;
  padding: 10px;
  border-radius: 5px;
  overflow-x: auto;
}
</style>
