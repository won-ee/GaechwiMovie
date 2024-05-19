<template>
  <div class="container">
    <span style="--clr:#eeff00;"></span>
    <span style="--clr:#00ffdd;"></span>
    <span style="--clr:#e900d5;"></span>
    <div class="form-container">
      <h2>Login</h2>
      <div class="input-container">
        <input type="text" placeholder="Username" class="custom-placeholder" v-model="username">
      </div>
      <div class="input-container">
        <input type="password" placeholder="Password" class="custom-placeholder" v-model="password">
      </div>
      <div class="input-container">
        <input type="submit" value="Sign in" class="custom-button" @click="logIn">
      </div>
      <div class="links-container">
        <a href="#" @click="router.push({name:'usersignup'})">Signup</a>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { ref } from 'vue'
import axios from 'axios'

const router = useRouter() 
const username = ref('')
const password = ref('')

const logIn = () => {
  if (!username.value) {
    alert('아이디를 입력해주세요')
    return
  }
  if (!password.value) {
    alert('비밀번호를 입력해주세요')
    return
  }

  const payload = {
    username: username.value,
    password: password.value
  }
  handleLogin(payload)
}

const handleLogin = async () => {
  try {
    const response = await axios.post('http://127.0.0.1:8000/accounts/login/', {
      username: username.value,
      password: password.value
    })

    if (response.status === 200) {
      router.push({ name: 'main' })
    }
  } catch (error) {
    console.error('로그인 에러:', error)
  }
}
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: serif;
}

body {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: -webkit-linear-gradient(to right, #272727, #000000);
  background: linear-gradient(to right, #202020, #000000);
  width: 100%;
  overflow: hidden;
}

.container {
  position: relative;
  width: 500px;
  height: 500px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.container span {
  position: absolute;
  inset: 0;
  border: 2px solid #fff;
  transition: 0.5s;
}

.container span:nth-child(1) {
  border-radius: 38% 62% 63% 37% / 41% 44% 56% 59%;
  animation: animate 6s linear infinite;
}

.container span:nth-child(2) {
  border-radius: 41% 44% 56% 59%/38% 62% 63% 37%;
  animation: animate 4s linear infinite;
}

.container span:nth-child(3) {
  border-radius: 41% 44% 56% 59%/38% 62% 63% 37%;
  animation: animate2 10s linear infinite;
}

.container:hover span {
  border: 6px solid var(--clr);
  filter: drop-shadow(0 0 20px var(--clr));
}

@keyframes animate {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

@keyframes animate2 {
  0% {
    transform: rotate(360deg);
  }
  100% {
    transform: rotate(0deg);
  }
}

.form-container {
  position: absolute;
  width: 300px;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  gap: 20px;
}

.form-container h2 {
  font-size: 2em;
  color: #fff;
}

.input-container {
  position: relative;
  width: 100%;
}

.input-container input {
  position: relative;
  width: 100%;
  padding: 12px 20px;
  background: transparent;
  border: 2px solid #fff;
  border-radius: 40px;
  font-size: 1.2em;
  color: #fff;
  box-shadow: none;
  outline: none;
}

.input-container input[type="submit"] {
  width: 100%;
  background: #0078ff;
  background: -webkit-linear-gradient(to right, #240b36, #c31432);
  background: linear-gradient(to right, #240b36, #c31432);
  border: none;
  cursor: pointer;
}

.input-container input::placeholder {
  color: rgba(255, 255, 255, 0.75);
}

.links-container {
  position: relative;
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 130px;
  
}

.links-container a {
  color: #fff;
  text-decoration: none;
  
}

.custom-placeholder::placeholder {
  font-family: 'Montserrat', sans-serif; 
  color: rgba(255, 255, 255, 0.75);
}
a{
  font-family: 'Montserrat', sans-serif; 
  color: rgba(255, 255, 255, 0.75);
}

.custom-button {
  font-family: 'Montserrat', sans-serif;
  color: #fff;
  border: none; 
  padding: 10px 20px; 
  cursor: pointer; 
}
</style>
