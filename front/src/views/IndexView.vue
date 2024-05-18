<template>
  <h1><p>{{ keyword }}</p></h1>
  <h3>영화</h3>
  <div v-if="filteredMovies.length">
    <MovieCard v-for="movie in filteredMovies" :key="movie.id" :movie="movie" />
  </div>
  <p v-else>검색 결과가 없습니다.</p>

  <h3>인물</h3>
  <div v-if="filteredMovies.length">
    <MovieCard v-for="movie in filteredMovies" :key="movie.id" :movie="movie" />
  </div>
  <p v-else>검색 결과가 없습니다.</p>

</template>

<script setup>
import { ref, onMounted } from 'vue'
import {useRouter,useRoute} from 'vue-router'
import axios from 'axios'
import MovieCard from '@/components/movie/MovieCard.vue'
import ActorCard from '@/components/actor/ActorCard.vue'

const router=useRouter()
const route = useRoute();
const keyword = ref('');
const movies = ref([])
const filteredMovies = ref([])


const fetchData = function(){
    return axios({
      method:'get',
      url:'http://127.0.0.1:8000/movies/',
    })
    .then((response) => {
      console.log(response);
      movies.value = response.data
      filterMovies()
    })
    .catch((error) => {
      console.log(error)
    })
  }

const filterMovies = () => {
  filteredMovies.value = movies.value.filter(movie => 
  movie.title && movie.title.toLowerCase().includes(keyword.value.toLowerCase())
  )
}



onMounted(() => {
  console.log(route.params.name);
  keyword.value = route.params.name
  fetchData()
})

</script>


<style scoped>

</style>
