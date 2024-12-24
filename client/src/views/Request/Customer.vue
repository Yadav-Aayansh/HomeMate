<script setup>
    import { ref, inject, watch } from 'vue'
    import { bookingStore } from '@/stores/booking.js'
    import { readableDate, getCookie } from '@/utils.js'
    import Popup from '@/components/Popup.vue'

    const apiUrl = import.meta.env.VITE_API_URL;

    const updateTitle = inject('updateTitle')
    updateTitle('Service Requests')

    const stats = ref('')
    const fetchStats = async () => {
        const response = await fetch(`${apiUrl}/stats?page=services`, {
            method: 'GET',
            credentials: 'include'
        })
        const data = await response.json()
        if (response.ok) {
            stats.value = data
        }
    }

    fetchStats()

    const filter = ref('Requested')
    const service_requests = ref([])
    const fetchRequests = async () => {
        const response = await fetch(`${apiUrl}/service-requests?filter=${filter.value}`, {
            method: 'GET',
            credentials: 'include'
        })
        const data = await response.json()
        if (response.ok) {
            service_requests.value = data
        }
    }

    fetchRequests()

    watch(filter, (newValue) => {
        fetchStats()
        fetchRequests()
    })

    // View
    const isViewOpen = ref(false)
    const selectedRequest = ref(null)
    const openViewModal = (request) => {
        isViewOpen.value = true;
        selectedRequest.value = request;
    }

    // Edit 
    const isEditOpen = ref(false)
    const editRequest = ref(null)
    const openEditModal = (request) => {
        isEditOpen.value = true
        editRequest.value = { ...request }
    }

    const update = async () => {
        const response = await fetch(`${apiUrl}/service-requests/${editRequest.value.service_request_id}`, {
            method: 'PUT',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRF-TOKEN': getCookie('csrf_access_token')
            },
            body: JSON.stringify(editRequest.value)
        })
        const data = await response.json()
        if (response.ok) {
            isEditOpen.value = false
            fetchStats()
            fetchRequests()
        }
    }

    // Cancel
    const isCancelOpen = ref(false)
    const cancelRequest = ref(null)
    const openCancelModal = (request) => {
        isCancelOpen.value = true
        cancelRequest.value = request
    }

    const cancel = async () => {
        cancelRequest.value.status = 'Cancelled'
        const response = await fetch(`${apiUrl}/service-requests/${cancelRequest.value.service_request_id}`, {
            method: 'PUT',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRF-TOKEN': getCookie('csrf_access_token')
            },
            body: JSON.stringify(cancelRequest.value)
        })
        const data = await response.json()
        if (response.ok) {
            isCancelOpen.value = false
            fetchStats()
            fetchRequests()
        } else {
            console.log('failed')
        }
    }

    // Pay Fee
    const isPaymentOpen = ref(false)
    const paymentRequest = ref(null)
    const additional = ref(null)
    const order = ref(null)
    const openPaymentModal = async (request) => {
        const response = await fetch(`${apiUrl}/payment?service_request_id=${request.service_request_id}`)
        const data = await response.json()
        order.value = data.order
        additional.value = data.additional
        isPaymentOpen.value = true
        paymentRequest.value = request

    }

    const payment = async () => {
        const options = {
            key: import.meta.env.VITE_RAZORPAY_CLIENT_ID,
            amount: order.value.amount,
            currency: order.value.currency,
            name: "HomeMate",
            description: "Service Request Fee",
            order_id: order.value.id,
            handler: async (response) => {
                try {
                    const verifyResponse = await fetch(`${apiUrl}/payment`, {
                        method: 'POST',
                        credentials: 'include',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRF-TOKEN': getCookie('csrf_access_token')
                        },
                        body: JSON.stringify({
                            service_request_id: paymentRequest.value.service_request_id,
                            payment_id: response.razorpay_payment_id,
                            order_id: response.razorpay_order_id,
                            signature: response.razorpay_signature,
                        }),
                    });

                    const result = await verifyResponse.json();

                    if (verifyResponse.ok) {
                        isPaymentOpen.value = false
                        fetchStats()
                        fetchRequests()
                    } else {
                        alert('Payment verification failed!');
                    }
                } catch {
                    alert('Verification failed!');
                }
            },
            theme: {
                color: 'rgba(109, 74, 255, 0.2)',
            },
        };

        const rzp1 = new Razorpay(options);
        rzp1.open();
    }


    // Review
    const isReviewOpen = ref(false)
    const reviewRequest = ref(null)

    const openReviewModal = async (request) => {
        isReviewOpen.value = true
        reviewRequest.value = request
        const response = await fetch(`${apiUrl}/review/${reviewRequest.value}`, {
            method: 'GET',
            credentials: 'include',
        })
        const data = await response.json()
        if (response.ok) {
            hoverRatingValue.value = data.rating
            review_text.value = data.review_text
        }
    }

    const hoverRatingValue = ref(0)
    const hoverRating = (value) => {
        hoverRatingValue.value = value
    }
    const rating = ref(0)
    const review_text = ref('')
    const setRating = (value) => {
        rating.value = value
    }

    const submitReview = async () => {
        const response = await fetch(`${apiUrl}/review/${reviewRequest.value}`, {
            method: 'PUT',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRF-TOKEN': getCookie('csrf_access_token')
            },
            body: JSON.stringify({
                'review_text': review_text.value,
                'rating': rating.value
            })
        })
        const data = await response.json()
        if (response.ok) {
            isReviewOpen.value = false
            fetchStats()
            fetchRequests()
        } else {
            console.log('failed')
        }
    }



