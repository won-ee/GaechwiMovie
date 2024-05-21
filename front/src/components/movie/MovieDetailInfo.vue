<template>
  <div class="movie-detail">
    <div class="movie-detail-image"
      :style="{ backgroundImage: `url(${getImageUrl(url)})` }">
    </div>
  <div class="container movie-content">
    <div class="row">
      <div class="col-md-4">
        <div class="movie-poster">
          <img
            class="mt-2 movie-poster-image img-fluid"
            :src="getImageUrl(movie.poster_image)"
          />
          <div @click="router.push({name:'review',params:{'moiveId':movie.id}})">
            <button class="createeReview" type="submit" form="message">
              Create Review
            </button>
          </div>
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
            &nbsp;&nbsp;<button class="custom-btn btn-5" @click="likemovie"><span>개추💖</span></button>
            &nbsp;<button class="custom-btn btn-5" @click="dislikemovie"><span>비추💔</span></button>
          </div>

        </div>
        <div class="movie-overview mt-3">{{ movie.overview }}</div>
        <div>Director</div>
        <img class="director-image img-fluid" :src="getImageUrl(director.profile_image)" />
        {{ director.birth_date }} / {{director.gender }} / {{director.nationality }} 
        <div>{{ director.name }}</div>
        <div>Actor</div>
        <div class="row actors-wrapper mt-3">
          <div
            class="actor col-6 col-sm-4 col-md-3 col-lg-2 text-center mb-3"
            v-for="actor in movie.actors"
            :key="actor.id"
          >
            <img class="actor-image img-fluid" :src="getImageUrl(actor.profile_image)" @click="router.push({name:'actordetail',params:{'actorId':actor.id}})" />
            <div>{{ actor.name }}</div>
          </div>
        </div>
      </div>
    </div>
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
const userkey = localStorage.getItem('userkey')
const url = ref([])
const director = ref([])

const urlname = function (pullurl) {
  url.value = pullurl.split('/').pop()
}

const getMovies = async () => {
  return axios({
    method: 'get',
    url: `http://127.0.0.1:8000/movies/${route.params.movieId}`,
  })
    .then((response) => {
      movie.value = response.data
      urlname(response.data.backdrop_image)
      getDirector(response.data.director)
      console.log(response.data)
    })
    .catch((error) => {
      console.log(error)
    })
}

const getDirector = async (pk) => {
  return axios({
    method: 'get',
    url: `http://127.0.0.1:8000/movies/director/${pk}/`,
  })
    .then((response) => {
      director.value = response.data

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


const likemovie =function(){
  axios({
      method:'post',
      url:`http://127.0.0.1:8000/movies/${movie.value.id}/like`,
      headers: {Authorization: `Token ${localStorage.getItem('userkey')}`}

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

const dislikemovie =function(){
  axios({
      method:'post',
      url:`http://127.0.0.1:8000/movies/${movie.value.id}/dislike`,
      headers: {Authorization: `Token ${localStorage.getItem('userkey')}`}
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
.director-image{
  width: 20%;
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
  background: transparent
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
.createeReview {
  width: 300px;
  height: 60px;
  margin-top: 80px;
  border: 0px;
  background-color: rgba(255,255,255,.2);
  border-radius: 12px;
  color: white !important;
}
</style>
