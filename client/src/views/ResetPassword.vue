<script setup>
    import logo from '@/assets/logo.png'
    import back_left from '@/assets/back-left.svg'
    import back_right from '@/assets/back-right.svg'
    import forgot from '@/assets/forgot.svg'
    import router from '@/router';
    import { ref } from 'vue';
    import { useRoute } from 'vue-router';
    import Popup from '@/components/Popup.vue'


    const goBack = () => router.go(-1)
    const apiUrl = import.meta.env.VITE_API_URL

    const passwordVisible = ref(false);

    const togglePasswordVisibility = () => {
        passwordVisible.value = !passwordVisible.value;
    }

    const route = useRoute();
    const token = route.query.token;

    const isMessage = ref(false)
    const errorMsg = ref(null)
    const message = ref('')
    const password = ref('')
    const confirm_password = ref('')
    const resetPassword = async() => {
        const response = await fetch(`${apiUrl}/reset-password`, {
            method: 'POST',
            credentials:'include',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                token: token,
                password: password.value,
                confirm_password: confirm_password.value
            })
        })
        const data = await response.json()
        if (response.ok) {
            message.value = data.message
            isMessage.value = true
        } else {
            errorMsg.value = data.message
        }
    }

    const login = () => {
        router.push('/login')
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

                    <button class="navbar-toggler" type="button" data-bs-toggle="collapse"
                        data-bs-target="#navbarTogglerDemo02" aria-controls="navbarTogglerDemo02" aria-expanded="false"
                        aria-label="Toggle navigation">
                        <span class="navbar-toggler-icon"></span>
                    </button>
                    <div class="collapse navbar-collapse" id="navbarTogglerDemo02">
                        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                        </ul>

                        <div class="d-flex flex-column align-items-center me-2 me-md-3 me-lg-4">
                            <i class="ri-menu-4-fill fs-3"></i>
                        </div>

                    </div>
                </div>
            </nav>
        </div>

        <div class="container-fluid">
            <div class="row mt-5 d-flex justify-content-center">
                <!-- Left Side: Tagline -->
                <div class="col-12 col-md-5 dots mb-5">
                    <img :src="forgot" class="hola" height="600px">
                </div>



                <!-- Right Side: Account Type Selection -->
                <div class="col-12 col-md-7 d-flex flex-column align-items-center justify-content-center mb-5">
                    <div class="custom-card">
                        <div class="card-body">
                            <div class="card-title mb-3 d-flex align-items-center gap-2">
                                <div>
                                    <i class="ri-corner-up-left-double-fill back-button2" @click="goBack"></i>
                                </div>
                                <h3 class="mt-1">Reset Your Password?</h3>
                            </div>
                            <p class="mb-3 text-center">Enter a new password in order to change your account password</p>
                            <div class="fs-5 text-danger text-center">
                                {{ errorMsg }}
                            </div>
                            <form @submit.prevent="resetPassword">


                                <div class="mb-3">
                                    <label for="password"
                                        class="form-label text-muted fw-semibold mb-2">Password</label>
                                    <div class="position-relative">
                                        <i
                                            class="ri-lock-2-line custom_icon position-absolute top-50 start-0 translate-middle-y ms-3 text-muted"></i>
                                        <input :type="passwordVisible ? 'text' : 'password' "
                                            class="form-control custom_input ps-5" v-model="password" minlength="8"
                                            placeholder="Enter your password" required>

                                        <i class="ri-eye-fill huhu custom_icon position-absolute top-50 end-0 translate-middle-y me-3 text-muted"
                                            @click="togglePasswordVisibility" v-if="!passwordVisible"></i>
                                        <i class="ri-eye-off-fill huhu custom_icon position-absolute top-50 end-0 translate-middle-y me-3 text-muted"
                                            @click="togglePasswordVisibility" v-if="passwordVisible"></i>
                                    </div>
                                </div>

                                <div class="mb-3">
                                    <label for="confirm_password"
                                        class="form-label text-muted fw-semibold mb-2">Confirm Password</label>
                                    <div class="position-relative">
                                        <i
                                            class="ri-lock-2-line custom_icon position-absolute top-50 start-0 translate-middle-y ms-3 text-muted"></i>
                                        <input :type="passwordVisible ? 'text' : 'password' "
                                            class="form-control custom_input ps-5" v-model="confirm_password" minlength="8"
                                            placeholder="Confirm your password" required>
                                    </div>
                                </div>


                                <div class="cus-container mt-3 text-decoration-none">
                                    <button class="cus-btn" type="submit">
                                        <span> Reset Password </span>
                                        <i class="ri-arrow-right-fill"></i>
                                    </button>
                                </div>
                            </form>

                            <div class="text-center mt-4">
                                <p class="text-muted">Remembered your password?</p>
                                <RouterLink to="/login" class="custom_text fw-semibold">Go back to Login</RouterLink>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

        </div>
    </div>

    <!-- Popup Message Modal -->
    <Popup :isOpen="isMessage" title="Reset Link Sent" @close="isMessage=false" :showConfirm="true" confirmButton="green" buttonName="Login" :myfunction="login">
        <p>{{message}}</p>     
    </Popup>
</template>

<style scoped>
    .holi {
        background-repeat: repeat;
        background-size: calc(100vw * 1);
    }

    .cus-container {
        display: flex;
    }

    .custom_input {
        padding: 10px 33px;
        border: 2px solid #e9eded;
    }

    .custom_icon {
        font-size: 22px;
    }

    .custom_text {
        color: slateblue;
        text-decoration: none;
    }

    .navbar {
        border: 1px rgb(191, 194, 193) solid;
    }

    .cus-nav {
        width: 90%;
        background-color: white;
        border-radius: 20px;
        margin: 0 auto;
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

    .cus-bg {
        background-color: rgba(109, 74, 255, 0.1);
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

    .hola {
        padding-left: 100px;
    }
</style>