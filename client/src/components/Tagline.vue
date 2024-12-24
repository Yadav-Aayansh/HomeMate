<script setup>
    import { computed } from 'vue';
    import { signupStore } from '@/stores/signup.js';
    import logo from '@/assets/logo.png';
    
    const signup_Store = signupStore();
    const role = computed(() => signup_Store.role);
    </script>
    
    <template>
            <!-- <div class="text-left">
                <img src="../assets/home.png" alt="HomeMate Logo" width="100%">
                <div class="d-flex justify-content-center align-items-center mb-4">
                    <img :src="logo" alt="HomeMate Logo" class="logo me-2">
                    <h2 class="title mt-2 kg-text">HomeMate</h2>
                </div>
                <h2 class="text-center mb-5">Welcome to HomeMate!</h2>
        
                <div v-if="role === 'Customer'">
                    <div class="feature mb-4">
                        <h4 class="feature-title text-center">
                            <i class="bi bi-phone"></i> Effortless Service Booking
                        </h4>
                        <p class="text-center">Unlock the convenience of booking home services with just a few taps—anytime, anywhere.</p>
                    </div>
                    <div class="feature mb-4">
                        <h4 class="feature-title text-center">
                            <i class="bi bi-check-circle"></i> Quality You Can Trust
                        </h4>
                        <p class="text-center">Choose from a network of thoroughly vetted professionals, ensuring you receive top-notch service every time.</p>
                    </div>
                    <div class="feature mb-4">
                        <h4 class="feature-title text-center">
                            <i class="bi bi-arrow-clockwise"></i> Stay in the Loop
                        </h4>
                        <p class="text-center">Get real-time updates on your service status and communicate directly with your provider for a seamless experience.</p>
                    </div>
                    <div class="feature mb-4">
                        <h4 class="feature-title text-center">
                            <i class="bi bi-pencil"></i> Your Feedback Matters
                        </h4>
                        <p class="text-center">Rate your experience and help us maintain excellence. Your voice shapes our community!</p>
                    </div>
                </div>
        
                <div v-else>
                    <div class="feature mb-4">
                        <h4 class="feature-title text-center">
                            <i class="bi bi-handshake"></i> Join a Growing Marketplace
                        </h4>
                        <p class="text-center">Connect with a steady stream of clients eager for your expertise—grow your business effortlessly.</p>
                    </div>
                    <div class="feature mb-4">
                        <h4 class="feature-title text-center">
                            <i class="bi bi-calendar"></i> Own Your Schedule
                        </h4>
                        <p class="text-center">Flexibility at its best! Choose the jobs that fit your skills and availability for a perfect work-life balance.</p>
                    </div>
                    <div class="feature mb-4">
                        <h4 class="feature-title text-center">
                            <i class="bi bi-cash"></i> Earn Fairly, Work Smart
                        </h4>
                        <p class="text-center">Competitive compensation for your hard work, with prompt payments that reward your efforts without delay.</p>
                    </div>
                    <div class="feature mb-4">
                        <h4 class="feature-title text-center">
                            <i class="bi bi-star"></i> Build Your Reputation
                        </h4>
                        <p class="text-center">Shine through customer feedback! Your profile gets stronger with every positive review you earn.</p>
                    </div>
                </div>
            </div> -->
    </template>
    
    <style scoped>
    .cus-stuff {
        padding: 20px;
        /* background: linear-gradient(315deg, rgba(255, 222, 233, 0.2) 0%, rgba(181, 255, 252, 0.2) 100%);
        border-radius: 30px; 
        border: 10px solid white; 
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1); 
        position: relative; */

    }
    
    .logo {
        max-width: 90px;
    }
    
    .feature {
        padding: 15px;
        border: 1px solid rgba(0, 0, 0, 0.1); /* Added border for visual separation */
        border-radius: 8px; /* Rounded corners for a modern look */
        background-color: white; /* White background for contrast */
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1); /* Soft shadow for depth */
    }
    
    .feature-title {
        font-weight: bold;
        font-size: 1.25em; /* Increased font size for better readability */
    }

    </style>
    