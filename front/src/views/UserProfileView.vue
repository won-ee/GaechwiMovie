<template>
  <main id="main" class="flexbox-col-start-center full-height">
    <div class="view-width full-height">
      <section class="profile-header">
        <div class="profile-header-inner flexbox">
          <div class="phi-info-wrapper flexbox">
            <div class="phi-info-left flexbox">
              <div class="phi-profile-picture-wrapper">
                <div class="phi-profile-picture-inner flexbox">
                  <img class="phi-profile-picture" :src="profileSrc" alt="Profile Picture">
                </div>
              </div>
              <div class="phi-profile-username-wrapper flexbox-col-left">
                <h3 class="phi-profile-username flexbox">{{ profile.username }}<span class="material-icons-round">verified</span></h3>
              </div>
            </div>
          </div>
          <div class="profile-header-overlay"></div>
          <img class="profile-header-image" :src="profileheaderSrc" alt="Header Image">
        </div>
      </section>
      <section class="profile-page no-margin">
        <h3 style="margin-left: 60px; margin-top: 50px;">{{ profile.username }} like movie</h3>
        <div class="profile-page-inner">
          <div v-if="movielist.length" class="profile-page-grid">
            <div class="profile-page-item" v-for="movie in movielist" :key="movie.pk">
              <img 
                class="profile-page-item-image"
                :src="getImageUrl(movie.poster_image)"
                alt="..."
                @click="goToMovieDetail(movie.pk)"
              />
            </div>
          </div>
          <div v-else>
            좋아하는 영화가 없습니다.
          </div>
        </div>
      </section>
      <section class="profile-page no-margin">
        <h3 style="margin-left: 60px;">{{ profile.username }} dislike movie</h3>
        <div class="profile-page-inner">
          <div v-if="worstlist.length" class="profile-page-grid">
            <div class="profile-page-item" v-for="movie in worstlist" :key="movie.pk">
              <img 
                class="profile-page-item-image"
                :src="getImageUrl(movie.poster_image)"
                alt="..."
                @click="goToMovieDetail(movie.pk)"
              />
            </div>
          </div>
          <div v-else>
            싫어하는 영화가 없습니다.
          </div>
        </div>
      </section>
    </div>
  </main>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import profileSrc from '@/assets/profile.png';
import profileheaderSrc from '@/assets/profileheader.jpg';
import { useRouter } from 'vue-router';
import axios from 'axios';

const router = useRouter();
const profile = ref({});
const userkey = ref(null);
const userid = localStorage.getItem('userid');
const movielist = ref([]);
const worstlist = ref([]);

const loadUserKey = async () => {
  userkey.value = localStorage.getItem('userkey');
};

const userProfile = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:8000/accounts/user/', {
      headers: { Authorization: `Token ${userkey.value}` },
    });
    profile.value = response.data;
  } catch (error) {
    console.error(error);
  }
};

const getMovie = async () => {
  try {
    const response = await axios.get(`http://127.0.0.1:8000/movies/${userid}/user_like_movie`);
    movielist.value = response.data.like_movies;
  } catch (error) {
    console.error(error);
  }
};

const getWorst = async () => {
  try {
    const response = await axios.get(`http://127.0.0.1:8000/movies/${userid}/user_dislike_movie`);
    worstlist.value = response.data.dislike_movies;
  } catch (error) {
    console.error(error);
  }
};

const getImageUrl = (path) => {
  return path ? `https://image.tmdb.org/t/p/w500${path}` : '';
};

const goToMovieDetail = (movieId) => {
  router.push({ name: 'moviedetail', params: { movieId } });
};

onMounted(async () => {
  await loadUserKey();
  await userProfile();
  await getMovie();
  await getWorst();
});
</script>

<style scoped>
html, body, #main {
  height: 100%;
  margin: 0;
  padding: 0;
}
.full-height {
  height: 100%;
}
.flexbox {
  display: flex;
  justify-content: center;
  align-items: center;
}
.flexbox-col-start-center {
  display: flex;
  flex-direction: column;
  align-items: center;
  height: 100%;
}
.view-width {
  width: 100%;
}
.profile-header {
  width: 100%;
  position: relative;
}
.profile-header-inner {
  width: 100%;
  position: relative;
  overflow: hidden;
  z-index: 2;
}
.profile-header-overlay {
  width: 100%;
  height: 100%;
  position: absolute;
  background: linear-gradient(hsla(var(--background), .33) 0%, hsla(var(--background), .77) 50%, hsla(var(--background), 1) 100%);
  z-index: 3;
}
.profile-header-image {
  opacity: 60%;
  min-width: 100%;
  max-width: 100%;
  max-height: 100%;
  min-height: 100%;
  position: absolute;
  filter: hue-rotate(-5deg) saturate(1.25);
  object-fit: cover;
}
.phi-info-wrapper {
  padding: 4em 4em 8em 4em;
  width: 100%;
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 2em;
  z-index: 5;
}
.phi-info-left {
  width: 100%;
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 2em;
  z-index: 5;
}
.phi-profile-picture-wrapper {
  width: 10em;
  height: 10em;
  position: relative;
}
.phi-profile-picture-inner {
  width: 100%;
  height: 100%;
  position: relative;
  border-radius: 50%;
  overflow: hidden;
  z-index: 6;
}
.phi-profile-picture {
  min-width: 100%;
  max-width: 105%;
  min-height: 100%;
  position: absolute;
  object-fit: cover;
}
.phi-profile-username span {
  margin: 0 0 0 .3em;
}
.phi-profile-tagline {
  color: hsl(var(--grooble));
}
.profile-page {
  margin: 5em 0;
  width: 100%;
}
.no-margin {
  margin-top: 0;
}
.profile-page > h3 {
  font-size: var(--paragraph);
  text-transform: uppercase;
  margin: 0;
}
.profile-page-inner {
  margin: 1.5em 0;
  display: flex;
  flex-wrap: wrap;
  gap: 0;
}
.profile-page-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 0;
  justify-content: center;
}
.profile-page-item {
  width: 200px; 
  height: 300px; 
  position: relative;
  cursor: pointer;
}
.profile-page-item-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  vertical-align: bottom;
}
</style>
