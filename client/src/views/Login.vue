<script setup>
    import google from '@/assets/google.svg';
    import facebook from '@/assets/facebook.svg';
    import microsoft from '@/assets/microsoft.svg';
    import logo from '@/assets/logo.png'
    import back_left from '@/assets/back-left.svg'
    import back_right from '@/assets/back-right.svg'
    import login from '@/assets/login.png'

    import router from '@/router';
    import { ref } from 'vue';

    const goBack = () => router.go(-1)

    const apiUrl = import.meta.env.VITE_API_URL;
    const errorMsg = ref('')

    const params = new URLSearchParams(window.location.search)
    errorMsg.value = params.get('error')

    const finalSubmit = async (event) => {
        const form = event.target
        if (!form.checkValidity()) {
            form.reportValidity()
            return
        }

        try {
            const data = {
                "user_mail": form.user_mail.value,
                "password": form.password.value
            }
            const response = await fetch(`${apiUrl}/login`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data),
                credentials: 'include'
            })

            const token_or_error = await response.json()

            if (response.status === 200) {
                router.push('/dashboard')
            } else if (response.status === 401 || response.status === 404 || response.status === 400) {
                errorMsg.value = token_or_error['message']
            } else {
                console.log(response.text)
            }
        }
        catch (error) {
            console.log('Fetch Error: ', error)
            return null;
        }
    }

    // Google OAuth
    const googleClientId = import.meta.env.VITE_GOOGLE_CLIENT_ID
    const facebookClientId = import.meta.env.VITE_FACEBOOK_CLIENT_ID

    const googleOAuthUrl = `https://accounts.google.com/o/oauth2/v2/auth?client_id=${googleClientId}&redirect_uri=${apiUrl}/login/google-oauth&response_type=code&scope=email%20profile%20openid`
    const facebookOAuthUrl = `https://www.facebook.com/v12.0/dialog/oauth?client_id=${facebookClientId}&redirect_uri=${apiUrl}/login/facebook-oauth&response_type=code&scope=email,public_profile`


    const oauthLogin = async () => {
        const oauth_data = {
            'oauth_user': true,
            'user_mail': credentials.get('user_mail'),
            'platform': credentials.get('platform'),
            'unique_id': credentials.get('unique_id')
        }
        const oauthLogin = await fetch(`${apiUrl}/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(oauth_data),
            credentials: 'include'
        })

        const token_or_error = await oauthLogin.json()

        if (oauthLogin.status === 200) {
            router.push('/dashboard')
        } else if (oauthLogin.status === 401 || oauthLogin.status === 404) {
            errorMsg.value = token_or_error['message']
        } else {
            console.log(oauthLogin.text)
        }
    }

    const credentials = new URLSearchParams(window.location.search)
    if (credentials.get('oauth_user') === 'True') {
        oauthLogin()
    }


    const passwordVisible = ref(false);

    const togglePasswordVisibility = () => {
        passwordVisible.value = !passwordVisible.value;
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
                <div class="col-12 col-md-5 mb-5">
                    <img :src="login" class="hola" height="600px">
                </div>



                <!-- Right Side: Account Type Selection -->
                <div class="col-12 col-md-7 d-flex flex-column align-items-center justify-content-center mb-5">
                    <div class="custom-card">
                        <div class="card-body">
                            <div class="card-title mb-3 d-flex align-items-center gap-2">
                                <div>
                                    <i class="ri-corner-up-left-double-fill back-button2" @click="goBack"></i>
                                </div>
                                <h3 class="mt-1">Login to Your Account!</h3>
                            </div>

                            <div class="fs-5 mb-1 text-danger text-center">
                                {{ errorMsg }}
                            </div>
                            <form @submit.prevent="finalSubmit" novalidate>
                                <div class="mb-3">
                                    <label class="form-label text-muted fw-semibold mb-2" for="user_mail">Username or
                                        Email</label>
                                    <div class="position-relative">
                                        <i
                                            class="ri-user-smile-line custom_icon position-absolute top-50 start-0 translate-middle-y ms-3 text-muted"></i>
                                        <input class="form-control custom_input ps-5" type="text" name="user_mail"
                                            minlength="3" maxlength="255" placeholder="Enter your username or email" required>
                                    </div>
                                </div>


                                <div class="mb-3">
                                    <label for="password"
                                        class="form-label text-muted fw-semibold mb-2">Password</label>
                                    <div class="position-relative">
                                        <i
                                            class="ri-lock-2-line custom_icon position-absolute top-50 start-0 translate-middle-y ms-3 text-muted"></i>
                                        <input :type="passwordVisible ? 'text' : 'password' "
                                            class="form-control custom_input ps-5" name="password" minlength="8"
                                            placeholder="Enter your password" required>

                                        <i class="ri-eye-fill huhu custom_icon position-absolute top-50 end-0 translate-middle-y me-3 text-muted"
                                            @click="togglePasswordVisibility" v-if="!passwordVisible"></i>
                                        <i class="ri-eye-off-fill huhu custom_icon position-absolute top-50 end-0 translate-middle-y me-3 text-muted"
                                            @click="togglePasswordVisibility" v-if="passwordVisible"></i>
                                    </div>
                                </div>

                                <!-- Forgot Password Link -->
                                <div class="text-end mb-3">
                                    <RouterLink to="/forgot-password" class="custom_text fw-semibold">Forgot Password?
                                    </RouterLink>
                                </div>


                                <div class="cus-container mt-3 text-decoration-none">
                                    <button class="cus-btn" type="submit">
                                        <span> Login </span>
                                        <i class="ri-arrow-right-fill"></i>
                                    </button>
                                </div>

                            </form>

                            <div class="d-flex align-items-center justify-content-center my-4">
                                <p class="text-center">Don't have an account?
                                    <RouterLink to="/signup" class="custom_text fw-bold">Signup</RouterLink>
                                </p>
                            </div>

                            <div class="d-flex align-items-center my-4">
                                <hr class="flex-grow-1" />
                                <span class="mx-2">OR</span>
                                <hr class="flex-grow-1" />
                            </div>

                            <div class="d-flex flex-column gap-3">
                                <a :href="googleOAuthUrl"
                                    class="oauth-btn oauth rounded d-flex flex-row align-items-center justify-content-center gap-2 p-2">
                                    <img :src="google" alt="">
                                    <div class="">
                                        Login with Google
                                    </div>
                                </a>
                                <a :href="facebookOAuthUrl"
                                    class="oauth-btn oauth rounded d-flex flex-row align-items-center justify-content-center gap-2 p-2">
                                    <img :src="facebook" alt="">
                                    <div>
                                        Login with Facebook
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
    .holi {
        background-repeat: repeat;
        background-size: calc(100vw * 1);
    }

    .cus-container {
        display: flex;

    }

    .huhu {
        cursor: pointer;
    }

    .custom_text {
        color: slateblue;
        text-decoration: none;
    }

    .custom_input {
        padding: 10px 33px;
        border: 2px solid #e9eded;
    }

    .custom_icon {
        font-size: 22px;
    }

    .cus-container2 {
        display: block;
        justify-content: end;
        margin-bottom: 5px;

    }

    .navbar {
        border: 1px rgb(191, 194, 193) solid;
    }


    .myBtn {
        background-color: #585858;
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

    .hola {
        padding-left: 100px;
    }
</style>