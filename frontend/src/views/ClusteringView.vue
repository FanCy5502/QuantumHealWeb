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

export default {
  setup() {
    const route = useRoute();
    const chart = ref(null);

    onMounted(() => {
      fetch(`/result/view_clustering/${route.params.patient_id}`)
        .then((res) => res.json())
        .then((data) => {
          if (data.success) {
            renderChart(data.data);
          }
        });
    });

    function renderChart(points) {
      const myChart = echarts.init(chart.value);
      myChart.setOption({
        tooltip: {},
        xAxis3D: { type: "value" },
        yAxis3D: { type: "value" },
        zAxis3D: { type: "value" },
        grid3D: {},
        series: [
          {
            type: "scatter3D",
            data: points.map(([x, y, z, , cluster]) => ({
              value: [x, y, z],
              itemStyle: { color: clusterColor(cluster) },
            })),
            symbolSize: 4,
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