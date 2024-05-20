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
      userkey.value = response.data
      isLogin.value = true
      localStorage.setItem('userkey', response.data.key)
      localStorage.setItem('isLogin', 'true')
      router.push({ name: 'main' })
      userProfile(response.data.key)
    })
    .catch((error) => {
      console.log(error)
    })
  }

  const userProfile = function(key){

    axios({
      method:'get',
      url:'http://127.0.0.1:8000/accounts/user/',
      headers: {Authorization: `Token ${key}`}
    })
    .then((response) => {
      localStorage.setItem('userid', response.data.pk)
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
    localStorage.removeItem('userid')
  }

  return { MovieList, getMovies, userkey, Login, isLogin, logOut,getWorstMovies,WorstMovieList}
}, {
  persist: true 
})
