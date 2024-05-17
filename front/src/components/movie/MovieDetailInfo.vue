<template>
  <div class="movie-content d-flex">
    <div class="movie-poster">
      <img
        class="mt-2 movie-poster-image"
        :src="getImageUrl(movie.poster_path)"
      />
    </div>
    <div class="ml-4 w-75">
      <h1 class="movie-title">{{ movie.title }}</h1>
      <div class="movie-information-wrapper mt-4 d-flex align-items-center">
        <div>{{ movie.release_date }}</div>
        <span class="ml-1">ㆍ</span>
        <div>{{ movie.runtime }} 분</div>
        <span class="ml-1">ㆍ</span>
        <div class="ml-2 d-flex genres-wrapper">
          <div
            class="genres"
            v-for="genre in movie.genres"
            :key="genre.id"
          >
            {{ genre.name }}
          </div>
        </div>
      </div>
      <div class="movie-overview mt-3">{{ movie.overview }}</div>
      <div class="ml-2 d-flex actors-wrapper">
        <div
          class="actor"
          v-for="actor in movie.actors"
          :key="actor.id"
        >
          <img class="actor-image" :src="getImageUrl(actor.profile_path)" />
          <div>{{ actor.name }}</div>
        </div>
      </div>
    </div>
  </div>
</template>


<script setup>
import { ref, onMounted } from 'vue'
import {useRoute} from 'vue-router'
import axios from'axios'

const route = useRoute()

const movie =ref([])
const getMovies = function(){
    axios({
      method:'get',
      url:`http://127.0.0.1:8000/movies/${route.params.movieId}`,
    })
    .then((response) => {
      movie.value = response.data
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
  await getMovies() 
})
</script>


<style scoped>
.movie-detail {
  position: relative;
  padding: 40px 40px;
}
.movie-detail-image {
  background-size: cover;
  height: 100vh;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 0;
}
.movie-detail-image::after {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  min-height: 100vh;
  background-color: rgb(40, 40, 40);
  opacity: 0.8;
  content: "";
  display: block;
}
.movie-content {
  position: relative;
  z-index: 999;
}
.movie-title {
  margin-left: 5px;
}
.movie-information-wrapper {
  font-size: 13px;
}
.genres {
  display: flex;
  align-items: center;
}
.genres:not(:first-of-type)::before {
  content: "/";
  margin-bottom: 4px;
  margin-left: 6px;
  margin-right: 1px;
  font-size: 20px;
}
.movie-overview {
  max-width: 60%;
  font-size: 14px;
  color: #dddddddd;
}
.homepage-link:hover {
  opacity: 0.5;
}

.actor {
  margin-right: 10px;
  text-align: center;
}
.actor-image {
  width: 100px;
  height: auto;
}
</style>
