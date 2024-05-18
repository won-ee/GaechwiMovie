<template>
  
  <div class="col" >
    <div class="card"  style="width: 18rem;" @click="goMovieDetail(movie.pk)" >
      <img :src="getImageUrl(movie.poster_path)" class="card-img-top" alt="..." />
    </div>
  </div>


</template>

<script setup>
import { useRouter } from 'vue-router';
import { useMovieStore } from '@/stores/counter';
const store = useMovieStore()

defineProps({
  movie:Object
})

const router = useRouter()

const goMovieDetail=function(id){
  router.push({name:'moviedetail',params:{'movieId':id}})
}

const getImageUrl = (path) => {
  if (!path) {
    return
  }
  return `https://image.tmdb.org/t/p/w500${path}`
}
</script>

<style scoped>

</style>
