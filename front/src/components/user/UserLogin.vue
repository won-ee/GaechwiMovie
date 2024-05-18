<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-6">
        <div class="text-center mb-4">
          <h2>로그인</h2>
        </div>
        <div class="mb-3">
          <label for="email" class="form-label">이메일</label>
          <input v-model="username" type="email" id="email" placeholder="you@example.com" />
        </div>
        <div class="mb-3">
          <label for="password" class="form-label">비밀번호</label>
          <input type="password" class="form-control" id="password" />
        </div>
        <div class="d-grid gap-2">
          <button class="btn btn-info mt-4">로그인</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>

</script>

<style></style>
