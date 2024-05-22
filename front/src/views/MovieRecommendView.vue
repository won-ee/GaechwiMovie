<template>
  <div class="title">
    <h1>영화 추천</h1>
  </div>
  <button class="nextpage">다시 추천해주세요</button>
  <div class="movie-container" v-if="movielist.length">
    <div class="movie-list-wrapper">
      <div class="movie-list">
        <MovieCard
          class="movie-item"
          v-for="movie in movielist"
          :key="movie.id"
          :movie="movie"
        />
      </div>
      <i class="fas fa-chevron-right arrow"></i>
    </div>
  </div>
  <div class="bubbleContainer">
    <div class="bubbleBody">
      <div class="chat">
        <div v-for="(chat, index) in chatlog" :key="'chat' + index" class="chat-message">
          <div class="mychat" v-if="chat.my">{{ chat.my }}</div>
          <div class="gptchat" v-if="chat.gpt">{{ chat.gpt }}</div>
        </div>
       
        <input 
          type="text" 
          v-model="inputchat" 
          name="formUsername" 
          placeholder="채팅을 시작하세요..."
          @keydown.enter="chat()">
      </div>
      <button class="btnSendMessage" type="submit" @click="chat()">Send</button>
    </div>
  </div>
</template>

<script setup>
import axios from 'axios'
import { ref, onMounted } from 'vue'
import MovieCard from '@/components/movie/MovieCard.vue'

const movielist = ref([])
const userid = localStorage.getItem('userid')
let pagepk = 1

const fetchData = async () => {
  try {
    const response = await axios.get(`http://127.0.0.1:8000/movies/${userid}/recommended/${pagepk}/`)
    movielist.value = response.data
  } catch (error) {
    console.error(error)
  }
}

onMounted(async () => {
  await fetchData()

  const nextpage = document.querySelector('.nextpage')

  nextpage.addEventListener('click', () => {
    pagepk += 1
    fetchData()
  })

  const arrows = document.querySelectorAll(".arrow")
  const movieLists = document.querySelectorAll(".movie-list")

  arrows.forEach((arrow, i) => {
    const itemNumber = movieLists[i].querySelectorAll(".movie-item").length
    let clickCounter = 0

    arrow.addEventListener("click", () => {
      const ratio = Math.floor(window.innerWidth / 270)
      clickCounter++
      const currentTransform = window.getComputedStyle(movieLists[i]).transform
      const matrix = currentTransform !== 'none' ? currentTransform : 'matrix(1, 0, 0, 1, 0, 0)'
      const translateX = parseInt(matrix.split(',')[4].trim())

      if (itemNumber - (4 + clickCounter) + (4 - ratio) >= 0) {
        movieLists[i].style.transform = `translateX(${translateX - 300}px)`
      } else {
        movieLists[i].style.transform = "translateX(0)"
        clickCounter = 0
      }
    })
  })
})

const inputchat = ref('')
const chatlog = ref([])

const chat = async function() {
  const api = 'https://api.openai.com/v1/chat/completions'
  const key = 'sk-proj-2y5MeZ5AwEShg3zqkkbET3BlbkFJMURTlOkcUQlACUtQ8OdU'
  
  try {
    const res = await axios.post(api, {
      model: 'gpt-3.5-turbo',
      messages: [{ role: 'user', content: inputchat.value }],
    }, {
      headers: { Authorization: `Bearer ${key}`, 'Content-Type': 'application/json' }
    })
    chatlog.value.push({my: inputchat.value, gpt: res.data.choices[0].message.content})
  } catch (err) {
    chatlog.value.push({my: inputchat.value, gpt: '고장'})
    console.error(err)
  }
  
  inputchat.value = ''
}
</script>

<style scoped>
.title {
  margin-top: 5px;
  margin-left: 20px;
  color: #fff;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
}

img {
  width: 200px;
}

.movie-list-wrapper {
  position: relative;
  overflow: hidden;
}

.movie-list {
  display: flex;
  align-items: center;
  height: 300px;
  transform: translateX(0);
  transition: all 1s ease-in-out;
}

.arrow {
  font-size: 120px;
  position: absolute;
  top: 90px;
  right: 0;
  color: lightgray;
  opacity: 0.5;
  cursor: pointer;
}

.movie-container {
  margin-top: 20px;
}

.nextpage {
  position: fixed;
  width: 200px;
  height: 60px;
  margin-top: 80px;
  border: 0;
  background-color: rgba(255, 255, 255, 0.2);
  border-radius: 12px;
  color: white !important;
  top: 5px;
  left: 200px;
  opacity: 70%;
}

.bubbleContainer {
  position: relative;
  width: 60vw;
  height: 450px;
  margin: 50px auto 0;
  margin-top: 5px;
}

.bubbleBody {
  position: relative;
  width: 100%;
  height: 100%;
  background-color: rgba(255, 255, 255, 0.3);
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  padding: 20px;
  box-sizing: border-box;
  overflow-y: auto;
}

.chat {
  display: flex;
  flex-direction: column;
}

.chat-message {
  display: flex;
  flex-direction: column;
  margin-bottom: 10px;
}

.mychat, .gptchat {
  max-width: 70%;
  padding: 10px 15px;
  border-radius: 10px;
  margin: 5px 0;
  color: white;
  word-wrap: break-word;
}

.mychat {
  align-self: flex-start;
  background-color: #0d6efd;
  text-align: left;
  border-bottom-left-radius: 0;
}

.gptchat {
  align-self: flex-end;
  background-color: #6c757d;
  text-align: right;
  border-bottom-right-radius: 0;
}

input {
  position: absolute;
  bottom: 5px;
  width: 75%;
  height: 50px;
  border: none;
  background-color: rgba(255, 255, 255, 0);
  color: white;
  padding: 10px;
  box-sizing: border-box;
}

input::placeholder {
  color: rgba(255, 255, 255, 0.5);
}

.btnSendMessage {
  position: absolute;
  bottom: 10px;
  right: 10px;
  width: 100px;
  height: 40px;
  background-color: #0d6efd;
  border: none;
  border-radius: 12px;
  color: white !important;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.btnSendMessage:hover {
  background-color: #084298;
}
</style>
