<template>
  <h1>영화 추천</h1>
</template>

<script setup>
import axios from 'axios'
import { onMounted,ref } from 'vue'

const movielist = ref([])

// const fetchData = function(){
//     return axios({
//       method:'get',
//       url:`http://127.0.0.1:8000/movies/recommended/`,
//     })
//     .then((response) => {
//       movielist.value = response.data
//     })
//     .catch((error) => {
//       console.log(error)
//     })
//   }
// onMounted(
//   fetchData()
// )
</script>


<style scoped>

</style>
