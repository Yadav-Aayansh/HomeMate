<script setup>
</script>

<template>
    <div class="loader-div">
        <div class="loader">
            <div></div>
        </div>
    </div>
</template>

<style scoped>
    @keyframes loader {
        0% {
            transform: translate(-50%, -50%) rotate(0deg);
        }
        100% {
            transform: translate(-50%, -50%) rotate(360deg);
        }
    }

    .loader div {
        position: absolute;
        width: 66px;
        height: 66px;
        border: 10px solid #6d4aff;
        border-top-color: transparent;
        border-radius: 50%;
        animation: loader 0.5025125628140703s linear infinite;
    }

    
    .loader-div {
        display: flex;
        justify-content: center; 
        align-items: center;
        height: 100vh; 
        width: 100vw;
        position: fixed; 
        top: 0;
        left: 0;
        background: rgba(255, 255, 255, 0.8); 
        z-index: 9999; 
    }

    .loader {
        position: relative;
        transform: translateZ(0) scale(1);
        backface-visibility: hidden;
        transform-origin: 0 0;
    }

    .loader div {
        box-sizing: content-box;
    }
</style>
