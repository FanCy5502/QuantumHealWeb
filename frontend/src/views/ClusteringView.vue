<template>
  <div>
    <h2>聚类结果 3D 可视化</h2>
    <div ref="chart" style="width: 800px; height: 600px;"></div>
  </div>
</template>

<script>
import { onMounted, ref } from "vue";
import { useRoute } from "vue-router";
import * as echarts from "echarts";
import "echarts-gl";
import axios from "axios"; // 导入 axios

export default {
  setup() {
    const route = useRoute();
    const chart = ref(null);

    onMounted(() => {
      axios
        .get(`/result/view_clustering/${route.params.patient_id}`) // 使用 axios 发起请求
        .then((response) => {
          const data = response.data; // 获取响应的数据
          if (data.success) {
            renderChart(data.data);
          }
        })
        .catch((error) => {
          console.error("请求失败:", error);
        });
    });
    
    function renderChart(points) {
      if (!points || points.length === 0) {
        console.warn("数据为空");
        return;
      }

      const myChart = echarts.init(chart.value);

      // 计算坐标轴范围
      const xs = points.map(p => p[0]);
      const ys = points.map(p => p[1]);
      const zs = points.map(p => p[2]);

      const getRange = arr => [Math.min(...arr), Math.max(...arr)];
      const [xMin, xMax] = getRange(xs);
      const [yMin, yMax] = getRange(ys);
      const [zMin, zMax] = getRange(zs);

      myChart.setOption({
        tooltip: {},
        xAxis3D: { type: "value", min: xMin, max: xMax, name: "X" },
        yAxis3D: { type: "value", min: yMin, max: yMax, name: "Y" },
        zAxis3D: { type: "value", min: zMin, max: zMax, name: "Z" },
        grid3D: {
          viewControl: {
            autoRotate: true,
            distance: 180,
          },
        },
        series: [
          {
            type: "scatter3D",
            data: points.map(([x, y, z, cluster]) => ({
              value: [x, y, z],
              itemStyle: {
                color: clusterColor(cluster),
                opacity: 0.6, // 增加透明度
              },
            })),
            symbolSize: 5, // 适当调整点的大小
          },
        ],
      });
    }

    function clusterColor(label) {
      const colors = ["#ff0000", "#00ff00", "#0000ff", "#ff00ff"];
      return colors[label % colors.length];
    }


    return { chart };
  },
};
</script>
