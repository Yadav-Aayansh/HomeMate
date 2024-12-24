<script setup>
    import banner from '@/assets/Banner.png';
    import { currentUserStore } from '@/stores/currentUser';
    import { ref, inject } from 'vue';
    import { getCookie } from '@/utils.js';
    import Popup from '@/components/Popup.vue';

    const updateTitle = inject('updateTitle')
    updateTitle('My Profile')

    // Change Picture Modal
    const isModalOpen = ref(false);
    const openModal = () => {
        isModalOpen.value = true;
    };

    const staticUrl = import.meta.env.VITE_STATIC_URL
    const apiUrl = import.meta.env.VITE_API_URL

    const currentUser_Store = currentUserStore()
    const role = currentUser_Store.role

    const name = ref('')
    const username = ref('')
    const email = ref('')
    const profile_picture = ref('')
    const categories = ref([])
    const category = ref('')
    const description = ref('')
    const service_type = ref('')
    const service_fee = ref(0)
    const profile_verified = ref(0)
    const rating = ref(0)
    const fee = ref(0)
    const services = ref([''])
    const experience = ref(0)
    const availability = ref('')
    const identity_proof = ref(null)

    const fieldErrors = ref({});

    // Pincode Related
    const pincodes = ref([]);
    const pincodeInput = ref('');
    const error = ref('');

    const addPincode = () => {
        if (!/^\d{6}$/.test(pincodeInput.value)) {
            error.value = 'Pincode must be a 6-digit number';
            return;
        }
        if (pincodes.value.includes(pincodeInput.value)) {
            error.value = 'Pincode already added';
            return;
        }
        error.value = '';
        pincodes.value.push(pincodeInput.value);
        pincodeInput.value = '';
    };

    const removePincode = (index) => {
        pincodes.value.splice(index, 1);
    };

    const removeLastPincode = (event) => {
        if (event.key === 'Backspace' && !pincodeInput.value && pincodes.value.length > 0) {
            pincodes.value.pop();
        }
    };

    // Fetch Profile
    const fetchProfile = async () => {
        const response = await fetch(`${apiUrl}/profile`, {
            method: 'GET',
            credentials: 'include'
        });
        if (response.ok) {
            const data = await response.json()
            name.value = data.name
            username.value = data.username
            email.value = data.email
            fee.value = data.fee
            rating.value = data.rating
            profile_picture.value = data.profile_picture
            profile_verified.value = data.profile_verified
            description.value = data.description
            experience.value = data.experience
            availability.value = data.availability
            pincodes.value = data.serviceable_pincodes
            identity_proof.value = data.identity_proof

            const fetchCategories = await fetch(`${apiUrl}/services`, {
                method: 'GET',
                credentials:'include'
            })
            if (response.ok) {
                const data = await fetchCategories.json()
                categories.value = data['Service Categories']
            }

            const fetchCategory = await fetch(`${apiUrl}/services?service_type=${data.service_type}`, {
                method: 'GET',
                credentials:'include'
            })
            if (fetchCategory.ok) {
                const data = await fetchCategory.json()
                category.value = data['Service Category']
                service_fee.value = data['Service Fee']
                fetchServices(data['Service Category'])
            }
            service_type.value = data.service_type

        } else {
            console.log('Something went wrong')
        }
    }

    const fetchServices = async (category) => {
        try {
            const response = await fetch(`${apiUrl}/services?category=${category}`, {
                method: 'GET',
                credentials:'include'
            })
            if (response.ok) {
                const data = await response.json()
                services.value = data['Services']
            }
        }
        catch (error) {
            console.log('Fetch error:', error)
            return null;
        }
    }

    fetchProfile()

    const updateProfile = async (event) => {
        fieldErrors.value = {};
        const formData = new FormData(event.target);
        formData.append('serviceable_pincodes', pincodes.value)

        const response = await fetch(`${apiUrl}/profile`, {
            method: 'PUT',
            credentials: 'include',
            headers: {
                'X-CSRF-TOKEN': getCookie('csrf_access_token')
            },
            body: formData
        })

        if (!response.ok && response.status === 400) {
            const errorData = await response.json();
            const errorText = errorData.message;
            const fields = ['name', 'username', 'email', 'category', 'availability', 'description', 'service type', 'service fee', 'experience'];

            fields.forEach(field => {
                if (errorText.toLowerCase().includes(field)) {
                    fieldErrors.value[field] = `${errorText}`;
                }
            });
        }
        selectedFile.value = null;
        editForDocument.value = true
        fetchProfile()
    }


    const deletePicture = async () => {
        const response = await fetch(`${apiUrl}/profile`, {
            method: 'DELETE',
            credentials: 'include',
            headers: {
                'X-CSRF-TOKEN': getCookie('csrf_access_token')
            },
        })
        if (response.ok) {
            isModalOpen.value = false;
            fetchProfile();
        }
    }

    // Photo Upload
    const selectedFile = ref(null);
    const change_picture_file = ref(null)
    const handleFileChange = (event) => {
        const file = event.target.files[0];
        if (file) {
            selectedFile.value = file
            event.target.name = 'change_picture'
        }
    }
    const removeFile = () => {
        selectedFile.value = null;
        change_picture_file.value.removeAttribute('name')

    };

    // Identity Upload
    const identityFile = ref(null)
    const changeIdentity = (event) => {
        const file = event.target.files[0]
        if (file) {
            identityFile.value.setAttribute('name', 'identity_proof')
        } else {
            identityFile.value.removeAttribute('name')
        }
    }

    const editForDocument = ref(true)
    const changeEditMode = () => {
        editForDocument.value = !editForDocument.value
    }


