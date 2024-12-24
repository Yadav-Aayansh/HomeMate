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
    fetchStats()

    watch(filter, (newValue) => {
        fetchRequests()
        fetchStats()
    })

    // View
    const isViewOpen = ref(false)
    const selectedRequest = ref(null)
    const openViewModal = (request) => {
        isViewOpen.value = true;
        selectedRequest.value = request;
    }

    // Cancel
    const isCancelOpen = ref(false)
    const cancelRequest = ref(null)
    const openCancelModal = (request) => {
        isCancelOpen.value = true
        cancelRequest.value = request
    }

    const cancel = async () => {
        const response = await fetch(`${apiUrl}/service-requests/${cancelRequest.value.service_request_id}`, {
            method: 'DELETE',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRF-TOKEN': getCookie('csrf_access_token')
            },
        })
        const data = await response.json()
        if (response.ok) {
            isCancelOpen.value = false
            fetchRequests()
            fetchStats()
        } else {
            console.log('failed')
        }
    }

    const isExport = ref(false)
    const exportCSV = async() => {
        const response = await fetch(`${apiUrl}/tasks`, {
            method: 'GET',
            credentials:'include'
        })
        if (response.ok) {
            isExport.value = true
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
                    <p class="summary-number">{{stats.requests}}</p>
                    <p class="summary-change"
                        :class="{'text-success': stats.requests_progress >= 0, 'text-danger': stats.requests_progress < 0}">
                        {{ stats.requests_progress }}% from last month
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
                        {{ stats.completed_progress }}% from last month </p>
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
                <div class="d-flex justify-content-between align-items-center">
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
                    <div>
                        <button class="btn book_now_btn btn-sm me-2" @click="exportCSV()"> Export CSV</button>
                    </div>
                </div>
                <table class="table table-striped text-center table-bordered table-hover align-middle mb-0">
                    <thead class="table-success">
                        <tr>
                            <th scope="col">Request ID</th>
                            <th scope="col">Service</th>
                            <th scope="col">Customer</th>
                            <th scope="col">Professional</th>
                            <th scope="col">Priority</th>
                            <th v-if="filter==='In Progress'" scope="col">Payment Status</th>
                            <th scope="col">Request Date</th>
                            <th v-if="filter==='Completed'" scope="col">Completion Date</th>
                            <th scope="col">Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="request in service_requests" :key="request.service_request_id">
                            <th scope="row">#{{ request.service_request_id }}</th>
                            <td>{{ request.service }}</td>
                            <td>{{ request.customer }}</td>
                            <td>{{ request.service_professional }}</td>
                            <td><span class="badge bg-primary">{{ request.priority }}</span></td>
                            <td v-if="filter==='In Progress'">
                                <span v-if="request.payment_status" class="badge bg-success">Paid</span>
                                <span v-else class="badge bg-warning">Unpaid</span>
                            </td>
                            <td>{{ readableDate(request.request_date) }}</td>
                            <td v-if="filter==='Completed'">
                                <span v-if="request.completion_date">{{ readableDate(request.completion_date) }}</span>
                                <span v-else>N/A</span>
                            </td>
                            <td>
                                <button class="btn book_now_btn btn-sm me-2" @click="openViewModal(request)"><i
                                        class="ri-eye-line"></i> View</button>
                                <button class="btn ban_btn btn-sm" @click="openCancelModal(request)"><i
                                        class="ri-delete-bin-3-line me-1"></i>Delete</button>
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
                <p><strong>Customer:</strong> {{ selectedRequest.customer }}</p>
                <p><strong>Service Professional:</strong> {{ selectedRequest.service_professional }}</p>
                <p><strong>Priority:</strong> <span>{{ selectedRequest.priority }}</span></p>
                <p><strong>Payment Status:</strong>
                    <span v-if="selectedRequest.payment_status"> Paid</span>
                    <span v-else>Unpaid</span>
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

        <!-- Popup Cancel Modal -->
        <Popup :isOpen="isCancelOpen" title="Delete Request" @close="isCancelOpen=false" :showConfirm="true"
            confirmButton="red" buttonName="Delete" :myfunction="cancel">
            <p>Are you sure you want to delete this request?</p>
        </Popup>

         <!-- Popup Export Modal -->
         <Popup :isOpen="isExport" title="Export as CSV" @close="isExport=false" >
            <p>You will soon receive a notification on your email with the CSV attached.</p>     
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
</style>