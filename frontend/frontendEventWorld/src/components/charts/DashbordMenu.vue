<template>
    <div class="gauge-container">
      <div class="gauge">
        <Doughnut :data="getChartData(upcoming, total)" :options="chartOptions" />
        <p class="gauge-label">À venir</p>
      </div>
      <div class="gauge">
        <Doughnut :data="getChartData(past, total)" :options="chartOptions" />
        <p class="gauge-label">Passés</p>
      </div>
      <div class="gauge">
        <Doughnut :data="getChartData(sold, sold + available)" :options="chartOptions" />
        <p class="gauge-label">Taux de remplissage</p>
      </div>
      <div class="gauge">
        <Doughnut :data="getChartData(available, sold + available)" :options="chartOptions" />
        <p class="gauge-label">Places restantes des événements</p>
      </div>
    </div>
  </template>
  
  <script setup>
  import { Doughnut } from 'vue-chartjs'
  import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js'
  
  ChartJS.register(ArcElement, Tooltip, Legend)
  
  const props = defineProps({
    total: Number,
    upcoming: Number,
    past: Number,
    sold: Number,
    available: Number
  })
  
  const getChartData = (value, max) => {
    const percent = Math.min((value / (max || 1)) * 100, 100)
    return {
      labels: ['Réalisé', 'Reste'],
      datasets: [{
        data: [percent, 100 - percent],
        backgroundColor: ['#4e79a7', '#e0e0e0'],
        borderWidth: 0
      }]
    }
  }
  
  const chartOptions = {
    circumference: 180,
    rotation: -90,
    cutout: '70%',
    plugins: {
      tooltip: { enabled: false },
      legend: { display: false }
    }
  }
  </script>
  
  <style scoped>
  .gauge-container {
    display: flex;
    justify-content: center;
    gap: 40px;
    margin-top: 20px;
    flex-wrap: wrap;
  }
  .gauge {
    width: 190px;
    text-align: center;
  }
  .gauge-label {
    margin-top: 10px;
    font-weight: bold;
  }
  </style>
  