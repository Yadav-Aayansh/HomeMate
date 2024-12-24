<script setup>
    import { ref, watch, inject } from 'vue';
    import Popup from '@/components/Popup.vue';
    import { getCookie } from '@/utils.js'

    const apiUrl = import.meta.env.VITE_API_URL
    const updateTitle = inject('updateTitle')
    updateTitle('Available Services')

    const selectedCate = ref('Assembly')
    const services = ref([])
    const fetchServices = async (category) => {
        selectedCate.value = category
        const response = await fetch(`${apiUrl}/services?category=${category}`, {
            method: "GET",
            credentials: 'include'
        })
        services.value = await response.json()
    }

    fetchServices('Assembly')

    watch(selectedCate, (newValue => fetchServices(newValue)))

    // Add New Service
    const addNew = ref({'name': '', 'category': '', 'base_price': '', 'time_required': '', 'description': ''})
    const isAddOpen = ref(false)

    const addService = async () => {
        console.log(addNew)
        const response = await fetch(`${apiUrl}/services`, {
            method: 'POST',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRF-TOKEN': getCookie('csrf_access_token')
            },
            body: JSON.stringify(addNew.value)
        })
        const data = await response.json()
        if (response.ok) {
            isAddOpen.value = false
            fetchServices(selectedCate.value)
        }
    }

    // Edit Service
    const isEditOpen = ref(false)
    const editService = ref('')
    const selectEdit = (service) => {
        editService.value = service
        isEditOpen.value = true
    }

    const update = async () => {
        const response = await fetch(`${apiUrl}/services/${editService.value.service_id}`, {
            method: 'PUT',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRF-TOKEN': getCookie('csrf_access_token')
            },
            body: JSON.stringify(editService.value)
        })
        const data = await response.json()
        if (response.ok) {
            isEditOpen.value = false
            fetchServices(selectedCate.value)
        }
    }

    // Delete Service
    const isDeleteOpen = ref(false)
    const deleteService = ref('')
    const selectDelete = (service) => {
        deleteService.value = service
        isDeleteOpen.value = true
    }

    const delete_Service = async () => {
        const response = await fetch(`${apiUrl}/services/${deleteService.value.service_id}`, {
            method: 'DELETE',
            credentials: 'include',
            headers: {
                'X-CSRF-TOKEN': getCookie('csrf_access_token')
            },
        })
        const data = await response.json()
        if (response.ok) {
            isDeleteOpen.value = false
            fetchServices(selectedCate.value)
        }
    }

</script>


