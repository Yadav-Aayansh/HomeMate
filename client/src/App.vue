<script setup>
  import { RouterView } from 'vue-router';
  import { ref, onMounted } from 'vue';
  import Loader from '@/components/Loader.vue';

  const loading = ref(true)
  onMounted(() => {
    window.onload = () => {
      loading.value = false
    }
  }
  )



</script>

<template>
  <div v-if="loading">
    <Loader />
  </div>
  <div v-else>
    <RouterView />
  </div>

</template>