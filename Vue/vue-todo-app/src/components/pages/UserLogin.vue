<template>
    <div class="container">
      <h2>Login</h2>
      <form @submit.prevent="login">
        <div class="form-group">
          <label for="username">Username:</label>
          <input type="text" id="username" v-model="username" class="form-control">
        </div>
        <div class="form-group">
          <label for="password">Password:</label>
          <input type="password" id="password" v-model="password" class="form-control">
        </div>
        <button type="submit" class="btn btn-primary">Login</button>
      </form>
    </div>
  </template>

<script lang="js">
import { defineComponent, ref } from 'vue';
import useAuthStore from '../stores/auth.js';

export default defineComponent({
    setup() {
        const authStore = useAuthStore();
        const username = ref('');
        const password = ref('');

        const login = async () => {
            await authStore.login(username.value, password.value);
        };

        return { username, password, login };
    }
});
</script>
