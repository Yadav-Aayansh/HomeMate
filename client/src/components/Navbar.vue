<script setup>
    import { ref } from 'vue';
    import {currentUserStore} from '@/stores/currentUser.js'
    import admin from '@/assets/admin.jpg'
    import customer from '@/assets/customer2.png'
    import servicer from '@/assets/servicer.png'


    const collapse = ref(false)
    const emit = defineEmits(['status'])

    const updateCollapse = () => {
        collapse.value = !collapse.value
        emit('status', collapse.value)
    }

    const currentUser_Store = currentUserStore()
    const role = currentUser_Store.role
    
    const profile_pic = ref('')
    if (role === 'Admin') {
        profile_pic.value = admin
    } else if (role === 'Customer') {
        profile_pic.value = customer
    } else if (role === 'Professional') {
        profile_pic.value = servicer
    }

</script>

<template>
    <nav class="navbar navbar-expand-lg navbar-light cus-nav">
        <div class="container-fluid">
            <button class="my-btn me-3" aria-label="Menu" @click="updateCollapse">
                <i class="ri-menu-4-line"></i>
            </button>

            <div class="navbar-brand">
                <h3 class="kg-text2">HomeMate</h3>
            </div>

            <div class="ms-auto d-flex align-items-center">
                <button class="my-btn me-2" aria-label="Notifications">
                    <i class="ri-notification-3-line"></i>
                </button>
                <button class="my-btn" aria-label="Profile">
                    <img :src="profile_pic" class="pic">
                </button>
            </div>
        </div>
    </nav>
</template>


<style scoped>
    .cus-nav {
        border-radius: 10px;
        border-bottom: 2px white solid;
        position: fixed;
        z-index: 100000;
        width: 100vw;
        overflow: hidden;
        padding: 10px 20px;
        background-color: rgba(214, 212, 238, 1);
        box-shadow: rgba(0, 0, 0, 0.12) 0px 1px 3px, rgba(0, 0, 0, 0.24) 0px 1px 2px;    }

    .my-btn {
        border-radius: 50%;
        color: white;
        height: 2.4rem;
        width: 2.4rem;
        background-color: white;
        /* Customize your button color */
        border: none;
        /* Remove border */
        display: flex;
        align-items: center;
        justify-content: center;
        margin-left: 0.5rem;
        /* Space between buttons */
        transition: background-color 0.3s;
        /* Smooth transition on hover */
    }

    .my-btn:hover {
        background-color: white;
        /* Darker shade on hover */
    }

    .picture {
        border-radius: 50%;
        overflow: hidden;
        /* Prevents image overflow */
        height: 2.7rem;
        width: 2.7rem;
    }

    .picture img {
        height: 100%;
        width: 100%;
        object-fit: cover;
        /* Maintain aspect ratio of the image */
    }

    i {
        color: black;
        font-size: 1.5rem;
        line-height: 1.8rem;
    }

    .pic {
        height: 40px;
        border-radius: 50%;
    }
</style>