<template>
  <div class="movie-detail">
    <div class="movie-detail-image"
      :style="{ backgroundImage: `url(${getImageUrl(url)})` }">
    </div>
  </div>
  <div>
    <div class="bubbleContainer">
      <div class="bubbleBody">
        <form id="message" @submit.prevent="addReview">
          <input type="text" v-model="newReview.title" name="formUsername" placeholder="Review title">
          <textarea v-model="newReview.content" name="formMessage" placeholder="Review Content"></textarea>
          <button class="btnSendMessage" type="submit" form="message">Send</button>
        </form>
      </div>
    </div>
  </div>

</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const movie = ref([])
const reviewlist = ref([])
const url = ref([])
const newReview = ref({ title: '', content: '' })

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

const addReview = function() {
  axios({
    method: 'post',
    url: `http://127.0.0.1:8000/movies/${movie.value.id}/create_review/`,
    headers: { Authorization: `Token ${userkey}` },
    data: newReview.value
  })
  .then((response) => {
    console.log(response)
    getReview()
    newReview.value = { title: '', content: '' }
  })
  .catch((error) => {
    console.log(error)
  })
}


onMounted(async () => {
  await getMovies()
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


.bubbleContainer {
  position: relative;
  width: 60vw;
  height: 250px;
  margin: 50px auto 0;
  
  div.bubbleBody,
  &::after {
    position: absolute;
  }
  
  .bubbleBody{
    width: 100%;
    height: 200px;
    background-color: rgba(255,255,255,.3);
    border-radius: 10px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    
    form {
      padding: 30px;
      box-sizing: border-box;
      
      & * {
        display: block;
        width: 100%;
        border: none;
        outline: none;
        font-size: 20px;
        color: #0D3544;
        padding: 10px;
        box-sizing: border-box;
      }
      
      input {
        height: 50px;
        border-bottom: 1px solid rgba(0,0,0,1);
        background-color: rgba(255,255,255,.0);
        color: white;
      }

      
      textarea {
        height: 80px;
        resize: none;
        background-color: rgba(255,255,255,.0);
        color: white;
      }
      input::placeholder,
      textarea::placeholder {
       color: white;
}
    }
  }
  
  &::after {
    content: "";
    width: 0px;
    height: 0px;
    top: 200px;
    left: 80px;
    border-left: 30px solid transparent;
    border-right: 30px solid transparent;
    border-top: 30px solid  rgba(255,255,255,.3);;
  }
}
.btnSendMessage {
  width: 300px;
  height: 60px;
  margin-top: 80px;
  color: white;
  background-color: rgba(255,255,255,.2);
  border-radius: 12px;
  color: white !important;
}

</style>
