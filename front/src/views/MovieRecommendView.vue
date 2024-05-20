<template>
  <h1>영화 추천</h1>
  <div v-if="movielist.length">
    <div v-for="movie in movielist" >
      <img :src="getImageUrl(movie.poster_path)" alt="..." @click="goMovieDetail(movie.pk)" />
      <span>{{movie.title}}</span>
    </div>
  </div>
</template>

<script setup>
import axios from 'axios'
import { onMounted,ref } from 'vue'

const movielist = ref([])
const userid = localStorage.getItem('userid')

const fetchData = async()=>{
    return axios({
      method:'get',
      url:`http://127.0.0.1:8000/movies/${userid}/user_filtered_movie`,
    })
    .then((response) => {
      // console.log(response.data)
      movielist.value = response.data
    })
    .catch((error) => {
      console.log(error)
    })
  }

onMounted(async () => {
  await fetchData()
})
</script>


<style scoped>

</style>
