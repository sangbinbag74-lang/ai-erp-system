<template>
  <header class="app-header">
    <div class="header-container">
      <!-- 좌측: 로고 및 네비게이션 -->
      <div class="header-left">
        <!-- 로고 -->
        <router-link to="/" class="logo">
          <Icon name="heroicons:cpu-chip" class="w-8 h-8 text-primary-600" />
          <span class="logo-text">ERPNext AI</span>
        </router-link>
        
        <!-- 메인 네비게이션 -->
        <nav class="main-nav">
          <!-- 모듈 드롭다운 -->
          <div class="nav-dropdown" @click="toggleModulesDropdown" ref="modulesDropdown">
            <button class="nav-button" :class="{ active: showModulesDropdown }">
              <Icon name="heroicons:squares-2x2" class="w-5 h-5" />
              <span>모듈</span>
              <Icon name="heroicons:chevron-down" class="w-4 h-4 transition-transform" 
                    :class="{ 'rotate-180': showModulesDropdown }" />
            </button>
            
            <!-- 모듈 드롭다운 메뉴 -->
            <div class="dropdown-menu modules-menu" v-show="showModulesDropdown">
              <div class="modules-grid">
                <router-link 
                  v-for="module in modules" 
                  :key="module.name"
                  :to="module.route"
                  class="module-item"
                  @click="closeDropdowns"
                >
                  <Icon :name="module.icon" class="w-6 h-6" />
                  <div>
                    <div class="module-name">{{ module.name }}</div>
                    <div class="module-desc">{{ module.description }}</div>
                  </div>
                </router-link>
              </div>
            </div>
          </div>
          
          <!-- 빠른 링크들 -->
          <router-link to="/dashboard" class="nav-link" active-class="active">
            <Icon name="heroicons:chart-bar-square" class="w-5 h-5" />
            <span>대시보드</span>
          </router-link>
        </nav>
      </div>
      
      <!-- 우측: 검색, 알림, 사용자 메뉴 -->
      <div class="header-right">
        <!-- 전역 검색 -->
        <div class="global-search" ref="searchContainer">
          <button 
            @click="toggleSearch" 
            class="search-trigger"
            :class="{ active: showSearch }"
            title="전역 검색 (Ctrl+K)"
          >
            <Icon name="heroicons:magnifying-glass" class="w-5 h-5" />
          </button>
          
          <!-- 검색 패널 -->
          <div class="search-panel" v-show="showSearch" @click.stop>
            <div class="search-input-container">
              <Icon name="heroicons:magnifying-glass" class="w-5 h-5 search-icon" />
              <input 
                v-model="searchQuery"
                @input="performSearch"
                placeholder="문서, 고객, 제품 검색... (Ctrl+K)"
                class="search-input"
                ref="searchInput"
                @keydown.escape="closeSearch"
              >
              <kbd class="search-kbd">⌘K</kbd>
            </div>
            
            <!-- 검색 결과 -->
            <div class="search-results" v-if="searchResults.length > 0">
              <div class="result-section" v-for="section in groupedResults" :key="section.type">
                <div class="result-section-title">{{ section.title }}</div>
                <router-link 
                  v-for="result in section.items" 
                  :key="result.id"
                  :to="result.route"
                  class="search-result-item"
                  @click="closeSearch"
                >
                  <Icon :name="result.icon" class="w-5 h-5" />
                  <div>
                    <div class="result-title">{{ result.title }}</div>
                    <div class="result-subtitle">{{ result.subtitle }}</div>
                  </div>
                </router-link>
              </div>
            </div>
            
            <!-- 최근 검색 -->
            <div class="recent-searches" v-if="searchQuery === '' && recentSearches.length > 0">
              <div class="result-section-title">최근 검색</div>
              <div 
                v-for="search in recentSearches" 
                :key="search"
                class="recent-search-item"
                @click="searchQuery = search; performSearch()"
              >
                <Icon name="heroicons:clock" class="w-4 h-4" />
                <span>{{ search }}</span>
              </div>
            </div>
          </div>
        </div>
        
        <!-- 알림 -->
        <div class="notifications" ref="notificationDropdown">
          <button 
            @click="toggleNotifications" 
            class="notification-button"
            :class="{ active: showNotifications }"
            title="알림"
          >
            <Icon name="heroicons:bell" class="w-5 h-5" />
            <span v-if="unreadNotifications > 0" class="notification-badge">
              {{ unreadNotifications > 99 ? '99+' : unreadNotifications }}
            </span>
          </button>
          
          <!-- 알림 드롭다운 -->
          <div class="dropdown-menu notification-menu" v-show="showNotifications">
            <div class="notification-header">
              <h3>알림</h3>
              <button @click="markAllAsRead" class="mark-all-read">모두 읽음</button>
            </div>
            <div class="notification-list">
              <div 
                v-for="notification in notifications" 
                :key="notification.id"
                class="notification-item"
                :class="{ unread: !notification.read }"
                @click="markAsRead(notification)"
              >
                <div class="notification-icon">
                  <Icon :name="notification.icon" class="w-5 h-5" />
                </div>
                <div class="notification-content">
                  <div class="notification-title">{{ notification.title }}</div>
                  <div class="notification-message">{{ notification.message }}</div>
                  <div class="notification-time">{{ formatTime(notification.timestamp) }}</div>
                </div>
              </div>
            </div>
            <div class="notification-footer">
              <router-link to="/notifications" @click="closeDropdowns">모든 알림 보기</router-link>
            </div>
          </div>
        </div>
        
        <!-- AI 상태 표시 -->
        <div class="ai-status" :class="aiStatus.toLowerCase()">
          <Icon name="heroicons:cpu-chip" class="w-5 h-5" />
          <span class="status-dot"></span>
        </div>
        
        <!-- 사용자 메뉴 -->
        <div class="user-menu" ref="userDropdown">
          <button 
            @click="toggleUserMenu" 
            class="user-button"
            :class="{ active: showUserMenu }"
          >
            <div class="user-avatar">
              <img v-if="user.avatar" :src="user.avatar" :alt="user.name" />
              <Icon v-else name="heroicons:user" class="w-5 h-5" />
            </div>
            <span class="user-name">{{ user.name }}</span>
            <Icon name="heroicons:chevron-down" class="w-4 h-4 transition-transform" 
                  :class="{ 'rotate-180': showUserMenu }" />
          </button>
          
          <!-- 사용자 드롭다운 메뉴 -->
          <div class="dropdown-menu user-dropdown-menu" v-show="showUserMenu">
            <div class="user-info">
              <div class="user-avatar-large">
                <img v-if="user.avatar" :src="user.avatar" :alt="user.name" />
                <Icon v-else name="heroicons:user" class="w-6 h-6" />
              </div>
              <div>
                <div class="user-name-large">{{ user.name }}</div>
                <div class="user-email">{{ user.email }}</div>
              </div>
            </div>
            <hr class="dropdown-divider">
            <router-link to="/profile" class="dropdown-item" @click="closeDropdowns">
              <Icon name="heroicons:user-circle" class="w-5 h-5" />
              <span>프로필 설정</span>
            </router-link>
            <router-link to="/settings" class="dropdown-item" @click="closeDropdowns">
              <Icon name="heroicons:cog-6-tooth" class="w-5 h-5" />
              <span>환경 설정</span>
            </router-link>
            <button class="dropdown-item" @click="toggleDarkMode">
              <Icon :name="isDarkMode ? 'heroicons:sun' : 'heroicons:moon'" class="w-5 h-5" />
              <span>{{ isDarkMode ? '라이트 모드' : '다크 모드' }}</span>
            </button>
            <hr class="dropdown-divider">
            <button class="dropdown-item text-error" @click="logout">
              <Icon name="heroicons:arrow-right-on-rectangle" class="w-5 h-5" />
              <span>로그아웃</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </header>
