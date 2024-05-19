<template>
  
  <div  class="actor-list-item" @click="goMovieDetail(actor.pk)" >
    <img class="actor-list-item-img" :src="getImageUrl(actor.profile_path)" alt="..." />
    <span class="actor-list-item-title">{{actor.name}}</span>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'


defineProps({
  actor:Object
})

const router = useRouter()

const goMovieDetail=function(id){
  router.push({name:'actordetail',params:{'actorId':id}})
}

const getImageUrl = (path) => {
  if (!path) {
    return
  }
  return `https://image.tmdb.org/t/p/w500${path}`
}
</script>

<style scoped>

.actor-list-item {
  margin-top: 0px;
  margin-right: 30px;
  position: relative;
}

.actor-list-item:hover .actor-list-item-img {
  transform: scale(1.2);
  margin: 0 30px;
  opacity: 0.5;
}

.actor-list-item:hover .actor-list-item-title,
.actor-list-item:hover .actor-list-item-desc,
.actor-list-item:hover .actor-list-item-button {
  opacity: 1;
}

.actor-list-item-img {
  transition: all 1s ease-in-out;
  width: 200px;
  /* height: 200px; */
  object-fit: cover;
  border-radius: 20px;
}

.actor-list-item-title {
  padding: 0 0px;
  font-size: 20px;
  font-weight: bold;
  position: absolute;
  top: 10%;
  left: 50px;
  opacity: 0;
  transition: 1s all ease-in-out;
}

.actor-list-item-desc {
  padding: 10px;
  font-size: 14px;
  position: absolute;
  top: 30%;
  left: 50px;
  width: 230px;
  opacity: 0;
  transition: 1s all ease-in-out;
}


</style>
