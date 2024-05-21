<template>
  <h1>영화 추천</h1>
  <div v-if="movielist.length">
    <div v-for="movie in movielist" >
      <img :src="getImageUrl(movie.poster_image)" alt="..." @click="goMovieDetail(movie.pk)" />
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
      url:`http://127.0.0.1:8000/movies/${userid}/recommended/`,
    })
    .then((response) => {
      console.log(response.data)
      movielist.value = response.data
    })
    .catch((error) => {
      console.log(error)
    })
  }
  
  const getImageUrl = (path) => {
  if (!path) {
    return
  }
  return `https://image.tmdb.org/t/p/original/${path}`
}
onMounted(async () => {
  await fetchData()
})
</script>


<style scoped>
img{
  width: 200px;
}
</style>
