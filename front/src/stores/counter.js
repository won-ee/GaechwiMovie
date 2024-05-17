import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from'axios'



export const useMovieStore = defineStore('movie', () => {
  const MovieList = ref([])
  
  const getMovies = function(){
    return axios({
      method:'get',
      url:'http://127.0.0.1:8000/movies/',
    })
    .then((response) => {
      MovieList.value = response.data
    })
    .catch((error) => {
      console.log(error)
    })
  }
  return {MovieList,getMovies}
})
