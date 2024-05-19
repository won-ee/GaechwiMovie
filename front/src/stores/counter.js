import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { useRouter } from 'vue-router' 
import axios from'axios'



export const useMovieStore = defineStore('movie', () => {
  const MovieList = ref([])
  const userkey =ref(null)
  const router = useRouter()
  const isLogin = ref(false)


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

  const Login = function(payload){
    const {username,password} = payload
    return axios({
      method:'post',
      url :'http://127.0.0.1:8000/accounts/login/',
      data:{
        username,password
      }
    })
    .then((response) => {
      userkey.value = response.data
      isLogin.value = true
      router.push({ name: 'main' })
    })
    .catch((error) => {
      console.log(error)
    })
  }
  const logOut=()=>{
    isLogin.value = false
    userkey.value = null
  }
  return {MovieList,getMovies,userkey,Login,isLogin,logOut}
})
