<template>
  <div class="gauge-container">
    <div class="gauge">
      <Doughnut :data="getChartData(upcoming, total, '#8b5cf6', '#e0e0e0')" :options="chartOptions" />
      <p class="gauge-label">À venir</p>
      <p class="gauge-value">{{ upcoming }}</p>
    </div>
    <div class="gauge">
      <Doughnut :data="getChartData(past, total, '#3b82f6', '#e0e0e0')" :options="chartOptions" />
      <p class="gauge-label">Passés</p>
      <p class="gauge-value">{{ past }}</p>
    </div>
    <div class="gauge">
      <Doughnut :data="getChartData(sold, sold + available, '#10b981', '#e0e0e0')" :options="chartOptions" />
      <p class="gauge-label">Taux de remplissage</p>
      <p class="gauge-value">{{ Math.round((sold / (sold + available || 1)) * 100) }}%</p>
    </div>
    <div class="gauge">
      <Doughnut :data="getChartData(available, sold + available, '#f59e0b', '#e0e0e0')" :options="chartOptions" />
      <p class="gauge-label">Places restantes</p>
      <p class="gauge-value">{{ available }}</p>
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

const getChartData = (value, max, color, bgColor) => {
  const percent = Math.min((value / (max || 1)) * 100, 100)
  return {
    labels: ['Réalisé', 'Reste'],
    datasets: [{
      data: [percent, 100 - percent],
      backgroundColor: [color, bgColor],
      borderWidth: 2,
      borderColor: '#ffffff',
      hoverBorderWidth: 4,
    }]
  }
}

const chartOptions = {
  circumference: 180,
  rotation: -90,
  cutout: '75%',
  plugins: {
    tooltip: {
      enabled: true,
      callbacks: {
        label: (context) => {
          const label = context.label || ''
          const value = context.raw || 0
          return `${label} : ${value.toFixed(1)}%`
        }
      }
    },
    legend: { display: false }
  },
  responsive: true,
  maintainAspectRatio: false,
}
</script>

<style scoped>
.gauge-container {
  display: flex;
  justify-content: center;
  gap: 30px;
  margin-top: 20px;
  flex-wrap: wrap;
}

.gauge {
  width: 120px;
  height: 120px;
  text-align: center;
  background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
  border-radius: 50%;
  padding: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
}

.gauge:hover {
  transform: scale(1.05);
}

.gauge-label {
  margin-top: 8px;
  font-weight: 600;
  font-size: 14px;
  color: #374151;
}

.gauge-value {
  margin-top: 4px;
  font-size: 16px;
  font-weight: bold;
  color: #1f2937;
}
</style>