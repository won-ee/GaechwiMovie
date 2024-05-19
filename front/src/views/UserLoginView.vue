<template>
  <div class="wrapper">
    <UserLogin />
  </div>
</template>

<script setup>
import UserLogin from '@/components/user/UserLogin.vue'
</script>

<style scoped>
.wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background: -webkit-linear-gradient(to right, #272727, #000000);
  background: linear-gradient(to right, #202020, #000000);
}
</style>
