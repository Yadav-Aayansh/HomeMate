<script setup>
  import logo from '@/assets/logo.png';
  import google from '@/assets/google.svg';
  import microsoft from '@/assets/microsoft.svg';
  import facebook from '@/assets/facebook.svg';
  import signup from '@/assets/signup1.png'
  import back_left from '@/assets/back-left.svg'
  import back_right from '@/assets/back-right.svg'

  import { ref, computed } from 'vue';
  import router from '@/router';
  import { signupStore } from '@/stores/signup.js'
  import Tagline from '@/components/Tagline.vue'

  const goBack = () => router.go(-1)

  const signup_Store = signupStore()

  const formattedRole = () => {
    if (signup_Store.role === 'Service Professional') {
      return 'Professional'
    }
    return signup_Store.role
  }


  const username = ref(signup_Store.username)
  const email = ref(signup_Store.email)
  const password = ref(signup_Store.password)
  const confirm_password = ref(signup_Store.confirm_password)

  const usernameInput = ref(null)
  const emailInput = ref(null)
  const passwordInput = ref(null)
  const confirm_passwordInput = ref(null)

  function pseudoSubmit(event) {
    event.preventDefault()
    const form = event.target;

    if (!form.checkValidity()) {
      form.reportValidity()
      return
    }

    const pattern = /^[a-zA-Z0-9_]{3,20}$/
    if (!pattern.test(username.value)) {
      usernameInput.value.setCustomValidity('Username can only contain letters, numbers, and underscores.');
      usernameInput.value.reportValidity()
      return
    }
    if (password.value.length < 8) {
      passwordInput.value.setCustomValidity('Password must be at least 8 characters.')
      passwordInput.value.reportValidity()
      return
    }
    if (confirm_password.value.length < 8) {
      confirm_passwordInput.value.setCustomValidity('Confirm Password must be at least 8 characters.')
      confirm_passwordInput.value.reportValidity()
      return
    }
    if (password.value != confirm_password.value) {
      passwordInput.value.setCustomValidity('Password and Confirm Password must be same.')
      confirm_passwordInput.value.setCustomValidity('Password and Confirm Password must be same.')
      passwordInput.value.reportValidity()
      confirm_passwordInput.value.reportValidity()
      return
    }
    else {
      signup_Store.changeUsername(username.value)
      signup_Store.changeEmail(email.value)
      signup_Store.changePassword(password.value)
      signup_Store.changeConfirmPassword(confirm_password.value)
      router.push('/signup/additional-info')
    }
  }

  function clearCustom(input) {
    input.setCustomValidity('')
  }

  // OAuth
  const googleClientId = import.meta.env.VITE_GOOGLE_CLIENT_ID
  const facebookClientId = import.meta.env.VITE_FACEBOOK_CLIENT_ID

  const apiUrl = import.meta.env.VITE_API_URL
  const roleState = encodeURIComponent(`role=${signup_Store.role}`)
  const googleOAuthUrl = `https://accounts.google.com/o/oauth2/v2/auth?client_id=${googleClientId}&redirect_uri=${apiUrl}/signup/google-oauth&response_type=code&scope=email%20profile%20openid&state=${roleState}`
  const facebookOAuthUrl = `https://www.facebook.com/v12.0/dialog/oauth?client_id=${facebookClientId}&redirect_uri=${apiUrl}/signup/facebook-oauth&response_type=code&scope=email,public_profile&state=${roleState}`;

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
              <p>STEP 2 OF 3</p>
              <div class="d-flex justify-content-center">
                <div class="horizontal-bar mx-1 bar-secondary"></div>
                <div class="horizontal-bar mx-1 bar-primary"></div>
                <div class="horizontal-bar mx-1 bar-secondary"></div>
              </div>
            </div>

          </div>
        </div>
      </nav>
    </div>

    <div class="container-fluid">
      <div class="row mt-3 d-flex justify-content-center">
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
                <h3 class="mt-1">Create a {{formattedRole()}} Account</h3>
              </div>
              <form @submit="pseudoSubmit" novalidate>
                <div class="mb-3">
                  <label for="username" class="form-label text-muted fw-semibold mb-2">Username</label>
                  <div class="position-relative">
                    <i class="ri-user-smile-line custom_icon position-absolute top-50 start-0 translate-middle-y ms-3 text-muted"></i>
                    <input type="text" class="form-control custom_input ps-5" v-model="username" ref="usernameInput"
                      @input="clearCustom(usernameInput)" minlength="3" maxlength="20" placeholder="Choose a username"
                      required>
                  </div>
                </div>

                <div class="mb-3">
                  <label for="email " class="form-label text-muted fw-semibold mb-2">Email</label>
                  <div class="position-relative">
                    <i class="ri-mail-line custom_icon position-absolute top-50 start-0 translate-middle-y ms-3 text-muted"></i>
                    <input type="email" class="form-control custom_input ps-5" v-model="email" ref="emailInput"
                      @input="clearCustom(emailInput)" placeholder="Enter your email address" required>
                  </div>
                </div>

                <div class="mb-3">
                  <label for="password" class="form-label text-muted fw-semibold mb-2">Password</label>
                  <div class="position-relative">
                    <i class="ri-lock-2-line custom_icon position-absolute top-50 start-0 translate-middle-y ms-3 text-muted"></i>
                    <input type="password" class="form-control custom_input ps-5" v-model="password" ref="passwordInput"
                      @input="clearCustom(passwordInput)" placeholder="Create a password" required>
                  </div>
                </div>

                <div class="mb-3">
                  <label for="confirm_password" class="form-label text-muted fw-semibold mb-2">Confirm Password</label>
                  <div class="position-relative">
                    <i class="ri-lock-2-line custom_icon position-absolute top-50 start-0 translate-middle-y ms-3 text-muted"></i>
                    <input type="password" class="form-control custom_input ps-5" v-model="confirm_password" ref="confirm_passwordInput"
                      @input="clearCustom(confirm_passwordInput)" placeholder="Confirm password" required>
                  </div>
                </div>

                <div class="cus-container mt-3 text-decoration-none">
                  <button class="cus-btn" type="submit">
                    <span> Next </span>
                    <i class="ri-arrow-right-fill"></i>
                  </button>
                </div>

              </form>

              <div class="d-flex align-items-center my-4">
                <hr class="flex-grow-1" />
                <span class="mx-2">OR</span>
                <hr class="flex-grow-1" />
              </div>

              <div class="d-flex flex-column gap-3">
                <a :href="googleOAuthUrl"
                  class="oauth-btn oauth rounded d-flex flex-row align-items-center justify-content-center gap-2 p-2">
                  <img :src="google" alt="">
                  <div>
                    Signup with Google
                  </div>
                </a>
                <a :href="facebookOAuthUrl"
                  class="oauth-btn oauth rounded d-flex flex-row align-items-center justify-content-center gap-2 p-2">
                  <img :src="facebook" alt="">
                  <div>
                    Signup with Facebook
                  </div>
                </a>
              </div>
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

  .myBtn {
    background-color: #585858;
  }

    .custom_icon {
        font-size: 20px;
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
    transition: all ease 0.3s;
    font-weight: 600;
    font-size: 16px;
    box-shadow: 3px 3px 4px 1px #48484840;
    border: transparent;
    color: rgb(43, 43, 43);
    background-color: rgba(239, 239, 239);
    text-decoration: none;
  }

  .oauth-btn:hover {
    color: white;
    background-color: rgba(14, 14, 14, 0.895);
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