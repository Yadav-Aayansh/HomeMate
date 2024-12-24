import { currentUserStore } from "@/stores/currentUser.js"
import { jwtDecode } from "jwt-decode"

const apiUrl = import.meta.env.VITE_API_URL

export async function tokenChecker() {
    const response = await fetch(`${apiUrl}/token-chekcer`, {
        method: 'GET',
        credentials: 'include'
    })
    if (response.status === 200) {
        const data = await response.json()
        const decodedToken = jwtDecode(data.token)

        const currentUser_Store = currentUserStore()
        currentUser_Store.updateRole(decodedToken.role)
        currentUser_Store.updateUsername(decodedToken.sub)
        currentUser_Store.updateEmail(decodedToken.email)
        
        if (decodedToken.role === 'Customer') {
            currentUser_Store.updatePincode(decodedToken.pincode)
        }
        return true;
    } else {
        return false;
    }
}

export function getCookie(name) {
    let cookieArr = document.cookie.split(";");
    for (let cookie of cookieArr) {
        let [key, value] = cookie.split("=");
        if (key && key.trim() === name) {
            return decodeURIComponent(value);
        }
    }
    return null;
}

export function readableDate(date) {
    date = date.split('T')[0]
    const options = { day: 'numeric', month: 'short', year: 'numeric' };
    return new Date(date).toLocaleDateString('en-GB', options);
}
