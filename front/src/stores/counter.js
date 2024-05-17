// import { ref, computed } from 'vue'
// import { defineStore } from 'pinia'
// import axios from'axios'


// export const useMovieStore = defineStore('movie', () => {
//   const MovieList = ref([])
//   const myid = "326ec925602b659f623ccfb9a46396e3"

//   const Movie = ref([])
//   axios({
//     method:'get',
//     url:`https://api.themoviedb.org/3/discover/movie?api_key=${myid}&include_adult=false&include_video=false&language=ko-kr&page=1&sort_by=vote_average.desc&without_genres=99,10755&vote_count.gte=200`,
//   })
//   .then((response) => {
//     MovieList.value = response.data.results
//   })
//   .catch((error) => {
//     console.log(error)
//   })

 

//   const updateMovie= function(id){

//     const options = {
//       method: 'GET',
//       url: `https://api.themoviedb.org/3/movie/${id}`,
//       params: {language: 'en-US'},
//       headers: {
//         accept: 'application/json',
//         Authorization: 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIzMjZlYzkyNTYwMmI2NTlmNjIzY2NmYjlhNDYzOTZlMyIsInN1YiI6IjY2M2Q3ZDZjOTE0ZDU3Mzk3OGE0MTcwNSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.FLkVpZ5-Oy3sFrFpCVurtGQ4vJ-WxnmJhBAzSp7VK-M'
//       }
//     };

//     axios
//       .request(options)
//       .then(function (response) {
//         Movie.value=response.data;
//       })
//       .catch(function (error) {
//         console.error(error);
//       });
//     }

//   return { MovieList,updateMovie,MovieList,Movie }
// })
