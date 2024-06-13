<template>
  <div class="container">
    <h2>Register</h2>
    <form @submit.prevent="register" ref="form">
      <div class="form-group">
        <label for="email">Email:</label>
        <input type="email" id="email" v-model="email" class="form-control" required>
      </div>
      <div class="form-group">
        <label for="username">Username:</label>
        <input type="text" id="username" v-model="username" class="form-control" required>
      </div>
      <div class="form-group">
        <label for="password">Password:</label>
        <input type="password" id="password" v-model="password" class="form-control" required>
      </div>
      <div v-if="error" class="alert alert-danger">{{ error }}</div>
      <button type="submit" class="btn btn-primary">Register</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'UserRegister',
  data() {
    return {
      email: '',
      username: '',
      password: '',
      error: null
    };
  },
  methods: {
    async register() {
      try {
        const response = await axios.post('/register', {
          email: this.email,
          username: this.username,
          password: this.password
        });
        console.log(response.data);
        // Reset form after successful registration
        this.$refs.form.reset();
        this.$router.push('/login');
      } catch (error) {
        this.error = error.response.data.message || 'Registration failed.';
        console.error(error);
      }
    }
  }
};
</script>
