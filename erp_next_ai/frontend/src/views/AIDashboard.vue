<template>
  <div class="dashboard-layout">
    <!-- 상단 헤더 -->
    <header class="top-header">
      <div class="header-left">
        <div class="company-logo">
          <svg class="w-8 h-8" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect width="32" height="32" rx="8" fill="url(#logo-gradient)"/>
            <path d="M8 12h16M8 16h12M8 20h8" stroke="white" stroke-width="2" stroke-linecap="round"/>
            <defs>
              <linearGradient id="logo-gradient" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" style="stop-color:#3B82F6"/>
                <stop offset="100%" style="stop-color:#1E40AF"/>
              </linearGradient>
            </defs>
          </svg>
        </div>
        <div class="company-info">
          <h1 class="app-title">TechFlow ERP</h1>
          <span class="company-subtitle">통합 경영 시스템</span>
        </div>
      </div>
      
      <div class="header-center">
        <div class="search-container" :class="{ active: searchQuery }">
          <input 
            type="text" 
            placeholder="모듈, 거래처, 제품 검색..." 
            class="global-search"
            v-model="searchQuery"
            @focus="showSearchResults = true"
            @blur="hideSearchResults"
            @keydown.enter="performSearch"
          />
          <button class="search-btn" @click="performSearch">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
            </svg>
          </button>
          
          <!-- 검색 결과 드롭다운 -->
          <div v-if="showSearchResults && searchQuery" class="search-results">
            <div class="search-section">
              <h4 class="search-section-title">모듈</h4>
              <div v-for="module in filteredModules" :key="module.name" 
                   @click="navigateToModule(module)"
                   class="search-result-item">
                <div class="search-icon" :style="`background-color: ${module.color}20`">
                  <component :is="module.icon" class="w-4 h-4" :style="`color: ${module.color}`" />
                </div>
                <span>{{ module.name }}</span>
              </div>
            </div>
            
            <div class="search-section" v-if="filteredQuickActions.length">
              <h4 class="search-section-title">빠른 작업</h4>
              <div v-for="action in filteredQuickActions" :key="action.name"
                   @click="openQuickLink(action)"
                   class="search-result-item">
                <component :is="action.icon" class="w-4 h-4 text-blue-600" />
                <span>{{ action.name }}</span>
              </div>
            </div>

            <div class="search-section" v-if="!filteredModules.length && !filteredQuickActions.length">
              <div class="search-no-results">
                <svg class="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.172 16.172a4 4 0 015.656 0M9 12h6m-6-4h6m2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                <p class="text-gray-500 text-sm mt-2">검색 결과가 없습니다</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="header-right">
        <button class="header-btn notification-btn" @click="showNotifications = !showNotifications">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"></path>
          </svg>
          <span class="notification-badge" v-if="notifications.length">{{ notifications.length }}</span>
        </button>
        
        <div class="profile-dropdown" @click="showProfileMenu = !showProfileMenu">
          <div class="profile-avatar">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
            </svg>
          </div>
          <div class="profile-info">
            <span class="profile-name">김시스템</span>
            <span class="profile-role">시스템 관리자</span>
          </div>
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
          </svg>
          
          <!-- 프로필 메뉴 -->
          <div v-if="showProfileMenu" class="profile-menu">
            <a href="#" class="menu-item">프로필 설정</a>
            <a href="#" class="menu-item">환경 설정</a>
            <a href="#" class="menu-item">도움말</a>
            <hr class="menu-divider" />
            <a href="#" class="menu-item text-red-600">로그아웃</a>
          </div>
        </div>
      </div>
    </header>

    <!-- 메인 컨테이너 -->
    <div class="main-container">
      <!-- 사이드바 -->
      <aside class="sidebar">
        <nav class="sidebar-nav">
          <!-- 모듈 네비게이션 -->
          <div class="nav-section">
            <h3 class="nav-title">모듈</h3>
            <div class="nav-grid">
              <div 
                v-for="module in modules" 
                :key="module.name"
                class="module-card"
                :class="{ active: $route.path === module.path || selectedModule?.name === module.name }"
                @click="selectModule(module)"
              >
                <div class="module-icon" :style="`background-color: ${module.color}20`">
                  <component :is="module.icon" class="w-6 h-6" :style="`color: ${module.color}`" />
                </div>
                <span class="module-name">{{ module.name }}</span>
              </div>
            </div>
          </div>

          <!-- 빠른 링크 -->
          <div class="nav-section">
            <h3 class="nav-title">빠른 액세스</h3>
            <div class="quick-links">
              <button 
                v-for="link in quickLinks" 
                :key="link.name"
                @click="openQuickLink(link)"
                class="quick-link-btn"
              >
                <component :is="link.icon" class="w-5 h-5" />
                <span>{{ link.name }}</span>
              </button>
            </div>
          </div>
        </nav>

        <!-- 시스템 상태 -->
        <div class="system-status">
          <h4 class="status-title">시스템 상태</h4>
          <div class="status-items">
            <div class="status-item" :class="apiStatus">
              <div class="status-indicator"></div>
              <span>API 서버</span>
              <span class="status-text">{{ apiStatusText }}</span>
            </div>
            <div class="status-item" :class="dbStatus">
              <div class="status-indicator"></div>
              <span>데이터베이스</span>
              <span class="status-text">{{ dbStatusText }}</span>
            </div>
          </div>
        </div>
      </aside>

      <!-- 메인 콘텐츠 영역 -->
      <main class="main-content">
        <!-- 대시보드 콘텐츠 -->
        <div class="dashboard-content">
          <!-- 대시보드 헤더 -->
          <div class="dashboard-header">
            <h2 class="dashboard-title">대시보드</h2>
            <div class="dashboard-actions">
              <button class="action-btn" @click="refreshDashboard">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
                </svg>
                새로고침
              </button>
              <button class="action-btn" @click="customizeDashboard">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 100 4m0-4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 100 4m0-4v2m0-6V4"></path>
                </svg>
                사용자 정의
              </button>
            </div>
          </div>

          <!-- 주요 지표 카드 -->
          <div class="metrics-grid">
            <div class="metric-card" v-for="metric in dashboardMetrics" :key="metric.name">
              <div class="metric-header">
                <div class="metric-icon" :style="`background-color: ${metric.color}20`">
                  <component :is="metric.icon" class="w-6 h-6" :style="`color: ${metric.color}`" />
                </div>
                <div class="metric-info">
                  <h3 class="metric-title">{{ metric.name }}</h3>
                  <p class="metric-value">{{ metric.value }}</p>
                  <p class="metric-change" :class="metric.changeType">
                    {{ metric.change }}
                  </p>
                </div>
              </div>
              <div class="metric-chart">
                <!-- 간단한 차트 영역 -->
                <div class="chart-placeholder">📊</div>
              </div>
            </div>
          </div>

          <!-- 최근 활동 -->
          <div class="activity-section">
            <h3 class="section-title">최근 활동</h3>
            <div class="activity-list">
              <div v-for="activity in recentActivities" :key="activity.id" class="activity-item">
                <div class="activity-icon" :style="`background-color: ${activity.color}20`">
                  <component :is="activity.icon" class="w-5 h-5" :style="`color: ${activity.color}`" />
                </div>
                <div class="activity-content">
                  <p class="activity-title">{{ activity.title }}</p>
                  <p class="activity-description">{{ activity.description }}</p>
                  <p class="activity-time">{{ activity.time }}</p>
                </div>
                <button class="activity-action" @click="viewActivity(activity)">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
                  </svg>
                </button>
              </div>
            </div>
          </div>

          <!-- 할 일 목록 -->
          <div class="todo-section">
            <h3 class="section-title">오늘 할 일</h3>
            <div class="todo-list">
              <div v-for="todo in todos" :key="todo.id" class="todo-item" :class="{ completed: todo.completed }">
                <input 
                  type="checkbox" 
                  v-model="todo.completed" 
                  @change="updateTodo(todo)"
                  class="todo-checkbox"
                />
                <span class="todo-text">{{ todo.text }}</span>
                <span class="todo-priority" :class="todo.priority">{{ todo.priority }}</span>
              </div>
            </div>
          </div>
        </div>
      </main>

      <!-- 우측 패널 (모듈 상세) -->
      <aside class="right-panel" v-if="selectedModule">
        <div class="panel-header">
          <h3 class="panel-title">{{ selectedModule.name }}</h3>
          <button @click="closeRightPanel" class="close-btn">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
          </button>
        </div>
        <div class="panel-content">
          <div class="module-overview">
            <div class="module-header-info">
              <div class="module-large-icon" :style="`background-color: ${selectedModule.color}20`">
                <component :is="selectedModule.icon" class="w-8 h-8" :style="`color: ${selectedModule.color}`" />
              </div>
              <div>
                <h4 class="module-title">{{ selectedModule.name }}</h4>
                <p class="module-description">{{ getModuleDescription(selectedModule.name) }}</p>
              </div>
            </div>

            <div class="module-actions">
              <button 
                @click="navigateToModule(selectedModule)"
                class="btn-primary"
              >
                모듈로 이동
              </button>
              <button 
                @click="showModuleHelp(selectedModule)"
                class="btn-secondary"
              >
                도움말
              </button>
            </div>

            <div class="module-stats">
              <h5 class="stats-title">주요 지표</h5>
              <div class="stats-grid">
                <div v-for="stat in getModuleStats(selectedModule.name)" :key="stat.label" class="stat-item">
                  <div class="stat-value">{{ stat.value }}</div>
                  <div class="stat-label">{{ stat.label }}</div>
                </div>
              </div>
            </div>

            <div class="module-recent">
              <h5 class="recent-title">최근 활동</h5>
              <div class="recent-list">
                <div v-for="activity in getModuleRecentActivity(selectedModule.name)" :key="activity.id" class="recent-item">
                  <div class="recent-icon" :style="`background-color: ${selectedModule.color}20`">
                    <component :is="activity.icon" class="w-4 h-4" :style="`color: ${selectedModule.color}`" />
                  </div>
                  <div class="recent-content">
                    <div class="recent-text">{{ activity.text }}</div>
                    <div class="recent-time">{{ activity.time }}</div>
                  </div>
                </div>
              </div>
            </div>

            <div class="module-quick-actions">
              <h5 class="actions-title">빠른 작업</h5>
              <div class="actions-list">
                <button v-for="action in getModuleQuickActions(selectedModule.name)" :key="action.name"
                        @click="executeModuleAction(action, selectedModule)"
                        class="action-btn">
                  <component :is="action.icon" class="w-4 h-4" />
                  {{ action.name }}
                </button>
              </div>
            </div>
          </div>
        </div>
      </aside>
    </div>

    <!-- AI 어시스턴트 플로팅 창 -->
    <div class="ai-assistant" :class="{ expanded: aiExpanded }">
      <div class="ai-header" @click="toggleAI">
        <div class="ai-avatar-small">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"></path>
          </svg>
        </div>
        <span class="ai-title-small">AI 어시스턴트</span>
        <svg class="w-4 h-4 ai-toggle-icon" :class="{ rotated: aiExpanded }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
        </svg>
      </div>

      <div v-if="aiExpanded" class="ai-content">
        <div class="ai-chat-area">
          <div class="ai-messages" ref="messagesContainer">
            <div v-for="message in aiMessages" :key="message.id" class="ai-message" :class="message.type">
              <div class="message-content">{{ message.content }}</div>
              <div class="message-time">{{ message.time }}</div>
            </div>
          </div>
        </div>

        <div class="ai-input-area">
          <div class="ai-input-container">
            <textarea
              v-model="aiInput"
              @keydown.enter.exact.prevent="sendAIMessage"
              placeholder="AI에게 도움을 요청하세요..."
              class="ai-input"
              rows="2"
            ></textarea>
            <button @click="sendAIMessage" class="ai-send-btn" :disabled="!aiInput.trim()">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"></path>
              </svg>
            </button>
          </div>
          
          <div class="ai-suggestions">
            <button 
              v-for="suggestion in aiSuggestions" 
              :key="suggestion.id"
              @click="useAISuggestion(suggestion.text)"
              class="suggestion-chip"
            >
              {{ suggestion.text }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, onMounted, nextTick, computed } from 'vue'
