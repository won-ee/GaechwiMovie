<template>
  <nav>
    <RouterLink :to="{name:'main'}">메인</RouterLink> |
    <RouterLink :to="{name:'recommend'}">영화추천</RouterLink> |
    <RouterLink :to="{name:'randam'}">영화랜덤</RouterLink> |
    <RouterLink :to="{name:'community'}">게시판</RouterLink> |
    <RouterLink :to="{name:'index'}">서치</RouterLink> |
    <RouterLink :to="{name:'login'}">로그인</RouterLink> |
    <RouterLink :to="{name:'signup'}">회원가입</RouterLink> |
    <RouterLink :to="{name:'detail'}">디테일</RouterLink> |
    <RouterLink :to="{name:'index'}">인덱스</RouterLink> |
  </nav>


  <RouterView/>
</template>

<script setup>
import {RouterView,RouterLink} from 'vue-router'


</script>


<style scoped>

</style>
