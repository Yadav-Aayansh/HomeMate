<script setup>
  import Admin from '@/views/Professional/Admin.vue'
  import Customer from '@/views/Professional/Customer.vue'
  import { currentUserStore } from '@/stores/currentUser.js'
  const currentUser_Store = currentUserStore()
  const role = currentUser_Store.role
</script>

<template>
 <Customer v-if="role === 'Customer'"/>
 <Admin v-if="role === 'Admin'"/>
</template>