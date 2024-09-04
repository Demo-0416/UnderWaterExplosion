import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/detail',
      name: 'detail',
      component: () => import('@/views/Home.vue')
    },
    {
      path: '/',
      name: 'login',
      component: () => import('@/views/Login.vue')
    },
    {
      path: '/list',
      name: 'list',
      component: () => import('@/views/List.vue')
    }, {
      path: '/boat',
      name: 'boat',
      component: () => import('@/components/three.vue')
    }
  ]
})

export default router