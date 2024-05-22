<template>
    <div  class="movie-list-item" @click="goMovieDetail(movie.id)" >
      <img class="movie-list-item-img" :src="getImageUrl(movie.poster_path)" alt="..." />
      <span class="movie-list-item-title">{{movie.title}}</span>
    </div>
</template>

<script setup>
import { useRouter } from 'vue-router';


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

.movie-list-item {
  margin-right: 30px;
  margin-bottom: 0px;
  position: relative;
}

.movie-list-item:hover .movie-list-item-img {
  transform: scale(1.2);
  margin: 0 30px;
  opacity: 0.5;
}

.movie-list-item:hover .movie-list-item-title,
.movie-list-item:hover .movie-list-item-desc,
.movie-list-item:hover .movie-list-item-button {
  opacity: 1;
}

.movie-list-item-img {
  transition: all 1s ease-in-out;
  width: 200px;
  /* height: 200px; */
  object-fit: cover;
  border-radius: 20px;
}

.movie-list-item-title {
  padding: 0 0px;
  font-size: 20px;
  font-weight: bold;
  position: absolute;
  top: 10%;
  left: 50px;
  opacity: 0;
  transition: 1s all ease-in-out;
}

.movie-list-item-desc {
  padding: 10px;
  font-size: 14px;
  position: absolute;
  top: 30%;
  left: 50px;
  width: 230px;
  opacity: 0;
  transition: 1s all ease-in-out;
}


</style>
