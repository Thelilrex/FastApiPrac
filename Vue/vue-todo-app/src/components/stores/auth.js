import { defineStore } from 'pinia';
import axios from 'axios';
import { router } from '@/router';

const useAuthStore = defineStore('auth', {
    state: () => ({
        token: null,
        user: null,
    }),
    actions: {
        async login(username, password) {
            try {
                const response = await axios.post('http://localhost:8000/token', { username, password });
                this.token = response.data.access_token;
                axios.defaults.headers.common['Authorization'] = `Bearer ${this.token}`;
                await this.fetchUser();
                router.push('/dashboard');
            } catch (error) {
                console.error('Failed to login:', error);
            }
        },
        async fetchUser() {
            if (!this.token) return;
            try {
                const response = await axios.get('/users/me');
                this.user = response.data;
            } catch (error) {
                console.error('Failed to fetch user:', error);
            }
        },
        logout() {
            this.token = null;
            this.user = null;
            delete axios.defaults.headers.common['Authorization'];
            router.push('/login');
        }
    }
});

export default useAuthStore;