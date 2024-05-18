<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-6">
        <h2 class="text-center mb-4">회원가입</h2>
        <div class="mb-3">
          <label for="nickname" class="form-label">닉네임</label>
          <input v-model="username" type="nickname"  id="nickname" placeholder="닉네임" />
        </div>
        <div class="mb-3">
          <label for="email" class="form-label">이메일</label>
          <input v-model="username" type="email"  id="email" placeholder="name@example.com" />
        </div>
        <div class="mb-4">
          <label for="password1" class="form-label">비밀번호</label>
          <input v-model="password1" type="password"  id="password1" placeholder="비밀번호" />
        </div>
        <div class="mb-4">
          <label for="password2" class="form-label">비밀번호 확인</label>
          <input type="password"  id="password2"
            placeholder="비밀번호 확인" />
        </div>
        <div class="d-grid">
          <button  class="btn btn-info mt-4">회원가입</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>

</script>

<style></style>
