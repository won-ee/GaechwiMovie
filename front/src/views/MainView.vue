<template>
  <div id="m"></div>
  <p>favorite movie</p>
  <div>
    <div class="row row-cols-2 row-cols-md-3 g-4" v-if="movielist.length">
      <MovieCard
        v-for="movie in movielist"
        :key="movie.id"
        :movie="movie"
      />
    </div>
  </div>

  <p>least favorite movie</p>
  <p>favorite actor</p>
  <p>least favorite actor</p>

</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useMovieStore } from '@/stores/counter'
import MovieCard from '@/components/movie/MovieCard.vue'
// import ActorCard from '@/components/actor/ActorCard.vue'


const store = useMovieStore()

const movielist = ref([])
// console.log(movielist);
onMounted(async () => {
  await store.getMovies() 
  movielist.value = store.MovieList
})
</script>

<style scoped>
</style>