</script>

<template>
    <div class="cus-card3 p-4">

        <div class="dashboard-summary mb-4">
            <!-- Total Requests -->
            <div class="summary-card">
                <div class="summary-icon bg-primary">
                    <i class="ri-file-list-3-line"></i>
                </div>
                <div class="summary-details">
                    <h5>Total Requests</h5>
                    <p class="summary-number">{{stats.total}}</p>
                    <p class="summary-change"
                  :class="{'text-success': stats.total_progress >= 0, 'text-danger': stats.total_progress < 0}">
                  {{ stats.total_progress }}% from last month
               </p>
                </div>
            </div>

            <!-- In Progress -->
            <div class="summary-card">
                <div class="summary-icon bg-warning">
                    <i class="ri-loader-2-line"></i>
                </div>
                <div class="summary-details">
                    <h5>Pending</h5>
                    <p class="summary-number">{{stats.pending}}</p>
                    <p class="summary-change"
                    :class="{'text-success': stats.pending_progress >= 0, 'text-danger': stats.pending_progress < 0}">
                    {{ stats.pending_progress }}% from last month </p>              
                </div>
            </div>

            <!-- Completed -->
            <div class="summary-card">
                <div class="summary-icon bg-success">
                    <i class="ri-check-line"></i>
                </div>
                <div class="summary-details">
                    <h5>Completed</h5>
                    <p class="summary-number">{{stats.completed}}</p>
                    <p class="summary-change"
                    :class="{'text-success': stats.completed_progress >= 0, 'text-danger': stats.completed_progress < 0}">
                    {{ stats.completed_progress }}% from last month  </p>            
                </div>
            </div>

            <!-- Rejected -->
            <div class="summary-card">
                <div class="summary-icon bg-danger">
                    <i class="ri-close-large-fill"></i>
                </div>
                <div class="summary-details">
                    <h5>Failed</h5>
                    <p class="summary-number">{{stats.failed}}</p>
                    <p class="summary-change"
                    :class="{'text-success': stats.failed_progress >= 0, 'text-danger': stats.failed_progress < 0}">
                    {{ stats.failed_progress }}% from last month </p>               
                </div>
            </div>

        </div>

        <div class="card shadow-sm border-0">
            <div class="card-body p-0">
                <div class="filter-buttons">
                    <div>
                        <label>
                            <input type="radio" name="filter" v-model="filter" value="Requested">
                            <span>Requested</span>
                        </label>
                    </div>
                    <div>
                        <label>
                            <input type="radio" name="filter" v-model="filter" value="In Progress">
                            <span>In Progress</span>
                        </label>
                    </div>
                    <div>
                        <label>
                            <input type="radio" name="filter" v-model="filter" value="Completed">
                            <span>Completed</span>
                        </label>
                    </div>
                    <div>
                        <label>
                            <input type="radio" name="filter" v-model="filter" value="Rejected">
                            <span>Rejected</span>
                        </label>
                    </div>
                    <div>
                        <label>
                            <input type="radio" name="filter" v-model="filter" value="Cancelled">
                            <span>Cancelled</span>
                        </label>
                    </div>
                </div>
                <table class="table table-striped text-center table-bordered table-hover align-middle mb-0">
                    <thead class="table-light">
                        <tr>
                            <th scope="col">Request ID</th>
                            <th scope="col">Service</th>
                            <th scope="col">Professional</th>
                            <th scope="col">Priority</th>
                            <th scope="col">Request Date</th>
                            <th v-if="filter==='Completed'" scope="col">Completion Date</th>
                            <th scope="col">Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="request in service_requests" :key="request.service_request_id">
                            <th scope="row">#{{ request.service_request_id }}</th>
                            <td>{{ request.service }}</td>
                            <td>{{ request.service_professional }}</td>
                            <td><span class="badge bg-primary">{{ request.priority }}</span></td>
                            <td>{{ readableDate(request.request_date) }}</td>
                            <td v-if="filter==='Completed'">
                                <span v-if="request.completion_date">{{ readableDate(request.completion_date) }}</span>
                                <span v-else>N/A</span>
                            </td>
                            <td>
                                <button class="btn book_now_btn btn-sm me-2" @click="openViewModal(request)"><i class="ri-eye-line me-1"></i>View</button>
                                <button v-if="filter==='Requested'" @click="openEditModal(request)"
                                    class="btn accept_btn btn-sm me-2"><i class="ri-edit-circle-line me-1"></i>Edit</button>
                                <button v-if="filter==='Requested'" @click="openCancelModal(request)"
                                    class="btn ban_btn btn-sm me-2"><i class="ri-close-large-line me-1"></i>Cancel</button>

                                <button v-if="filter==='In Progress' & !request.payment_status" @click="openPaymentModal(request)"
                                    class="btn ban_btn btn-sm me-2"><i class="ri-money-rupee-circle-line me-1"></i>Pay</button>
                                <button v-if="filter==='In Progress' & request.payment_status"
                                class="btn accept_btn btn-sm me-2"><i class="ri-check-double-line me-1"></i>Paid</button>

                                <button v-if="filter==='Completed'" @click="openReviewModal(request.service_request_id)"
                                    class="btn accept_btn btn-sm me-2"><i class="ri-edit-circle-line me-1"></i>Review</button>
        
                            </td>
                        </tr>
                        <tr v-if="!service_requests.length">
                            <td colspan="8" class="text-center py-3 text-muted">No service requests found</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>

        <!-- Popup View Modal -->
        <Popup :isOpen="isViewOpen" title="Request Details" @close="isViewOpen=false">
            <div v-if="selectedRequest">
                <p><strong>Request ID:</strong> #{{ selectedRequest.service_request_id }}</p>
                <p><strong>Service:</strong> {{ selectedRequest.service }}</p>
                <p><strong>Service Professional:</strong> {{ selectedRequest.service_professional }}</p>
                <p><strong>Priority:</strong> <span> {{ selectedRequest.priority }}</span></p>
                <p><strong>Payment Status:</strong>
                    <span v-if="selectedRequest.payment_status"> Paid</span>
                    <span v-else > Unpaid</span>
                </p>
                <p><strong>Status:</strong> {{ selectedRequest.status }}</p>
                <p><strong>Request Date:</strong> {{ readableDate(selectedRequest.request_date) }}</p>
                <p><strong>Address:</strong> {{ selectedRequest.address }}</p>
                <p><strong>Pincode:</strong> {{ selectedRequest.pincode }}</p>
                <p v-if="selectedRequest.remarks"><strong>Remarks:</strong> {{ selectedRequest.remarks }}</p>
                <p v-if="!selectedRequest.remarks"><strong>Remarks:</strong> N/A</p>

                <p v-if="selectedRequest.completion_date"><strong>Completion Date:</strong> {{
                    readableDate(selectedRequest.completion_date) }}</p>
                <p v-if="!selectedRequest.completion_date"><strong>Completion Date:</strong> N/A</p>
            </div>
        </Popup>

        <!-- Popup Edit Modal -->
        <Popup :isOpen="isEditOpen" title="Edit Request Details" @close="isEditOpen=false" :showConfirm="true"
            confirmButton="green" buttonName="Update" :myfunction="update">
            <form>
                <div class="mb-3">
                    <label class="form-label fw-bold">Selected Service</label>
                    <input type="text" class="form-control" :value="editRequest.service" readonly>
                </div>
                <div class="mb-3">
                    <label class="form-label fw-bold">Selected Professional</label>
                    <input type="text" class="form-control" :value="editRequest.service_professional" readonly>
                </div>
                <div class="mb-3">
                    <label class="form-label fw-bold">Priority</label>
                    <select class="form-select" v-model="editRequest.priority">
                        <option>Medium</option>
                        <option>High</option>
                        <option>Low</option>
                    </select>
                </div>
                <div class="mb-3">
                    <label class="form-label fw-bold">Address</label>
                    <textarea class="form-control" rows="2" placeholder="Enter your address"
                        v-model="editRequest.address"></textarea>
                </div>
                <div class="mb-3">
                    <label class="form-label fw-bold">Pincode</label>
                    <input type="text" class="form-control" placeholder="Enter pincode" v-model="editRequest.pincode">
                </div>
                <div class="mb-3">
                    <label class="form-label fw-bold">Remarks</label>
                    <textarea class="form-control" rows="2" placeholder="Additional details (optional)"
                        v-model="editRequest.remarks"></textarea>
                </div>
            </form>
        </Popup>

        <!-- Popup Cancel Modal -->
        <Popup :isOpen="isCancelOpen" title="Cancel Request" @close="isCancelOpen=false" :showConfirm="true"
            confirmButton="red" buttonName="Cancel" :myfunction="cancel">
            <label class="form-label">Please let us know why you're cancelling.</label>
            <textarea class="form-control" rows="3" placeholder="Provide a reason (optional)"
                v-model="cancelRequest.cancellation_reason"></textarea>
        </Popup>

        <!-- Popup Payment Modal -->
        <Popup :isOpen="isPaymentOpen" title="Final Payment Review" @close="isPaymentOpen=false" :showConfirm="true"
            confirmButton="green" buttonName="Pay Now" :myfunction="payment">
            <div v-if="paymentRequest">
                <p><strong>Request ID:</strong> {{ paymentRequest.service_request_id }}</p>
                <p><strong>Service Provided:</strong> {{ paymentRequest.service }}</p>
                <p><strong>Service Professional:</strong> {{ paymentRequest.service_professional }}</p>
                <p><strong>Time Required:</strong> {{ additional.time_required }}</p>
                <p><strong>Professional Fee:</strong> ₹{{ additional.fee }}</p>
                <p><strong>Total Cost:</strong> ₹{{ additional.total }}</p>
            </div>
        </Popup>

        <!-- Popup Review Modal -->
        <Popup :isOpen="isReviewOpen" title="Submit Review" @close="isReviewOpen=false" :showConfirm="true"
        confirmButton="green" buttonName="Submit" :myfunction="submitReview">
        <label class="form-label">Please share your feedback about this request.</label>
        <textarea class="form-control" rows="3" placeholder="Write your review here (optional)" 
            v-model="review_text"></textarea>

        <label class="form-label mt-3">Rate this request:</label>
        <div class="rating-container">
            <span 
                v-for="star in 5" :key="star" @click="setRating(star)" @mouseover="hoverRating(star)" class="star":class="{ filled: star <= reviewRequest.rating, hover: star <= hoverRatingValue }">&#9733;
            </span>
        </div>
        </Popup>



    </div>
