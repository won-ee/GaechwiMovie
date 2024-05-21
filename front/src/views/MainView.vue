<template>
  <div class="container">
    <div class="movie-list-container">
      <h1 class="movie-list-title">Best Movie</h1>
      <div class="movie-list-wrapper">
        <div class="movie-list">
          <MovieCard
        class="movie-item"
        v-for="movie in movielist"
        :key="movie.id"
        :movie="movie"
      />
        </div>
        <i class="fas fa-chevron-right arrow" ></i>
      </div>

      <h1 class="movie-list-title">Worst Movie</h1>
      <div class="worst-movie-list-wrapper">
        <div class="worst-movie-list">
          <MovieCard
        class="worst-movie-item"
        v-for="movie in worstlist"
        :key="movie.id"
        :movie="movie"
      />
        </div>
        <i class="fas fa-chevron-right worst-arrow" ></i>
      </div>
    </div>
  </div>

</template>

<script setup>
import { ref, onMounted,nextTick } from 'vue'
import { useMovieStore } from '@/stores/counter'
import MovieCard from '@/components/movie/MovieCard.vue'


const store = useMovieStore()

const movielist = ref([])
const worstlist = ref([])


onMounted(async () => {
  await store.getMovies() 
  await store.getWorstMovies() 

  movielist.value = store.MovieList
  worstlist.value = store.WorstMovieList
  
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

  await nextTick(() => {
    const arrows = document.querySelectorAll(".worst-arrow")
    const movieLists = document.querySelectorAll(".worst-movie-list")

    arrows.forEach((arrow, i) => {
      const itemNumber = movieLists[i].querySelectorAll(".worst-movie-item").length
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

.worst-movie-list-wrapper {
  position: relative;
  overflow: hidden;
}

.worst-movie-list {
  display: flex;
  align-items: center;
  height: 300px;
  transform: translateX(0);
  transition: all 1s ease-in-out;
}
.worst-arrow {
  font-size: 120px;
  position: absolute;
  top: 90px;
  right: 0;
  color: lightgray;
  opacity: 0.5;
  cursor: pointer;
}
</style>