import { useRouter } from 'vue-router'

export default {
  name: 'AIDashboard',
  setup() {
    const router = useRouter()
    // 반응형 데이터
    const searchQuery = ref('')
    const showNotifications = ref(false)
    const showProfileMenu = ref(false)
    const showSearchResults = ref(false)
    const selectedModule = ref(null)
    const aiExpanded = ref(false)
    const aiInput = ref('')
    const aiMessages = ref([
      {
        id: 1,
        type: 'ai',
        content: '안녕하세요! ERPNext AI 어시스턴트입니다. 어떤 도움이 필요하신가요?',
        time: '방금 전'
      }
    ])

    // 시스템 상태
    const apiStatus = ref('online')
    const apiStatusText = ref('정상')
    const dbStatus = ref('online')
    const dbStatusText = ref('정상')

    // 모듈 데이터
    const modules = ref([
      { name: '회계', path: '/accounts', icon: 'CalculatorIcon', color: '#3B82F6' },
      { name: '영업', path: '/sales', icon: 'ChartBarIcon', color: '#10B981' },
      { name: '구매', path: '/purchase', icon: 'ShoppingCartIcon', color: '#F59E0B' },
      { name: '재고', path: '/stock', icon: 'CubeIcon', color: '#8B5CF6' },
      { name: '제조', path: '/manufacturing', icon: 'CogIcon', color: '#EF4444' },
      { name: '프로젝트', path: '/projects', icon: 'FolderIcon', color: '#06B6D4' },
      { name: '인사', path: '/hr', icon: 'UsersIcon', color: '#F97316' },
      { name: 'CRM', path: '/crm', icon: 'UserGroupIcon', color: '#EC4899' },
      { name: '자산', path: '/assets', icon: 'BuildingLibraryIcon', color: '#6366F1' },
      { name: '품질', path: '/quality', icon: 'ShieldCheckIcon', color: '#84CC16' },
      { name: '지원', path: '/support', icon: 'ChatBubbleLeftRightIcon', color: '#14B8A6' },
      { name: '웹사이트', path: '/website', icon: 'GlobeAltIcon', color: '#F43F5E' }
    ])

    // 빠른 링크
    const quickLinks = ref([
      { name: '신규 고객', icon: 'UserPlusIcon', action: 'create_customer' },
      { name: '판매 주문', icon: 'DocumentPlusIcon', action: 'create_sales_order' },
      { name: '구매 주문', icon: 'ShoppingBagIcon', action: 'create_purchase_order' },
      { name: '재고 입고', icon: 'ArrowUpTrayIcon', action: 'stock_entry' },
      { name: '송장 발행', icon: 'DocumentTextIcon', action: 'create_invoice' },
      { name: '보고서', icon: 'ChartPieIcon', action: 'view_reports' }
    ])

    // 대시보드 지표
    const dashboardMetrics = ref([
      {
        name: '월 매출',
        value: '₩1,250,000,000',
        change: '+12.5%',
        changeType: 'positive',
        icon: 'CurrencyDollarIcon',
        color: '#10B981'
      },
      {
        name: '신규 고객',
        value: '156',
        change: '+8.2%',
        changeType: 'positive',
        icon: 'UsersIcon',
        color: '#3B82F6'
      },
      {
        name: '미결제 송장',
        value: '23',
        change: '-5.1%',
        changeType: 'negative',
        icon: 'ExclamationTriangleIcon',
        color: '#F59E0B'
      },
      {
        name: '재고 가치',
        value: '₩850,000,000',
        change: '+3.7%',
        changeType: 'positive',
        icon: 'CubeIcon',
        color: '#8B5CF6'
      }
    ])

    // 최근 활동
    const recentActivities = ref([
      {
        id: 1,
        title: '새로운 판매 주문',
        description: '(주)테크솔루션에서 ERP 시스템 주문',
        time: '5분 전',
        icon: 'ShoppingBagIcon',
        color: '#10B981'
      },
      {
        id: 2,
        title: '재고 부족 알림',
        description: '원자재 A의 재고가 최소 수준 이하로 감소',
        time: '15분 전',
        icon: 'ExclamationTriangleIcon',
        color: '#F59E0B'
      },
      {
        id: 3,
        title: '송장 승인 완료',
        description: 'INV-2024-001 송장이 승인되었습니다',
        time: '1시간 전',
        icon: 'DocumentCheckIcon',
        color: '#3B82F6'
      }
    ])

    // 할 일 목록
    const todos = ref([
      { id: 1, text: '월말 재무보고서 검토', completed: false, priority: 'high' },
      { id: 2, text: '신규 공급업체 계약 승인', completed: false, priority: 'medium' },
      { id: 3, text: '직원 성과 평가 완료', completed: true, priority: 'low' },
      { id: 4, text: '재고 실사 계획 수립', completed: false, priority: 'high' }
    ])

    // 알림 목록
    const notifications = ref([
      { id: 1, title: '새로운 주문', content: '고객으로부터 새 주문이 접수되었습니다' },
      { id: 2, title: '재고 알림', content: '일부 품목의 재고가 부족합니다' }
    ])

    // AI 제안사항
    const aiSuggestions = ref([
      { id: 1, text: '오늘의 매출 현황 보여줘' },
      { id: 2, text: '재고 부족 품목 주문 생성해줘' },
      { id: 3, text: '이번 달 수익성 분석해줘' },
      { id: 4, text: '고객 만족도 개선 방안 제시해줘' }
    ])

    // 검색 관련 computed
    const filteredModules = computed(() => {
      if (!searchQuery.value) return []
      return modules.value.filter(module => 
        module.name.toLowerCase().includes(searchQuery.value.toLowerCase())
      )
    })

    const filteredQuickActions = computed(() => {
      if (!searchQuery.value) return []
      return quickLinks.value.filter(action => 
        action.name.toLowerCase().includes(searchQuery.value.toLowerCase())
      )
    })

    // 메서드
    const toggleAI = () => {
      aiExpanded.value = !aiExpanded.value
    }

    const sendAIMessage = () => {
      if (!aiInput.value.trim()) return

      // 사용자 메시지 추가
      aiMessages.value.push({
        id: Date.now(),
        type: 'user',
        content: aiInput.value,
        time: '방금 전'
      })

      const userMessage = aiInput.value
      aiInput.value = ''

      // AI 응답 시뮬레이션
      setTimeout(() => {
        aiMessages.value.push({
          id: Date.now() + 1,
          type: 'ai',
          content: `"${userMessage}"에 대해 분석하고 있습니다. 잠시만 기다려주세요...`,
          time: '방금 전'
        })
        
        // 스크롤을 맨 아래로
        nextTick(() => {
          const container = document.querySelector('.ai-messages')
          if (container) {
            container.scrollTop = container.scrollHeight
          }
        })
      }, 1000)
    }

    const useAISuggestion = (text) => {
      aiInput.value = text
      sendAIMessage()
    }

    const openQuickLink = (link) => {
      // 빠른 링크 기능 실제 구현
      const actions = {
        'create_customer': () => router.push('/crm'),
        'create_sales_order': () => router.push('/sales'),
        'create_purchase_order': () => router.push('/purchase'),
        'stock_entry': () => router.push('/stock'),
        'create_invoice': () => router.push('/accounts'),
        'view_reports': () => {
          // AI 메시지 추가
          aiMessages.value.push({
            id: Date.now(),
            type: 'ai',
            content: '보고서를 생성하고 있습니다... 어떤 종류의 보고서가 필요하신가요?',
            time: '방금 전'
          })
          aiExpanded.value = true
          nextTick(() => {
            const container = document.querySelector('.ai-messages')
            if (container) {
              container.scrollTop = container.scrollHeight
            }
          })
        }
      }
      
      if (actions[link.action]) {
        actions[link.action]()
      }
    }

    const refreshDashboard = () => {
      // 대시보드 데이터 새로고침
      checkSystemStatus()
      
      // 메트릭 데이터 업데이트 (시뮬레이션)
      dashboardMetrics.value.forEach(metric => {
        const randomChange = (Math.random() * 10 - 5).toFixed(1)
        metric.change = randomChange >= 0 ? `+${randomChange}%` : `${randomChange}%`
        metric.changeType = randomChange >= 0 ? 'positive' : 'negative'
      })
      
      // 알림 메시지
      aiMessages.value.push({
        id: Date.now(),
        type: 'ai',
        content: '대시보드 데이터가 성공적으로 새로고침되었습니다.',
        time: new Date().toLocaleTimeString('ko-KR', { hour: '2-digit', minute: '2-digit' })
      })
      
      if (!aiExpanded.value) {
        aiExpanded.value = true
      }
    }

    const customizeDashboard = () => {
      // 대시보드 사용자 정의 모드
      aiMessages.value.push({
        id: Date.now(),
        type: 'ai',
        content: '대시보드 사용자 정의 기능입니다. 어떤 위젯을 추가하거나 제거하고 싶으신가요?',
        time: new Date().toLocaleTimeString('ko-KR', { hour: '2-digit', minute: '2-digit' })
      })
      
      aiExpanded.value = true
      nextTick(() => {
        const container = document.querySelector('.ai-messages')
        if (container) {
          container.scrollTop = container.scrollHeight
        }
      })
    }

    const viewActivity = (activity) => {
      // 활동 상세 보기
      const moduleMap = {
        'ShoppingBagIcon': '/sales',
        'ExclamationTriangleIcon': '/stock', 
        'DocumentCheckIcon': '/accounts'
      }
      
      const route = moduleMap[activity.icon] || '/dashboard'
      router.push(route)
    }

    const updateTodo = (todo) => {
      console.log('할 일 업데이트:', todo)
    }

    const closeRightPanel = () => {
      selectedModule.value = null
    }

    // 검색 관련 메서드
    const performSearch = () => {
      if (!searchQuery.value.trim()) return
      
      // AI 어시스턴트에 검색 결과 표시
      aiMessages.value.push({
        id: Date.now(),
        type: 'ai',
        content: `"${searchQuery.value}"에 대한 검색을 수행했습니다. ${filteredModules.value.length + filteredQuickActions.value.length}개의 결과를 찾았습니다.`,
        time: new Date().toLocaleTimeString('ko-KR', { hour: '2-digit', minute: '2-digit' })
      })
      
      if (!aiExpanded.value) {
        aiExpanded.value = true
      }
      
      nextTick(() => {
        const container = document.querySelector('.ai-messages')
        if (container) {
          container.scrollTop = container.scrollHeight
        }
      })
    }

    const navigateToModule = (module) => {
      router.push(module.path)
      showSearchResults.value = false
      searchQuery.value = ''
    }

    const hideSearchResults = () => {
      setTimeout(() => {
        showSearchResults.value = false
      }, 200)
    }

    // 모듈 관련 메서드
    const selectModule = (module) => {
      selectedModule.value = module
    }

    const getModuleDescription = (moduleName) => {
      const descriptions = {
        '회계': '재무 관리, 회계 처리 및 세무 신고 기능',
        '영업': '고객 관리, 판매 프로세스 및 매출 분석',
        '구매': '공급업체 관리, 구매 주문 및 비용 관리',
        '재고': '재고 추적, 창고 관리 및 재고 최적화',
        '제조': '생산 계획, 품질 관리 및 제조 프로세스',
        '프로젝트': '프로젝트 계획, 진행 관리 및 리소스 할당',
        '인사': '직원 관리, 급여 처리 및 성과 평가',
        'CRM': '고객 관계 관리 및 영업 기회 추적',
        '자산': '고정자산 관리, 감가상각 및 유지보수',
        '품질': '품질 보증, 검사 관리 및 개선 프로세스',
        '지원': '고객 지원, 티켓 관리 및 문제 해결',
        '웹사이트': '온라인 마케팅, SEO 및 콘텐츠 관리'
      }
      return descriptions[moduleName] || '모듈 설명이 없습니다'
    }

    const getModuleStats = (moduleName) => {
      const stats = {
        '회계': [
          { label: '미결제 송장', value: '23건' },
          { label: '월 매출', value: '₩1.2B' },
          { label: '현금흐름', value: '+8.5%' }
        ],
        '영업': [
          { label: '신규 리드', value: '47건' },
          { label: '진행 중 거래', value: '12건' },
          { label: '성공률', value: '67%' }
        ],
        '재고': [
          { label: '부족 품목', value: '8개' },
          { label: '재고 가치', value: '₩450M' },
          { label: '회전율', value: '12.3' }
        ]
      }
      return stats[moduleName] || [
        { label: '총 항목', value: '0' },
        { label: '활성', value: '0' },
        { label: '상태', value: '정상' }
      ]
    }

    const getModuleRecentActivity = (moduleName) => {
      const activities = {
        '회계': [
          { id: 1, icon: 'DocumentTextIcon', text: '송장 INV-001 생성됨', time: '10분 전' },
          { id: 2, icon: 'CurrencyDollarIcon', text: '결제 완료 - ₩2,500,000', time: '1시간 전' }
        ],
        '영업': [
          { id: 1, icon: 'UserPlusIcon', text: '신규 고객 등록', time: '30분 전' },
          { id: 2, icon: 'ChartBarIcon', text: '제안서 제출 완료', time: '2시간 전' }
        ]
      }
      return activities[moduleName] || [
        { id: 1, icon: 'InformationCircleIcon', text: '최근 활동이 없습니다', time: '' }
      ]
    }

    const getModuleQuickActions = (moduleName) => {
      const actions = {
        '회계': [
          { name: '새 송장', icon: 'DocumentPlusIcon' },
          { name: '결제 등록', icon: 'CurrencyDollarIcon' },
          { name: '보고서 생성', icon: 'ChartBarIcon' }
        ],
        '영업': [
          { name: '새 리드', icon: 'UserPlusIcon' },
          { name: '주문 생성', icon: 'ShoppingCartIcon' },
          { name: '제안서 작성', icon: 'DocumentTextIcon' }
        ]
      }
      return actions[moduleName] || [
        { name: '모듈 보기', icon: 'EyeIcon' }
      ]
    }

    const showModuleHelp = (module) => {
      aiMessages.value.push({
        id: Date.now(),
        type: 'ai',
        content: `${module.name} 모듈에 대한 도움말을 제공합니다. 이 모듈의 주요 기능과 사용 방법을 설명해드리겠습니다.`,
        time: new Date().toLocaleTimeString('ko-KR', { hour: '2-digit', minute: '2-digit' })
      })
      
      if (!aiExpanded.value) {
        aiExpanded.value = true
      }
    }

    const executeModuleAction = (action, module) => {
      aiMessages.value.push({
        id: Date.now(),
        type: 'ai',
        content: `${module.name} 모듈에서 "${action.name}" 작업을 실행합니다.`,
        time: new Date().toLocaleTimeString('ko-KR', { hour: '2-digit', minute: '2-digit' })
      })
    }

    // 시스템 상태 확인
    const checkSystemStatus = async () => {
      try {
        // API 서버 상태 확인
        const startTime = Date.now()
        const response = await fetch('/api/health', { 
          method: 'GET',
          timeout: 5000 
        })
        const responseTime = Date.now() - startTime
        
        if (response.ok) {
          const data = await response.json()
          apiStatus.value = 'online'
          apiStatusText.value = `정상 (${responseTime}ms)`
        } else {
          apiStatus.value = 'error'
          apiStatusText.value = `오류 (${response.status})`
        }
      } catch (error) {
        apiStatus.value = 'offline'
        apiStatusText.value = '연결 실패'
        console.warn('API 서버 연결 실패:', error.message)
      }

      try {
        // 데이터베이스 상태 확인
        const startTime = Date.now()
        const response = await fetch('/api/db-health', {
          method: 'GET',
          timeout: 5000
        })
        const responseTime = Date.now() - startTime
        
        if (response.ok) {
          const data = await response.json()
          dbStatus.value = 'online'
          dbStatusText.value = `정상 (${responseTime}ms)`
        } else {
          dbStatus.value = 'error'
          dbStatusText.value = `오류 (${response.status})`
        }
      } catch (error) {
        dbStatus.value = 'offline'
        dbStatusText.value = '연결 실패'
        console.warn('데이터베이스 연결 실패:', error.message)
      }

      // 서버가 없을 때 시뮬레이션 데이터 사용
      if (apiStatus.value === 'offline' && dbStatus.value === 'offline') {
        // 개발 환경에서 시뮬레이션
        setTimeout(() => {
          const isApiOk = Math.random() > 0.2 // 80% 확률로 정상
          const isDbOk = Math.random() > 0.1  // 90% 확률로 정상
          
          if (isApiOk) {
            apiStatus.value = 'online'
            apiStatusText.value = '정상 (시뮬레이션)'
          } else {
            apiStatus.value = 'error'
            apiStatusText.value = '일시적 오류'
          }
          
          if (isDbOk) {
            dbStatus.value = 'online'
            dbStatusText.value = '정상 (시뮬레이션)'
          } else {
            dbStatus.value = 'error'
            dbStatusText.value = '연결 지연'
          }
        }, 1000)
      }
    }

    onMounted(() => {
      checkSystemStatus()
      // 시스템 상태를 주기적으로 확인
      setInterval(checkSystemStatus, 30000)
    })

    return {
      searchQuery,
      showNotifications,
      showProfileMenu,
      showSearchResults,
      selectedModule,
      aiExpanded,
      aiInput,
      aiMessages,
      apiStatus,
      apiStatusText,
      dbStatus,
      dbStatusText,
      modules,
      quickLinks,
      dashboardMetrics,
      recentActivities,
      todos,
      notifications,
      aiSuggestions,
      filteredModules,
      filteredQuickActions,
      toggleAI,
      sendAIMessage,
      useAISuggestion,
      openQuickLink,
      performSearch,
      navigateToModule,
      hideSearchResults,
      refreshDashboard,
      customizeDashboard,
      viewActivity,
      updateTodo,
      closeRightPanel
    }
  }
}
</script>

