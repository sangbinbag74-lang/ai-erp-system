import { createRouter, createWebHistory } from 'vue-router'

// 레이아웃
const DefaultLayout = () => import('@/core/layouts/DefaultLayout.vue')

// 페이지 컴포넌트들
const Home = () => import('@/views/Home.vue')
const Dashboard = () => import('@/views/Dashboard.vue')
const Login = () => import('@/views/auth/Login.vue')

// Accounts 모듈
const AccountsDashboard = () => import('@/views/accounts/Dashboard.vue')
const CustomerList = () => import('@/views/accounts/CustomerList.vue')
const CustomerForm = () => import('@/views/accounts/CustomerForm.vue')

// Sales 모듈
const SalesDashboard = () => import('@/views/sales/Dashboard.vue')
const SalesOrderList = () => import('@/views/sales/SalesOrderList.vue')
const SalesOrderForm = () => import('@/views/sales/SalesOrderForm.vue')

// Purchase 모듈
const PurchaseDashboard = () => import('@/views/purchase/Dashboard.vue')
const SupplierList = () => import('@/views/purchase/SupplierList.vue')
const PurchaseOrderList = () => import('@/views/purchase/PurchaseOrderList.vue')

// Stock 모듈
const StockDashboard = () => import('@/views/stock/Dashboard.vue')
const ItemList = () => import('@/views/stock/ItemList.vue')
const ItemForm = () => import('@/views/stock/ItemForm.vue')
const WarehouseList = () => import('@/views/stock/WarehouseList.vue')
const StockEntryList = () => import('@/views/stock/StockEntryList.vue')

// HR 모듈
const HRDashboard = () => import('@/views/hr/Dashboard.vue')
const EmployeeList = () => import('@/views/hr/EmployeeList.vue')
const EmployeeForm = () => import('@/views/hr/EmployeeForm.vue')
const AttendanceList = () => import('@/views/hr/AttendanceList.vue')

// Projects 모듈
const ProjectsDashboard = () => import('@/views/projects/Dashboard.vue')
const ProjectList = () => import('@/views/projects/ProjectList.vue')
const ProjectForm = () => import('@/views/projects/ProjectForm.vue')
const TaskList = () => import('@/views/projects/TaskList.vue')
const TimesheetList = () => import('@/views/projects/TimesheetList.vue')

// CRM 모듈
const CRMDashboard = () => import('@/views/crm/Dashboard.vue')
const LeadList = () => import('@/views/crm/LeadList.vue')
const OpportunityList = () => import('@/views/crm/OpportunityList.vue')

// Manufacturing 모듈
const ManufacturingDashboard = () => import('@/views/manufacturing/Dashboard.vue')

// Support 모듈
const SupportDashboard = () => import('@/views/support/Dashboard.vue')

// Assets 모듈
const AssetsDashboard = () => import('@/views/assets/Dashboard.vue')

// Quality 모듈
const QualityDashboard = () => import('@/views/quality/Dashboard.vue')

// Website 모듈
const WebsiteDashboard = () => import('@/views/website/Dashboard.vue')

// 설정 및 기타
const Profile = () => import('@/views/settings/Profile.vue')
const Settings = () => import('@/views/settings/Settings.vue')
const NotFound = () => import('@/views/errors/NotFound.vue')

