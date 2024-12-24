<script setup>
    import { ref, onMounted, watch } from 'vue';
    import Chart from 'chart.js/auto';

    const props = defineProps({
        count: Array,
        percentage: Array
    });

    const barChart = ref(null);
    let chartInstance = null;

    const updateChart = () => {
        if (chartInstance) {
            chartInstance.destroy();
        }

        chartInstance = new Chart(barChart.value, {
            type: 'bar',
            data: {
                labels: ['Earning (In Thousands)', 'Customers', 'Reviews', 'Requests'],
                datasets: [
                    {
                        label: 'Overall Analysis',
                        data: props.count,
                        backgroundColor: [
                            'rgba(54, 162, 235, 0.5)',
                            'rgba(255, 215, 0, 0.5)',
                            'rgba(255, 99, 132, 0.5)',
                            'rgba(75, 192, 192, 0.5)'
                        ],
                        borderColor: [
                            'rgba(54, 162, 235, 1)',
                            'rgba(255, 215, 0, 1)',
                            'rgba(255, 99, 132, 1)',
                            'rgba(75, 192, 192, 1)'
                        ],
                        borderWidth: 1,
                        yAxisID: 'y1'
                    },
                    {
                        label: 'Growth Percentage',
                        data: props.percentage,
                        type: 'line',
                        borderColor: 'rgba(109, 74, 255, 0.5)',
                        tension: 0.1,
                        fill: false,
                        yAxisID: 'y2'
                    }
                ]
            },
            options: {
                responsive: true,
                animations: {
                    tension: {
                        duration: 1000,
                        easing: 'linear',
                        from: 1,
                        to: 0,
                        loop: true
                    }
                },
                barPercentage: 0.8,
                categoryPercentage: 0.8,
                scales: {
                y1: {  // Left Y-axis
                    ticks: {
                        beginAtZero: true,
                        callback: function(value) { return value ; }, 
                    },
                    position: 'left',
                },
                y2: {  // Right Y-axis
                    ticks: {
                        beginAtZero: true,
                        callback: function(value) { return value + '%'; },
                    },
                    position: 'right',
                    grid: {
                        drawOnChartArea: false, 
                    },
                }
            },
            }
        });
    };

    onMounted(updateChart);

    watch(() => props.count, updateChart);
</script>

<template>
    <div class="container">
        <canvas ref="barChart"></canvas>
    </div>
</template>

<style scoped>
    .container {
        height: 100%;
        display: flex;
        justify-content: center;
    }
</style>