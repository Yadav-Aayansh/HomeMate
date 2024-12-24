<script setup>
  import logo from '@/assets/logo.png';
  import signup from '@/assets/signup1.png'
  import back_left from '@/assets/back-left.svg'
  import back_right from '@/assets/back-right.svg'


  import { ref, onMounted } from 'vue';
  import router from '@/router';
  import { signupStore } from '@/stores/signup.js'

  const goBack = () => router.go(-1)

  const errorMsg = ref('')
  const signup_Store = signupStore()

  const name = ref(signup_Store.name)
  const nameInput = ref(null)

  const apiUrl = import.meta.env.VITE_API_URL;

  const category = ref('')
  const service = ref(null)
  const service_type = ref('')
  const availability = ref('')
  const categories = ref([])
  const fetchCategories = async () => {
    try {
      const response = await fetch(`${apiUrl}/services`, {
        method: 'GET',
        credentials: 'include'
      })
      if (!response.ok) {
        throw new Error('Network response is not okay!')
      }
      const data = await response.json()
      categories.value = data['Service Categories']
    }
    catch (error) {
      console.log('Fetch error:', error)
      return null;
    }
  }

  const services = ref([])
  const fetchServices = async (category) => {
    try {
      const response = await fetch(`${apiUrl}/services?category=${category}`, {
        method: 'GET',
        credentials: 'include'
      })
      if (!response.ok) {
        throw new Error('Network response is not okay!')
      }
      const data = await response.json()
      services.value = data['Services']
    }
    catch (error) {
      console.log('Fetch error:', error)
      return null;
    }
  }

  onMounted(fetchCategories);

  const finalSubmit = async (event) => {
    const form = event.target;
    if (!form.checkValidity()) {
      form.reportValidity()
      return
    }


    try {
      if (signup_Store.role === 'Customer') {
        var additional = {
          "pincode": form.pincode.value,
          "address": form.address.value,
          "role": signup_Store.role
        }
      } if (signup_Store.role === 'Service Professional') {
        var additional = {
          "category": form.category.value,
          "service_type": form.service.value,
          "availability": form.availability.value,
          "experience": form.experience.value,
          "role": 'Professional'
        }
      }
      const data = {
        "username": signup_Store.username,
        "email": signup_Store.email,
        "password": signup_Store.password,
        "confirm_password": signup_Store.confirm_password,
        "oauth_user": signup_Store.oauth_user,
        "name": form.name.value,
        "platform": signup_Store.platform,
        "unique_id": signup_Store.unique_id,
        ...additional
      }

      const response = await fetch(`${apiUrl}/signup`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      })
      if (response.status == 200) {
        router.push("/login")
      } else if (response.status == 400) {
        const error = await response.json()
        errorMsg.value = error['message']
      } else {
        console.log(response.text)
      }

    }
    catch (error) {
      console.log('Fetch error:', error)
      return null;
    }

  }


  const address = ref('')
  const pincode = ref()
  const searchResults = ref([])
  const searchResult = async () => {
    const response = await fetch(`${apiUrl}/autocomplete?q=${address.value}`)
    const data = await response.json()
    if (response.ok) {
      searchResults.value = data.result
    }
  }

  const selectAddress = (item) => {
    address.value = item.address
    pincode.value = item.pincode
    searchResults.value.length = 0
  }


</script>


