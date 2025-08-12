import { createRouter, createWebHistory } from 'vue-router'

// 기본 컴포넌트들
const Dashboard = () => import('@/views/Dashboard.vue')

const routes = [
  // 홈 라우트
  {
    path: '/',
    name: 'Dashboard',
    component: Dashboard,
    meta: { 
      title: 'ERPNext AI 대시보드',
      requiresAuth: false // 개발 단계에서는 인증 비활성화
    }
  },
  
  // 대시보드 라우트 (동일한 컴포넌트)
  {
    path: '/dashboard',
    redirect: '/'
  },

  // 404 처리
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/views/Dashboard.vue'), // 임시로 대시보드로 리다이렉트
    meta: { title: '페이지를 찾을 수 없음' }
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else {
      return { top: 0 }
    }
  }
})

// 페이지 제목 설정
router.beforeEach((to, from, next) => {
  if (to.meta.title) {
    document.title = to.meta.title
  } else {
    document.title = 'ERPNext AI System'
  }
  next()
})

export default router