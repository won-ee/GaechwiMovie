import { createRouter, createWebHistory } from 'vue-router'
import MainView from '@/views/MainView.vue'
import MovieDetailView from'@/views/MovieDetailView.vue'
import ActorDetailView from'@/views/ActorDetailView.vue'
import IndexView from '@/views/IndexView.vue'

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
  ]
})

export default router
