<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
  <div class="container-fluid">
    <img class="navbar-brand" :src="logoSrc" @click="router.push({name:'main'})" style="width: 50px;"/>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarScroll" aria-controls="navbarScroll" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarScroll">
      <ul class="navbar-nav me-auto my-2 my-lg-0 navbar-nav-scroll" style="--bs-scroll-height: 100px;">
        <li class="nav-item">
          <a class="nav-link" @click="router.push({name:'movierecommend'})" >영화추천</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" @click="router.push({name:'moviechoice'})" >호불호</a>
        </li>
        
        <li class="nav-item">
          <a class="nav-link" v-if="!store.isLogin" @click="router.push({name:'userlogin'})" >로그인</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" v-if="!store.isLogin" @click="router.push({name:'usersignup'})" >회원가입</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" v-if="store.isLogin" @click="logOut()" >로그아웃</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" v-if="store.isLogin" @click="router.push({name:'userprofile'})" >프로필</a>
        </li>
      </ul>
      <form class="d-flex" role="search" @submit.prevent="searchresultshow">
        <input 
        class="form-control me-2" 
        type="search" 
        placeholder="Search" 
        aria-label="Search"
        v-model="search"
        >
        <button class="btn btn-outline-secondary" type="submit" >Search</button>
      </form>
    </div>
  </div>
</nav>

</template>


<script setup>
import {ref} from 'vue'
import {useRouter} from 'vue-router'
import logoSrc from '@/assets/logo.png'
import {useMovieStore} from '@/stores/counter'
const router = useRouter()
const store = useMovieStore()

const search=ref('')
const searchresultshow = () => {
  router.push({ name: 'indexView', params: { 'name': search.value } })
  search.value=''
}
const logOut = ()=>{
  store.logOut()
  router.push({name:'main'})
}
</script>


<style scoped>

.navbar {
  position: relative;
  z-index: 2; 
}

.dropdown {
  position: absolute;
  z-index: 3; 
}
</style>
