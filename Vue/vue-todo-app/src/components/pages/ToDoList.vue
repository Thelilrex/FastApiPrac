<!-- src/views/Dashboard.vue -->
<template>
  <div>
    <h1>Dashboard</h1>
    <p>Welcome, {{ user?.username }}</p>
    <button @click="logout">Logout</button>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { useAuthStore } from '../stores/auth.ts';

export default defineComponent({
    setup() {
        const authStore = useAuthStore();

        const logout = () => {
            authStore.logout();
        };

        return { user: authStore.user, logout };
    }
});
</script>