<!-- src/components/charts/MiniGauge.vue -->
<template>
    <div class="mini-gauge">
      <Doughnut :data="chartData" :options="chartOptions" />
      <div class="label">{{ Math.round(fillRate) }}%</div>
    </div>
  </template>
  
  <script setup>
  import { computed } from 'vue'
  import { Doughnut } from 'vue-chartjs'
  import {
    Chart as ChartJS,
    ArcElement,
    Tooltip,
  } from 'chart.js'
  
  ChartJS.register(ArcElement, Tooltip)
  
  const props = defineProps({
    sold: Number,
    total: Number,
  })
  
  const fillRate = computed(() => {
    if (!props.total || props.total === 0) return 0
    return (props.sold / props.total) * 100
  })
  
  const chartData = computed(() => ({
    labels: ['Vendu', 'Restant'],
    datasets: [
      {
        data: [fillRate.value, 100 - fillRate.value],
        backgroundColor: [
          fillRate.value < 50 ? '#4caf50' : fillRate.value < 80 ? '#ffa726' : '#ef5350',
          '#eeeeee',
        ],
        borderWidth: 0,
      },
    ],
  }))
  
  const chartOptions = {
    cutout: '75%',
    plugins: { tooltip: { enabled: false }, legend: { display: false } },
    responsive: true,
    maintainAspectRatio: false,
  }
  </script>
  
  <style scoped>
  .mini-gauge {
    width: 60px;
    height: 60px;
    position: relative;
  }
  .label {
    position: absolute;
    top: 50%;
    left: 50%;
    font-size: 0.7rem;
    transform: translate(-50%, -50%);
    font-weight: bold;
  }
  </style>
  