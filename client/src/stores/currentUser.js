import { defineStore } from "pinia";

export const currentUserStore = defineStore('currentUser', {
    state: () => ({
        role: '',
        username: '',
        email: '',
        pincode: ''
    }),

    actions: {
        updateRole(role) {
            this.role = role
        },
        updateUsername(username) {
            this.username = username
        },
        updateEmail(email) {
            this.email = email
        },
        updatePincode(pincode) {
            this.pincode = pincode
        }
    }
})