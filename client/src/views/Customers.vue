<script setup>
    import { ref, inject } from 'vue';
    import Popup from '@/components/Popup.vue'
    import { getCookie } from '@/utils.js'

    const updateTitle = inject('updateTitle');
    updateTitle('Customers');

    const apiUrl = import.meta.env.VITE_API_URL

    const name = ref('');
    const is_ban = ref('');
    const customers = ref([])

    const updateCustomers = async () => {
        const query = `name=${name.value}&is_ban=${is_ban.value}`
        const response = await fetch(`${apiUrl}/customers?${query}`, {
            method: 'GET',
            credentials: 'include'
        })
        const data = await response.json()
        if (response.ok) {
            customers.value = data.customers
        }
    }

    updateCustomers()

    // View
    const isViewOpen = ref(false)
    const selectedCustomer = ref(null)
    const openViewModal = (customer) => {
        isViewOpen.value = true;
        selectedCustomer.value = customer;
    }

    // Action
    const isActionOpen = ref(false)
    const actionCustomer = ref(null)
    const openActionModal = (customer_id) => {
        isActionOpen.value = true
        actionCustomer.value = customer_id
    }

    const action = async () => {
        const response = await fetch(`${apiUrl}/customers/${actionCustomer.value}`, {
            method: 'PUT',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRF-TOKEN': getCookie('csrf_access_token')
            },
        })
        const data = await response.json()
        if (response.ok) {
            isActionOpen.value = false
            updateCustomers()
        } else {
            console.log('failed')
        }
    }

</script>

<template>
    <div class="cus-card">
        <div class="card hole shadow-sm border-0">
            <div class="card-body p-0">
                <div class="row mt-3 mb-2 mx-2">
                    <div class="col-auto">
                        <i class="ri-filter-3-line text-primary fs-3"></i>
                    </div>
                    <div class="col-auto">
                        <input type="search" v-model="name" class="form-control shadow-sm" placeholder="Search by name..." aria-label="Search" />
                    </div>
                    <div class="col-auto">
                        <select v-model="is_ban" class="form-select shadow-sm w-auto">
                            <option value="">Account Status</option>
                            <option value="True">Banned</option>
                            <option value="False">Active</option>
                          </select>
                    </div>
                    <div class="col-auto">
                        <button class="btn book_now_btn" @click="updateCustomers"><i class="ri-send-plane-fill me-1"></i> Apply</button>
                    </div>
                  </div>
                <table class="table table-striped text-center table-bordered table-hover align-middle hole">
                    <thead class="table-success">
                        <tr>
                            <th>ID</th>
                            <th>Name</th>
                            <th>Username</th>
                            <th>Address</th>
                            <th>Pincode</th>
                            <th>Requests</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="customer in customers" :key="customer.id">
                            <td>{{ customer.customer_id }}</td>
                            <td>{{ customer.name }}</td>
                            <td>{{ customer.username }}</td>
                            <td>{{customer.address}}</td>
                            <td>{{customer.pincode}}</td>
                            <td>{{ customer.requests }}</td>
                            <td>
                                <button class="btn book_now_btn btn-sm me-2" @click="openViewModal(customer)"><i
                                        class="ri-eye-line"></i> View</button>
                                <button class="btn ban_btn btn-sm" @click="openActionModal(customer.customer_id)"><i
                                        class="ri-indeterminate-circle-line me-1"></i>{{ customer.is_ban ? 'Unban' : 'Ban'
                                    }}</button>
                            </td>
                        </tr>
                        <tr v-if="!customers.length">
                            <td colspan="8" class="text-center py-3 text-muted">No customer found</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>

    <!-- Popup View Modal -->
    <Popup :isOpen="isViewOpen" title="Customer Details" @close="isViewOpen=false">
        <div v-if="selectedCustomer">
            <p><strong>Customer ID:</strong> #{{ selectedCustomer.customer_id }}</p>
            <p><strong>Name:</strong> {{ selectedCustomer.name }}</p>
            <p><strong>Username:</strong> {{ selectedCustomer.username }}</p>
            <p><strong>Email:</strong> {{ selectedCustomer.email }}</p>
            <p><strong>Requests:</strong> {{ selectedCustomer.requests }}</p>
            <p><strong>Address:</strong> {{ selectedCustomer.address }}</p>
            <p><strong>Pincode:</strong> <span>{{ selectedCustomer.pincode }}</span></p>
            <p><strong>Account Status:</strong> <span>{{ selectedCustomer.is_ban ? 'Banned' : 'Active' }}</span></p>
           
        </div>
    </Popup>

    <!-- Popup Action Modal -->
    <Popup :isOpen="isActionOpen" title="Change Account Status" @close="isActionOpen=false" :showConfirm="true"
    confirmButton="red" buttonName="Yes, Confirm" :myfunction="action">
    <p>Are you sure you want to change this customer's  account status?</p>
</Popup>
</template>

<style scoped>
    .custom-card {
        border: 2px rgb(183, 175, 175) solid;
        border-radius: 10px;
    }
    .hole {
        margin-bottom: 0.7px;
    }
    .table-hover tbody tr:hover {
        background-color: #f1f5f9;
    }

    .table thead th {
        font-weight: bold;
        font-size: 0.9rem;
        color: #666;
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