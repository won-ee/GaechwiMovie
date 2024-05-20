import { ref } from 'vue'
import { defineStore } from 'pinia'
import { useRouter } from 'vue-router'
import axios from 'axios'

export const useMovieStore = defineStore('movie', () => {
  const MovieList = ref([])
  const WorstMovieList = ref([])
  const userkey = ref(null)
  const isLogin = ref(false)
  const router = useRouter()

  const getMovies = function() {
    return axios({
      method: 'get',
      url: 'http://127.0.0.1:8000/movies/',
    })
    .then((response) => {
      MovieList.value = response.data
    })
    .catch((error) => {
      console.log(error)
    })
  }
  
  const getWorstMovies = function() {
    return axios({
      method: 'get',
      url: 'http://127.0.0.1:8000/movies/worstmovie/',
    })
    .then((response) => {
      WorstMovieList.value = response.data
    })
    .catch((error) => {
      console.log(error)
    })
  }
  
  const Login = function(payload) {
    const { username, password } = payload
    return axios({
      method: 'post',
      url: 'http://127.0.0.1:8000/accounts/login/',
      data: {
        username, password
      }
    })
    .then((response) => {
      console.log(response.data)
      userkey.value = response.data
      isLogin.value = true
      console.log(response.data);
      localStorage.setItem('userkey', response.data.key)
      localStorage.setItem('isLogin', 'true')
      router.push({ name: 'main' })
    })
    .catch((error) => {
      console.log(error)
    })
  }

  const logOut = () => {
    isLogin.value = false
    userkey.value = null
    localStorage.removeItem('userkey')
    localStorage.removeItem('isLogin')
  }

  return { MovieList, getMovies, userkey, Login, isLogin, logOut,getWorstMovies,WorstMovieList}
}, {
  persist: true 
})