</template>

<script>
import { ref, reactive, onMounted, onUnmounted, computed, nextTick } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { Icon } from '@iconify/vue'
import { globalAI } from '@/composables/useAI'

export default {
  name: 'AppHeader',
  components: {
    Icon
  },
  setup() {
    const router = useRouter()
    const route = useRoute()

    // 반응형 상태
    const showModulesDropdown = ref(false)
    const showSearch = ref(false)
    const showNotifications = ref(false)
    const showUserMenu = ref(false)
    const searchQuery = ref('')
    const searchResults = ref([])
    const isDarkMode = ref(false)

    // 참조
    const modulesDropdown = ref(null)
    const searchContainer = ref(null)
    const searchInput = ref(null)
    const notificationDropdown = ref(null)
    const userDropdown = ref(null)

    // 사용자 정보
    const user = reactive({
      name: '관리자',
      email: 'admin@erpnext.ai',
      avatar: null
    })

    // 모듈 정의
    const modules = ref([
      {
        name: '회계',
        description: '복식부기, 거래처, 결제',
        route: '/accounts',
        icon: 'heroicons:calculator'
      },
      {
        name: '영업',
        description: '고객관리, 주문서, 송장',
        route: '/sales',
        icon: 'heroicons:chart-bar'
      },
      {
        name: '구매',
        description: '공급업체, 구매주문, 입고',
        route: '/purchase',
        icon: 'heroicons:shopping-cart'
      },
      {
        name: '재고',
        description: '창고관리, 재고이동, 평가',
        route: '/stock',
        icon: 'heroicons:cube'
      },
      {
        name: '인사',
        description: '직원관리, 급여, 출근',
        route: '/hr',
        icon: 'heroicons:users'
      },
      {
        name: '제조',
        description: 'BOM, 작업지시, 생산',
        route: '/manufacturing',
        icon: 'heroicons:cog-6-tooth'
      },
      {
        name: '프로젝트',
        description: '프로젝트관리, 작업추적',
        route: '/projects',
        icon: 'heroicons:folder'
      },
      {
        name: 'CRM',
        description: '리드관리, 기회관리',
        route: '/crm',
        icon: 'heroicons:heart'
      },
      {
        name: '지원',
        description: '이슈추적, 유지보수',
        route: '/support',
        icon: 'heroicons:lifebuoy'
      },
      {
        name: '자산',
        description: '고정자산, 감가상각',
        route: '/assets',
        icon: 'heroicons:building-office'
      },
      {
        name: '품질',
        description: '품질검사, 템플릿',
        route: '/quality',
        icon: 'heroicons:shield-check'
      },
      {
        name: '웹사이트',
        description: '콘텐츠관리, 전자상거래',
        route: '/website',
        icon: 'heroicons:globe-alt'
      }
    ])

    // 알림 상태
    const notifications = ref([
      {
        id: 1,
        title: '새 주문 접수',
        message: '고객 ABC Corp.에서 새 주문이 접수되었습니다.',
        icon: 'heroicons:shopping-bag',
        read: false,
        timestamp: new Date(Date.now() - 1000 * 60 * 5) // 5분 전
      },
      {
        id: 2,
        title: '재고 부족 알림',
        message: '노트북 Dell XPS 13의 재고가 부족합니다.',
        icon: 'heroicons:exclamation-triangle',
        read: false,
        timestamp: new Date(Date.now() - 1000 * 60 * 30) // 30분 전
      },
      {
        id: 3,
        title: 'AI 분석 완료',
        message: '월말 매출 분석 보고서가 준비되었습니다.',
        icon: 'heroicons:chart-bar',
        read: true,
        timestamp: new Date(Date.now() - 1000 * 60 * 60 * 2) // 2시간 전
      }
    ])

    const recentSearches = ref(['고객 ABC Corp', '노트북 Dell', '월말 보고서'])

    // 계산된 속성
    const unreadNotifications = computed(() => 
      notifications.value.filter(n => !n.read).length
    )

    const aiStatus = computed(() => globalAI.status)

    const groupedResults = computed(() => {
      const groups = {}
      searchResults.value.forEach(result => {
        if (!groups[result.type]) {
          groups[result.type] = {
            type: result.type,
            title: result.typeTitle,
            items: []
          }
        }
        groups[result.type].items.push(result)
      })
      return Object.values(groups)
    })

    // 드롭다운 토글 메서드
    const toggleModulesDropdown = () => {
      showModulesDropdown.value = !showModulesDropdown.value
      closeOtherDropdowns('modules')
    }

    const toggleSearch = async () => {
      showSearch.value = !showSearch.value
      closeOtherDropdowns('search')
      
      if (showSearch.value) {
        await nextTick()
        searchInput.value?.focus()
      }
    }

    const toggleNotifications = () => {
      showNotifications.value = !showNotifications.value
      closeOtherDropdowns('notifications')
    }

    const toggleUserMenu = () => {
      showUserMenu.value = !showUserMenu.value
      closeOtherDropdowns('user')
    }

    const closeOtherDropdowns = (except = '') => {
      if (except !== 'modules') showModulesDropdown.value = false
      if (except !== 'search') showSearch.value = false
      if (except !== 'notifications') showNotifications.value = false
      if (except !== 'user') showUserMenu.value = false
    }

    const closeDropdowns = () => {
      closeOtherDropdowns()
    }

    const closeSearch = () => {
      showSearch.value = false
      searchQuery.value = ''
      searchResults.value = []
    }

    // 검색 기능
    const performSearch = async () => {
      if (!searchQuery.value.trim()) {
        searchResults.value = []
        return
      }

      // 실제로는 API를 호출하여 검색
      // 여기서는 더미 데이터로 시뮬레이션
      const query = searchQuery.value.toLowerCase()
      const mockResults = [
        {
          id: 1,
          type: 'customer',
          typeTitle: '고객',
          title: 'ABC Corporation',
          subtitle: '서울시 강남구',
          route: '/customers/abc-corp',
          icon: 'heroicons:building-office-2'
        },
        {
          id: 2,
          type: 'item',
          typeTitle: '제품',
          title: '노트북 Dell XPS 13',
          subtitle: '전자제품 > 컴퓨터',
          route: '/items/laptop-dell-xps-13',
          icon: 'heroicons:computer-desktop'
        },
        {
          id: 3,
          type: 'sales_order',
          typeTitle: '주문서',
          title: 'SO-2024-001',
          subtitle: 'ABC Corporation - ₩1,500,000',
          route: '/sales-orders/so-2024-001',
          icon: 'heroicons:document-text'
        }
      ]

      searchResults.value = mockResults.filter(result => 
        result.title.toLowerCase().includes(query) ||
        result.subtitle.toLowerCase().includes(query)
      )

      // 검색어를 최근 검색에 추가
      if (query && !recentSearches.value.includes(query)) {
        recentSearches.value.unshift(query)
        if (recentSearches.value.length > 5) {
          recentSearches.value.pop()
        }
      }
    }

    // 알림 관련 메서드
    const markAsRead = (notification) => {
      notification.read = true
    }

    const markAllAsRead = () => {
      notifications.value.forEach(n => n.read = true)
    }

    // 시간 포맷팅
    const formatTime = (timestamp) => {
      const now = new Date()
      const diff = now - timestamp
      const minutes = Math.floor(diff / (1000 * 60))
      const hours = Math.floor(minutes / 60)
      const days = Math.floor(hours / 24)

      if (minutes < 1) return '방금 전'
      if (minutes < 60) return `${minutes}분 전`
      if (hours < 24) return `${hours}시간 전`
      if (days < 7) return `${days}일 전`
      return timestamp.toLocaleDateString('ko-KR')
    }

    // 다크모드 토글
    const toggleDarkMode = () => {
      isDarkMode.value = !isDarkMode.value
      document.documentElement.setAttribute('data-theme', isDarkMode.value ? 'dark' : 'light')
      localStorage.setItem('darkMode', isDarkMode.value)
      closeDropdowns()
    }

    // 로그아웃
    const logout = () => {
      closeDropdowns()
      // 실제 로그아웃 로직
      router.push('/login')
    }

    // 외부 클릭 감지
    const handleClickOutside = (event) => {
      if (modulesDropdown.value && !modulesDropdown.value.contains(event.target)) {
        showModulesDropdown.value = false
      }
      if (searchContainer.value && !searchContainer.value.contains(event.target)) {
        showSearch.value = false
      }
      if (notificationDropdown.value && !notificationDropdown.value.contains(event.target)) {
        showNotifications.value = false
      }
      if (userDropdown.value && !userDropdown.value.contains(event.target)) {
        showUserMenu.value = false
      }
    }

    // 키보드 단축키
    const handleKeyboard = (event) => {
      if ((event.ctrlKey || event.metaKey) && event.key === 'k') {
        event.preventDefault()
        toggleSearch()
      }
    }

    // 라이프사이클
    onMounted(() => {
      document.addEventListener('click', handleClickOutside)
      document.addEventListener('keydown', handleKeyboard)
      
      // 다크모드 초기 설정
      const savedDarkMode = localStorage.getItem('darkMode')
      if (savedDarkMode) {
        isDarkMode.value = JSON.parse(savedDarkMode)
        document.documentElement.setAttribute('data-theme', isDarkMode.value ? 'dark' : 'light')
      }
    })

    onUnmounted(() => {
      document.removeEventListener('click', handleClickOutside)
      document.removeEventListener('keydown', handleKeyboard)
    })

    return {
      // 상태
      showModulesDropdown,
      showSearch,
      showNotifications,
      showUserMenu,
      searchQuery,
      searchResults,
      isDarkMode,
      user,
      modules,
      notifications,
      recentSearches,

      // 참조
      modulesDropdown,
      searchContainer,
      searchInput,
      notificationDropdown,
      userDropdown,

      // 계산된 속성
      unreadNotifications,
      aiStatus,
      groupedResults,

      // 메서드
      toggleModulesDropdown,
      toggleSearch,
      toggleNotifications,
      toggleUserMenu,
      closeDropdowns,
      closeSearch,
      performSearch,
      markAsRead,
      markAllAsRead,
      formatTime,
      toggleDarkMode,
      logout
    }
  }
}
</script>

