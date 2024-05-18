<template>
  <h1><p>{{ keyword }}</p></h1>
  <h3>영화</h3>
  <div class="row row-cols-2 row-cols-md-3 g-4"  v-if="movies.length">
    <MovieCard v-for="movie in movies" :key="movie.id" :movie="movie" />
  </div>
  <p v-else>검색 결과가 없습니다.</p>

  <h3>인물</h3>


</template>

<script setup>
import { ref, onMounted } from 'vue'
import {useRoute} from 'vue-router'
import axios from 'axios'
import MovieCard from '@/components/movie/MovieCard.vue'
// import ActorCard from '@/components/actor/ActorCard.vue'

const route = useRoute();
const keyword = ref('');
const movies = ref([])


const fetchData = function(){
    return axios({
      method:'get',
      url:`http://127.0.0.1:8000/movies/${keyword.value}/`,
    })
    .then((response) => {
      console.log(response);
      movies.value = response.data
    })
    .catch((error) => {
      console.log(error)
    })
  }


onMounted(() => {
  console.log(route.params.name);
  keyword.value = route.params.name
  fetchData()
})

</script>


<style scoped>

</style>
