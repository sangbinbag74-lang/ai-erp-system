<template>
  <div id="app" class="min-h-screen bg-gray-50">
    <!-- AI 코파일럿 -->
    <AICopilot />
    
    <!-- 메인 레이아웃 -->
    <div class="app-layout" :class="{ 'with-ai-sidebar': true }">
      <!-- 헤더 -->
      <AppHeader />
      
      <!-- 메인 컨텐츠 -->
      <main class="main-content">
        <router-view />
      </main>
      
      <!-- 푸터 -->
      <AppFooter />
    </div>

    <!-- 글로벌 알림 -->
    <NotificationCenter />
    
    <!-- 로딩 오버레이 -->
    <LoadingOverlay v-if="globalLoading" />
  </div>
</template>

<script>
import { ref, onMounted, provide } from 'vue'
import { useRouter } from 'vue-router'
import { useHead } from '@vueuse/head'
import AICopilot from '@/core/ai/AICopilot.vue'
import AppHeader from '@/core/layouts/AppHeader.vue'
import AppFooter from '@/core/layouts/AppFooter.vue'
import NotificationCenter from '@/core/components/NotificationCenter.vue'
import LoadingOverlay from '@/core/components/LoadingOverlay.vue'
import { startAIMonitoring, globalAI } from '@/composables/useAI'
import { useNotification } from '@/composables/useNotification'

export default {
  name: 'App',
  components: {
    AICopilot,
    AppHeader,
    AppFooter,
    NotificationCenter,
    LoadingOverlay
  },
  setup() {
    const router = useRouter()
    const { showNotification } = useNotification()
    const globalLoading = ref(false)

    // 메타 태그 설정
    useHead({
      title: 'ERPNext AI System',
      meta: [
        { name: 'description', content: 'AI 기반 차세대 ERP 시스템' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1' },
        { name: 'theme-color', content: '#3b82f6' }
      ],
      link: [
        { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' },
        { rel: 'preconnect', href: 'https://fonts.googleapis.com' },
        { 
          rel: 'preconnect', 
          href: 'https://fonts.gstatic.com', 
          crossorigin: true 
        },
        {
          rel: 'stylesheet',
          href: 'https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap'
        }
      ]
    })

    // 글로벌 로딩 상태 제공
    provide('globalLoading', {
      value: globalLoading,
      show: () => { globalLoading.value = true },
      hide: () => { globalLoading.value = false }
    })

    // 애플리케이션 초기화
    const initializeApp = async () => {
      try {
        // AI 모니터링 시작
        startAIMonitoring()
        
        // 초기 연결 확인
        setTimeout(() => {
          if (globalAI.status === 'connected') {
            showNotification('AI 어시스턴트가 준비되었습니다! 🤖', 'success')
          } else {
            showNotification('AI 서비스 연결을 확인하는 중...', 'info')
          }
        }, 2000)

      } catch (error) {
        console.error('앱 초기화 오류:', error)
        showNotification('앱 초기화 중 오류가 발생했습니다.', 'error')
      }
    }

    // 전역 오류 핸들러
    const handleGlobalError = (error, errorInfo) => {
      console.error('Global error:', error, errorInfo)
      showNotification('예상치 못한 오류가 발생했습니다.', 'error')
    }

    // 라우터 가드
    router.beforeEach((to, from, next) => {
      // 페이지 변경 시 로딩 표시
      globalLoading.value = true
      
      // 페이지 제목 업데이트
      if (to.meta?.title) {
        document.title = `${to.meta.title} - ERPNext AI System`
      }
      
      next()
    })

    router.afterEach(() => {
      // 페이지 로드 완료 후 로딩 숨김
      setTimeout(() => {
        globalLoading.value = false
      }, 300)
    })

    // 컴포넌트 마운트 시
    onMounted(() => {
      initializeApp()
    })

    // 전역 키보드 단축키
    const handleKeyboard = (event) => {
      // Ctrl/Cmd + K: AI 어시스턴트 토글
      if ((event.ctrlKey || event.metaKey) && event.key === 'k') {
        event.preventDefault()
        // AI 코파일럿 토글 로직은 AICopilot 컴포넌트에서 처리
      }

      // Escape: 모달/드롭다운 닫기
      if (event.key === 'Escape') {
        // 전역 이스케이프 이벤트 발생
        document.dispatchEvent(new CustomEvent('global-escape'))
      }
    }

    onMounted(() => {
      document.addEventListener('keydown', handleKeyboard)
    })

    return {
      globalLoading,
      handleGlobalError
    }
  }
}
</script>

<style scoped>
.app-layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  transition: margin-left 0.3s ease-in-out;
}

.app-layout.with-ai-sidebar {
  margin-left: 60px; /* AI 사이드바가 collapsed 상태일 때 */
}

@media (max-width: 768px) {
  .app-layout.with-ai-sidebar {
    margin-left: 0; /* 모바일에서는 오버레이 방식 */
  }
}

.main-content {
  flex: 1;
  padding: 0;
  background: #f8fafc;
  min-height: calc(100vh - 64px - 60px); /* 헤더와 푸터 높이 제외 */
}

/* 스크롤 개선 */
.main-content {
  scroll-behavior: smooth;
  overflow-x: hidden;
}

/* 반응형 레이아웃 */
@media (max-width: 1024px) {
  .main-content {
    padding: 0 1rem;
  }
}

@media (max-width: 640px) {
  .main-content {
    padding: 0 0.5rem;
  }
}

/* 프린트 스타일 */
@media print {
  .app-layout {
    margin-left: 0 !important;
  }
  
  .main-content {
    padding: 0 !important;
  }
}

/* 접근성 개선 */
@media (prefers-reduced-motion: reduce) {
  .app-layout,
  .main-content {
    transition: none !important;
  }
}

/* 다크모드 지원 */
@media (prefers-color-scheme: dark) {
  .main-content {
    background: #1e293b;
    color: #f1f5f9;
  }
}

/* 고대비 모드 지원 */
@media (prefers-contrast: high) {
  .main-content {
    border: 2px solid #000;
  }
}
</style>

<style>
/* 전역 스타일 */
#app {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

/* 포커스 가시성 개선 */
*:focus {
  outline: 2px solid #3b82f6;
  outline-offset: 2px;
}

/* 버튼 포커스 */
button:focus,
a:focus {
  outline: 2px solid #3b82f6;
  outline-offset: 2px;
}

/* 입력 필드 포커스 */
input:focus,
textarea:focus,
select:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

/* 링크 스타일 */
a {
  color: #3b82f6;
  text-decoration: none;
  transition: color 0.2s ease;
}

a:hover {
  color: #1d4ed8;
  text-decoration: underline;
}

/* 스크롤바 스타일링 */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: #f1f5f9;
}

