<script setup>
  import { ref, watch } from 'vue';
  import logo from '@/assets/logo.png';
  import router from '@/router';
  import { signupStore } from '@/stores/signup.js'
  import Tagline from '@/components/Tagline.vue'
  import signup from '@/assets/signup1.png'
  import back_left from '@/assets/back-left.svg'
  import back_right from '@/assets/back-right.svg'

  const signup_Store = signupStore()
  const roleChecker = (role) => selectedRole.value === role;

  const selectedRole = ref(signup_Store.role)
  watch(selectedRole, () => {
    signup_Store.changeRole(selectedRole.value)
  })

  const goBack = () => router.go(-1)

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
              <p>STEP 1 OF 3</p>
              <div class="d-flex justify-content-center">
                <div class="horizontal-bar mx-1 bar-primary"></div>
                <div class="horizontal-bar mx-1 bar-secondary"></div>
                <div class="horizontal-bar mx-1 bar-secondary"></div>
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
                  <h3 class="mt-1">Select Your Account Type</h3>
                </div>
                <div class="row">
                  <label>
                    <div class="card" :class="roleChecker('Customer') ? 'cus-bg' : ''">
                      <div class="card-header d-flex justify-content-between">
                        <div>
                          <i class="bi bi-person fs-5"></i>
                          <span class="ms-2 kg-text3">I'm a Customer</span>
                        </div>
                        <input class="cus-radio" type="radio" name="role" value="Customer" v-model="selectedRole" checked>
                      </div>
                      <div class="card-body">
                        <p>I want to book services and get tasks done.</p>
                      </div>
                    </div>
                  </label>
                </div>
                <div class="row mt-3">
                  <label>
                    <div class="card" :class="roleChecker('Service Professional') ? 'cus-bg' : ''">
                      <div class="card-header d-flex justify-content-between">
                        <div>
                          <i class="bi bi-gear fs-5"></i>
                          <span class="kg-text3 ms-2">I'm a Service Professional</span>
                        </div>
                        <input class="cus-radio" type="radio" name="role" value="Service Professional"
                          v-model="selectedRole">
                      </div>
                      <div class="card-body">
                        <p>I want to offer my services and get paid.</p>
                      </div>
                    </div>
                  </label>
                </div>
                <RouterLink to="/signup/personal-info" class="cus-container mt-3 text-decoration-none">
                  <button class="cus-btn">
                    <span> Next </span>
                    <i class="ri-arrow-right-fill"></i>
                  </button>
                </RouterLink>
              </div>
            </div>
          </div>
      </div>

  </div>

  </div>
</template>



<style scoped>
    .holi {
        background-repeat: repeat;
        background-size: calc(100vw * 1);
    }

  .cus-container {
    display: flex;
  }

  .navbar {
    border: 1px rgb(191, 194, 193) solid;
  }

  .cus-container2 {
    display: block;
    justify-content: end;
    margin-bottom: 5px;

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
    font-weight: 700;
    font-size: 1.25rem;
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
</style>