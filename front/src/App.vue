<template id ="app">
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
  <div class="container-fluid">
    <a class="navbar-brand" @click="router.push({name:'main'})">GaeChwi</a>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarScroll" aria-controls="navbarScroll" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarScroll">
      <ul class="navbar-nav me-auto my-2 my-lg-0 navbar-nav-scroll" style="--bs-scroll-height: 100px;">
        <li class="nav-item">
          <a class="nav-link" >영화추천</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" >호불호</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" >로그인</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" >회원가입</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" >프로필</a>
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
  <RouterView/>
</template>

<script setup>
import {ref} from 'vue'
import {RouterView,useRouter} from 'vue-router'
const router = useRouter()


const search=ref('')
const searchresultshow = () => {
  router.push({ name: 'indexView', params: { 'name': search.value } })
  search.value=''
}

</script>

<style scoped>

.router-link-exact-active {
  color: white !important
}
</style>