::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}

/* Firefox 스크롤바 */
html {
  scrollbar-width: thin;
  scrollbar-color: #cbd5e1 #f1f5f9;
}

/* 선택 영역 스타일 */
::selection {
  background: #3b82f6;
  color: white;
}

::-moz-selection {
  background: #3b82f6;
  color: white;
}

/* 드래그 앤 드롭 */
.drag-over {
  border: 2px dashed #3b82f6 !important;
  background: rgba(59, 130, 246, 0.05) !important;
}

/* 로딩 애니메이션 */
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes slideInUp {
  from { opacity: 0; transform: translateY(100%); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes slideInRight {
  from { opacity: 0; transform: translateX(100%); }
  to { opacity: 1; transform: translateX(0); }
}

.fade-in {
  animation: fadeIn 0.3s ease-out;
}

.slide-in-up {
  animation: slideInUp 0.3s ease-out;
}

.slide-in-right {
  animation: slideInRight 0.3s ease-out;
}

/* 유틸리티 클래스 */
.text-truncate {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.visually-hidden {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}

/* 반응형 텍스트 */
@media (max-width: 640px) {
  .responsive-text {
    font-size: 0.875rem;
  }
}

/* 인쇄 최적화 */
@page {
  margin: 1cm;
}

@media print {
  * {
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }
  
  .no-print {
    display: none !important;
  }
  
  .print-break-before {
    page-break-before: always;
  }
  
  .print-break-after {
    page-break-after: always;
  }
}
</style>