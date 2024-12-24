<script setup>
    import { ref, watch, inject } from 'vue';
    import { currentUserStore } from '@/stores/currentUser.js'
    import { bookingStore } from '@/stores/booking.js'
    import router from '@/router'
    import NotFound from '@/assets/not_found.png'
    import Popup from '@/components/Popup.vue'
  
    const updateTitle = inject('updateTitle')
    updateTitle('Service Professionals')
  
    const staticUrl = import.meta.env.VITE_STATIC_URL;
    const apiUrl = import.meta.env.VITE_API_URL;
  
    const currentUser_Store = currentUserStore()
  
    const service_professionls = ref([])
    const offset = ref(0);
    const pincode = ref(currentUser_Store.pincode);
    const service_type = ref('');
    const experience = ref('');
    const fee_min = ref(100);
    const fee_max = ref(10000);
    const sort_by = ref('');
    const availability = ref('');
    const city = ref(null)
  
    const updateProfessionals = async () => {
      const query = `pincode=${pincode.value}&service_type=${service_type.value}&experience=${experience.value}&fee_min=${fee_min.value}&fee_max=${fee_max.value}&sort_by=${sort_by.value}&availability=${availability.value}`
      const response = await fetch(`${apiUrl}/servicer?${query}`, {
        method: 'GET',
        credentials: 'include'
      })
      const data = await response.json()
      if (response.ok) {
        service_professionls.value = data.professionals
      }
  
      const pinToCity = await fetch(`${apiUrl}/pincode-to-city?q=${pincode.value}`)
      const list_city = await pinToCity.json()
      if (pinToCity.ok) {
        city.value = list_city.result[0].city
      }
    }
  
    const search = ref('')
    const searchResults = ref([])
    const searchResult = async () => {
      const response = await fetch(`${apiUrl}/autocomplete?q=${search.value}`)
      const data = await response.json()
      if (response.ok) {
        searchResults.value = data.result
      }
    }
  
    const selectAddress = (item) => {
      search.value = item.address
      pincode.value = item.pincode
      searchResults.value.length = 0
    }
  
    watch(search, (newValue) => {
      if (newValue === '') {
        pincode.value = ''
        searchResults.value.length = 0
      }
    })
  
    const category = ref(null)
    const categories = ref([])
    const fetchCategories = async () => {
      try {
        const response = await fetch(`${apiUrl}/services`, {
          method: 'GET',
          credentials: 'include'
        })
        if (response.ok) {
          const data = await response.json()
          categories.value = data['Service Categories']
        }
      }
      catch {
        return null;
      }
    }
  
  
    fetchCategories()
  
    const service = ref(null)
    const services = ref([])
    const fetchServices = async (cat) => {
      category.value = cat
      try {
        const response = await fetch(`${apiUrl}/services?category=${cat}`,{
          method: 'GET',
          credentials: 'include'
        })
        if (response.ok) {
          const data = await response.json()
          services.value = data['Services']        }
        
      }
      catch {
        return null;
      }
    }
  
  
    const booking_store = bookingStore()
    category.value = booking_store.category
    service_type.value = booking_store.service_type
    fetchServices(category.value)
    updateProfessionals()
  
  
    const bookService = (service_professional_id) => {
      booking_store.updateServicerId(service_professional_id)
      router.push(`/dashboard/service-professionals/${service_professional_id}`)
  
    }
  
  
  
  
  
  </script>
  
  <template>
    <div class="container-fluid">
      <div class="row mb-5">
        <aside class="col-lg-4 d-none d-lg-block position-sticky top-0">
          <div class="cus_filter_box">
            <h3 class="my-3 mt-0 font-weight-bold text-homemate">
              <i class="ri-filter-3-line"></i> Filters
            </h3>
  
            <div class="card-one rounded-4">
              <div class="card-body p-4">
                <form @submit.prevent="updateProfessionals()" method="post">
                  <div class="form-group mb-3">
                    <label for="category" class="fw-semibold">Category</label>
                    <select class="form-select rounded-pill" name="category" v-model="category" required
                      @change="fetchServices($event.target.value)">
                      <option v-if="!category" value="">Select a category</option>
                      <option v-for="cat in categories" :key="cat" :value="cat">
                        {{ cat }}
                      </option>
                    </select>
                  </div>
  
                  <div class="form-group mb-3">
                    <label for="service_type" class="fw-semibold">Service Type</label>
                    <select class="form-select rounded-pill" v-model="service_type" name="service" required
                      @change="service_type=$event.target.value">
                      <option v-if="!category" value="">Select a category first </option>
                      <option v-else-if="category && !service" value="">Select a service type</option>
                      <option v-for="ser in services" :key="ser" :value="ser">
                        {{ ser }}
                      </option>
                    </select>
                  </div>
  
                  <div class="form-group mb-3">
                    <label for="search" class="fw-semibold">Address</label>
                    <input type="search" class="form-control rounded-pill" v-model="search" @input="searchResult"
                      placeholder="Search here..." />
                    <div v-if="searchResults.length > 0" class="search-results">
                      <div v-for="item in searchResults" :key="item.id" @click="selectAddress(item)">
                        {{ `${item.address}, ${item.pincode}` }}
                      </div>
                    </div>
                  </div>
  
                  <div class="form-group mb-3">
                    <label for="experience" class="fw-semibold">Experience</label>
                    <select class="form-select rounded-pill" v-model="experience">
                      <option value="">Select experience</option>
                      <option value="1">1+ years</option>
                      <option value="3">3+ years</option>
                      <option value="5">5+ years</option>
                      <option value="10">10+ years</option>
                    </select>
                  </div>
  
                  <div class="form-group mb-3">
                    <label for="availability" class="fw-semibold">Availability</label>
                    <select class="form-select rounded-pill" v-model="availability">
                      <option value="">Select availability</option>
                      <option value="Full Time">Full Time</option>
                      <option value="Part Time">Part Time</option>
                    </select>
                  </div>
  
                  <div class="form-group mb-3">
                    <label for="tasks" class="fw-semibold">Fee Range</label>
                    <div class="range-slider mt-4">
                      <div class="slider-track"></div>
                      <input type="range" min="100" max="10000" step="1" v-model="fee_min" class="thumb thumb-left">
                      <input type="range" min="100" max="10000" step="1" v-model="fee_max" class="thumb thumb-right">
                    </div>
                    <div class="price-values mt-2">
                      <span>Min: ₹<span>{{fee_min}}</span></span>
                      <span>Max: ₹<span>{{fee_max}}</span></span>
                    </div>
                  </div>
  
  
                  <div class="form-group mb-4">
                    <label for="sort" class="fw-semibold">Sort By</label>
                    <select class="form-select rounded-pill" v-model="sort_by">
                      <option value="">Relevance</option>
                      <option value="rating">Rating</option>
                      <option value="experience">Experience</option>
                      <option value="feeHigh">Fee (Low to High)</option>
                      <option value="fee">Fee (High to Low)</option>
                      <!-- <option value="tasks_done">Tasks Done</option> -->
                    </select>
                  </div>
  
                  <button class="btn change-pic btn-block rounded-pill shadow-sm">
                    <i class="ri-search-line mr-1"></i> Apply Filters
                  </button>
                </form>
              </div>
            </div>
          </div>
        </aside>
  
        <!-- Main content: Service Professionals List -->
        <main class="col-lg-8">
          <h3 class="text-center mb-3" v-if="city">Service Professionals in {{city}}</h3>
          <h3 class="text-center mb-3" v-if="!city">Service Professionals</h3>


          <div class="card mb-4 d-flex justify-content-center align-items-center" v-if="service_professionls.length < 1">
            <img :src="NotFound" height="400px">
            <div class="text-center mb-5">
              <h3 class="my_color" >Oops! No Professional Found...</h3>
              <p>Sorry, we couldn’t find any professionals. Please adjust your filters or try again later!</p>
            </div>
          </div>
          
          <div class="card-one mb-4" v-for="professional in service_professionls">
            <!-- Left Side: Photo and Button -->
            <div class="d-flex flex-row align-items-start position-relative">
              <div class="d-flex flex-column align-items-center p-3">
                <img :src="`${staticUrl}/profile/photos/${professional.profile_picture}`" alt="User Photo"
                  class="mb-2 profile-picture">
                <button class="book_now_btn" @click="bookService(professional.service_professional_id)" type="button">Book
                  Now<i class="ri-arrow-right-up-line"></i></button>
              </div>
  
              <!-- Right Side: Details and Price -->
              <div class="p-3 flex-grow-1 position-relative">
  
                <div class="p-4 rounded-xl cus-card2 bg-gradient">
                  <div class="d-flex justify-content-between align-items-center mb-3">
                    <h3 class="kg-text2">{{professional.name}}</h3>
                    <div class="price-tag text-right fs-5 fw-semibold">₹{{professional.fee}}/Hr</div>
                  </div>
  
                  <div class="text-muted mb-2">
                    <i class="ri-star-line me-2"></i>
                    <span class="fw-semibold mt">Rating:</span> <strong>{{professional.rating}}/5</strong>
                  </div>
  
                  <div class="text-muted mb-2">
                    <i class="ri-trophy-line me-2"></i>
                    <span class="fw-semibold">Experience:</span> <strong>{{professional.experience}} years</strong>
                  </div>
  
                  <div class="text-muted mb-2">
                    <i class="ri-time-line me-2"></i>
                    <span class="fw-semibold">Availability:</span> <strong>{{professional.availability}}</strong>
                  </div>
                </div>
              </div>
            </div>
  
            <div class="bg-light p-3 rounded">
              <h4 class="description-heading mb-2">How I Can Help:</h4>
              <p class="description-text mb-0">
                {{professional.description}}
              </p>
            </div>
  
          </div>
        </main>
      </div>
  
      <!-- Mobile Filter Button -->
      <div class="d-lg-none text-center mt-4">
        <button type="button" class="btn btn-primary rounded-pill" data-bs-toggle="modal" data-bs-target="#filterModal">
          <i class="ri-filter-3-line"></i> Filter
        </button>
      </div>
  
      <!-- Mobile Filter Modal -->
      <div class="modal fade" id="filterModal" tabindex="-1" aria-labelledby="filterModalLabel" aria-hidden="true">
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title" id="filterModalLabel">Filters</h5>
              <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
              <div>
                <div class="form-group mb-3">
                  <label for="area" class="fw-semibold">Area</label>
                  <input type="text" class="form-control rounded-pill" id="area" placeholder="Enter area" />
                </div>
  
                <div class="form-group mb-3">
                  <label for="experience" class="fw-semibold">Experience</label>
                  <select class="form-control rounded-pill" id="experience">
                    <option value="">Select experience</option>
                    <option value="1">1+ years</option>
                    <option value="3">3+ years</option>
                    <option value="5">5+ years</option>
                    <option value="10">10+ years</option>
                  </select>
                </div>
  
                <div class="form-group mb-3">
                  <label for="availability" class="fw-semibold">Availability</label>
                  <select class="form-control rounded-pill" id="availability">
                    <option value="">Select availability</option>
                    <option value="full">Full Time</option>
                    <option value="part">Part Time</option>
                  </select>
                </div>
  
                <div class="form-group mb-3">
                  <label for="tasks" class="fw-semibold">Tasks Done</label>
                  <input type="number" class="form-control rounded-pill" id="tasks"
                    placeholder="Minimum tasks completed" />
                </div>
  
                <div class="form-group mb-3">
                  <label for="fee" class="fw-semibold">Fee (Max)</label>
                  <input type="number" class="form-control rounded-pill" id="fee" placeholder="Enter maximum fee" />
                </div>
  
                <div class="form-group mb-4">
                  <label for="sort" class="fw-semibold">Sort By</label>
                  <select class="form-control rounded-pill" id="sort">
                    <option value="relevance">Relevance</option>
                    <option value="experience">Experience</option>
                    <option value="fee_low_high">Fee (Low to High)</option>
                    <option value="fee_high_low">Fee (High to Low)</option>
                    <option value="tasks_done">Tasks Done</option>
                  </select>
                </div>
  
                <button @click="updateProfessionals" class="btn change-pic btn-block rounded-pill shadow-sm">
                  <i class="ri-search-line mr-1"></i> Apply Filters
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <style scoped>
    .card-one {
      padding: 3px;
      border-radius: 15px;
      background-color: white;
      border: 1px solid rgb(149, 150, 151);
      position: relative;
    }
  
    .change-pic {
      color: rgb(68, 68, 68);
      font-weight: 700;
      border-color: rgba(42, 42, 42, 0.76);
    }
  
    .change-pic:hover {
      color: white;
      border-color: transparent;
      background-color: rgba(110, 74, 255, 0.659);
    }
  
    .profile-picture {
      height: 11rem;
      border-radius: 50%;
      border: 2px solid rgb(255, 222, 222);
    }

    .my_color {
      color:rgb(109, 74, 255)
    }
  
    .book_now_btn {
      display: inline-flex;
      padding: 3px 12px;
      border-radius: 10px;
      transition: all ease 0.3s;
      font-weight: 700;
      font-size: 20px;
      box-shadow: -3px 3px 0 #828086;
      border: 1px rgb(109, 74, 255, 0.3) solid;
      color: rgb(255, 255, 255);
      background-color: rgb(109, 74, 255, 0.6);
      margin: 10px;
    }
  
    .book_now_btn:hover {
      color: white;
      background-color: rgb(109, 74, 255);
    }
  
    .price-tag {
      background-color: rgb(0, 128, 0, 0.1);
      color: rgb(0, 128, 0);
      padding: 4px;
      border: 1px #c1bdc22e solid;
      border-radius: 8px;
      display: inline-block;
      font-weight: bold;
      box-shadow: transparent;
    }
  
    .description-heading {
      font-size: 1.4rem;
      font-weight: bold;
      color: #333;
      margin-bottom: 10px;
      border-bottom: 2px solid #007bff;
      padding-bottom: 5px;
    }
  
    .description-text {
      font-size: 1rem;
      color: #555;
      line-height: 1.6;
    }
  
    .cus-badge {
      border: 2px solid rgb(149, 150, 151);
      border-radius: 8px;
      background-color: darkblue;
      padding: 3px 10px;
      color: white;
    }
  
    #fix_cus_icon_rat {
      color: rgb(255, 183, 0);
      filter: drop-shadow(1px 1px 1px rgba(28, 28, 28, 0.174));
    }
  
    .search-results {
      border: 1px solid #ccc;
      max-height: 150px;
      overflow-y: auto;
      position: absolute;
      background-color: white;
      z-index: 10;
    }
  
    .search-results div {
      padding: 8px;
      cursor: pointer;
    }
  
    .search-results div:hover {
      background-color: #f1f1f1;
    }
  
    .range-slider {
      position: relative;
      width: 100%;
      height: 6px;
      margin: 20px 0;
      background-color: #ddd;
      border-radius: 5px;
    }
  
    .range-slider .range-track {
      position: absolute;
      height: 100%;
      background-color: #0d6efd;
      border-radius: 5px;
    }
  
    .range-slider input[type="range"] {
      -webkit-appearance: none;
      appearance: none;
      pointer-events: none;
      position: absolute;
      height: 6px;
      width: 100%;
      background: transparent;
    }
  
    .range-slider input[type="range"]::-webkit-slider-thumb {
      -webkit-appearance: none;
      appearance: none;
      pointer-events: auto;
      height: 18px;
      width: 18px;
      background-color: #0d6efd;
      border-radius: 50%;
      cursor: pointer;
      position: relative;
    }
  
    .range-slider input[type="range"]::-moz-range-thumb {
      pointer-events: auto;
      height: 18px;
      width: 18px;
      background-color: #0d6efd;
      border-radius: 50%;
      cursor: pointer;
      position: relative;
    }
  
    .price-values {
      display: flex;
      justify-content: space-between;
      margin-top: 10px;
    }
  
    @media (max-width: 768px) {
      .cus_filter_box {
        display: none;
      }
  
      .profile-picture {
        height: 6rem;
      }
  
      .d-lg-none {
        display: block;
      }
  
      .filter-modal-content {
        max-height: 80vh;
        overflow-y: auto;
      }
    }
  
    @media (min-width: 768px) {
      .row {
        display: flex;
        flex-wrap: nowrap;
      }
  
      .cus_filter_box {
        position: sticky;
        top: 0;
        height: 100vh;
        overflow-y: auto;
        padding-right: 15px;
      }
  
      .col-lg-8 {
        overflow-y: auto;
        height: 100vh;
      }
    }
  </style>