<style scoped>
/* 전체 레이아웃 - 흰색 테마 */
.dashboard-layout {
  min-height: 100vh;
  background-color: #f8fafc;
  display: flex;
  flex-direction: column;
}

/* 상단 헤더 */
.top-header {
  background: white;
  border-bottom: 1px solid #e2e8f0;
  padding: 0 24px;
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: sticky;
  top: 0;
  z-index: 100;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
}

.header-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.company-logo {
  display: flex;
  align-items: center;
  justify-content: center;
}

.company-info {
  display: flex;
  flex-direction: column;
}

.app-title {
  font-size: 20px;
  font-weight: 700;
  color: #1e293b;
  line-height: 1.2;
}

.company-subtitle {
  font-size: 12px;
  color: #64748b;
  font-weight: 500;
}

.header-center {
  flex: 1;
  max-width: 500px;
  margin: 0 40px;
}

.search-container {
  position: relative;
  display: flex;
  align-items: center;
}

.global-search {
  width: 100%;
  padding: 8px 16px 8px 40px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 14px;
  background: #f9fafb;
}

.search-btn {
  position: absolute;
  left: 12px;
  color: #6b7280;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 16px;
}

.header-btn {
  position: relative;
  padding: 8px;
  border-radius: 8px;
  color: #4b5563;
  transition: background-color 0.2s;
}

