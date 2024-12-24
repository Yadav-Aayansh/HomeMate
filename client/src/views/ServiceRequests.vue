<script setup>
  import Servicer from '@/views/Request/Servicer.vue'
  import Customer from '@/views/Request/Customer.vue'
  import Admin from '@/views/Request/Admin.vue'
  import { currentUserStore } from '@/stores/currentUser.js'
  const currentUser_Store = currentUserStore()
  const role = currentUser_Store.role
</script>

<template>
 <Servicer v-if="role === 'Professional'"/>
 <Customer v-if="role === 'Customer'"/>
 <Admin v-if="role === 'Admin'"/>
</template>