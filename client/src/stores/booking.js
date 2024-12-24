import { defineStore } from "pinia";

export const bookingStore = defineStore('bookingStore', {
    state: () => ({
        servicer_id: '',
        category: 'Assembly',
        service_type: 'Wardrobe Assembly'

    }),

    actions: {
        updateServicerId(servicer_id) {
            this.servicer_id = servicer_id
        },

        updateCategory(category) {
            this.category = category
        },

        updateServiceType(service_type) {
            this.service_type = service_type
        }


    }

})