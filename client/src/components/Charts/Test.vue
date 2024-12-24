<template>
    <div>
      <canvas ref="barChart"></canvas>
    </div>
  </template>
  
  <script setup>
  import { onMounted, ref } from 'vue';
  import Chart from 'chart.js/auto';
  
  export default {
    setup() {
      const barChart = ref(null);
  
      onMounted(() => {
        // Create the Bar chart after the component is mounted
        new Chart(barChart.value, {
          type: 'bar', // Chart type
          data: {
            labels: ['January', 'February', 'March', 'April'], // X-axis labels
            datasets: [
              {
                label: 'Sales', // Dataset label
                data: [10, 20, 30, 40], // Data points
                backgroundColor: 'rgba(75, 192, 192, 0.2)', // Bar color
                borderColor: 'rgba(75, 192, 192, 1)', // Border color
                borderWidth: 1, // Border width
              },
            ],
          },
          options: {
            responsive: true,
            scales: {
              y: {
                beginAtZero: true, // Start Y-axis from zero
              },
            },
          },
        });
      });
  
      return { barChart };
    },
  };
  </script>
  
  <style scoped>
  /* Optional: adjust canvas size */
  
  </style>
  