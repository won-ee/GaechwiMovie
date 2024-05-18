import { createRouter, createWebHistory } from 'vue-router'
import MainView from '@/views/MainView.vue'
import MovieDetailView from'@/views/MovieDetailView.vue'
import ActorDetailView from'@/views/ActorDetailView.vue'
import IndexView from '@/views/IndexView.vue'
import MovieRecommendView from '@/views/MovieRecommendView.vue'
import MovieChoiceView from '@/views/MovieChoiceView.vue'
import UserLoginView from '@/views/UserLoginView.vue'
import UserSignUpView from '@/views/UserSignUpView.vue'
import UserProfileView from '@/views/UserProfileView.vue'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'main',
      component: MainView
    },
    {
      path: '/moviedetail/:movieId',
      name: 'moviedetail',
      component: MovieDetailView
    },
    {
      path: '/actordetail/',
      name: 'actordetail',
      component: ActorDetailView
    },
    {
      path: '/indexView/:name',
      name: 'indexView',
      component: IndexView
    },
    {
      path: '/movierecommend',
      name: 'movierecommend',
      component: MovieRecommendView
    },
    {
      path: '/moviechoice',
      name: 'moviechoice',
      component: MovieChoiceView
    },
    {
      path: '/userlogin',
      name: 'userlogin',
      component: UserLoginView
    },
    {
      path: '/usersignup',
      name: 'usersignup',
      component: UserSignUpView
    },
    {
      path: '/userprofile',
      name: 'userprofile',
      component: UserProfileView
    },
  ]
})

export default router
