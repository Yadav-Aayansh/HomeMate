<script setup>
  import { ref, computed, provide } from 'vue'
  import Logout from '@/components/Logout.vue'
  import Sidebar from '@/components/Sidebar.vue'
  import Navbar from '@/components/Navbar.vue'
  import router from '@/router';

  const goBack = () => router.go(-1)

  // Important 
  const receivedCollapse = ref(false)
  const content = ref()

  const title = ref('Dashboard')
  const updateTitle = (my_title) => {
    title.value = my_title
  }

  // New Learning => provide, inject
  provide('updateTitle', updateTitle)

  const headerWidth = computed(() => (receivedCollapse.value ? '94.1vw' : '89vw'))

  const handleCollapse = (status) => {
    const windowWidth = window.innerWidth;
    if (windowWidth > 768) {
      if (status) {
        content.value.style.paddingLeft = '30px';

      } else {
        content.value.style.paddingLeft = '110px';
      }
    }
    receivedCollapse.value = status
  }

    const isModalOpen = ref(false);
    const logout = () => {
      isModalOpen.value = true;
    };
    
</script>

<template>
  <Navbar @status="handleCollapse" />

  <div class="layout">
    <nav id="sidebar" :class="{ 'collapsed': receivedCollapse }">
      <Sidebar :collapse="receivedCollapse" @title="updateTitle" @logout="logout"/>
    </nav>

    <div class="content" ref="content">
      <div class="full-width-header" :style="{width: headerWidth}">
        <h3 class="ms-4">
          <i class="ri-corner-up-left-double-fill back-button" @click="goBack"></i>
          {{ title }}
        </h3>
      </div>
      <div class="actual_routes">
        <router-view />
        <Logout v-if="isModalOpen" @close="isModalOpen = false" />
      </div>
    </div>
  </div>
</template>

<style scoped>
  .actual_routes {
    margin-top: 80px;
  }
  .layout {
    display: flex;
    padding-top: 70px;
  }

  #sidebar {
    width: auto;
    transition: all 0.3s ease;
    display: flex;
    align-items: center;
    position: fixed;
    top: 50%
  }

  .content {
    padding-left: 110px;
    padding-right: 50px;
    margin-top: -5px;
    flex: 1;
    overflow: hidden;
  }

  .full-width-header {
    border-bottom: 1px solid rgb(191, 194, 193); 
    position: fixed;
    z-index: 1000;
    padding: 20px 10px 10px 10px;
    background-color:rgb(239, 240, 241);
  }

  /* Mobile responsiveness */
  @media (max-width: 768px) {
    .layout {
      flex-direction: column;
    }

    #sidebar {
      align-self: flex-start;
      position: fixed;
      z-index: 1;
      top: 35%;
    }

    .content {
      width: 100%;
      padding: 10px;
    }

    .full-width-header {
    border-bottom: 1px solid rgb(191, 194, 193);
    width: 96vw;
    z-index: 1000;
    padding: 10px;
    background-color: rgb(239, 240, 241);
  }
  }
</style>


<!-- opacity: 0-1 -->