</script>

<template>
    <div class="row">
        <div class="col-md-12 col-12 mb-3">
            <div class="cus-card3">
                <form @submit.prevent="updateProfile">
                    <div class="profile">
                        <div class="banner">
                            <!-- <img :src="shapes" alt="Banner"> -->
                            <img :src="banner" alt="Banner" class="banner_img">
                        </div>
                        <div class="main">
                            <div class="d-flex align-items-center justify-content-between">
                                <div class="d-flex align-items-center">
                                    <img :src="`${staticUrl}/profile/photos/${profile_picture}`" alt="Profile Image"
                                        class="profile-picture" />
                                    <div class="ms-3 d-flex flex-column align-items-start">
                                        <h4 class="username-title"> {{name}} </h4>
                                        <div class="d-flex">
                                            <p class="fw-semibold cus-badge me-1"> Service Pro </p>
                                            <p class="fw-semibold cus-badge"> <i class="ri-star-fill"
                                                    id="fix_cus_icon_rat"></i> {{rating}}/5 </p>
                                        </div>
                                    </div>
                                </div>
                                <div class="verification_status">
                                    <div v-if="profile_verified">
                                        <i class="ri-verified-badge-line"></i>
                                        Congratulations! Account is Verified.
                                    </div>
                                    <div v-else>
                                        <i class="ri-close-circle-line"></i>
                                        Your account hasn’t been verified yet.
                                    </div>
                                </div>
                            </div>

                            <div class="d-flex justify-content-between">
                                <div class="cus_fix_btn_top">
                                    <label class="btn btn-md change-pic">
                                        Change Picture <i class="ri-pencil-line p-1"></i>
                                        <input type="file" class="d-none" @change="handleFileChange"
                                            ref="change_picture_file" />
                                    </label>

                                    <div @click="openModal" class="btn btn-md ms-2 remove-pic"> Remove Picture <i
                                            class="ri-delete-bin-3-line p-1"></i></div>
                                    
                                    <div v-if="selectedFile" class="file-name-container">
                                        <span class="file-name">{{ selectedFile.name }}</span>
                                        <button @click="removeFile" class="remove-file-btn">Remove</button>
                                    </div>
                                </div>
                            </div>
                        </div>

                    </div>
                    <div class="row information_display">
                        <div class="col-md-6 col-12">
                            <div class="card-body mt-3">

                                <div class="fs-5 text-danger text-center">
                                    {{ errorMsg }}
                                </div>

                                <div class="container-fluid pahele_ifno">
                                    <h4 class="mb-2 mt-4 custom_sub_title">Personal Information </h4>

                                    <div class="mb-4">
                                        <label class="form-label text-muted fw-semibold mb-2" for="name">Name</label>
                                        <div class="position-relative">
                                            <i
                                                class="ri-user-smile-line custom_icon position-absolute top-50 start-0 translate-middle-y ms-3 text-muted"></i>
                                            <input v-model="name" class="form-control custom_input ps-5" type="text"
                                                name="name" placeholder="Enter your name" required>
                                        </div>
                                        <div v-if="fieldErrors.name" class="text-danger mt-1">{{ fieldErrors.name }}
                                        </div>
                                    </div>

                                    <div class="mb-4">
                                        <label class="form-label text-muted fw-semibold mb-2"
                                            for="username">Username</label>
                                        <div class="position-relative">
                                            <i
                                                class="ri-user-line custom_icon position-absolute top-50 start-0 translate-middle-y ms-3 text-muted"></i>
                                            <input v-model="username" class="form-control custom_input ps-5" type="text"
                                                name="username" minlength="3" maxlength="30"
                                                placeholder="Enter your username" required>
                                        </div>
                                        <div v-if="fieldErrors.username" class="text-danger mt-1">{{
                                            fieldErrors.username }}</div>
                                    </div>

                                    <div class="mb-4">
                                        <label class="form-label text-muted fw-semibold mb-2" for="email">Email</label>
                                        <div class="position-relative">
                                            <i
                                                class="ri-mail-line custom_icon position-absolute top-50 start-0 translate-middle-y ms-3 text-muted"></i>
                                            <input v-model="email" class="form-control custom_input ps-5" type="email"
                                                name="email" maxlength="255" placeholder="Enter your email" required>
                                        </div>
                                        <div v-if="fieldErrors.email" class="text-danger mt-1">{{ fieldErrors.email }}
                                        </div>
                                    </div>

                                    <!-- Identity Proof Document Field -->
                                    <div class="mb-4">
                                        <label class="form-label text-muted fw-semibold mb-2" for="experience">Identity
                                            Proof</label>
                                        <div class="tag-input-container position-relative"
                                            style="display: flex; width: 100%;">
                                            <i class="ri-file-lock-line custom_icon p-2 top-50 text-muted ms-2"></i>
                                            <div v-if="profile_verified" style="top: 50">
                                                <a :href="`${staticUrl}/profile/identity/${identity_proof}`"
                                                    target="_blank" class="file-name fw-normal text-decoration-none">{{
                                                    identity_proof }}</a>
                                            </div> 
                                            <div v-else style="padding-right: 10px; width: 90%;">
                                                <div v-if="!identity_proof" class="document_picker">
                                                    <input type="file" @change="changeIdentity" ref="identityFile"
                                                        class="custom_input ps-1 tag-input" />
                                                </div>
                                                <div v-else>
                                                    <div v-if="editForDocument" style="display: flex; justify-content: space-between; align-items: center;">
                                                        <a :href="`${staticUrl}/profile/identity/${identity_proof}`"
                                                            target="_blank"
                                                            class="file-name fw-normal text-decoration-none">{{
                                                            identity_proof }}</a>
                                                        <i @click="changeEditMode" class="ri-pencil-line p-1"></i>
                                                    </div>
                                                    <div v-else class="document_picker">
                                                        <input type="file" @change="changeIdentity" ref="identityFile"
                                                            class="custom_input ps-1 tag-input" />
                                                        <i @click="changeEditMode" class="ri-arrow-go-back-line p-1"></i>
                                                    </div>
                                            </div>
                                                
                                            </div>
                                        </div>
                                    </div>


                                    <!-- Availability Field -->
                                    <div class="mb-4">
                                        <label class="form-label text-muted fw-semibold mb-2"
                                            for="availability">Availability</label>
                                        <div class="position-relative">
                                            <i
                                                class="ri-time-line custom_icon position-absolute top-50 start-0 translate-middle-y ms-3 text-muted"></i>
                                            <select class="form-select ps-5 custom_select" v-model="availability"
                                                name="availability" required>
                                                <option selected disabled>Select your availability</option>
                                                <option value="Full Time"> Full Time</option>
                                                <option value="Part Time"> Part Time</option>
                                            </select>
                                        </div>
                                        <div v-if="fieldErrors.availability" class="text-danger mt-1">{{
                                            fieldErrors.availability }}</div>
                                    </div>

                                    <!-- Experience Field -->
                                    <div class="mb-4">
                                        <label class="form-label text-muted fw-semibold mb-2"
                                            for="experience">Experience
                                            (Years)</label>
                                        <div class="position-relative">
                                            <i
                                                class="ri-trophy-line custom_icon position-absolute top-50 start-0 translate-middle-y ms-3 text-muted"></i>
                                            <input v-model="experience" class="form-control custom_input ps-5"
                                                type="number" step="0.1" name="experience" min="0" max="25"
                                                placeholder="Enter your experience" required>
                                        </div>
                                        <div v-if="fieldErrors.experience" class="text-danger mt-1">{{
                                            fieldErrors.experience }}</div>
                                    </div>



                                </div>
                            </div>
                        </div>


                        <div class="col-md-6 col-12">
                            <div class="card-body">

                                <div class="fs-5 text-danger text-center">
                                    {{ errorMsg }}
                                </div>

                                <h4 class="mb-2 mt-4 custom_sub_title">Professional Information </h4>

                                <!-- Description Field -->
                                <div class="mb-4">
                                    <label class="form-label text-muted fw-semibold mb-2"
                                        for="description">Description</label>
                                    <div class="position-relative">
                                        <i
                                            class="ri-information-line custom_icon position-absolute icon_fix_des start-0 translate-middle-y ms-3 text-muted"></i>
                                        <textarea v-model="description" class="form-control custom_input ps-5"
                                            name="description" maxlength="260" rows="2"
                                            placeholder="Describe yourself"></textarea>
                                    </div>
                                    <div v-if="fieldErrors.description" class="text-danger mt-1">{{
                                        fieldErrors.description }}</div>
                                </div>

                                <!-- Category Field -->
                                <div class="mb-4">
                                    <label class="form-label text-muted fw-semibold mb-2"
                                        for="category">Category</label>
                                    <div class="position-relative">
                                        <i
                                            class="ri-briefcase-line custom_icon position-absolute top-50 start-0 translate-middle-y ms-3 text-muted"></i>
                                        <select class="form-select ps-5 custom_select" v-model="category"
                                            name="category" required @change="fetchServices($event.target.value)">
                                            <option v-for="category in categories" :key="category" :value="category">
                                                {{ category }}
                                            </option>
                                        </select>
                                    </div>
                                    <div v-if="fieldErrors.category" class="text-danger mt-1">{{
                                        fieldErrors.category }}</div>
                                </div>


                                <!-- Service Type Field -->
                                <div class="mb-4">
                                    <label class="form-label text-muted fw-semibold mb-2" for="service_type">Service
                                        Type</label>
                                    <div class="position-relative">
                                        <i
                                            class="ri-briefcase-line custom_icon position-absolute top-50 start-0 translate-middle-y ms-3 text-muted"></i>
                                        <select class="form-select ps-5 custom_select" v-model="service_type"
                                            name="service_type" required>
                                            <option selected disabled>Select your service type</option>
                                            <option v-for="service in services" :key="service" :value="service">
                                                {{ service }}
                                            </option>
                                        </select>
                                    </div>
                                    <div v-if="fieldErrors.service_type" class="text-danger mt-1">{{
                                        fieldErrors['service type'] }}</div>
                                </div>



                                <!-- Service Fee -->
                                <div class="mb-4">
                                    <label class="form-label text-muted fw-semibold mb-2" for="fee">Service Fee
                                        (Per Hour)</label>
                                    <div class="position-relative">
                                        <i
                                            class="ri-money-rupee-circle-line custom_icon position-absolute top-50 start-0 translate-middle-y ms-3 text-muted"></i>
                                        <input v-model="fee" class="form-control custom_input ps-5" type="number"
                                            step="0.1" name="fee" :min="service_fee" max="99999999.99"
                                            :placeholder="`Enter your service fee higher than ${parseInt(service_fee)}`"
                                            required>
                                    </div>
                                    <div v-if="fieldErrors.fee" class="text-danger mt-1">{{ fieldErrors['service fee']
                                        }}</div>
                                </div>

                                <!-- Serviceable Pincodes -->
                                <div class="mb-4">
                                    <label class="form-label text-muted fw-semibold mb-2"
                                        for="serviceable_pincodes">Serviceable
                                        Pincodes</label>
                                    <div class="tag-input-container position-relative">
                                        <i class="ri-map-pin-line custom_icon p-2 top-50"></i>
                                        <span v-for="(pincode, index) in pincodes" :key="index" class="pincode-tag">
                                            {{ pincode }}
                                            <div @click="removePincode(index)" class="remove-tag-btn">x</div>
                                        </span>
                                        <input type="text" v-model="pincodeInput" @keyup.enter="addPincode"
                                            @keydown.backspace="removeLastPincode" class="custom_input ps-1 tag-input"
                                            placeholder="Enter 6-digit pincode and press enter" />
                                    </div>
                                    <div v-if="error" class="text-danger mt-2">
                                        {{ error }}
                                    </div>
                                </div>

                                <div class="mt-2">
                                    <button type="submit" class="btn btn-primary submit_btn">Submit </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </form>
                <Popup :isOpen="isModalOpen" title="Remove Picture Confirmation" @close="isModalOpen=false" :showConfirm="true" confirmButton="red" buttonName="Yes,
                                    Remove" :myfunction="deletePicture">
                                        <p>Are you sure you want to remove your profile picture? This action is
                                            permanent
                                            and cannot be undone. Please confirm to proceed.</p>
                                    </Popup>
            </div>
        </div>
    </div>
