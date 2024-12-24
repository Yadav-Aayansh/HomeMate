<script setup>
    import { ref } from 'vue';
    import { RouterLink } from 'vue-router';
    import logo from '@/assets/logo.png'
    import Group from '@/assets/Group.svg'
    import back_left from '@/assets/back-left.svg'
    import back_right from '@/assets/back-right.svg'
    import Footer from '@/components/Footer.vue'

    const moreInfo = ref(null)
    const learnMore = () => {
        if (moreInfo.value) {
            moreInfo.value.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            })
        }
    }


</script>

<template>
    <div :style="{ backgroundImage: `url(${back_left}), url(${back_right})` }" class="holi">

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

                    <RouterLink to="/login" class="btn login-btn me-3 fs-5 gap-1">
                        <i class="ri-login-circle-line"></i> Login
                    </RouterLink>

                    <RouterLink to="/signup" class="btn signup-btn fs-5 gap-1">
                        <i class="ri-edit-circle-line"></i>Get Started
                    </RouterLink>

                </div>
            </div>
        </nav>

        <section class="py-3 py-md-5 d-flex justify-content-center">
            <div class="container hero">
                <div class="row">
                    <div class="col-12 col-lg-6 pt-3 mb-5 mb-lg-0">
                        <h1 class="heading kg-text mt-5">One Solution For All Household Services.</h1>
                        <p class="paragraph">Effortlessly find and book trusted professionals for all your household
                            needs. Our platform connects you with skilled experts for any job, big or small.</p>
                        <div class="allbtn">
                            <a class="btn1 btns" @click="learnMore">Learn More <i class="ri-arrow-down-double-fill"></i></a>
                            <RouterLink to="/signup" class="btn2 btns">Create Account <i class="ri-login-circle-line"></i></RouterLink>
                        </div>
                    </div>
                    <div class="col-12 col-lg-6 text-center">
                        <img class="svg mx-auto" :src="Group" alt="">
                    </div>
                </div>
            </div>
        </section>

        <div class="container mt-5">
            <div class="row" ref="moreInfo">
                <div class="col-md-4">
                    <div class="home_card text-center">
                        <div class="card-body">
                            <i class="ri-calendar-check-line" style="font-size: 3rem; color: #007bff;"></i>
                            <h4 class="card-title mt-3">Effortless Service Booking</h4>
                            <p class="card-text">
                                Find and book trusted professionals with ease. Search by name, location, or pin code.
                            </p>
                        </div>
                    </div>
                </div>

                <div class="col-md-4">
                    <div class="home_card text-center">
                        <div class="card-body">
                            <i class="ri-shield-check-line" style="font-size: 3rem; color: #28a745;"></i>
                            <h4 class="card-title mt-3">Professional & Verified Experts</h4>
                            <p class="card-text">
                                Verified, customer-rated experts ensure high-quality, reliable services every time.
                            </p>
                        </div>
                    </div>
                </div>

                <div class="col-md-4">
                    <div class="home_card text-center">
                        <div class="card-body">
                            <i class="ri-bar-chart-box-line" style="font-size: 3rem; color: #ffc107;"></i>
                            <h4 class="card-title mt-3">Real-Time Updates & Reports</h4>
                            <p class="card-text">
                                Get reminders and detailed activity reports directly at your fingertips.
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <Footer></Footer>
    </div>
</template>

<style scoped>
    .holi {
        background-repeat: repeat;
        background-size: calc(100vw * 1);
    }

    .home_card {
        padding: 20px;
        background: linear-gradient(315deg, rgba(255, 222, 233, 0.2) 0%, rgba(181, 255, 252, 0.2) 100%);
        border-radius: 15px;
        border: 1px rgb(138, 134, 134) solid;
        position: relative;
    }

    .cus-nav {
        width: 90%;
        background-color: white;
        border-radius: 20px;
        margin: 0 auto;
        border: 1px rgb(186, 180, 180) solid;
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

    .login-btn {
        display: inline-flex;
        padding: 3px 5px;
        border-radius: 10px;
        transition: all ease 0.3s;
        font-weight: 600;
        font-size: 5px;
        box-shadow: 3px 3px 4px 1px #48484840;
        border: 1px rgb(43, 43, 43) solid;
        color: rgba(43, 43, 43, 0.9);
        background-color: rgb(180, 235, 52, 0.6);
    }

    .mysvgs {
        height: 100;
        overflow: hidden;
    }

    .svgs {
        position: absolute;

    }

    .login-btn:hover {
        color: rgb(43, 43, 43);
        background-color: rgb(180, 235, 52);
    }

    .signup-btn {
        display: inline-flex;
        padding: 3px 5px;
        border-radius: 10px;
        transition: all ease 0.3s;
        font-weight: 600;
        font-size: 16px;
        box-shadow: 3px 3px 4px 1px #48484840;
        border: 1px rgb(43, 43, 43) solid;
        color: rgb(255, 255, 255);
        background-color: rgb(109, 74, 255, 0.6);
    }

    .signup-btn:hover {
        color: white;
        background-color: rgb(109, 74, 255);
    }

    .hero {
        width: 80%;
    }

    .svg {
        max-width: 100%;
    }


    .heading {
        font-size: 50px;
        color: slateblue;
        margin-bottom: 20px;
    }

    .paragraph {
        font-size: 20px;
        color: rgb(109, 102, 157);
        line-height: 1.5;
        margin-bottom: 30px;
    }

    .allbtn {
        display: flex;
        justify-content: center;
        gap: 25px;
        padding-top: 20px;
        margin-bottom: 40px;
    }

    .btns {
        text-decoration: none;
        padding: 8px 25px;
        font-weight: 700;
        border-radius: 8px;
        font-size: 20px;
        transition: all 0.3s ease-in-out;
        cursor: pointer;
    }

    .btn1 {
        background-color: slateblue;
        color: white;
        border: none;
    }

    .btn1:hover {
        background-color: darkslateblue;
    }

    .btn2 {
        background-color: transparent;
        border: 2px solid slateblue;
        color: slateblue;
    }
</style>