const routes = [
  // 인증
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: {
      requiresAuth: false,
      layout: 'auth'
    }
  },

  // 메인 레이아웃을 사용하는 라우트들
  {
    path: '/',
    component: DefaultLayout,
    meta: { requiresAuth: true },
    children: [
      // 홈 및 대시보드
      {
        path: '',
        name: 'Home',
        component: Home,
        meta: { title: '홈' }
      },
      {
        path: '/dashboard',
        name: 'Dashboard', 
        component: Dashboard,
        meta: { title: '대시보드' }
      },

      // Accounts 모듈
      {
        path: '/accounts',
        name: 'AccountsModule',
        children: [
          {
            path: '',
            name: 'AccountsDashboard',
            component: AccountsDashboard,
            meta: { title: '회계 대시보드' }
          },
          {
            path: 'customers',
            name: 'CustomerList',
            component: CustomerList,
            meta: { title: '고객 목록' }
          },
          {
            path: 'customers/new',
            name: 'CustomerCreate',
            component: CustomerForm,
            meta: { title: '고객 생성' }
          },
          {
            path: 'customers/:id',
            name: 'CustomerEdit',
            component: CustomerForm,
            props: true,
            meta: { title: '고객 수정' }
          }
        ]
      },

      // Sales 모듈
      {
        path: '/sales',
        name: 'SalesModule',
        children: [
          {
            path: '',
            name: 'SalesDashboard',
            component: SalesDashboard,
            meta: { title: '영업 대시보드' }
          },
          {
            path: 'orders',
            name: 'SalesOrderList',
            component: SalesOrderList,
            meta: { title: '주문서 목록' }
          },
          {
            path: 'orders/new',
            name: 'SalesOrderCreate',
            component: SalesOrderForm,
            meta: { title: '주문서 생성' }
          },
          {
            path: 'orders/:id',
            name: 'SalesOrderEdit',
            component: SalesOrderForm,
            props: true,
            meta: { title: '주문서 수정' }
          }
        ]
      },

      // Purchase 모듈
      {
        path: '/purchase',
        name: 'PurchaseModule',
        children: [
          {
            path: '',
            name: 'PurchaseDashboard',
            component: PurchaseDashboard,
            meta: { title: '구매 대시보드' }
          },
          {
            path: 'suppliers',
            name: 'SupplierList',
            component: SupplierList,
            meta: { title: '공급업체 목록' }
          },
          {
            path: 'orders',
            name: 'PurchaseOrderList',
            component: PurchaseOrderList,
            meta: { title: '구매주문 목록' }
          }
        ]
      },

      // Stock 모듈
      {
        path: '/stock',
        name: 'StockModule', 
        children: [
          {
            path: '',
            name: 'StockDashboard',
            component: StockDashboard,
            meta: { title: '재고 대시보드' }
          },
          {
            path: 'items',
            name: 'ItemList',
            component: ItemList,
            meta: { title: '제품 목록' }
          },
          {
            path: 'items/new',
            name: 'ItemCreate',
            component: ItemForm,
            meta: { title: '제품 생성' }
          },
          {
            path: 'items/:id',
            name: 'ItemEdit',
            component: ItemForm,
            props: true,
            meta: { title: '제품 수정' }
          },
          {
            path: 'warehouses',
            name: 'WarehouseList',
            component: WarehouseList,
            meta: { title: '창고 목록' }
          },
          {
            path: 'entries',
            name: 'StockEntryList',
            component: StockEntryList,
            meta: { title: '재고 이동' }
          }
        ]
      },

      // HR 모듈
      {
        path: '/hr',
        name: 'HRModule',
        children: [
          {
            path: '',
            name: 'HRDashboard',
            component: HRDashboard,
            meta: { title: '인사 대시보드' }
          },
          {
            path: 'employees',
            name: 'EmployeeList',
            component: EmployeeList,
            meta: { title: '직원 목록' }
          },
          {
            path: 'employees/new',
            name: 'EmployeeCreate',
            component: EmployeeForm,
            meta: { title: '직원 생성' }
          },
          {
            path: 'employees/:id',
            name: 'EmployeeEdit',
            component: EmployeeForm,
            props: true,
            meta: { title: '직원 수정' }
          },
          {
            path: 'attendance',
            name: 'AttendanceList',
            component: AttendanceList,
            meta: { title: '출근 관리' }
          }
        ]
      },

      // Projects 모듈
      {
        path: '/projects',
        name: 'ProjectsModule',
        children: [
          {
            path: '',
            name: 'ProjectsDashboard',
            component: ProjectsDashboard,
            meta: { title: '프로젝트 대시보드' }
          },
          {
            path: 'list',
            name: 'ProjectList',
            component: ProjectList,
            meta: { title: '프로젝트 목록' }
          },
          {
            path: 'new',
            name: 'ProjectCreate',
            component: ProjectForm,
            meta: { title: '프로젝트 생성' }
          },
          {
            path: ':id',
            name: 'ProjectEdit',
            component: ProjectForm,
            props: true,
            meta: { title: '프로젝트 수정' }
          },
          {
            path: 'tasks',
            name: 'TaskList',
            component: TaskList,
            meta: { title: '작업 목록' }
          },
          {
            path: 'timesheets',
            name: 'TimesheetList',
            component: TimesheetList,
            meta: { title: '근무시간 기록' }
          }
        ]
      },

      // CRM 모듈
      {
        path: '/crm',
        name: 'CRMModule',
        children: [
          {
            path: '',
            name: 'CRMDashboard',
            component: CRMDashboard,
            meta: { title: 'CRM 대시보드' }
          },
          {
            path: 'leads',
            name: 'LeadList',
            component: LeadList,
            meta: { title: '리드 목록' }
          },
          {
            path: 'opportunities',
            name: 'OpportunityList',
            component: OpportunityList,
            meta: { title: '영업 기회' }
          }
        ]
      },

      // 기타 모듈들
      {
        path: '/manufacturing',
        name: 'Manufacturing',
        component: ManufacturingDashboard,
        meta: { title: '제조 관리' }
      },
      {
        path: '/support',
        name: 'Support',
        component: SupportDashboard,
        meta: { title: '지원 관리' }
      },
      {
        path: '/assets',
        name: 'Assets',
        component: AssetsDashboard,
        meta: { title: '자산 관리' }
      },
      {
        path: '/quality',
        name: 'Quality',
        component: QualityDashboard,
        meta: { title: '품질 관리' }
      },
      {
        path: '/website',
        name: 'Website',
        component: WebsiteDashboard,
        meta: { title: '웹사이트 관리' }
      },

      // 설정 및 프로필
      {
        path: '/profile',
        name: 'Profile',
        component: Profile,
        meta: { title: '프로필 설정' }
      },
      {
        path: '/settings',
        name: 'Settings',
        component: Settings,
        meta: { title: '환경 설정' }
      }
    ]
  },

  // 404 페이지
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: NotFound,
    meta: { title: '페이지를 찾을 수 없음' }
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else if (to.hash) {
      return { el: to.hash, behavior: 'smooth' }
    } else {
      return { top: 0 }
    }
  }
})

// 전역 가드
router.beforeEach((to, from, next) => {
  // 로딩 상태 표시
  document.body.classList.add('router-loading')
  
  // 인증 확인
  const isAuthenticated = checkAuth()
  
  if (to.meta.requiresAuth !== false && !isAuthenticated) {
    next('/login')
    return
  }
  
  if (to.name === 'Login' && isAuthenticated) {
    next('/dashboard')
    return
  }

  // 페이지 제목 설정
  if (to.meta.title) {
    document.title = `${to.meta.title} - ERPNext AI System`
  } else {
    document.title = 'ERPNext AI System'
  }

  next()
})

router.afterEach(() => {
  // 로딩 상태 제거
  setTimeout(() => {
    document.body.classList.remove('router-loading')
  }, 100)
})

// 인증 확인 함수 (실제로는 store나 API로 확인)
function checkAuth() {
  // 임시: localStorage에서 토큰 확인
  return localStorage.getItem('authToken') || true // 개발용으로 임시 true
}

export default router