<style scoped>
.app-header {
  height: 64px;
  background: white;
  border-bottom: 1px solid #e2e8f0;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  position: sticky;
  top: 0;
  z-index: 40;
}

.header-container {
  height: 100%;
  max-width: 100%;
  margin: 0 auto;
  padding: 0 1rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 2rem;
}

.logo {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  text-decoration: none;
  color: #1e293b;
  font-weight: 700;
  font-size: 1.25rem;
}

.logo-text {
  font-weight: 700;
}

.main-nav {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.nav-dropdown {
  position: relative;
}

.nav-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border: none;
  background: none;
  color: #64748b;
  cursor: pointer;
  border-radius: 6px;
  transition: all 0.2s ease;
  font-size: 0.875rem;
  font-weight: 500;
}

.nav-button:hover,
.nav-button.active {
  background: #f1f5f9;
  color: #3b82f6;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  text-decoration: none;
  color: #64748b;
  border-radius: 6px;
  transition: all 0.2s ease;
  font-size: 0.875rem;
  font-weight: 500;
}

.nav-link:hover,
.nav-link.active {
  background: #f1f5f9;
  color: #3b82f6;
}

.dropdown-menu {
  position: absolute;
  top: 100%;
  left: 0;
  margin-top: 0.5rem;
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  z-index: 50;
  animation: slideInUp 0.2s ease-out;
}

