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
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import AICopilot from '@/core/ai/AICopilot.vue'
import AppHeader from '@/core/layouts/AppHeader.vue'
import AppFooter from '@/core/layouts/AppFooter.vue'

const router = useRouter()
const globalLoading = ref(false)

// 애플리케이션 초기화
const initializeApp = async () => {
  try {
    console.log('🚀 ERPNext AI System 시작됨')
  } catch (error) {
    console.error('앱 초기화 오류:', error)
  }
}

// 라우터 가드
router.beforeEach((to, from, next) => {
  globalLoading.value = true
  
  if (to.meta?.title) {
    document.title = `${to.meta.title} - ERPNext AI System`
  }
  
  next()
})

router.afterEach(() => {
  setTimeout(() => {
    globalLoading.value = false
  }, 300)
})

onMounted(() => {
  initializeApp()
})
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
</style>