<template>
    <div class="container hola">
        <div class="category-filter">
            <select v-model="selectedCate" class="form-select">
                <option value="Assembly">Assembly</option>
                <option value="Mounting">Mounting</option>
                <option value="Moving">Moving</option>
                <option value="Cleaning">Cleaning</option>
                <option value="Outdoor Help">Outdoor Help</option>
                <option value="Home Repairs">Home Repairs</option>
                <option value="Painting">Painting</option>
            </select>
            <div class="mt-4">
                <button class="edit_btn btn btn-md me-2" @click="isAddOpen=true"><i class="ri-add-circle-line me-2"></i>Add Service</button>
            </div>
        </div>


    </div>
    <div id="service-list" class="row d-flex justify-content-center">
        <div v-for="service in services" :key="service.id" class="col-md-4 mb-4 service-card"
            :data-category="service.category">
            <h5>{{ service.name }}</h5>
            <p class="details"><strong>Price:</strong> ₹{{ service.base_price }} | <strong>Time:</strong> {{
                service.time_required}}</p>
            <p> {{service.description}}</p>
            <div class="service-buttons mt-3 mb-3">
                <button class="edit_btn btn btn-md me-2" @click="selectEdit(service)">Edit <i
                        class="ri-edit-circle-line"></i> </button>
                <button class="btn btn-md delete_btn" @click="selectDelete(service)">Delete <i class="ri-delete-bin-3-line p-1"></i> </button>
            </div>
            <div class="service-card-footer">
                <span class="badge">{{ service.category }}</span>
                <span>Updated on: {{ service.updated_at.split('T')[0] }}</span>
            </div>
        </div>
    </div>

    <!-- Popup Add Modal -->
    <Popup :isOpen="isAddOpen" title="Add New Service" @close="isAddOpen=false" :showConfirm="true" confirmButton="green"
        buttonName="Add Service" :myfunction="addService">
        <form>
            <div class="mb-3">
                <label class="form-label fw-bold">Service Name</label>
                <input type="text" class="form-control" v-model="addNew.name" required>
            </div>
            <div class="mb-3">
                <label class="form-label fw-bold">Base Price</label>
                <input type="text" class="form-control" v-model="addNew.base_price" required>
            </div>
            <div class="mb-3">
                <label class="form-label fw-bold">Time Required (In hours/minutes)</label>
                <input type="text" class="form-control" v-model="addNew.time_required" required>
            </div>
            <div class="mb-3">
                <label class="form-label fw-bold">Description</label>
                <input class="form-control" minlength="20" v-model="addNew.description" required>
            </div>
            <div class="mb-3">
                <label class="form-label fw-bold">Category</label>
                <select v-model="addNew.category" class="form-select" required>
                    <option value="Assembly">Assembly</option>
                    <option value="Mounting">Mounting</option>
                    <option value="Moving">Moving</option>
                    <option value="Cleaning">Cleaning</option>
                    <option value="Outdoor Help">Outdoor Help</option>
                    <option value="Home Repairs">Home Repairs</option>
                    <option value="Painting">Painting</option>
                </select>
            </div>
        </form>
    </Popup>

    <!-- Popup Edit Modal -->
    <Popup :isOpen="isEditOpen" title="Edit Service" @close="isEditOpen=false" :showConfirm="true" confirmButton="green"
        buttonName="Update" :myfunction="update">
        <form>
            <div class="mb-3">
                <label class="form-label fw-bold">Service Name</label>
                <input type="text" class="form-control" v-model="editService.name" required>
            </div>
            <div class="mb-3">
                <label class="form-label fw-bold">Base Price</label>
                <input type="text" class="form-control" v-model="editService.base_price" required>
            </div>
            <div class="mb-3">
                <label class="form-label fw-bold">Time Required (In hours/minutes)</label>
                <input type="text" class="form-control" v-model="editService.time_required" required>
            </div>
            <div class="mb-3">
                <label class="form-label fw-bold">Description</label>
                <input class="form-control" minlength="20" v-model="editService.description" required>
            </div>
            <div class="mb-3">
                <label class="form-label fw-bold">Category</label>
                <select v-model="editService.category" class="form-select" required>
                    <option value="Assembly">Assembly</option>
                    <option value="Mounting">Mounting</option>
                    <option value="Moving">Moving</option>
                    <option value="Cleaning">Cleaning</option>
                    <option value="Outdoor Help">Outdoor Help</option>
                    <option value="Home Repairs">Home Repairs</option>
                    <option value="Painting">Painting</option>
                </select>
            </div>
        </form>
    </Popup>

    <!-- Popup Delete Modal -->
    <Popup :isOpen="isDeleteOpen" title="Delete Service" @close="isDeleteOpen=false" :showConfirm="true"
    confirmButton="red" buttonName="Delete" :myfunction="delete_Service">
    <p>Are you sure you want to delete this service? This action cannot be undone.</p>
</Popup>
</template>


<style scoped>
    .hola {
        margin-top: -15px;
    }

    .category-filter {
        text-align: center;
        margin-bottom: 10px;
        display: flex;
        justify-content: space-between;
    }

    .category-filter select {
        width: 25%;
        margin-top: 20px;
        padding: 10px;
    }

    .service-card {
        width: 420px;
        background: #ffffff;
        border-radius: 12px;
        padding: 20px;
        margin: 10px;
        box-shadow: 0 8px 15px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }

    .service-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 25px rgba(0, 0, 0, 0.1);
    }

    .service-card h5 {
        font-size: 1.8rem;
        font-weight: 600;
        color: #007bff;
    }

    .service-card p {
        color: #555;
        font-size: 1rem;
    }

    .service-card .details {
        font-size: 1.1rem;
        color: #6c757d;
        margin-bottom: 10px;
    }

    .service-card-footer {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .edit_btn {
        color: rgb(68, 68, 68);
        font-weight: 700;
        border-color: rgba(42, 42, 42, 0.76);
    }

    .edit_btn:hover {
        color: white;
        background-color: rgba(109, 74, 255, 0.6);
    }

    .delete_btn {
        color: rgb(39, 39, 39);
        font-weight: 700;
        border-color: rgba(28, 28, 28, 0.133);
        background-color: rgba(227, 24, 24, 0.707);
    }

    .delete_btn:hover {
        color: white;
        background-color: rgba(227, 24, 24);
    }

    .badge {
        font-size: 0.85rem;
        padding: 5px 10px;
        border-radius: 15px;
        background-color: #e0e0e0;
        color: #333;
    }

    .category {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-top: 20px;
    }

    .category i {
        font-size: 24px;
        color: #6c757d;
    }

    .category p {
        font-size: 18px;
        font-weight: 600;
        color: #343a40;
    }

    .category p.highlight {
        color: #007bff;
    }
</style>