<template>
  <div :style="{ backgroundImage: `url(${back_left}), url(${back_right})` }" class="holi">

    <div>
      <nav class="navbar navbar-expand-lg cus-nav mt-4">
        <div class="container-fluid">
          <div class="brand">
            <img :src="logo" alt="Logo" class="me-2" height="50px">
            <p class="brand">HomeMate</p>
          </div>

          <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarTogglerDemo02"
            aria-controls="navbarTogglerDemo02" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
          </button>
          <div class="collapse navbar-collapse" id="navbarTogglerDemo02">
            <ul class="navbar-nav me-auto mb-2 mb-lg-0">
            </ul>

            <div class="d-flex flex-column align-items-center me-2 me-md-3 me-lg-4">
              <p>STEP 3 OF 3</p>
              <div class="d-flex justify-content-center">
                <div class="horizontal-bar mx-1 bar-secondary"></div>
                <div class="horizontal-bar mx-1 bar-secondary"></div>
                <div class="horizontal-bar mx-1 bar-primary"></div>
              </div>
            </div>

          </div>
        </div>
      </nav>
    </div>


    <div class="container-fluid">
      <div class="row mt-5 d-flex justify-content-center">
        <!-- Left Side: Tagline -->
        <div class="col-12 col-md-5 mb-5">
          <img :src="signup" height="600px">
        </div>



        <!-- Right Side: Account Type Selection -->
        <div class="col-12 col-md-7 d-flex flex-column align-items-center justify-content-center mb-5">
          <div class="cus-card">
            <div class="card-body">
              <div class="card-title mb-3 d-flex align-items-center gap-2">
                <div>
                  <i class="ri-corner-up-left-double-fill back-button2" @click="goBack"></i>
                </div>
                <h3 class="mt-1">Additional Info For Account</h3>
              </div>
              <div>
                <div class="fs-5 text-danger text-center">
                  {{ errorMsg }}
                </div>
              </div>
              <form class="needs-validation" @submit.prevent="finalSubmit" novalidate>

                <div class="mb-3">
                  <label for="name" class="form-label text-muted fw-semibold mb-2">Name</label>
                  <div class="position-relative">
                    <i class="ri-user-6-line custom_icon position-absolute top-50 start-0 translate-middle-y ms-3 text-muted"></i>
                    <input type="text" class="form-control custom_input ps-5" v-model="name" name="name" placeholder="Enter your name"
                      required>
                  </div>
                </div>

                <div class="mb-3" v-if="signup_Store.role==='Customer'">
                  <label for="search" class="form-label text-muted fw-semibold mb-2">Address</label>
                  <div class="position-relative">
                    <i class="ri-home-2-line custom_icon position-absolute top-50 start-0 translate-middle-y ms-3 text-muted"></i>
                    <input type="search" class="form-control custom_input ps-5" v-model="address" name="address" @input="searchResult"
                      placeholder="Enter your address" required />
                    <div v-if="searchResults.length > 0" class="search-results">
                      <div v-for="item in searchResults" :key="item.id" @click="selectAddress(item)">
                        {{ `${item.address}, ${item.pincode}` }}
                      </div>
                    </div>
                  </div>
                </div>

                <div class="mb-3" v-if="signup_Store.role==='Customer'">
                  <label for="pincode" class="form-label text-muted fw-semibold mb-2">Pincode</label>
                  <div class="position-relative">
                    <i class="ri-map-pin-range-line custom_icon position-absolute top-50 start-0 translate-middle-y ms-3 text-muted"></i>
                    <input type="text" class="form-control custom_input ps-5" v-model="pincode" name="pincode"
                      placeholder="Enter your pincode" required>
                  </div>
                </div>

                <div class="mb-3" v-if="signup_Store.role==='Service Professional'">
                  <label for="category" class="form-label text-muted fw-semibold mb-2">Category</label>
                  <div class="position-relative">
                    <i class="ri-group-line custom_icon position-absolute top-50 start-0 translate-middle-y ms-3 text-muted"></i>
                    <select class="form-select custom_input ps-5" v-model="category" name="category" required
                      @change="fetchServices($event.target.value)">
                      <option v-if="!category" value="">Select a category</option>
                      <option v-for="cat in categories" :key="cat" :value="cat">
                        {{ cat }}
                      </option>
                    </select>
                  </div>
                </div>

                
                <div class="mb-3" v-if="signup_Store.role==='Service Professional'">
                  <label for="service_type" class="form-label text-muted fw-semibold mb-2">Service Type</label>
                  <div class="position-relative">
                    <i class="ri-service-line custom_icon position-absolute top-50 start-0 translate-middle-y ms-3 text-muted"></i>
                    <select class="form-select custom_input ps-5" v-model="service_type" name="service" required>
                      <option v-if="!category" value="">Select a category first </option>
                      <option v-else-if="category && !service" value="">Select a service type</option>
                      <option v-for="ser in services" :key="ser" :value="ser">
                        {{ ser }}
                      </option>
                    </select>
                  </div>
                </div>

              
                <div class="mb-3" v-if="signup_Store.role==='Service Professional'">
                  <label for="experience" class="form-label text-muted fw-semibold mb-2">Experience (In Years)</label>
                  <div class="position-relative">
                    <i class="ri-briefcase-2-line custom_icon position-absolute top-50 start-0 translate-middle-y ms-3 text-muted"></i>
                    <input type="number" class="form-control custom_input ps-5" v-model="experience" name="experience" min="0" max="25"
                      placeholder="Enter your experience" required>
                  </div>
                </div>

                <div class="mb-3" v-if="signup_Store.role==='Service Professional'">
                  <label for="availability" class="form-label text-muted fw-semibold mb-2">Availability</label>
                  <div class="position-relative">
                    <i class="ri-time-line custom_icon position-absolute top-50 start-0 translate-middle-y ms-3 text-muted"></i>
                    <select class="form-select custom_input ps-5" v-model="availability" name="availability" required>
                      <option value="">Select your availability</option>
                      <option value="Full Time"> Full Time</option>
                      <option value="Part Time"> Part Time</option>
                    </select>
                  </div>
                </div>


                <div class="cus-container mt-3">
                  <button class="cus-btn" type="submit">
                    <span> Submit </span>
                    <i class="ri-checkbox-circle-line"></i>
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>


  </div>