.header-btn:hover {
  background-color: #f3f4f6;
}

.notification-badge {
  position: absolute;
  top: 0;
  right: 0;
  background: #ef4444;
  color: white;
  font-size: 12px;
  padding: 2px 6px;
  border-radius: 10px;
  min-width: 16px;
  text-align: center;
}

.profile-dropdown {
  position: relative;
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.profile-dropdown:hover {
  background-color: #f3f4f6;
}

.profile-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: linear-gradient(135deg, #3b82f6, #1e40af);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 12px;
  font-weight: 600;
}

.profile-info {
  display: flex;
  flex-direction: column;
}

.profile-name {
  font-size: 14px;
  font-weight: 600;
  color: #1e293b;
  line-height: 1.2;
}

.profile-role {
  font-size: 12px;
  color: #64748b;
  font-weight: 500;
}

.profile-menu {
  position: absolute;
  top: 100%;
  right: 0;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 8px 0;
  min-width: 200px;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
  z-index: 50;
}

.menu-item {
  display: block;
  padding: 8px 16px;
  font-size: 14px;
  color: #374151;
  text-decoration: none;
  transition: background-color 0.2s;
}

.menu-item:hover {
  background-color: #f3f4f6;
}

.menu-divider {
  margin: 8px 0;
  border: none;
  border-top: 1px solid #e5e7eb;
}

/* 메인 컨테이너 */
.main-container {
  display: flex;
  flex: 1;
  height: calc(100vh - 64px);
}

/* 사이드바 */
.sidebar {
  width: 280px;
  background: white;
  border-right: 1px solid #e2e8f0;
  padding: 24px 16px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
}

.nav-section {
  margin-bottom: 32px;
}

.nav-title {
  font-size: 14px;
  font-weight: 600;
  color: #6b7280;
  margin-bottom: 16px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.nav-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
}

.module-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 16px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  text-decoration: none;
  color: #374151;
  transition: all 0.2s;
}

