<template>
  <div class="movie-detail">
    <div class="movie-detail-image"
      :style="{ backgroundImage: `url(${getImageUrl(url)})` }">
    </div>
    asdasmkldp;qmdiopkqmdkioplq
    <div class="review">
    <h1 class="movie-title">{{ movie.title }}</h1>
  <div class="input-wrapper" @click="promptReview()">
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
</div>
</div>
  </div>


</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import axios from 'axios'

const route = useRoute()
const movie = ref([])
const reviewlist = ref([])
const url = ref([])

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
.movie-title {
  margin-left: 5px;
}


.review{
  z-index: 1;
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