.modules-menu {
  width: 600px;
  max-width: 90vw;
}

.modules-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  padding: 0.5rem;
}

.module-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem;
  text-decoration: none;
  color: #1e293b;
  border-radius: 6px;
  transition: background 0.2s ease;
}

.module-item:hover {
  background: #f8fafc;
}

.module-name {
  font-weight: 600;
  margin-bottom: 0.25rem;
}

.module-desc {
  font-size: 0.75rem;
  color: #64748b;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.global-search {
  position: relative;
}

.search-trigger {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border: none;
  background: none;
  color: #64748b;
  cursor: pointer;
  border-radius: 6px;
  transition: all 0.2s ease;
}

.search-trigger:hover,
.search-trigger.active {
  background: #f1f5f9;
  color: #3b82f6;
}

.search-panel {
  position: absolute;
  top: 100%;
  right: 0;
  margin-top: 0.5rem;
  width: 400px;
  max-width: 90vw;
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  z-index: 50;
  animation: slideInUp 0.2s ease-out;
}

.search-input-container {
  position: relative;
  padding: 1rem;
  border-bottom: 1px solid #f1f5f9;
}

.search-icon {
  position: absolute;
  left: 1.75rem;
  top: 50%;
  transform: translateY(-50%);
  color: #94a3b8;
}

