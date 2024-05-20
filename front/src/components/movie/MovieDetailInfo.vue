<template>
  <div class="container movie-content">
    <div class="row">
      <div class="col-md-4">
        <div class="movie-poster">
          <img
            class="mt-2 movie-poster-image img-fluid"
            :src="getImageUrl(movie.poster_path)"
          />
        </div>
      </div>
      <div class="col-md-8">
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
            <button class="custom-btn btn-5" @click="likemovie"><span>개추💖</span></button>
            <button class="custom-btn btn-5" @click="dislikemovie"><span>비추💔</span></button>
          </div>

        </div>
        <div class="movie-overview mt-3">{{ movie.overview }}</div>
        <div class="row actors-wrapper mt-3">
          <div
            class="actor col-6 col-sm-4 col-md-3 col-lg-2 text-center mb-3"
            v-for="actor in movie.actors"
            :key="actor.id"
          >
            <img class="actor-image img-fluid" :src="getImageUrl(actor.profile_path)" @click="router.push({name:'actordetail',params:{'actorId':actor.pk}})" />
            <div>{{ actor.name }}</div>
          </div>
        </div>
      </div>
    </div>
    <div>
      <p>review title : <input type="text" style="color: #000;" v-model="reviewtitle"></p>
      <br>
      <p>review content : <input type="text" style="color: #000;" v-model="reviewcontent"></p>
      <input type="submit" value="리뷰쓰기" style="color: #000;" @click="goReview">
  </div>
    <div v-for="review in reviewlist">
        <p v-if="review.title" :id="review.pk" >{{ review.title }}<button  style="color: #000;" @click="deleteRiview(review.pk)">삭제</button> </p>
        <p v-if="review.content" :id="review.pk">{{ review.content }}<button  style="color: #000;" @click="deleteRiview(review.pk)">삭제</button></p>
    </div>
  </div>



</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const router = useRouter()
const movie = ref([])
const reviewlist = ref([])
const reviewtitle=ref('')
const reviewcontent=ref('')
const userkey = localStorage.getItem('userkey')

const getMovies = async () => {
  return axios({
    method: 'get',
    url: `http://127.0.0.1:8000/movies/${route.params.movieId}`,
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


const getReview = async ()=> {
  return axios({
    method: 'get',
    url: `http://127.0.0.1:8000/movies/${movie.value.id}/reviews`,
  })
    .then((response) => {
      reviewlist.value = response.data
    })
    .catch((error) => {
      console.log(error)
    })
}

const goReview = function() { 
  axios ({
    method:'post',
    url:`http://127.0.0.1:8000/movies/${movie.value.id}/create_review/`,
    headers: {Authorization: `Token ${userkey}`},
    data:{
      title:reviewtitle.value,
      content:reviewcontent.value
    }
    })
    .then((response) => {
      console.log(response)
    })
    .catch((error) => {
      console.log(error)
    })
    reviewtitle.value =''
    reviewcontent.value =''
    
    getReview()
}

const deleteRiview = function(reviewpk){
  axios ({
    method:'delete',
    url:`http://127.0.0.1:8000/movies/${movie.value.id}/${reviewpk}/delete_review/`,
    headers: {Authorization: `Token ${userkey}`},
    data:{
      title:reviewtitle.value,
      content:reviewcontent.value
    }
    })
    .then((response) => {
      console.log(response)
    })
    .catch((error) => {
      console.log(error)
    })
    reviewtitle.value =''
    reviewcontent.value =''
    
    getReview()
}

onMounted(async () => {
  await getMovies()

  await getReview()
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
  max-width: 100%;
  font-size: 14px;
  color: #dddddddd;
}
.homepage-link:hover {
  opacity: 0.5;
}
.actor-image {
  width: 100%;
  height: auto;
}
.btn-5 {
  width: 50px;
  height: 40px;
  line-height: 42px;
  padding: 0;
  border: none;
  background: rgb(255, 255, 255);
  background: linear-gradient(0deg, rgb(20, 20, 20) 0%, rgb(20, 20, 20) 100%);
}
.btn-5:hover {
  color: #ffffff;
  background: transparent;
   box-shadow:none;
}
.btn-5:before,
.btn-5:after{
  content:'';
  position:absolute;
  top:0;
  right:0;
  height:2px;
  width:0;
  background: #ffffff;
  box-shadow:
   -1px -1px 5px 0px #fff,
   7px 7px 20px 0px #0003,
   4px 4px 5px 0px #0002;
  transition:400ms ease all;
}
.btn-5:after{
  right:inherit;
  top:inherit;
  left:0;
  bottom:0;
}
.btn-5:hover:before,
.btn-5:hover:after{
  width:100%;
  transition:800ms ease all;
}
</style>
