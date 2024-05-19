<template>
  <h2>{{ actor.name }}</h2>
  <img class="actor-image" :src="getImageUrl(actor.profile_path)"/>
  

  <div class="container">
    <div class="movie-list-container">
      <h1 class="movie-list-title">Movie</h1>
      <div class="movie-list-wrapper">
        <div class="movie-list" >
          <MovieCard
        class="movie-item"
        v-for="movie in actor.movies"
        :key="movie.id"
        :movie="movie"
      />
        </div>
        <i class="fas fa-chevron-right arrow" ></i>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted,nextTick } from 'vue'
import {useRoute} from 'vue-router'
import MovieCard from '@/components/movie/MovieCard.vue'
import axios from'axios'

const route = useRoute()
const actor =ref([])

const getActor = function(){
    return axios({
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

  await nextTick(() => {
    const arrows = document.querySelectorAll(".arrow")
    const movieLists = document.querySelectorAll(".movie-list")

    arrows.forEach((arrow, i) => {
      const itemNumber = movieLists[i].querySelectorAll(".movie-item").length
      let clickCounter = 0
      arrow.addEventListener("click", () => {
        const ratio = Math.floor(window.innerWidth / 270)
        clickCounter++
        const currentTransform = window.getComputedStyle(movieLists[i]).transform
        const matrix = currentTransform !== 'none' ? currentTransform : 'matrix(1, 0, 0, 1, 0, 0)'
        const translateX = parseInt(matrix.split(',')[4].trim())
        if (itemNumber - (4 + clickCounter) + (4 - ratio) >= 0) {
          movieLists[i].style.transform = `translateX(${translateX - 300}px)`
        } else {
          movieLists[i].style.transform = "translateX(0)"
          clickCounter = 0
        }
      })
    })
  })
})


</script>


<style scoped>
h2{
  color: white;
  margin: 0 70px;
  font-size: 60px;
}
.actor-image{
  width: 300px;
  margin: 0 70px;
}
.container {
  background-color: #151515;
  min-height: calc(100vh - 50px);
  color: white;
  transition: 1s ease all;
}
.movie-list-container {
  padding: 0 20px;
}

.movie-list-container {
  padding: 0 20px;
}

.movie-list-wrapper {
  position: relative;
  overflow: hidden;
}

.movie-list {
  display: flex;
  align-items: center;
  height: 300px;
  transform: translateX(0);
  transition: all 1s ease-in-out;
}
.arrow {
  font-size: 120px;
  position: absolute;
  top: 90px;
  right: 0;
  color: lightgray;
  opacity: 0.5;
  cursor: pointer;
}
</style>
