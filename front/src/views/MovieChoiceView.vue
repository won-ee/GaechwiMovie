<template>
  <div class="container" v-if="movie.length"  >
    <div class="movie-list-container">
      <h1 class="movie-list-title" >{{movie[0].title}}</h1>
      <div class="movie-list-wrapper">
        <div class="movie-list">
          <div  class="movie-list-item" @click="goMovieDetail(movie[0].pk) " >
            <img class="movie-list-item-img" :src="getImageUrl(movie[0].poster_path)" alt="..."  @click="goMovieDetail(movie[0].id)"/>
            <span class="movie-list-item-title">{{movie[0].overview}}</span>
          </div>
        </div>
      </div>
    </div>
  </div>

</template>

<script setup>
import axios from 'axios'
import { onMounted,ref } from 'vue'
import { useRouter } from 'vue-router';

const router = useRouter()
const movie = ref([])

const goMovieDetail=function(id){
  router.push({name:'moviedetail',params:{'movieId':id}})
}

const getImageUrl = (path) => {
  if (!path) {
    return
  }
  return `https://image.tmdb.org/t/p/w500${path}`
}

const fetchData = function(){
    return axios({
      method:'get',
      url:`http://127.0.0.1:8000/movies/random`,
    })
    .then((response) => {
      console.log(response.data)
      movie.value = response.data
    })
    .catch((error) => {
      console.log(error)
    })
  }
  
onMounted(async () => {
await fetchData() 
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
  height: 600px;
  transform: translateX(0);
  transition: all 1s ease-in-out;
}
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
  width: 400px;
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