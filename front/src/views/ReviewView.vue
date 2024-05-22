<template>
  <div class="movie-detail">
    <div class="movie-detail-image"
      :style="{ backgroundImage: `url(${getImageUrl(url)})` }">
    </div>
    <div @click="router.push({name:'CreateReview',params:{'moiveId':movie.id}})">
    <button class="createeReview" type="submit" form="message">
      Create Review
    </button>
  </div>
  </div>
 
  <div class="Container" v-for="review in reviewlist" :key="review.id">
    <div class="profile-section">
      <img class="profile-picture" :src="profileSrc" alt="Profile Picture">
      <div class="username">{{ review.user.username }}</div>
    </div>
  
    <div class="bubbleContainer">
      <div class="bubbleBody">
        <div id="message">
          <div class="title">
            <p>Review title<br><span>{{ review.title }}</span></p>
          </div>
          <div class="content">
            <p>Review content<br><span>{{ review.content }}</span></p>
          </div>
        </div>
      </div>
      <div class="delete-container" @click="deleteReview(review.pk)">
        <p class="delete">리뷰삭제</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute,useRouter } from 'vue-router'
import axios from 'axios'
import profileSrc from '@/assets/profile.png';

const router = useRouter()
const route = useRoute()
const movie = ref([])
const reviewlist = ref([])
const url = ref([])
const userkey = localStorage.getItem('userkey')

const urlname = function (pullurl) {
  url.value = pullurl.split('/').pop()
}

const getImageUrl = (path) => {
  if (!path) {
    return
  }
  return `https://image.tmdb.org/t/p/original/${path}`
}

const getMovies = async () => {
  return axios({
    method: 'get',
    url: `http://127.0.0.1:8000/movies/${route.params.moiveId}/`,
  })
  .then((response) => {
    console.log(response.data)
    movie.value = response.data
    urlname(response.data.backdrop_image)
  })
  .catch((error) => {
    console.log(error)
  })
}

const deleteReview = function(reviewpk){
  axios({
    method: 'delete',
    url: `http://127.0.0.1:8000/movies/${movie.value.id}/${reviewpk}/delete_review/`,
    headers: { Authorization: `Token ${userkey}` }
  })
  .then((response) => {
    console.log(response)
    getReview()
  })
  .catch((error) => {
    console.log(error)
  })
}

const getReview = async () => {
  return axios({
    method: 'get',
    url: `http://127.0.0.1:8000/movies/${movie.value.id}/reviews`,
  })
  .then((response) => {
    console.log(response.data);
    reviewlist.value = response.data
  })
  .catch((error) => {
    console.log(error)
  })
}

onMounted(async () => {
  await getMovies()
  await getReview()
})
</script>

<style scoped>
.Container {
  display: flex;
  align-items: center;
  justify-content: center;
}
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
.bubbleContainer {
  position: relative;
  width: 60vw;
  height: 250px;
  margin: 50px;
  
}
.bubbleBody {
  width: 100%;
  height: 200px;
  background-color: rgba(255, 255, 255, .3);
  border-radius: 10px;
  

}
.bubbleBody p {
  color: rgba(0, 0, 0, 0.527);
  margin-top: 5px;
  margin-left: 15px;
}
form {
  padding: 30px;
  box-sizing: border-box;
}
form * {
  display: block;
  width: 100%;
  border: none;
  outline: none;
  font-size: 20px;
  color: #0D3544;
  padding: 10px;
  box-sizing: border-box;
}
.title {
  height: 50px;
  border-bottom: 1px solid rgba(0, 0, 0, 1);
  background-color: rgba(255, 255, 255, .0);
  color: white;
}
.content {
  height: 80px;
  background-color: rgba(255, 255, 255, .0);
  color: white;
}
.profile-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-right: 20px;
}
.profile-picture {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  margin-bottom: 10px;
  object-fit: cover;
  opacity: 80%;
}
.username {
  color: white;
  text-align: center;
  margin-top: 0;
  z-index: 1;
}
.delete-container {
  position: absolute;
  bottom: 30px; 
  right: 0px; 
}
.delete {
  background-color: rgba(169, 169, 169, 0.281);
  padding: 5px 10px;
  border-radius: 5px;
  cursor: pointer;
}
.createeReview {
  position:fixed;
  width: 200px;
  margin-left:60px;
  height: 60px;
  border: 0px;
  background-color: rgba(255,255,255,.2);
  border-radius: 12px;
  color: white !important;
}
</style>
