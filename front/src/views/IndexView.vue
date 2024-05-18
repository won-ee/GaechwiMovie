<template>
 
  <div class="container">
    <div class="movie-list-container">
      <h1 class="keyword-title">{{ keyword }}</h1>
      <h1 class="movie-list-title">Movie</h1>
      <div class="movie-list-wrapper">
        <div class="movie-list" v-if="movies.length">
          <MovieCard
        class="movie-item"
        v-for="movie in movies"
        :key="movie.id"
        :movie="movie"
      />
        </div>
        <p v-else>검색 결과가 없습니다.</p>
        <i class="fas fa-chevron-right arrow" ></i>
      </div>
    </div>
  </div>
  <h3>인물</h3>


</template>

<script setup>
import { ref, onMounted,nextTick } from 'vue'
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


onMounted(async() => {
  keyword.value = route.params.name
  await fetchData()
  await nextTick(() => {
    const arrows = document.querySelectorAll(".arrow");
    const movieLists = document.querySelectorAll(".movie-list");

    arrows.forEach((arrow, i) => {
      const itemNumber = movieLists[i].querySelectorAll(".movie-item").length;
      let clickCounter = 0;
      arrow.addEventListener("click", () => {
        const ratio = Math.floor(window.innerWidth / 270);
        clickCounter++;
        const currentTransform = window.getComputedStyle(movieLists[i]).transform;
        const matrix = currentTransform !== 'none' ? currentTransform : 'matrix(1, 0, 0, 1, 0, 0)';
        const translateX = parseInt(matrix.split(',')[4].trim());
        if (itemNumber - (4 + clickCounter) + (4 - ratio) >= 0) {
          movieLists[i].style.transform = `translateX(${translateX - 300}px)`;
        } else {
          movieLists[i].style.transform = "translateX(0)";
          clickCounter = 0;
        }
      });
    });
  });
});


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
.keyword-title {
  font-size: 60px;
}
</style>
