<template>
  <div class="container">
    <div class="movie-list-container">
      <h1 class="movie-list-title">GAECHWI's Movie Recommend</h1>
      <button class="nextpage">다시 추천해주세요</button>
      <div class="movie-list-wrapper">
        <div class="movie-list" v-if="movielist.length">
          <MovieCard
            class="movie-item"
            v-for="movie in movielist"
            :key="movie.id"
            :movie="movie"
          />
        </div>
        <p v-else>검색 결과가 없습니다.</p>
        <i class="fas fa-chevron-right arrow"></i>
      </div>
      <h1 class="gpt-list-title">Chat GPT's Movie Recommend</h1>
      <div class="gpt-list-wrapper">
        <div class="gpt-list" v-if="gptlist.length">
          <gptcard
            class="gpt-item"
            v-for="movie in gptlist"
            :key="movie.id"
            :movie="movie"
          />
        </div>
        <p v-else>검색 결과가 없습니다.</p>
        <i class="fas fa-chevron-right gpt-arrow"></i>
      </div>
    </div>
    <div class="bubbleContainer">
      <h1>Chat GPT Chat-bot</h1>
      <div class="bubbleBody">
        <div class="chat">
          <div
            v-for="(chat, index) in chatlog"
            :key="'chat' + index"
            class="chat-message"
          >
            <div class="mychat" v-if="chat.my">{{ chat.my }}</div>
            <div class="gptchat" v-if="chat.gpt">{{ chat.gpt }}</div>
          </div>
        </div>
        <div class="chat-input-container">
          <input
            type="text"
            v-model="inputchat"
            name="formUsername"
            placeholder="채팅을 시작하세요..."
            @keydown.enter="chat()"
          />
          <button class="btnSendMessage" type="submit" @click="chat()">Send</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import axios from 'axios';
import { ref, onMounted, nextTick } from 'vue';
import MovieCard from '@/components/movie/MovieCard.vue';
import gptcard from '@/components/movie/gptcard.vue';

const movielist = ref([]);
const chatmovielist = ref([]);
const userid = localStorage.getItem('userid');
let pagepk = 1;

const fetchData = async () => {
  try {
    const response = await axios.get(`http://127.0.0.1:8000/movies/${userid}/recommended/${pagepk}/`);
    movielist.value = response.data;
    console.log(response.data);
  } catch (error) {
    console.error(error);
  }
};

const inputchat = ref('');
const chatlog = ref([]);
const chatrecommendlist = ref([]);

const chatrecommend = async function () {
  const api = '';
  const key = ''
  try {
    const res = await axios.post(api, {
      model: 'gpt-4o',
      messages: [{
        role: 'user',
        content: `${chatmovielist.value}를 기반으로 영화를 추천해 주는데 ${chatmovielist.value} 영화는 빼고 추천해줘 
        ''사이의 문자를 tmbd movie id로 바꿔서 10개만 담에서 []만 보내줘 ${chatmovielist.value}영화가 너가 보내주는 리스트에 들어있다면 다 빼줘`
      }],
    }, {
      headers: { Authorization: `Bearer ${key}`, 'Content-Type': 'application/json' }
    });
    chatrecommendlist.value = res.data.choices[0].message.content.match(/\d+/g).map(Number);
    console.log(chatrecommendlist.value);
  } catch (err) {
    chatlog.value.push({ my: inputchat.value, gpt: '고장' });
    console.error(err);
  }
  inputchat.value = '';
};

const chat = async function () {
  try {
    const res = await axios.post(api, {
      model: 'gpt-4o',
      messages: [{ role: 'user', content: inputchat.value }],
    }, {
      headers: { Authorization: `Bearer ${key}`, 'Content-Type': 'application/json' }
    });
    chatlog.value.push({ my: inputchat.value, gpt: res.data.choices[0].message.content });
  } catch (err) {
    chatlog.value.push({ my: inputchat.value, gpt: '고장' });
    console.error(err);
  }
  inputchat.value = '';
};

const gptlist = ref([]);
const myid = '';

const gptMovie = async () => {
  for (const movieid of chatrecommendlist.value) {
    console.log(movieid);
    const options = {
      method: 'GET',
      url: `https://api.themoviedb.org/3/movie/${movieid}?api_key=${myid}`,
      params: { language: 'ko-KR' },
      headers: {
        accept: 'application/json',
        Authorization: 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIzMjZlYzkyNTYwMmI2NTlmNjIzY2NmYjlhNDYzOTZlMyIsInN1YiI6IjY2M2Q3ZDZjOTE0ZDU3Mzk3OGE0MTcwNSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.FLkVpZ5-Oy3sFrFpCVurtGQ4vJ-WxnmJhBAzSp7VK-M'
      }
    };
    try {
      const response = await axios.request(options);
      gptlist.value.push(response.data);
    } catch (error) {
      console.error(error);
    }
  }
};

