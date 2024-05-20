<template>
  <div class="container">
    <span style="--clr:#eeff00;"></span>
    <span style="--clr:#00ffdd;"></span>
    <span style="--clr:#e900d5;"></span>
    <div class="form-container">
      <h2>Sign Up</h2>
      <div class="input-container">
        <input type="text" class="custom-placeholder" placeholder="username" v-model="username" @keydown.enter="SignUp">
      </div>
      <div class="input-container">
        <input type="password"  class="custom-placeholder" placeholder="Password" v-model="password" @keydown.enter="SignUp">
      </div>
      <div class="input-container" >
        <input type="password" class="custom-placeholder" placeholder="Confirm Password" v-model="confirmPassword" @input="checkPasswordMatch" @keydown.enter="SignUp">
        <span v-if="password && confirmPassword && password !== confirmPassword" style="color: red; font-family: 'Montserrat', sans-serif;">Passwords do not match</span>
      </div>
      <div class="input-container">
        <input type="submit" class="custom-button" value="Sign Up" 
        @click="SignUp()">
      </div>
      <div class="links-container">
        <a href="#"  @click="router.push({name:'userlogin'})"> Already have an account?</a>
        <a href="#"  @click="router.push({name:'userlogin'})"> Log in</a>
      </div>
    </div>
  </div>
</template>

<script setup>
import axios from 'axios'
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter() 
const password = ref('')
const confirmPassword = ref('')
const username =ref('')


function SignUp() {

  if (password.value.length <8){
    alert("비밀번호를 8자리 이상 입력해 주세요.")
  }
  if (password.value !== confirmPassword.value) {
    alert("Passwords do not match");
    return
  }

  const payload = {
    username: username.value,
    password1: password.value,
    password2: confirmPassword.value,
    
  }
  signUpUser(payload)
}

const signUpUser = async (payload) => {
  try {
    const response = await axios.post("http://127.0.0.1:8000/accounts/signup/", payload);
    if (response.status === 204) {
        router.push({ name: "userlogin" });
    }
  } catch (error) {
    console.log(error)
}}

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
  width: 600px;
  height: 600px; 
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
  padding: 0 20px;
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
