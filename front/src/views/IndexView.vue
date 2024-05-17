<template>
  <h1><p>{{ keyword }}</p></h1>
  <h3>영화</h3>


  <h3>인물</h3>


</template>

<script setup>
import { ref, onMounted } from 'vue'
import {useRouter,useRoute} from 'vue-router'
import MovieCard from '@/components/movie/MovieCard.vue'
import ActorCard from '@/components/actor/ActorCard.vue'

const router=useRouter()
const route = useRoute();
const keyword = ref('');

onMounted(() => {
  console.log(route.params.name);
  keyword.value = route.params.name
  console.log(keyword);
})

</script>


<style scoped>

</style>
