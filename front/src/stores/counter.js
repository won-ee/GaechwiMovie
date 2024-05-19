import { ref } from 'vue'
import { defineStore } from 'pinia'
import { useRouter } from 'vue-router'
import axios from 'axios'

export const useMovieStore = defineStore('movie', () => {
  const MovieList = ref([])
  const userkey = ref(null)
  const isLogin = ref(false)
  const router = useRouter()
  const test = ref(null)
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
      localStorage.setItem('userkey', JSON.stringify(response.data))
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

  return { MovieList, getMovies, userkey, Login, isLogin, logOut }
}, {
  persist: true // 이 줄을 추가하여 상태를 로컬 스토리지에 저장하고 복원합니다.
})