</template>


<style scoped>
  .cus-container {
    display: flex;
  }

  .cus-container2 {
    display: block;
    justify-content: end;
    margin-bottom: 5px;

  }

  .holi {
        background-repeat: repeat;
        background-size: calc(100vw * 1);
    }

    .custom_input {
        padding: 10px 33px;
        border: 2px solid #e9eded;
    }

    .custom_icon {
        font-size: 22px;
    }

  .cus-btn {
    background-color: rgb(109, 74, 255);
    color: white;
    width: 100%;
    border-radius: 6px;
    font-weight: bold;
    cursor: pointer;
    transition: all 0.3s, color 0.3s;
    box-shadow: 4px 4px 0.5px #353535;
    outline: none;
    padding: 7.5px;
    border: transparent;
    border: 2px solid transparent;

  }

  .cus-btn:hover {
    border: 2px solid #353535;
    box-shadow: 4px 4px 0.5px #353535, inset 0px 0px 15px 3px #b2a3cb5e;
    color: rgb(109, 74, 255);
    background-color: rgba(240, 248, 255, 0.774);
  }

  .cus-btn i {
    font-weight: bold;
    transform: scale(10);
  }

  .user {
    font-weight: 600;
    font-size: 1.2em;
  }

  .cus-radio {
    appearance: none;
    width: 20px;
    height: 20px;
    background-color: #eee;
    border-radius: 50%;
    display: inline-block;
    position: relative;
    cursor: pointer;
    outline: none;
    border: 2px solid rgb(109, 74, 255);
  }

  .cus-radio:checked {
    background-color: rgb(109, 74, 255);
  }

  .cus-radio:checked::after {
    content: '';
    position: absolute;
    top: 3px;
    left: 3px;
    width: 10px;
    height: 10px;
    background-color: white;
    border-radius: 50%;
  }

  .cus-bg {
    background-color: rgba(109, 74, 255, 0.1);
  }

  .branding {
    display: flex;
    align-items: center;
    gap: 3px;
    text-decoration: none;
  }

  .title {
    font-size: 2em;
    font-weight: 900;
    color: black;
  }

  .back-button {
    border-color: black;
  }

  .oauth-btn {
    /* font-weight: bo; */
    padding: 5px;
  }

  .oauth-btn:hover {
    color: white;
    background-color: black;
  }

  .cus-nav {
    width: 90%;
    background-color: white;
    border-radius: 20px;
    margin: 0 auto;
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

  .placeholder {
    color: black !important;
    background-color: white;
    position: absolute;
    /* Allow positioning over the select */
    pointer-events: none;
    /* Prevent clicks on the placeholder */
    top: 8px;
    /* Adjust based on your select height */
    left: 50px;
    /* Position based on your input icon */
    z-index: 1;
    /* Ensure it appears above other elements */
    transition: 0.2s ease all;
    /* Smooth transition effect */
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
</style>