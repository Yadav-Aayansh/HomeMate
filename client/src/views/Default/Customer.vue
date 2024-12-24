<script setup>
    import { ref } from 'vue'
    import { bookingStore } from '@/stores/booking.js'
    import router from '@/router'
    import popular_project1 from '@/assets/popular_project1.jpg'
    import popular_project2 from '@/assets/popular_project2.jpg'
    import popular_project3 from '@/assets/popular_project3.jpg'
    import popular_project4 from '@/assets/popular_project4.jpg'

    const apiUrl = import.meta.env.VITE_API_URL

    const selectedCate = ref('Assembly')
    const services = ref([])
    const fetchServices = async (category) => {
        selectedCate.value = category
        const response = await fetch(`${apiUrl}/services?category=${category}`, {
            method: 'GET',
            credentials: 'include'
        })
        const data = await response.json()
        services.value = data['Services']
    }

    fetchServices('Assembly')

    const booking_store = bookingStore()
    const showServicers = (service) => {
        booking_store.updateCategory(selectedCate.value)
        booking_store.updateServiceType(service)
        router.push('/dashboard/service-professionals')
    }


</script>

<template>
    <!-- Main Content -->
    <div class="container text-center my-5">
        <div class="row">
            <div class="col">
                <div class="d-flex justify-content-center ">
                    <h1 class="heading kg-text mt-5">Book trusted help for home tasks</h1>
                </div>
                <div class="container pt-5">
                    <!-- Categories -->
                    <div class="d-flex justify-content-around align-items-center border-bottom pb-3 mb-4">
                        <div class="category" @click="fetchServices('Assembly')">
                            <i class="ri-hammer-line"></i>
                            <svg width="60" height="60" v-if="selectedCate==='Assembly'">
                                <path d="M 5 35 C 0 10 35 -15 55 15 C 70 25 55 50 45 50 C 35 50 23 51 9 44 Z"
                                    fill="rgba(110, 74, 255, 0.1)"></path>
                            </svg>
                            <p :class="{ highlight: selectedCate === 'Assembly' }">Assembly</p>
                        </div>
                        
                        <div class="category" @click="fetchServices('Mounting')">
                            <i class="ri-tools-line"></i>
                            <svg width="60" height="60" v-if="selectedCate==='Mounting'">
                                <path d="M 5 35 C 0 10 35 -15 55 15 C 70 25 55 50 45 50 C 35 50 23 51 9 44 Z"
                                    fill="rgba(110, 74, 255, 0.1)"></path>
                            </svg>
                            <p :class="{ highlight: selectedCate === 'Mounting' }">Mounting</p>
                        </div>
                        
                        <div class="category" @click="fetchServices('Moving')">
                            <i class="ri-truck-line"></i>
                            <svg width="60" height="60" v-if="selectedCate==='Moving'">
                                <path d="M 5 35 C 0 10 35 -15 55 15 C 70 25 55 50 45 50 C 35 50 23 51 9 44 Z"
                                    fill="rgba(110, 74, 255, 0.1)"></path>
                            </svg>
                            <p :class="{ highlight: selectedCate === 'Moving' }">Moving</p>
                        </div>
                        
                        <div class="category" @click="fetchServices('Cleaning')">
                            <i class="ri-brush-line"></i>
                            <svg width="60" height="60" v-if="selectedCate==='Cleaning'">
                                <path d="M 5 35 C 0 10 35 -15 55 15 C 70 25 55 50 45 50 C 35 50 23 51 9 44 Z"
                                    fill="rgba(110, 74, 255, 0.1)"></path>
                            </svg>
                            <p :class="{ highlight: selectedCate === 'Cleaning' }">Cleaning</p>
                        </div>
                        
                        <div class="category" @click="fetchServices('Outdoor Help')">
                            <i class="ri-tree-line"></i>
                            <svg width="60" height="60" v-if="selectedCate==='Outdoor Help'">
                                <path d="M 5 35 C 0 10 35 -15 55 15 C 70 25 55 50 45 50 C 35 50 23 51 9 44 Z"
                                    fill="rgba(110, 74, 255, 0.1)"></path>
                            </svg>
                            <p :class="{ highlight: selectedCate === 'Outdoor Help' }">Outdoor Help</p>
                        </div>
                        
                        <div class="category" @click="fetchServices('Home Repairs')">
                            <i class="ri-hammer-line"></i>
                            <svg width="60" height="60" v-if="selectedCate==='Home Repairs'">
                                <path d="M 5 35 C 0 10 35 -15 55 15 C 70 25 55 50 45 50 C 35 50 23 51 9 44 Z"
                                    fill="rgba(110, 74, 255, 0.1)"></path>
                            </svg>
                            <p :class="{ highlight: selectedCate === 'Home Repairs' }">Home Repairs</p>
                        </div>
                        
                        <div class="category" @click="fetchServices('Painting')">
                            <i class="ri-brush-line"></i>
                            <svg width="60" height="60" v-if="selectedCate==='Painting'">
                                <path d="M 5 35 C 0 10 35 -15 55 15 C 70 25 55 50 45 50 C 35 50 23 51 9 44 Z"
                                    fill="rgba(110, 74, 255, 0.1)"></path>
                            </svg>
                            <p :class="{ highlight: selectedCate === 'Painting' }">Painting</p>
                        </div>
                        
                        <div class="category" @click="fetchServices('Trending')">
                            <i class="ri-fire-line"></i>
                            <svg width="60" height="60" v-if="selectedCate==='Trending'">
                                <path d="M 5 35 C 0 10 35 -15 55 15 C 70 25 55 50 45 50 C 35 50 23 51 9 44 Z"
                                    fill="rgba(110, 74, 255, 0.1)"></path>
                            </svg>
                            <p :class="{ highlight: selectedCate === 'Trending' }">Trending</p>
                        </div>
                        
                    </div>

                    <!-- Sub-categories -->
                    <div class="sub-categories">
                        <button v-for="service in services" @click=showServicers(service)>{{service}} </button>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <div class="container mb-4">
        <h2 class="text-center mb-4">Popular Projects</h2>
        <div class="row row-cols-1 row-cols-md-3 row-cols-lg-4 g-4">
            <!-- Card 1 -->
            <div class="col">
                <div class="card h-100 shadow-sm">
                    <img :src="popular_project1" alt="Furniture Assembly" height="200px">
                    <div class="card-body text-center">
                        <h6 class="card-title fw-bold">Chair Assembly</h6>
                        <p class="card-text text-muted">Projects starting at ₹300</p>
                    </div>
                </div>
            </div>
            <!-- Card 2 -->
            <div class="col">
                <div class="card h-100 shadow-sm">
                    <img :src="popular_project2" alt="Mount Art or Shelves" height="200px">
                    <div class="card-body text-center">
                        <h6 class="card-title fw-bold">Picture Frame Mounting</h6>
                        <p class="card-text text-muted">Projects starting at ₹200</p>
                    </div>
                </div>
            </div>
            <!-- Card 3 -->
            <div class="col">
                <div class="card h-100 shadow-sm">
                    <img :src="popular_project3" alt="Mount a TV" height="200px">
                    <div class="card-body text-center">
                        <h6 class="card-title fw-bold">House Moving</h6>
                        <p class="card-text text-muted">Projects starting at ₹999</p>
                    </div>
                </div>
            </div>
            <!-- Card 4 -->
            <div class="col">
                <div class="card h-100 shadow-sm">
                    <img :src="popular_project4" alt="Help Moving" height="200px">
                    <div class="card-body text-center">
                        <h6 class="card-title fw-bold">Bathroom Cleaning</h6>
                        <p class="card-text text-muted">Projects starting at ₹500</p>
                    </div>
                </div>
            </div>
        </div>
    </div>

</template>

<style scoped>

    .category {
        cursor: pointer;
        position: relative;
        display: inline-block;
        text-align: center;
    }

    .category i {
        position: absolute;
        top: 0;
        left: 10px;
        font-size: 36px;
        z-index: 10;
    }

    .category svg {
        position: absolute;
        top: 0;
        left: 0;
        z-index: 5;
    }

    .category p {
        margin-top: 60px;
        font-size: 16px;
        color: #333;
    }

    .highlight {
        color: rgb(110, 74, 255) !important;
    }

    .sub-categories {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        justify-content: start;
    }

    .sub-categories button {
        display: inline-flex;
        padding: 7px 15px;
        border-radius: 10px;
        transition: all ease 0.3s;
        font-weight: 600;
        font-size: 18px;
        box-shadow: 3px 3px 4px 1px #48484840;
        border: 1px rgb(43, 43, 43) solid;
        color: rgb(0, 0, 0);
        margin: 10px;
    }
    .sub-categories button:hover {
        background-color: rgba(182, 170, 230, 0.501);
    }


    .heading {
        font-size: 50px;
        color: slateblue;
        margin-bottom: 20px;
    }
</style>