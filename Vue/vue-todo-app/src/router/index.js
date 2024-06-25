import useAuthStore from '../components/stores/auth.js';
import { createRouter, createWebHistory } from 'vue-router';

// Define your route components
const UserRegister = () => import('../components/pages/UserRegister.vue');
const UserLogin = () => import('../components/pages/UserLogin.vue');
const ToDoList = () => import('../components/pages/ToDoList.vue');

const routes = [
    { path: '/', component: UserRegister },
    { path: '/login', component: UserLogin },
    {
        path: '/dashboard',
        component: ToDoList,
        meta: { requiresAuth: true },
    },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

router.beforeEach((to, from, next) => {
    const authStore = useAuthStore();
    if (to.meta.requiresAuth && !authStore.token) {
        next('/login');
    } else {
        next();
    }
});

export {router};
