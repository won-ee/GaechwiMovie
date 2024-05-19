<template>
  <div  class="wrapper">
    <UserSignUp />
  </div>
</template>

<script setup>
import UserSignUp from '@/components/user/UserSignUp.vue'
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