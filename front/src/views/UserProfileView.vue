<template>
  <div class="container">
    <div class="outer-circle">
      <span style="--clr:#eeff00;"></span>
      <span style="--clr:#00ffdd;"></span>
      <span style="--clr:#e900d5;"></span>
      <div class="profile-container">
        <div class="profile-picture"><img :src="profileSrc" class="profile-picture" alt=""></div>
        <div class="profile-info">
          <h2>{{ profile.username }}</h2>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import profileSrc from '@/assets/profile.png'
import { useMovieStore } from '@/stores/counter'
import { onMounted } from 'vue'
import axios from 'axios'

const store = useMovieStore()
const profile = ref([])
const userkey = ref(null)

const loadUserKey = async () =>{
  return userkey.value= store.userkey.value
}

const userProfile = async ()=>{
    return axios({
      method:'get',
      url:'http://127.0.0.1:8000/accounts/user/',
      headers: {Authorization: `Token ${userkey.value}`}
    })
    .then((response) => {
      console.log(response.data);
      profile.value = response.data
    })
    .catch((error) => {
      console.log(error)
    })
  }
  onMounted(async () => {
  await loadUserKey() 
  await userProfile()
    })
</script>

<style scoped>
.container {
  position: relative;
  width: 500px;
  height: 400px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.outer-circle {
  position: relative;
  width: 350px;
  height: 350px;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.outer-circle span {
  position: absolute;
  inset: 0;
  border: 2px solid #fff;
  border-radius: 50%;
  transition: 0.5s;
}

.outer-circle span:nth-child(1) {
  border-radius: 38% 62% 63% 37% / 41% 44% 56% 59%;
  animation: animate 6s linear infinite;
}

.outer-circle span:nth-child(2) {
  border-radius: 41% 44% 56% 59%/38% 62% 63% 37%;
  animation: animate 4s linear infinite;
}

.outer-circle span:nth-child(3) {
  border-radius: 41% 44% 56% 59%/38% 62% 63% 37%;
  animation: animate2 10s linear infinite;
}

.profile-container {
  display: flex;
  align-items: center;
  gap: 20px;
}

.profile-picture {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  background-color: #fff;
}

.profile-info {
  display: flex;
  flex-direction: column;
}

h2 {
  font-family: 'Montserrat', sans-serif;
  font-size: 1.5em;
  margin: 0;
}

p {
  font-family: 'Montserrat', sans-serif;
  font-size: 1em;
  margin: 0;
  color: #666;
}

@keyframes animate {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

@keyframes animate2 {
  0% {
    transform: rotate(360deg);
  }
  100% {
    transform: rotate(0deg);
  }
}
</style>
