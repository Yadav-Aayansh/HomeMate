<script setup>
    import router from '@/router'
    import Popup from '@/components/Popup.vue'
    import { ref } from 'vue'

    const apiUrl = import.meta.env.VITE_API_URL

    const logout = async () => {
        const response = await fetch(`${apiUrl}/logout`, {
            method: 'GET',
            credentials: 'include'
        })
        if (response.status === 200) {
            router.push('/login')
        } else {
            alert('Something went wrong')
        }
    }

    const isModalOpen = ref(true)
    const openModal = () => {
        isModalOpen.value = true;
    }

</script>

<template>
    <Popup :isOpen="isModalOpen" title="Logout Confirmation" @close="isModalOpen=false" :showConfirm="true" confirmButton="red" buttonName="Logout" :myfunction="logout">
        <p>Are you sure you want to log out? This action will end your current session and you will need to log in again. Please confirm to proceed.</p>
    </Popup>
</template>