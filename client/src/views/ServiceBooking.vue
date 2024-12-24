<script setup>
  import { ref, inject } from 'vue';
  import { bookingStore } from '@/stores/booking.js'
  import router from '@/router'

  const apiUrl = import.meta.env.VITE_API_URL
  const staticUrl = import.meta.env.VITE_STATIC_URL

  // New Learning => provide, inject
  const updateTitle = inject('updateTitle')
  updateTitle('Service Booking')

  const professional = ref('{}')
  const description = ref('')
  const time_required = ref('')
  const service_id = ref(null)
  const customer_id = ref(null)
  const priority = ref('Medium')
  const remarks = ref(null)
  const address = ref('')
  const pincode = ref('')
  const booking_store = bookingStore()

  const fetchInfo = async () => {
    const response = await fetch(`${apiUrl}/servicer/${booking_store.servicer_id}`, {
      method: 'GET',
      credentials: 'include'
    })
    const data = await response.json()
    if (response.ok) {
      professional.value = data
    }

    const response2 = await fetch(`${apiUrl}/services?service_type=${booking_store.service_type}`, {
      method: 'GET',
      credentials: 'include'
    })
    const data2 = await response2.json()
    if (response2.ok) {
      description.value = data2['Service Description']
      time_required.value = data2['Service Time Required']
      service_id.value = data2['Service ID']
    }

    const response3 = await fetch(`${apiUrl}/profile`, {
      method: 'GET',
      credentials: 'include'
    })
    const data3 = await response3.json()
    if (response3.ok) {
      address.value = data3.address
      pincode.value = data3.pincode
      customer_id.value = data3.customer_id
    }
  }

  fetchInfo()

  const submitBooking = async() => {
    const booking_details = {
      'service_id': service_id.value,
      'customer_id': customer_id.value,
      'service_professional_id': booking_store.servicer_id,
      'address': address.value,
      'pincode': pincode.value,
      'remarks': remarks.value,
      'priority': priority.value
    }
    const response = await fetch(`${apiUrl}/service-requests`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(booking_details),
      credentials: 'include'
    })
    const data = await response.json()
    if (response.ok) {
      router.push('/dashboard/service-requests')
    }
  }



</script>

<template>
  <section class="container my-5">
    <div class="mb-4">
      <div class="row">
        <!-- Left Side: Professional and Service Details -->
        <div class="col-md-6">
          <div class="d-flex flex-row align-items-start position-relative">

            <!-- Professional and Service Details -->
            <div class="p-3 flex-grow-1 position-relative">
              <div class="card-one p-4 rounded-xl cus-card2 bg-gradient shadow-sm">
                <div class="d-flex align-items-center row">
                  <h3 class="mb-4">Service Professional Info</h3>
                  <div class="col-lg-4">
                    <img :src="`${staticUrl}/profile/photos/${professional.profile_picture}`" alt="User Photo"
                      class="profile-picture">
                  </div>

                  <div class="col-lg-8">
                    <div class="d-flex justify-content-between ">
                      <h3 class="kg-text2">{{professional.name}}</h3>
                      <div class="price-tag text-right fs-5 fw-semibold">₹{{professional.fee}}/Hr</div>
                    </div>
                    <div class="text-muted mb-1">
                      <i class="ri-star-line me-2"></i>
                      <span class="fw-semibold">Rating:</span> <strong>{{professional.rating}}/5</strong>
                    </div>
                    <div class="text-muted mb-1">
                      <i class="ri-trophy-line me-2"></i>
                      <span class="fw-semibold">Experience:</span> <strong>{{professional.experience}} years</strong>
                    </div>
                    <div class="text-muted mb-1">
                      <i class="ri-time-line me-2"></i>
                      <span class="fw-semibold">Availability:</span> <strong>{{professional.availability}}</strong>
                    </div>
                  </div>
                </div>
                <hr class="my-3">
                <div>
                  <h3 class="mb-4">Service Info</h3>
                  <h5 class="fw-bold text-primary">Service Type: {{booking_store.service_type}}</h5>
                  <p class="text-muted">Category: {{booking_store.category}}</p>
                  <p class="mb-1"><span class="fw-semibold">Time Required:</span> {{time_required}}</p>
                  <p class="mb-1"><span class="fw-semibold">Description:</span> {{description}}</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Right Side: Booking Form -->
        <div class="col-md-6">
          <form class="card-one p-4">
            <h4 class="text-center fw-bold mb-4">Book a Service</h4>
            <div class="mb-3">
              <label class="form-label fw-bold">Selected Service</label>
              <input type="text" class="form-control" :value="booking_store.service_type" readonly>
            </div>
            <div class="mb-3">
              <label class="form-label fw-bold">Selected Professional</label>
              <input type="text" class="form-control" :value="professional.name" readonly>
            </div>
            <div class="mb-3">
              <label class="form-label fw-bold">Priority</label>
              <select class="form-select" v-model="priority">
                <option>Medium</option>
                <option>High</option>
                <option>Low</option>
              </select>
            </div>
            <div class="mb-3">
              <label class="form-label fw-bold">Address</label>
              <textarea class="form-control" rows="2" v-model="address" placeholder="Enter your address"></textarea>
            </div>
            <div class="mb-3">
              <label class="form-label fw-bold">Pincode</label>
              <input type="text" class="form-control" v-model="pincode" placeholder="Enter pincode">
            </div>
            <div class="mb-3">
              <label class="form-label fw-bold">Remarks</label>
              <textarea class="form-control" rows="2" v-model="remarks" placeholder="Additional details (optional)"></textarea>
            </div>
            <!-- <div class="mb-3">
              <label class="form-label fw-bold">Payment Options </label>
              <div class="payment-methods">
                <label class="payment-option">
                  <input type="radio" name="payment" value="razorpay" checked>
                  <span class="custom-radio"></span>
                  Pay Online
                </label>
                <label class="payment-option">
                  <input type="radio" name="payment" value="cod">
                  <span class="custom-radio"></span>
                  Cash on Delivery (COD)
                </label>
              </div>
            </div> -->
            <button type="button" @click="submitBooking()" class="btn btn-primary btn-lg w-100 fw-bold">Submit Booking</button>
          </form>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
  .profile-picture {
    height: 11rem;
    border-radius: 50%;
    border: 2px solid rgb(255, 222, 222);
  }

  .price-tag {
    background-color: rgba(0, 128, 0, 0.1);
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

  .payment-methods {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .payment-option {
    position: relative;
    display: flex;
    align-items: center;
    padding: 12px 16px;
    border: 2px solid #e0e0e0;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.3s ease;
  }

  .payment-option:hover {
    border-color: #007bff;
    background-color: #f9f9f9;
  }

  .payment-option input {
    display: none;
  }

  .custom-radio {
    width: 20px;
    height: 20px;
    border: 2px solid #007bff;
    border-radius: 50%;
    margin-right: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.3s ease;
  }

  .payment-option input:checked+.custom-radio {
    background-color: #007bff;
    border-color: #007bff;
  }

  .custom-radio::before {
    content: "";
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background-color: #fff;
    opacity: 0;
    transform: scale(0);
    transition: all 0.3s ease;
  }

  .payment-option input:checked+.custom-radio::before {
    opacity: 1;
    transform: scale(1);
  }

  .payment-option input:checked+.custom-radio+label {
    font-weight: 600;
  }
</style>