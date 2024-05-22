<template>
  <h1>영화 추천</h1>
  <div v-if="movielist.length">
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
  </div>

  <button class="nextpage">다시</button>
</template>

<script setup>
import axios from 'axios'
import { onMounted,ref, nextTick } from 'vue'
import MovieCard from '@/components/movie/MovieCard.vue'

const movielist = ref([]) 
const userid = localStorage.getItem('userid')

let pagepk = 1

const fetchData = async()=>{
  
    return axios({
      method:'get',
      url:`http://127.0.0.1:8000/movies/${userid}/recommended/${pagepk}/`,
    })
    .then((response) => {
      console.log(response.data)
      movielist.value = response.data
    })
    .catch((error) => {
      console.log(error)
    })
  }
  
  const getImageUrl = (path) => {
  if (!path) {
    return
  }
  return `https://image.tmdb.org/t/p/original/${path}`
}

onMounted(async () => {
  await fetchData()

  const nextpage = document.querySelector('.nextpage')

  nextpage.addEventListener('click', () => {
      pagepk+=1
      fetchData()
    })

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
img{
  width: 200px;
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
