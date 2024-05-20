<template>
<div>
    <img :src="profileSrc" alt="">
    <h1>{{ profile.username }} 님 ㅎㅇ요</h1>
    <h1>너 id {{ userid }} 임</h1>

</div>

</template>


<script setup>
import { ref } from 'vue'
import profileSrc from '@/assets/profile.png'
import { onMounted } from 'vue'
import axios from 'axios'

const profile = ref([])
const userkey = ref(null)
const userid = localStorage.getItem('userid')
const movielist = ref([])

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
      movielist.value = response.data
      
    })
    .catch((error) => {
      console.log(error)
    })
  }
  onMounted(async () => {
  await loadUserKey() 
  await userProfile()
  await getMovie()
    })
</script>

<style scoped>
</style>
