<template>
  <h1>{{ actor.name }}</h1>
  <img class="actor-image" :src="getImageUrl(actor.profile_path)" @click="router.push({name:'actordetail',params:{'actorId':actor.pk}})" />
  <div class="row row-cols-2 row-cols-md-3 g-4" >
    <ActorMovieCard v-for="movie in actor.movies" :key="movie.id" :movie="movie" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import {useRoute,useRouter} from 'vue-router'
import ActorMovieCard from '@/components/actor/ActorMovieCard.vue';
import axios from'axios'

const route = useRoute()
const router = useRouter()
const actor =ref([])

const getActor = function(){
    axios({
      method:'get',
      url:`http://127.0.0.1:8000/movies/actors/${route.params.actorId}/`,
    })
    .then((response) => {
      actor.value = response.data
      console.log(actor.value);
    })
    .catch((error) => {
      console.log(error)
    })
  }

const getImageUrl = (path) => {
  if (!path) {
    return
  }
  return `https://image.tmdb.org/t/p/w500${path}`
}


onMounted(async () => {
  await getActor() 
})
</script>


<style scoped>
h1{
  color: white;
}
.actor-image{
  width: 300px;
}
</style>
