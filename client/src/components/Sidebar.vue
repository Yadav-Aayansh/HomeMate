<script setup>
    import { onMounted, computed, ref } from 'vue';
    import { RouterLink } from 'vue-router'
    import { Tooltip } from 'bootstrap';
    import logo from '@/assets/logo.png'
    import { currentUserStore } from '@/stores/currentUser.js'
    import router from '@/router/index.js'
    import { useRoute } from 'vue-router'
    import Logout from '@/components/Logout.vue'

    const currentUser_Store = currentUserStore()
    const role = currentUser_Store.role

    const emit = defineEmits(['title', 'logout'])
    const updateTitle = (title) => {
        emit('title', title)
    }

    const logout = () => {
        emit('logout', true);
    }

    const props = defineProps({
        collapse: Boolean
    })

    

    const route = useRoute()
    const isServiceProfessionalActive = computed(() => {
        return route.path === '/dashboard/service-professionals' || route.path.startsWith('/dashboard/service-professionals/')
    })

    onMounted(() => {
        const tooltips = document.querySelectorAll('[data-bs-toggle="tooltip"]');
        tooltips.forEach(tooltip => new Tooltip(tooltip));
    });
</script>

<template>
    <nav class="cus-nav mt-4 ms-3" v-if="!collapse">
        <div class="container-fluid">
            <div class="side-content mt-4">
                <RouterLink to="/dashboard" @click="updateTitle('Dashboard')" class="btn my-btn mb-3 nav-item" data-bs-toggle="tooltip" data-bs-placement="right" title="Home" exact-active-class="active-link">
                    <i class="ri-home-7-line"></i>
                </RouterLink>

                <RouterLink to="/dashboard/profile" v-if="role === 'Professional'" class="btn my-btn mb-3 nav-item" data-bs-toggle="tooltip" data-bs-placement="right" title="Profile" active-class="active-link">
                    <i class="ri-user-smile-line"></i>
                </RouterLink>

                <RouterLink to="/dashboard/services" v-if="role === 'Admin'" class="btn my-btn mb-3 nav-item" data-bs-toggle="tooltip" data-bs-placement="right" title="Services" active-class="active-link">
                    <i class="ri-lightbulb-line"></i>
                </RouterLink>

                <RouterLink to="/dashboard/customers" v-if="role === 'Admin'" class="btn my-btn mb-3 nav-item" data-bs-toggle="tooltip" data-bs-placement="right" title="Customers" active-class="active-link">
                    <i class="ri-group-line"></i>
                </RouterLink>

                <RouterLink to="/dashboard/service-professionals" v-if="role === 'Customer' || role === 'Admin'" class="btn my-btn mb-3 nav-item" data-bs-toggle="tooltip" data-bs-placement="right" title="Service Professionals"
                :class="{ 'active-link': isServiceProfessionalActive }">
                    <i class="ri-briefcase-line"></i>
                </RouterLink>

                <RouterLink to="/dashboard/service-requests" class="btn my-btn mb-3 nav-item" data-bs-toggle="tooltip" data-bs-placement="right" title="Service Requests" active-class="active-link">
                    <i class="ri-service-line"></i>
                </RouterLink>

                <RouterLink to="#" @click.prevent="logout" class="btn my-btn mb-4 nav-item" data-bs-toggle="tooltip" data-bs-placement="right" title="Logout">
                    <i class="ri-logout-circle-line"></i>
                </RouterLink>
                
            </div>
        </div>
    </nav>
</template>

<style scoped>
    .cus-nav {
        /* width: 4em; */
        display: flex;
        justify-content: center;
        align-items: center;
        border: 1px rgb(191, 194, 193) solid;
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
        border-radius: 20px;
        margin: 0 auto;
        position: fixed;
        
        /* background-color: rgba(34, 32, 32, 0.729); */

    }

    .side-content {
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
    }

    .brand {
        display: flex;
        justify-content: center;
        align-items: center;
        font-size: 23px;
        font-family: 'KG';
    }

    .brand p {
        margin-top: 6px;
    }

    .my-btn {
        display: inline-flex;
        padding: 3px 5px;
        border-radius: 10px;
        transition: all ease 0.3s;
        /* font-weight: 500; */
        /* font-size: 5px; */
        border-radius: 50%;
        height: 2.4rem;
        width: 2.4rem;
        /* background-color: rgba(148, 140, 140, 0.296); */
        display: flex;
        justify-content: center;
        align-items: center;
        
    }

    .my-btn:hover {
        color: white;
        background-color: rgb(109, 74, 255, 0.6);
    }

    .active-link {
        color: white;
        background-color: rgb(109, 74, 255, 0.6);
    }

    i {
        font-size: 1.6rem;
        line-height: 1.8rem;
    }

    /* Mobile responsiveness */
@media (max-width: 768px) {
    .cus-nav {
        width: 100%; /* Full width on mobile */
        position: relative; /* Stack above content */
    }
}
    
</style>

<!-- box-shadow: 3px 3px 4px 1px #48484840;
border: 1px rgb(43, 43, 43) solid;
color: rgba(43, 43, 43, 0.9);
background-color: rgb(180, 235, 52, 0.6); -->