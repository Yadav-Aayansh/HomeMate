<script setup>
   import { ref } from 'vue';
   import Summary from '@/components/Charts/Summary_Professional.vue'
   import Request from '@/components/Charts/Request_Admin.vue'

   const apiUrl = import.meta.env.VITE_API_URL

   const stats = ref('')
   const count = ref()
   const percentage = ref()
   const ratio = ref()
   const fetchData = async () => {
      const response = await fetch(`${apiUrl}/stats?page=home`, {
         method: 'GET',
         credentials: 'include'
      })

      const data = await response.json()
      stats.value = data
      count.value = [(data.earning/1000), data.customer, data.review, data.request ]
      percentage.value = [data.earning_progress, data.customer_progress, data.review_progress, data.request_progress]
      ratio.value = [data.completed, data.pending, data.failed]
   }

   fetchData()


</script>

<template>
   <div class="ps-4 pe-4 pb-4">
      <div class="dashboard-summary mb-4">
         <!-- Revenue -->
         <div class="summary-card">
            <div class="summary-icon bg-success">
               <i class="ri-money-rupee-circle-line"></i>
            </div>
            <div class="summary-details">
               <h5>Total Earning</h5>
               <p class="summary-number">₹{{ stats.earning }}</p>
               <p class="summary-change"
                  :class="{'text-success': stats.earning_progress >= 0, 'text-danger': stats.earning_progress < 0}">
                  {{ stats.earning_progress }}% from last month
               </p>
            </div>
         </div>

         <!-- Total Customers -->
         <div class="summary-card">
            <div class="summary-icon bg-info">
               <i class="ri-user-line"></i>
            </div>
            <div class="summary-details">
               <h5>Unique Customers</h5>
               <p class="summary-number">{{ stats.customer }}</p>
               <p class="summary-change"
                  :class="{'text-success': stats.customer_progress >= 0, 'text-danger': stats.customer_progress < 0}">
                  {{ stats.customer_progress }}% from last month
               </p>
            </div>
         </div>

         <!-- Total Professionals -->
         <div class="summary-card">
            <div class="summary-icon bg-primary">
               <i class="ri-star-line"></i>
            </div>
            <div class="summary-details">
               <h5>Total Reviews</h5>
               <p class="summary-number">{{ stats.review }}</p>
               <p class="summary-change"
                  :class="{'text-success': stats.review_progress >= 0, 'text-danger': stats.review_progress < 0}">
                  {{ stats.review_progress }}% from last month
               </p>
            </div>
         </div>

         <!-- Total Requests -->
         <div class="summary-card">
            <div class="summary-icon bg-secondary">
               <i class="ri-file-list-line"></i>
            </div>
            <div class="summary-details">
               <h5>Total Requests</h5>
               <p class="summary-number">{{ stats.request }}</p>
               <p class="summary-change"
                  :class="{'text-success': stats.request_progress >= 0, 'text-danger': stats.request_progress < 0}">
                  {{ stats.request_progress }}% from last month
               </p>
            </div>
         </div>
      </div>

      <h3 class="mb-2">Performance Insights</h3>
      <div class="d-flex graph">
         <div class="chart_card">
            <h4>Platform Distrubution </h4>
            <Summary :count="count" :percentage="percentage"></Summary>
         </div>
         <div class="service_card">
            <h4 class="hola">Service Request Ratio</h4>
               <Request :ratio="ratio"></Request>
          </div>  
      </div>


   </div>
</template>

<style scoped>
   .dashboard-summary {
      display: flex;
      gap: 20px;
      flex-wrap: wrap;
      justify-content: space-between;
   }

   .summary-card {
      width: 23%;
      border-radius: 12px;
      background: #fff;
      box-shadow: 0 6px 18px rgba(0, 0, 0, 0.1);
      transition: all 0.3s ease-in-out;
      padding: 20px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      cursor: pointer;
   }

   .summary-card:hover {
      transform: translateY(-5px);
      box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
   }

   /* Icon Circle Style */
   .summary-icon {
      width: 60px;
      height: 60px;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 30px;
      color: #fff;
      transition: background-color 0.3s ease;
   }

   .graph {
      max-height: 440px;
   }

   .chart_card {
      width: 60vw;
      padding: 20px;
      border-radius: 20px;
      border: 2px solid black;
      background-color: #fff;
      box-shadow: rgba(8, 8, 8, 0.9) 0px 10px;
      margin: 10px;
   }

   .service_card {
      width: 40vw;
      border-radius: 20px;
      border: 2px solid black;
      background-color: #fff;
      box-shadow: rgba(8, 8, 8, 0.9) 0px 10px;
      margin: 10px;
   }

   .hola {
      margin-top: 20px;
      margin-left: 20px;
      margin-bottom: -30px;
   }
</style>