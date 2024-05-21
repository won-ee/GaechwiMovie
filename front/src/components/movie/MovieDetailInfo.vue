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
        <img class="actor-image img-fluid" :src="getImageUrl(movie.director)" />
        <div class="row actors-wrapper mt-3">
          <div
            class="actor col-6 col-sm-4 col-md-3 col-lg-2 text-center mb-3"
            v-for="actor in movie.actors"
            :key="actor.id"
          >
            <img class="actor-image img-fluid" :src="getImageUrl(actor.profile_image)" @click="router.push({name:'actordetail',params:{'actorId':actor.pk}})" />
            <div>{{ actor.name }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
  </div>

  <!-- <div class="input-wrapper" @click="promptReview()">
  <div class="block">
    <p>
      <span><span class="purple">input</span> <span class="white">( Review )</span></span>
    </p>
  </div>
</div>
<div class="wrapper">
  <div class="block" v-for="review in reviewlist" :key="review.pk" >
    <p>
      <span><span class="purple">class</span> <span class="white">{{review.user.username  }} {</span></span>
      <span class="inline gray">// Review</span>
        <span class="inline green">title<span class="white">:</span> <span class="orange">{{ review.title }}</span></span>
        <span class="inline green">content<span class="white">:</span> <span class="yellow">{{ review.content }}</span></span>
      <span>};</span>
      <span class="bottom"><span class="red" @click="deleteReview(review.pk)">delete</span><span class="white">();</span></span>
    </p>
  </div>
</div> -->
  

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
      console.log(response.data)
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

const promptReview = function() {
  const title = prompt("리뷰 제목을 입력하세요:");
  if (title) {
    const content = prompt("리뷰 내용을 입력하세요:");
    if (content) {
      axios({
        method: 'post',
        url: `http://127.0.0.1:8000/movies/${movie.value.id}/create_review/`,
        headers: { Authorization: `Token ${userkey}` },
        data: {
          title: title,
          content: content
        }
      })
      .then((response) => {
        console.log(response)
        getReview()
      })
      .catch((error) => {
        console.log(error)
      })
    }
  }
}

const deleteReview = function(reviewpk){
  axios ({
    method:'delete',
    url:`http://127.0.0.1:8000/movies/${movie.value.id}/${reviewpk}/delete_review/`,
    headers: {Authorization: `Token ${userkey}`}
    })
    .then((response) => {
      console.log(response)
      getReview()
    })
    .catch((error) => {
      console.log(error)
    })
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
.input-wrapper {
  display: flex;
  align-items: center;
  margin:10px 10px 10px 100px ;
}
.wrapper {
  display: flex;
  align-items: center;
  margin:0 100px ;
}
.block {
  margin: 10px;
  background-color: #011627;;
  box-shadow: 0 10px 25px 0 rgba(109, 106, 106, 0.4);
  color: #d6deeb;
  border-radius: 25px;
  transition: transform .3s cubic-bezier(.175,.885,.32,1.275),-webkit-transform .3s cubic-bezier(.175,.885,.32,1.275);
}
.block:hover {
  transform: scale(1.05, 1.05);
}
.block p {
  margin: 2em;
}
.block p span {
  display: block;
}
.inline {
  margin-left: 1em;
}
.green {
  color: #7fdbca;
}
.gray {
  display: inline-block;
  color: #aeb1b8;
}
.block p span .white {
  display: inline-block;
  color: #d6deeb;
}
.block p span .purple {
  display: inline-block;
  color:#c792ea;
}
.block p span .yellow {
  display: inline-block;
  color:  #ecc48d;
}
.block p span .orange {
  display: inline-block;
  color:  #f78c6c;
}
.block p span .red {
  display: inline-block;
  color: #ff5874;
}
.block p span .purple {
  display: inline-block;
  color: #c792ea;
  font-style: italic;
}
.block p span .ani {
  display: inline-block;
  color: #d6deeb;
  animation: ani 1s linear infinite;
}
.bottom {
  margin-top: 1em;
}
::selection {
  color: #f5f5f5;
  background: #ff5874;
}

</style>
