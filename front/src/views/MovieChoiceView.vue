<template>
  <div class="movie-detail">
    <div class="movie-detail-image" :style="{ backgroundImage: `url(${getImageUrl(url)})` }"></div>
    <div class="container" v-if="movie.length">
      <div class="movie-list-container">
        <h1 class="movie-list-title">{{ movie[0].title }}</h1>
        <div class="movie-list-wrapper">
          <div class="movie-list">
            <div class="movie-list-item" @click="goMovieDetail(movie[0].pk)">
              <img class="movie-list-item-img" :src="getImageUrl(movie[0].poster_image)" alt="..." @click="goMovieDetail(movie[0].id)" />
              <span class="movie-list-item-title">{{ movie[0].title }}</span>
            </div>
          </div>
        </div>
      </div>
        <ul>
            <li>
              <button @click="likemovie()">💖 </button> 
            </li>
            <li>
              <button @click="dislikemovie()">💔</button>
            </li>
            <li>
              <button @click="fetchData">❓</button>
            </li>
          </ul>
    </div>
    
  </div>
</template>

<script setup>
import axios from 'axios'
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const movie = ref([])
const url = ref([])

const urlname = function (pullurl) {
  url.value = pullurl.split('/').pop()
}

const goMovieDetail = function (id) {
  router.push({ name: 'moviedetail', params: { 'movieId': id } })
}

const getImageUrl = (path) => {
  if (!path) {
    return
  }
  return `https://image.tmdb.org/t/p/original/${path}`
}

const fetchData = function () {
  return axios({
    method: 'get',
    url: `http://127.0.0.1:8000/movies/random`,
  })
    .then((response) => {
      movie.value = response.data
      urlname(response.data[0].backdrop_image)
    })
    .catch((error) => {
      console.log(error)
    })
}

const likemovie = function () {
  axios({
    method: 'post',
    url: `http://127.0.0.1:8000/movies/${movie.value[0].id}/like`,
    headers: { Authorization: `Token ${localStorage.getItem('userkey')}` },
  })
    .then((response) => {
      console.log(response.data)
      movie.value = response.data
    })
    .catch((error) => {
      console.log(error)
    })
  fetchData()
}

const dislikemovie = function () {
  axios({
    method: 'post',
    url: `http://127.0.0.1:8000/movies/${movie.value[0].id}/dislike`,
    headers: { Authorization: `Token ${localStorage.getItem('userkey')}` },
  })
    .then((response) => {
      movie.value = response.data
    })
    .catch((error) => {
      console.log(error)
    })
  fetchData()
}

onMounted(async () => {
  await fetchData()
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

.container {
  background-color: #151515;
  min-height: calc(100vh - 50px);
  color: white;
  transition: 1s ease all;
}

.movie-list-container {
  padding: 0 20px;
}

.movie-list-wrapper {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  position: relative;
  overflow: hidden;
  height: 100%;
}

.movie-list {
  display: flex;
  flex-direction: column;
  align-items: center;
  height: 100%;
  justify-content: space-between;
}

.movie-list-item {
  margin-bottom: 30px;
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
  width: 400px;
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

ul{
  padding: 0;
  display: flex;
  justify-content: center;
  align-items: center;
}

li{
  display: inline-block;
  position: relative;
  
  
  list-style-type: none;
  margin: 0 10px 10px;
  &:nth-child(3) button {
    background: #728618b4;
  }
  &:nth-child(2) button {
    background: #247BA0;
  }
  &:nth-child(1) button {
    background: #942542;
  }
}
button {
  /* margin-top: 180px; */
  position: relative;
  background: rebeccapurple;
  width: 100px;
  height: 100px;
  border-radius: 50%;
  border:5px solid white;
  color: white;
  font-family: Verdana;
  font-weight: bold;
  font-size: 50px;
  cursor: pointer;
  padding: 0;
}
</style>
