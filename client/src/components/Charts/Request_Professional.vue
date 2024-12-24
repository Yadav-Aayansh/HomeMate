<script setup>
    import { ref, onMounted, watch } from 'vue';
    import Chart from 'chart.js/auto';

    const props = defineProps({
        ratio: Array
    });

    const doughnutChart = ref(null);
    let chartInstance = null;

    const updateChart = () => {
        if (chartInstance) {
            chartInstance.destroy();
        }

        chartInstance = new Chart(doughnutChart.value, {
            type: 'doughnut',
            data: {
                labels: ['Completed', 'Pending', 'Failed'],
                datasets: [
                    {
                        data: props.ratio,
                        backgroundColor: [
                            'rgba(54, 162, 235, 0.5)',
                            'rgba(255, 215, 0, 0.5)',
                            'rgba(255, 99, 132, 0.5)'
                        ],
                        borderColor: [
                            'rgba(54, 162, 235, 1)',
                            'rgba(255, 215, 0, 1)',
                            'rgba(255, 99, 132, 1)'
                        ],
                    },
                ]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'right',
                    },
                },
            }
        });
    };

    onMounted(updateChart);

    watch(() => props.ratio, updateChart);
</script>

<template>
    <div class="container">
        <canvas ref="doughnutChart"></canvas>
    </div>
</template>

<style scoped>
    .container {
        height: 100%;
        display: flex;
        justify-content: center;
    }
</style>