<template >
  <div id="m"></div>
  <p>favorite movie</p>
  <span>
    <MovieCard @click="router.push({name:'moviedetail'})"/>
  </span>

  <p>least favorite movie</p>
  <span>
    <MovieCard 
    @click="router.push({name:'moviedetail'})"
    />
  </span>

  <p>favorite actor</p>
  <span>
    <ActorCard
    @click="router.push({name:'actordetail'})" 
    />
  </span>

  <p>least favorite actor</p>
  <span>
    <ActorCard
    @click="router.push({name:'actordetail'})" 
    />
  </span>

</template>

<script setup>

import {useRouter} from 'vue-router'
import { useMovieStore } from '@/stores/counter'
import MovieCard from '@/components/movie/MovieCard.vue'
import ActorCard from '@/components/actor/ActorCard.vue'



const router = useRouter()


</script>


<style scoped>


</style>