.search-input {
  width: 100%;
  padding: 0.75rem 2.5rem 0.75rem 2.5rem;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  font-size: 0.875rem;
  outline: none;
  transition: border-color 0.2s ease;
}

.search-input:focus {
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.search-kbd {
  position: absolute;
  right: 1.75rem;
  top: 50%;
  transform: translateY(-50%);
  background: #f1f5f9;
  color: #64748b;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.75rem;
  font-family: monospace;
}

.search-results,
.recent-searches {
  max-height: 300px;
  overflow-y: auto;
}

.result-section-title {
  padding: 0.75rem 1rem 0.5rem;
  font-size: 0.75rem;
  font-weight: 600;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.search-result-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1rem;
  text-decoration: none;
  color: #1e293b;
  transition: background 0.2s ease;
}

.search-result-item:hover {
  background: #f8fafc;
}

.result-title {
  font-weight: 500;
  margin-bottom: 0.25rem;
}

.result-subtitle {
  font-size: 0.75rem;
  color: #64748b;
}

.recent-search-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1rem;
  cursor: pointer;
  transition: background 0.2s ease;
  color: #64748b;
}

.recent-search-item:hover {
  background: #f8fafc;
}

.notification-button {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border: none;
  background: none;
  color: #64748b;
  cursor: pointer;
  border-radius: 6px;
  transition: all 0.2s ease;
}

