import { createRouter, createWebHistory } from 'vue-router'

// AI 대시보드
const AIDashboard = () => import('@/views/AIDashboard.vue')

// ERPNext 모듈들
const AccountsModule = () => import('@/views/modules/AccountsModule.vue')
const SalesModule = () => import('@/views/modules/SalesModule.vue')
const PurchaseModule = () => import('@/views/modules/PurchaseModule.vue')
const StockModule = () => import('@/views/modules/StockModule.vue')
const HRModule = () => import('@/views/modules/HRModule.vue')
const ProjectsModule = () => import('@/views/modules/ProjectsModule.vue')
const CRMModule = () => import('@/views/modules/CRMModule.vue')
const SupportModule = () => import('@/views/modules/SupportModule.vue')

// AI 기능 페이지들
const AIFileManager = () => import('@/views/ai/AIFileManager.vue')
const AIWorkflowDesigner = () => import('@/views/ai/AIWorkflowDesigner.vue')
const AIAnalytics = () => import('@/views/ai/AIAnalytics.vue')
const AITraining = () => import('@/views/ai/AITraining.vue')

const routes = [
  // AI 대시보드
  {
    path: '/',
    name: 'AIDashboard',
    component: AIDashboard,
    meta: { 
      title: 'ERPNext AGI System',
      requiresAuth: false,
      icon: 'heroicons:cpu-chip'
    }
  },
  
  // ERPNext 모듈 라우트들
  {
    path: '/accounts',
    name: 'Accounts',
    component: AccountsModule,
    meta: { 
      title: '회계 관리',
      module: 'Accounts',
      requiresAuth: false,
      icon: 'heroicons:calculator'
    }
  },
  {
    path: '/sales',
    name: 'Sales',
    component: SalesModule,
    meta: { 
      title: '영업 관리',
      module: 'Sales',
      requiresAuth: false,
      icon: 'heroicons:chart-bar-square'
    }
  },
  {
    path: '/purchase',
    name: 'Purchase',
    component: PurchaseModule,
    meta: { 
      title: '구매 관리',
      module: 'Purchase',
      requiresAuth: false,
      icon: 'heroicons:shopping-cart'
    }
  },
  {
    path: '/stock',
    name: 'Stock',
    component: StockModule,
    meta: { 
      title: '재고 관리',
      module: 'Stock',
      requiresAuth: false,
      icon: 'heroicons:cube'
    }
  },
  {
    path: '/hr',
    name: 'HR',
    component: HRModule,
    meta: { 
      title: '인사 관리',
      module: 'HR',
      requiresAuth: false,
      icon: 'heroicons:users'
    }
  },
  {
    path: '/projects',
    name: 'Projects',
    component: ProjectsModule,
    meta: { 
      title: '프로젝트 관리',
      module: 'Projects',
      requiresAuth: false,
      icon: 'heroicons:folder'
    }
  },
  {
    path: '/crm',
    name: 'CRM',
    component: CRMModule,
    meta: { 
      title: '고객 관계 관리',
      module: 'CRM',
      requiresAuth: false,
      icon: 'heroicons:user-group'
    }
  },
  {
    path: '/support',
    name: 'Support',
    component: SupportModule,
    meta: { 
      title: '고객 지원',
      module: 'Support',
      requiresAuth: false,
      icon: 'heroicons:chat-bubble-left-right'
    }
  },

  // AI 기능 페이지들
  {
    path: '/ai',
    children: [
      {
        path: 'files',
        name: 'AIFileManager',
        component: AIFileManager,
        meta: { 
          title: 'AI 파일 관리',
          requiresAuth: false,
          icon: 'heroicons:document-magnifying-glass'
        }
      },
      {
        path: 'workflows',
        name: 'AIWorkflowDesigner',
        component: AIWorkflowDesigner,
        meta: { 
          title: 'AI 워크플로 설계',
          requiresAuth: false,
          icon: 'heroicons:squares-plus'
        }
      },
      {
        path: 'analytics',
        name: 'AIAnalytics',
        component: AIAnalytics,
        meta: { 
          title: 'AI 분석',
          requiresAuth: false,
          icon: 'heroicons:chart-pie'
        }
      },
      {
        path: 'training',
        name: 'AITraining',
        component: AITraining,
        meta: { 
          title: 'AI 학습 관리',
          requiresAuth: false,
          icon: 'heroicons:academic-cap'
        }
      }
    ]
  },

  // 대시보드 리다이렉트
  {
    path: '/dashboard',
    redirect: '/'
  },

  // 404 처리
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: AIDashboard,
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