</template>

<style scoped>
    .dashboard-container {
        max-width: 1200px;
        margin: 0 auto;
    }

    .dashboard-summary {
        display: flex;
        gap: 20px;
        flex-wrap: wrap;
        justify-content: space-between;
    }

    .summary-card {
        width: 23%;
        border-radius: 12px;
        background: #fff;
        box-shadow: 0 6px 18px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease-in-out;
        padding: 20px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        cursor: pointer;
    }

    .summary-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
    }

    /* Icon Circle Style */
    .summary-icon {
        width: 60px;
        height: 60px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 30px;
        color: #fff;
        transition: background-color 0.3s ease;
    }

    .filter-buttons {
        display: flex;
        gap: 15px;
        border-radius: 7px;
        flex-direction: row;
        padding: 5px 10px;
        align-items: center;
    }

    .filter-buttons label {
        display: flex;
        align-items: center;
        cursor: pointer;
    }

    .filter-buttons input[type="radio"] {
        display: none;
    }

    .filter-buttons span {
        font-size: 16px;
        color: #333;
    }

    .filter-buttons input[type="radio"]:checked+span {
        font-weight: bold;
        color: rgb(109, 74, 255);
        background-color: white;
        padding: 3px 5px;
        border-radius: 7px;
    }

    .table-hover tbody tr:hover {
        background-color: #f1f5f9;
    }

    .table thead th {
        font-weight: bold;
        font-size: 0.9rem;
        color: #666;
    }

    .badge {
        font-size: 0.8rem;
        padding: 4px 8px;
        border-radius: 8px;
    }

    .btn-outline-secondary {
        border: none;
        background-color: #e7e9ec;
        color: #555;
    }

    .summary-details {
        margin-left: 20px;
        flex: 1;
    }

    .summary-details h5 {
        margin: 0;
        font-weight: 500;
        font-size: 1.2rem;
        color: #333;
    }

    .summary-number {
        font-size: 1.5rem;
        font-weight: 700;
        color: #1a2d4f;
    }

    .summary-change {
        font-size: 1rem;
        margin-top: 5px;
    }
    .book_now_btn {
        color: rgb(68, 68, 68);
        font-weight: 700;
        border-color: rgba(42, 42, 42, 0.76);
    }

    .book_now_btn:hover {
        color: white;
        background-color: rgba(109, 74, 255, 0.6);
    }
    .accept_btn {
        color: white;
        font-weight: 700;
        border-color: rgba(42, 42, 42, 0.76);
        background-color: rgba(81, 162, 124, 0.8);
    }

    .accept_btn:hover {
        color: black;
        background-color: rgba(113, 172, 144, 0.8)
    }

    .ban_btn {
        color: rgb(68, 68, 68);
        font-weight: 700;
        border-color: rgba(42, 42, 42, 0.76);
        background-color: rgba(227, 24, 24, 0.707);
    }

    .ban_btn:hover {
        color: white;
        background-color: rgba(227, 24, 24, 0.707);
    }
    .rating-container {
        display: flex;
        gap: 0.5rem;
        justify-content: center;
    }

    .star {
        font-size: 2rem;
        cursor: pointer;
        transition: transform 0.2s ease, color 0.2s ease;
        color: #d3d3d3; 
    }

    .star.filled {
        color: #8f07ff; 
    }

    .star.hover {
        color: #d380ff; 
    }

    .star:hover {
        transform: scale(1.2);
    }

    .rating-container:hover .star {
        transform: scale(1);
        opacity: 0.7;
    }

    .rating-container .star:hover {
        opacity: 1;
    }

</style>