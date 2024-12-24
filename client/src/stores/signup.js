import { defineStore } from "pinia";

export const signupStore = defineStore('signup',{
    state: () => ({
        role: 'Customer',
        username: '',
        email: '',
        password: '',
        confirm_password: '',
        oauth_user: false,
        name: '',
        platform: '',
        unique_id: '',
    }),

    actions: {
        changeRole(role) {
            this.role = role
        },
        changeUsername(username) {
            this.username = username
        },
        changeEmail(email) {
            this.email = email
        },
        changePassword(password) {
            this.password = password
        },
        changeConfirmPassword(confirm_password) {
            this.confirm_password = confirm_password
        },
        changeOauth() {
            this.oauth_user = !this.oauth_user
        },
        changeName(name) {
            this.name = name
        },
        changePlatform(platform) {
            this.platform = platform
        },
        changeUniqueId(unique_id) {
            this.unique_id = unique_id
        },
    }
})