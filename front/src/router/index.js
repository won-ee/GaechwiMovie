import { createRouter, createWebHistory } from 'vue-router'
import MainView from '@/views/MainView.vue'
import CommunityView from '@/views/CommunityView.vue'
import DetailView from'@/views/DetailView.vue'
import IndexView from '@/views/IndexView.vue'
import LoginView from '@/views/LoginView.vue'
import RandomView from '@/views/RandomView.vue'
import RecommendView from '@/views/RecommendView.vue'
import SignUpView from '@/views/SignUpView.vue'



const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'main',
      component: MainView
    },
    {
      path: '/community/',
      name: 'community',
      component: CommunityView
    },
    {
      path: '/detail/',
      name: 'detail',
      component: DetailView
    },
    {
      path: '/index/',
      name: 'index',
      component: IndexView
    },
    {
      path: '/login/',
      name: 'login',
      component: LoginView
    },
    {
      path: '/randam/',
      name: 'randam',
      component: RandomView
    },
    {
      path: '/recommend/',
      name: 'recommend',
      component: RecommendView
    },
    {
      path: '/signup/',
      name: 'signup',
      component: SignUpView
    },
  ]
})

export default router