.module-card:hover {
  border-color: #3b82f6;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  transform: translateY(-1px);
}

.module-card.active {
  border-color: #3b82f6;
  background-color: #eff6ff;
}

.module-icon {
  width: 48px;
  height: 48px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 8px;
}

.module-name {
  font-size: 13px;
  font-weight: 500;
  text-align: center;
}

.quick-links {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.quick-link-btn {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 12px;
  border-radius: 6px;
  text-align: left;
  font-size: 14px;
  color: #374151;
  transition: background-color 0.2s;
}

.quick-link-btn:hover {
  background-color: #f3f4f6;
}

/* 시스템 상태 */
.system-status {
  margin-top: auto;
  padding-top: 24px;
  border-top: 1px solid #e5e7eb;
}

.status-title {
  font-size: 14px;
  font-weight: 600;
  color: #6b7280;
  margin-bottom: 16px;
}

.status-items {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.status-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
}

.status-indicator {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.status-item.online .status-indicator {
  background-color: #10b981;
}

.status-item.error .status-indicator {
  background-color: #ef4444;
}

.status-item.offline .status-indicator {
  background-color: #6b7280;
}

.status-text {
  margin-left: auto;
  font-weight: 500;
}

/* 메인 콘텐츠 */
.main-content {
  flex: 1;
  padding: 24px;
  overflow-y: auto;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.dashboard-title {
  font-size: 24px;
  font-weight: 600;
  color: #1e293b;
}

.dashboard-actions {
  display: flex;
  gap: 12px;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  background: white;
  font-size: 14px;
  color: #374151;
  transition: all 0.2s;
}

.action-btn:hover {
  border-color: #3b82f6;
  color: #3b82f6;
}

/* 지표 카드 */
.metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 20px;
  margin-bottom: 32px;
}

.metric-card {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 20px;
  transition: box-shadow 0.2s;
}

.metric-card:hover {
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.metric-header {
  display: flex;
  align-items: flex-start;
  gap: 16px;
}

.metric-icon {
  width: 48px;
  height: 48px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.metric-info {
  flex: 1;
}

.metric-title {
  font-size: 14px;
  color: #6b7280;
  margin-bottom: 4px;
}

.metric-value {
  font-size: 24px;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 4px;
}

.metric-change {
  font-size: 12px;
  font-weight: 500;
}

.metric-change.positive {
  color: #10b981;
}

.metric-change.negative {
  color: #ef4444;
}

.chart-placeholder {
  font-size: 32px;
  text-align: center;
  margin-top: 16px;
  opacity: 0.3;
}

/* 활동 섹션 */
.activity-section, .todo-section {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 24px;
}

.section-title {
  font-size: 18px;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 16px;
}

.activity-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.activity-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  border-radius: 8px;
  transition: background-color 0.2s;
}

.activity-item:hover {
  background-color: #f8fafc;
}

.activity-icon {
  width: 40px;
  height: 40px;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.activity-content {
  flex: 1;
}

.activity-title {
  font-size: 14px;
  font-weight: 500;
  color: #1e293b;
  margin-bottom: 2px;
}

.activity-description {
  font-size: 13px;
  color: #6b7280;
  margin-bottom: 2px;
}

.activity-time {
  font-size: 12px;
  color: #9ca3af;
}

.activity-action {
  padding: 4px;
  border-radius: 4px;
  color: #6b7280;
  transition: all 0.2s;
}

.activity-action:hover {
  background-color: #f3f4f6;
  color: #3b82f6;
}

/* 할 일 목록 */
.todo-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.todo-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  border-radius: 6px;
  transition: background-color 0.2s;
}

.todo-item:hover {
  background-color: #f8fafc;
}

.todo-item.completed {
  opacity: 0.6;
}

.todo-item.completed .todo-text {
  text-decoration: line-through;
}

.todo-checkbox {
  width: 16px;
  height: 16px;
}

.todo-text {
  flex: 1;
  font-size: 14px;
  color: #374151;
}

.todo-priority {
  font-size: 12px;
  font-weight: 500;
  padding: 2px 8px;
  border-radius: 12px;
}

.todo-priority.high {
  background-color: #fee2e2;
  color: #dc2626;
}

.todo-priority.medium {
  background-color: #fef3c7;
  color: #d97706;
}

.todo-priority.low {
  background-color: #d1fae5;
  color: #059669;
}

/* 우측 패널 */
.right-panel {
  width: 400px;
  background: white;
  border-left: 1px solid #e2e8f0;
  display: flex;
  flex-direction: column;
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid #e5e7eb;
}

.panel-title {
  font-size: 18px;
  font-weight: 600;
  color: #1e293b;
}

.close-btn {
  padding: 4px;
  border-radius: 4px;
  color: #6b7280;
  transition: all 0.2s;
}

.close-btn:hover {
  background-color: #f3f4f6;
  color: #ef4444;
}

.panel-content {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
}

/* AI 어시스턴트 플로팅 창 */
.ai-assistant {
  position: fixed;
  bottom: 24px;
  left: 24px;
  width: 350px;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
  z-index: 1000;
  transition: all 0.3s ease;
}

.ai-assistant:not(.expanded) {
  height: 56px;
}

.ai-assistant.expanded {
  height: 500px;
}

.ai-header {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  cursor: pointer;
  border-bottom: 1px solid #e5e7eb;
}

.ai-assistant:not(.expanded) .ai-header {
  border-bottom: none;
}

.ai-avatar-small {
  width: 32px;
  height: 32px;
  background: linear-gradient(135deg, #3b82f6, #8b5cf6);
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.ai-title-small {
  flex: 1;
  font-size: 14px;
  font-weight: 500;
  color: #1e293b;
}

.ai-toggle-icon {
  transition: transform 0.3s;
}

.ai-toggle-icon.rotated {
  transform: rotate(180deg);
}

.ai-content {
  display: flex;
  flex-direction: column;
  height: calc(100% - 73px);
}

.ai-chat-area {
  flex: 1;
  overflow: hidden;
}

.ai-messages {
  height: 100%;
  overflow-y: auto;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.ai-message {
  max-width: 80%;
  word-wrap: break-word;
}

.ai-message.user {
  align-self: flex-end;
}

.ai-message.user .message-content {
  background: #3b82f6;
  color: white;
  border-radius: 12px 12px 4px 12px;
}

.ai-message.ai .message-content {
  background: #f1f5f9;
  color: #1e293b;
  border-radius: 12px 12px 12px 4px;
}

.message-content {
  padding: 8px 12px;
  font-size: 14px;
  line-height: 1.4;
}

.message-time {
  font-size: 11px;
  color: #9ca3af;
  margin-top: 4px;
  text-align: right;
}

.ai-message.ai .message-time {
  text-align: left;
}

.ai-input-area {
  border-top: 1px solid #e5e7eb;
  padding: 16px;
}

.ai-input-container {
  display: flex;
  gap: 8px;
  margin-bottom: 12px;
}

.ai-input {
  flex: 1;
  padding: 8px 12px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 14px;
  resize: none;
  min-height: 36px;
}

.ai-send-btn {
  padding: 8px;
  background: #3b82f6;
  color: white;
  border-radius: 6px;
  transition: background-color 0.2s;
}

.ai-send-btn:hover:not(:disabled) {
  background: #2563eb;
}

.ai-send-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.ai-suggestions {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.suggestion-chip {
  padding: 4px 8px;
  background: #f1f5f9;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  font-size: 12px;
  color: #475569;
  transition: all 0.2s;
}

.suggestion-chip:hover {
  background: #e2e8f0;
  border-color: #cbd5e1;
}

/* 검색 관련 스타일 */
.search-container {
  position: relative;
  display: flex;
  align-items: center;
}

.search-container.active .global-search {
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.search-results {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1);
  z-index: 50;
  max-height: 400px;
  overflow-y: auto;
  margin-top: 4px;
}

.search-section {
  padding: 12px 16px;
}

.search-section:not(:last-child) {
  border-bottom: 1px solid #f1f5f9;
}

.search-section-title {
  font-size: 12px;
  font-weight: 600;
  color: #6b7280;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 8px;
}

.search-result-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 12px;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s;
  font-size: 14px;
  color: #374151;
}

.search-result-item:hover {
  background: #f3f4f6;
  color: #1f2937;
}

.search-icon {
  width: 24px;
  height: 24px;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.search-no-results {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 32px 16px;
  text-align: center;
}

/* 반응형 디자인 */
@media (max-width: 1024px) {
  .sidebar {
    width: 240px;
  }
  
  .nav-grid {
    grid-template-columns: 1fr;
  }
  
  .ai-assistant {
    width: 300px;
  }
}

@media (max-width: 768px) {
  .main-container {
    flex-direction: column;
  }
  
  .sidebar {
    width: 100%;
    height: auto;
    border-right: none;
    border-bottom: 1px solid #e2e8f0;
  }
  
  .metrics-grid {
    grid-template-columns: 1fr;
  }
  
  .ai-assistant {
    left: 16px;
    right: 16px;
    width: auto;
  }
}
</style>