.notification-button:hover,
.notification-button.active {
  background: #f1f5f9;
  color: #3b82f6;
}

.notification-badge {
  position: absolute;
  top: 6px;
  right: 6px;
  min-width: 18px;
  height: 18px;
  background: #ef4444;
  color: white;
  font-size: 0.625rem;
  font-weight: 600;
  border-radius: 9px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.notification-menu {
  width: 350px;
  max-width: 90vw;
  right: 0;
}

.notification-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  border-bottom: 1px solid #f1f5f9;
}

.notification-header h3 {
  margin: 0;
  font-weight: 600;
}

.mark-all-read {
  background: none;
  border: none;
  color: #3b82f6;
  font-size: 0.75rem;
  cursor: pointer;
}

.notification-list {
  max-height: 300px;
  overflow-y: auto;
}

.notification-item {
  display: flex;
  gap: 0.75rem;
  padding: 1rem;
  cursor: pointer;
  transition: background 0.2s ease;
  border-left: 3px solid transparent;
}

.notification-item.unread {
  background: #f8fafc;
  border-left-color: #3b82f6;
}

.notification-item:hover {
  background: #f1f5f9;
}

.notification-icon {
  flex-shrink: 0;
  width: 32px;
  height: 32px;
  background: #f1f5f9;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #3b82f6;
}

.notification-content {
  flex: 1;
  min-width: 0;
}

.notification-title {
  font-weight: 500;
  margin-bottom: 0.25rem;
}

.notification-message {
  font-size: 0.875rem;
  color: #64748b;
  margin-bottom: 0.5rem;
}

.notification-time {
  font-size: 0.75rem;
  color: #94a3b8;
}

.notification-footer {
  padding: 1rem;
  border-top: 1px solid #f1f5f9;
  text-align: center;
}

.notification-footer a {
  color: #3b82f6;
  text-decoration: none;
  font-size: 0.875rem;
}

.ai-status {
  position: relative;
  display: flex;
  align-items: center;
  padding: 0.5rem;
  color: #64748b;
}

.ai-status .status-dot {
  position: absolute;
  bottom: 2px;
  right: 2px;
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #94a3b8;
}

.ai-status.connected .status-dot {
  background: #10b981;
}

.ai-status.disconnected .status-dot {
  background: #ef4444;
}

.ai-status.connecting .status-dot {
  background: #f59e0b;
  animation: pulse 2s infinite;
}

.user-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.25rem 0.5rem;
  border: none;
  background: none;
  color: #1e293b;
  cursor: pointer;
  border-radius: 6px;
  transition: all 0.2s ease;
}

.user-button:hover,
.user-button.active {
  background: #f1f5f9;
}

.user-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  overflow: hidden;
  background: #e2e8f0;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #64748b;
}

.user-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.user-name {
  font-size: 0.875rem;
  font-weight: 500;
}

.user-dropdown-menu {
  width: 250px;
  right: 0;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem;
}

.user-avatar-large {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  overflow: hidden;
  background: #e2e8f0;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #64748b;
}

.user-avatar-large img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.user-name-large {
  font-weight: 600;
  margin-bottom: 0.25rem;
}

.user-email {
  font-size: 0.75rem;
  color: #64748b;
}

.dropdown-divider {
  margin: 0;
  border: none;
  border-top: 1px solid #f1f5f9;
}

.dropdown-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  width: 100%;
  padding: 0.75rem 1rem;
  border: none;
  background: none;
  color: #1e293b;
  text-decoration: none;
  cursor: pointer;
  transition: background 0.2s ease;
  font-size: 0.875rem;
}

.dropdown-item:hover {
  background: #f8fafc;
}

.dropdown-item.text-error {
  color: #ef4444;
}

@keyframes slideInUp {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

/* 반응형 */
@media (max-width: 768px) {
  .header-container {
    padding: 0 0.5rem;
  }
  
  .header-left {
    gap: 1rem;
  }
  
  .main-nav {
    gap: 0.5rem;
  }
  
  .user-name {
    display: none;
  }
  
  .modules-grid {
    grid-template-columns: 1fr;
  }
  
  .search-panel {
    width: 300px;
  }
}
</style>