const getlikeMovie = async () => {
  try {
    const response = await axios.get(`http://127.0.0.1:8000/movies/${localStorage.getItem('userid')}/user_like_movie`);

    response.data.like_movies.forEach(element => {
      chatmovielist.value.push(element.title);
    });
    console.log(chatmovielist.value);
  } catch (error) {
    console.error(error);
  }
};

onMounted(async () => {
  await fetchData();
  await getlikeMovie();
  await chatrecommend();
  await gptMovie();

  const nextpage = document.querySelector('.nextpage');
  nextpage.addEventListener('click', async () => {
    pagepk += 1;
    await fetchData();
    await chatrecommend();
    await gptMovie();
  });

  await nextTick(() => {
    const arrows = document.querySelectorAll(".arrow");
    const movieLists = document.querySelectorAll(".movie-list");

    arrows.forEach((arrow, i) => {
      const itemNumber = movieLists[i].querySelectorAll(".movie-item").length;
      let clickCounter = 0;

      arrow.addEventListener("click", () => {
        const ratio = Math.floor(window.innerWidth / 270);
        clickCounter++;
        const currentTransform = window.getComputedStyle(movieLists[i]).transform;
        const matrix = currentTransform !== 'none' ? currentTransform : 'matrix(1, 0, 0, 1, 0, 0)';
        const translateX = parseInt(matrix.split(',')[4].trim());

        if (itemNumber - (4 + clickCounter) + (4 - ratio) >= 0) {
          movieLists[i].style.transform = `translateX(${translateX - 300}px)`;
        } else {
          movieLists[i].style.transform = "translateX(0)";
          clickCounter = 0;
        }
      });
    });
  });

  await nextTick(() => {
    const arrows = document.querySelectorAll(".gpt-arrow");
    const gptLists = document.querySelectorAll(".gpt-list");

    arrows.forEach((arrow, i) => {
      const itemNumber = gptLists[i].querySelectorAll(".gpt-item").length;
      let clickCounter = 0;

      arrow.addEventListener("click", () => {
        const ratio = Math.floor(window.innerWidth / 270);
        clickCounter++;
        const currentTransform = window.getComputedStyle(gptLists[i]).transform;
        const matrix = currentTransform !== 'none' ? currentTransform : 'matrix(1, 0, 0, 1, 0, 0)';
        const translateX = parseInt(matrix.split(',')[4].trim());

        if (itemNumber - (4 + clickCounter) + (4 - ratio) >= 0) {
          gptLists[i].style.transform = `translateX(${translateX - 300}px)`;
        } else {
          gptLists[i].style.transform = "translateX(0)";
          clickCounter = 0;
        }
      });
    });
  });
});
</script>

<style scoped>
.container {
  background-color: #151515;
  min-height: calc(100vh - 50px);
  color: white;
  transition: 1s ease all;
  padding: 20px;
  height: 100%;
  box-sizing: border-box;
}
.movie-list-container {
  padding: 20px 0;
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
.gpt-list-wrapper {
  position: relative;
  overflow: hidden;
}

.gpt-list {
  display: flex;
  align-items: center;
  height: 300px;
  transform: translateX(0);
  transition: all 1s ease-in-out;
}
.arrow {
  font-size: 50px;
  position: absolute;
  top: 50%;
  right: 0;
  transform: translateY(-50%);
  color: lightgray;
  opacity: 0.5;
  cursor: pointer;
}
.gpt-arrow {
  font-size: 50px;
  position: absolute;
  top: 50%;
  right: 0;
  transform: translateY(-50%);
  color: lightgray;
  opacity: 0.5;
  cursor: pointer;
}
.nextpage {
  display: block;
  position: absolute;
  top: 95px;
  right: 10%;
  width: 200px;
  height: 60px;
  margin: 20px 0;
  border: 0;
  background-color: rgba(255, 255, 255, 0.2);
  border-radius: 12px;
  color: white !important;
  opacity: 70%;
  cursor: pointer;
  text-align: center;
  line-height: 60px;
}

.bubbleContainer {
  width: 60vw;
  height: 600px;
  margin: 50px auto 0;
  background-color: rgba(255, 255, 255, 0.1);
  border-radius: 10px;
  padding: 20px;
  box-sizing: border-box;
}

.bubbleBody {
  width: 100%;
  height: 93%;
  background-color: rgba(255, 255, 255, 0.3);
  border-radius: 10px;
  padding: 20px;
  display: flex;
  flex-direction: column;
}

.chat {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow-y: auto;
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

.chat-input-container {
  display: flex;
  align-items: center;
  margin-top: 10px;
}

input {
  flex: 1;
  height: 50px;
  border: none;
  background-color: rgba(255, 255, 255, 0.1);
  color: white;
  padding: 10px;
  box-sizing: border-box;
  border-radius: 10px;
}

input::placeholder {
  color: rgba(255, 255, 255, 0.5);
}

.btnSendMessage {
  width: 100px;
  height: 40px;
  background-color: #0d6efd;
  border: none;
  border-radius: 12px;
  color: white !important;
  margin-left: 10px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.btnSendMessage:hover {
  background-color: #084298;
}
</style>
