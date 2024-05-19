<template id ="app">
  <div>
    <NavBar></NavBar>
  </div>
 
  <div>
    <RouterView/>
  </div>
  
</template>

<script setup>
import NavBar from '@/components/nav/NavBar.vue';

import {RouterView} from 'vue-router'
</script>

<style scoped>
.app-container {
  position: relative;
}

.navbar {
  position: relative;
  z-index: 2; /* Ensure NavBar is above RouterView */
}

.router-view-container {
  margin-top: 60px; /* Adjust this value according to the height of your NavBar */
  z-index: 1;
}

</style>
