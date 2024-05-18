<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
  <div class="container-fluid">
    <a class="navbar-brand" @click="router.push({name:'main'})">GaeChwi</a>
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
          <a class="nav-link" @click="router.push({name:'userlogin'})" >로그인</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" @click="router.push({name:'usersignup'})" >회원가입</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" @click="router.push({name:'userprofile'})" >프로필</a>
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
        <button class="btn btn-outline-success" type="submit" >Search</button>
      </form>
    </div>
  </div>
</nav>

</template>


<script setup>
import {ref} from 'vue'
import {useRouter} from 'vue-router'
const router = useRouter()

const search=ref('')
const searchresultshow = () => {
  router.push({ name: 'indexView', params: { 'name': search.value } })
  search.value=''
}
</script>


<style scoped>

.navbar {
  position: relative;
  z-index: 2; /* Ensure NavBar is above RouterView */
}

.dropdown {
  position: absolute;
  z-index: 3; /* Ensure dropdown is above other content */
}
</style>
