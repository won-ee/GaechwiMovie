<template>
<div>
    <img :src="profileSrc" alt="">
    <h1>{{ profile.username }} 님 ㅎㅇ요</h1>
    <h1>니가 좋아하는 영화</h1>
    <span v-for="movie in movielist">
       {{ movie.title }}
       <img class="movie-list-item-img" :src="getImageUrl(movie.poster_path)" alt="..." @click="router.push({name:'moviedetail',params:{'movieId':movie.pk}})" />
    </span>
    <h1>니가 싫어하는 영화</h1>
    <span v-for="movie in worstlist">
       {{ movie.title }}
       <img class="movie-list-item-img" :src="getImageUrl(movie.poster_path)" alt="..." @click="router.push({name:'moviedetail',params:{'movieId':movie.pk}})" />
    </span>
   

</div>

</template>


<script setup>
import { ref,onMounted  } from 'vue'
import profileSrc from '@/assets/profile.png'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const profile = ref([])
const userkey = ref(null)
const userid = localStorage.getItem('userid')
const movielist = ref([])
const worstlist = ref([])

const loadUserKey = async () =>{
  return userkey.value = localStorage.getItem('userkey')
}


const userProfile = async ()=>{

    return axios({
      method:'get',
      url:'http://127.0.0.1:8000/accounts/user/',
      headers: {Authorization: `Token ${userkey.value}`}
    })
    .then((response) => {
      profile.value = response.data
    })
    .catch((error) => {
      console.log(error)
    })
  }

const getMovie = async ()=>{
    return axios({
      method:'get',
      url:`http://127.0.0.1:8000/movies/${userid}/user_like_movie`,
    })
    .then((response) => {
      console.log(response.data )
      movielist.value = response.data.like_movies
    })
    .catch((error) => {
      console.log(error)
    })
  }

  const getWorst = async ()=>{
    return axios({
      method:'get',
      url:`http://127.0.0.1:8000/movies/${userid}/user_dislike_movie`,
    })
    .then((response) => {
      console.log(response.data )
      worstlist.value = response.data.dislike_movies
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

  onMounted(async () => {
  await loadUserKey() 
  await userProfile()
  await getMovie()
  await getWorst()
    })
</script>

<style scoped>
img{
  width: 200px;
}
</style>
