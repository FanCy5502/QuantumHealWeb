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
import axios from "axios"; // 引入axios

export default {
  setup() {
    const route = useRoute();
    const chartBefore = ref(null);
    const chartAfter = ref(null);
    const beforeData = ref(null);  // 存放放疗前数据
    const afterData = ref(null);   // 存放放疗后数据
    const sendMessage = ref("");   // 存放消息
    const Success = ref(false);    // 成功状态

    onMounted(() => {
      Promise.all([
        axios.get(`/result/view_prediction/${route.params.patient_id}?pre=1`), // 使用axios发起请求
        axios.get(`/result/view_prediction/${route.params.patient_id}?pre=0`)  // 使用axios发起请求
      ])
      .then(([before, after]) => {
        beforeData.value = before.data; // 存放数据到 ref
        afterData.value = after.data;

        console.log("放疗前数据:", before.data);
        console.log("放疗后数据:", after.data);

        if (before.data.success && after.data.success) {
          nextTick(() => {
            renderChart(chartBefore.value, before.data.data, "rgba(255, 165, 0, 0.8)"); // 橙色点（放疗前）
            renderChart(chartAfter.value, after.data.data, "rgba(0, 255, 0, 0.8)");   // 绿色点（放疗后）
          });
        }
      })
      .catch(error => {
        console.error("获取预测数据出错:", error);
      });
    });
   

    function renderChart(container, points) {
      if (!container) {
        console.error("容器未找到:", container);
        return;
      }

      const myChart = echarts.init(container);

      if (!points || points.length === 0) {
        console.warn("数据为空");
        return;
      }

      // 提取X、Y、Z坐标和PETsparse值
      const xs = points.map(p => p[0]);
      const ys = points.map(p => p[1]);
      const zs = points.map(p => p[2]);
      const PETs = points.map(p => p[3]); // PETsparse 值

      // 计算坐标轴范围
      const getRange = arr => [Math.min(...arr), Math.max(...arr)];
      const [xMin, xMax] = getRange(xs);
      const [yMin, yMax] = getRange(ys);
      const [zMin, zMax] = getRange(zs);
      const [petMin, petMax] = getRange(PETs);

      // 映射 PETsparse 到颜色
      function getColor(petValue) {
        const ratio = (petValue - petMin) / (petMax - petMin); // 归一化
        let r, g, b;
        if (ratio < 0.5) {
          // 低于中间值，白色过渡到红色
          r = 255;
          g = Math.round(255 * (1 - ratio * 2)); // 逐渐降低绿色分量
          b = Math.round(255 * (1 - ratio * 2)); // 逐渐降低蓝色分量
        } else {
          // 高于中间值，红色过渡到黑色
          r = Math.round(255 * (1 - (ratio - 0.5) * 2)); // 逐渐降低红色分量
          g = 0;
          b = 0;
        }
        return `rgb(${r}, ${g}, ${b})`;
      }

      myChart.setOption({
        tooltip: {},
        xAxis3D: { type: "value", min: xMin, max: xMax, name: "X" },
        yAxis3D: { type: "value", min: yMin, max: yMax, name: "Y" },
        zAxis3D: { type: "value", min: zMin, max: zMax, name: "Z" },
        grid3D: {
          viewControl: { autoRotate: true, distance: 180 },
        },
        series: [
          {
            type: "scatter3D",
            data: points.map(([x, y, z, PETsparse]) => ({
              value: [x, y, z],
              itemStyle: {
                color: getColor(PETsparse),
                opacity: 0.6, // 增加透明度，提高层次感
              },
            })),
            symbolSize: 5, // 适当调整点的大小
          },
        ],
        visualMap: {
          show: true,
          dimension: 3, // 使用 PETsparse 作为颜色参考
          min: petMin,
          max: petMax,
          calculable: true,
          inRange: {
            color: ["#ffffff", "#ff0000", "#000000"], // 白 -> 红 -> 黑
          },
          text: ["高", "低"], // 颜色条的文字
          left: "right",
          top: "center",
        },
      });
    }


    return { chartBefore, chartAfter, beforeData, afterData, sendMessage, Success };
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