</template>

<style scoped>
    /*no opption single css */

    .icon_fix_des {
        top: 24.5px;
    }

    .pahele_ifno {
        padding-right: 40px;
    }

    .cus_fix_btn_top {
        margin-left: 43px;
        margin-top: 20px;
    }

    #fix_cus_icon_rat {
        color: rgb(255, 183, 0);
        filter: drop-shadow(1px 1px 1px rgba(28, 28, 28, 0.174));
    }

    /* end option */

    .my_profile_title {
        margin-top: 23px;
        font-weight: 700;
        color: #453685;
    }

    .custom_sub_title {
        border-top: 1px solid rgba(150, 185, 181, 0.132);
        padding-top: 10px;
    }

    .document_picker {
        display: flex; 
        width: 100%; 
        justify-content: 
        space-between; 
        align-items: center;
    }


    .banner {
        width: 100%;
        height: 25vh;
        overflow: hidden;
    }

    .banner_img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }



    .profile img {
        border-radius: 20px;
        height: auto;
        max-width: 100%;
    }

    .profile .main {
        margin-left: 20px;
        margin-top: -111px;
    }

    .profile .main .profile-picture {
        height: 220px;
        border-radius: 50%;
        border: 10px solid white;
        background-color: rgb(149, 150, 151);
    }

    .username-title {
        font-size: 33px;
        font-weight: 700;
        color: white;
    }

    .custom_text {
        color: rgba(100, 120, 155, 0.829);
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

    .remove-pic {
        color: rgb(39, 39, 39);
        font-weight: 700;
        border-color: rgba(28, 28, 28, 0.133);
        background-color: rgba(227, 24, 24, 0.707);
    }

    .remove-pic:hover {
        border-color: transparent;
        color: white;
        background-color: rgb(208, 24, 0);
    }

    .information_display {
        padding: 0 30px;
    }

    .custom_input {
        padding: 10px 33px;
        border: 2px solid #e9eded;
    }

    .custom_icon {
        font-size: 22px;
    }

    .custom_select {
        padding: 10px 33px;

    }

    .submit_btn {
        padding: 8px 40px;
        font-weight: 600;
        font-size: 17px;
        margin-bottom: 20px;
    }

    /*  */
    .tag-input-container {
        display: flex;
        align-items: center;
        flex-wrap: wrap;
        border: 1px solid rgb(228, 230, 232);
        border-radius: 4px;
        transition: all ease .3s;
        background-color: white;
        outline: none;
        flex: 1;
        min-width: 100px;
    }

    .pincode-tag {
        background-color: #e0e0e0;
        color: #333;
        padding: 5px;
        border-radius: 20px;
        display: flex;
        align-items: center;
        margin-right: 5px;
        margin-bottom: 5px;
    }

    .remove-tag-btn {
        background: none;
        border: none;
        color: #ff5b5b;
        cursor: pointer;
        font-size: 12px;
        font-weight: bold;
        margin-left: 5px;
    }

    .tag-input {
        border: none;
        outline: none;
        flex: 1;
        min-width: 100px;
        padding: 5px;
    }

    .tag-input-container:focus-within {
        box-shadow: 0px 0 0px 4px rgb(199, 207, 250);
    }

    .verification_status {
        border: 2px solid rgb(149, 150, 151);
        border-radius: 14px;
        width: 560px;
        padding: 14px 14px 10px;
        background-color: rgb(109, 74, 255, 0.1);
        color: rgb(109, 74, 255);
        border: 1px solid #c1bdc22e;
        display: inline-flex;
        justify-content: center;
        align-items: center;
        font-weight: bold;
        box-shadow: 0 0.5rem 1rem rgb(0 0 0 / 7%);
        margin: 120px 50px 0px 0px;
    }

    .cus-badge {
        border: 2px solid rgb(149, 150, 151);
        border-radius: 8px;
        background-color: darkblue;
        padding: 3px 10px;
        color: white;
    }
</style>