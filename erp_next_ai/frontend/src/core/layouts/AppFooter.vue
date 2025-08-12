<template>
  <footer class="app-footer">
    <div class="footer-container">
      <!-- 좌측: 회사 정보 -->
      <div class="footer-left">
        <div class="company-info">
          <div class="logo-section">
            <Icon name="heroicons:cpu-chip" class="w-6 h-6 text-primary-600" />
            <span class="company-name">ERPNext AI System</span>
          </div>
          <p class="company-description">
            AI 기반 차세대 ERP 솔루션으로 업무 자동화와 효율성을 극대화합니다.
          </p>
        </div>
        
        <!-- 빠른 링크 -->
        <div class="quick-links">
          <h4>빠른 링크</h4>
          <div class="links-grid">
            <router-link to="/dashboard">대시보드</router-link>
            <router-link to="/customers">고객 관리</router-link>
            <router-link to="/items">제품 관리</router-link>
            <router-link to="/sales-orders">주문 관리</router-link>
          </div>
        </div>
        
        <!-- 모듈 링크 -->
        <div class="module-links">
          <h4>주요 모듈</h4>
          <div class="links-grid">
            <router-link to="/accounts">회계</router-link>
            <router-link to="/sales">영업</router-link>
            <router-link to="/purchase">구매</router-link>
            <router-link to="/stock">재고</router-link>
            <router-link to="/hr">인사</router-link>
            <router-link to="/projects">프로젝트</router-link>
          </div>
        </div>
        
        <!-- 지원 및 도움말 -->
        <div class="support-links">
          <h4>지원</h4>
          <div class="links-grid">
            <a href="/help" target="_blank">도움말</a>
            <a href="/api-docs" target="_blank">API 문서</a>
            <a href="/support" target="_blank">기술 지원</a>
            <a href="/feedback" target="_blank">피드백</a>
          </div>
        </div>
      </div>
      
      <!-- 우측: 시스템 정보 및 상태 -->
      <div class="footer-right">
        <!-- 시스템 상태 -->
        <div class="system-status">
          <h4>시스템 상태</h4>
          <div class="status-items">
            <div class="status-item">
              <div class="status-indicator" :class="systemHealth.api"></div>
              <span>API 서버</span>
              <span class="status-text">{{ getStatusText(systemHealth.api) }}</span>
            </div>
            <div class="status-item">
              <div class="status-indicator" :class="systemHealth.database"></div>
              <span>데이터베이스</span>
              <span class="status-text">{{ getStatusText(systemHealth.database) }}</span>
            </div>
            <div class="status-item">
              <div class="status-indicator" :class="systemHealth.ai"></div>
              <span>AI 서비스</span>
              <span class="status-text">{{ getStatusText(systemHealth.ai) }}</span>
            </div>
          </div>
        </div>
        
        <!-- AI 기능 상태 -->
        <div class="ai-features">
          <h4>AI 기능</h4>
          <div class="feature-list">
            <div class="feature-item" v-for="feature in aiFeatures" :key="feature.name">
              <Icon :name="feature.icon" class="w-4 h-4" :class="feature.enabled ? 'text-success-600' : 'text-gray-400'" />
              <span :class="feature.enabled ? 'text-gray-900' : 'text-gray-500'">{{ feature.name }}</span>
              <span class="feature-status" :class="feature.enabled ? 'text-success-600' : 'text-gray-400'">
                {{ feature.enabled ? '활성' : '비활성' }}
              </span>
            </div>
          </div>
        </div>
        
        <!-- 성능 메트릭 -->
        <div class="performance-metrics" v-if="showMetrics">
          <h4>성능 지표</h4>
          <div class="metrics-grid">
            <div class="metric-item">
              <span class="metric-label">응답 시간</span>
              <span class="metric-value">{{ performance.responseTime }}ms</span>
            </div>
            <div class="metric-item">
              <span class="metric-label">메모리 사용량</span>
              <span class="metric-value">{{ performance.memoryUsage }}%</span>
            </div>
            <div class="metric-item">
              <span class="metric-label">활성 사용자</span>
              <span class="metric-value">{{ performance.activeUsers }}</span>
            </div>
            <div class="metric-item">
              <span class="metric-label">처리된 요청</span>
              <span class="metric-value">{{ performance.totalRequests.toLocaleString() }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 하단 정보 바 -->
    <div class="footer-bottom">
      <div class="footer-bottom-content">
        <!-- 좌측: 저작권 정보 -->
        <div class="copyright">
          <span>&copy; 2024 ERPNext AI System. All rights reserved.</span>
          <span class="separator">|</span>
          <span>Built with Vue.js, FastAPI & AI</span>
        </div>
        
        <!-- 가운데: 버전 정보 -->
        <div class="version-info">
          <span class="version-badge">v{{ systemVersion }}</span>
          <span class="build-info">Build {{ buildNumber }}</span>
          <button @click="toggleMetrics" class="metrics-toggle" title="성능 지표 토글">
            <Icon name="heroicons:chart-bar" class="w-4 h-4" />
          </button>
        </div>
        
        <!-- 우측: 소셜 링크 및 설정 -->
        <div class="footer-actions">
          <button @click="showSystemInfo" class="action-button" title="시스템 정보">
            <Icon name="heroicons:information-circle" class="w-4 h-4" />
          </button>
          <button @click="openFeedback" class="action-button" title="피드백 보내기">
            <Icon name="heroicons:chat-bubble-left-right" class="w-4 h-4" />
          </button>
          <button @click="toggleTheme" class="action-button" title="테마 변경">
            <Icon :name="isDarkMode ? 'heroicons:sun' : 'heroicons:moon'" class="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  </footer>
</template>

<script>
import { ref, reactive, computed, onMounted } from 'vue'
import { Icon } from '@iconify/vue'
import { globalAI } from '@/composables/useAI'

export default {
  name: 'AppFooter',
  components: {
    Icon
  },
  setup() {
    const showMetrics = ref(false)
    const isDarkMode = ref(false)

    // 시스템 정보
    const systemVersion = ref('1.0.0')
    const buildNumber = ref('20241208.1')

    // 시스템 상태
    const systemHealth = reactive({
      api: 'healthy',
      database: 'healthy', 
      ai: 'healthy'
    })

    // AI 기능 목록
    const aiFeatures = ref([
      { name: '파일 관리', icon: 'heroicons:document-text', enabled: true },
      { name: '자동화', icon: 'heroicons:cog-6-tooth', enabled: true },
      { name: '예측 분석', icon: 'heroicons:chart-bar', enabled: true },
      { name: '자연어 처리', icon: 'heroicons:chat-bubble-left-ellipsis', enabled: true }
    ])

    // 성능 메트릭
    const performance = reactive({
      responseTime: 45,
      memoryUsage: 68,
      activeUsers: 24,
      totalRequests: 1548932
    })

    // 계산된 속성
    const aiStatus = computed(() => globalAI.status)

    // 상태 텍스트 변환
    const getStatusText = (status) => {
      const statusMap = {
        'healthy': '정상',
        'warning': '주의',
        'error': '오류',
        'connecting': '연결 중'
      }
      return statusMap[status] || '알 수 없음'
    }

    // 메트릭 토글
    const toggleMetrics = () => {
      showMetrics.value = !showMetrics.value
    }

    // 시스템 정보 표시
    const showSystemInfo = () => {
      const info = {
        version: systemVersion.value,
        build: buildNumber.value,
        nodeEnv: import.meta.env.MODE,
        apiUrl: import.meta.env.VITE_API_URL,
        timestamp: new Date().toISOString()
      }
      
      console.log('System Information:', info)
      
      // 모달이나 알림으로 표시할 수도 있음
      alert(`ERPNext AI System\n\n버전: ${info.version}\n빌드: ${info.build}\n환경: ${info.nodeEnv}\nAPI: ${info.apiUrl}\n시간: ${info.timestamp}`)
    }

    // 피드백 창 열기
    const openFeedback = () => {
      // 실제로는 피드백 모달이나 외부 서비스 연결
      const subject = encodeURIComponent('ERPNext AI System 피드백')
      const body = encodeURIComponent(`ERPNext AI System에 대한 피드백을 보내주세요.

버전: ${systemVersion.value}
빌드: ${buildNumber.value}
브라우저: ${navigator.userAgent}
URL: ${window.location.href}

피드백 내용:
`)
      
      window.open(`mailto:feedback@erpnext.ai?subject=${subject}&body=${body}`, '_blank')
    }

    // 테마 토글
    const toggleTheme = () => {
      isDarkMode.value = !isDarkMode.value
      document.documentElement.setAttribute('data-theme', isDarkMode.value ? 'dark' : 'light')
      localStorage.setItem('darkMode', isDarkMode.value)
    }

    // 시스템 상태 업데이트
    const updateSystemHealth = async () => {
      try {
        // API 상태 확인
        const apiResponse = await fetch('/api/health')
        systemHealth.api = apiResponse.ok ? 'healthy' : 'error'
        
        // AI 상태 반영
        systemHealth.ai = aiStatus.value === 'connected' ? 'healthy' : 'error'
        
        // 데이터베이스는 API를 통해 간접 확인
        systemHealth.database = systemHealth.api === 'healthy' ? 'healthy' : 'warning'
        
      } catch (error) {
        systemHealth.api = 'error'
        systemHealth.database = 'error'
        console.error('Health check failed:', error)
      }
    }

    // 성능 메트릭 업데이트 (시뮬레이션)
    const updatePerformanceMetrics = () => {
      performance.responseTime = Math.floor(Math.random() * 50) + 30
      performance.memoryUsage = Math.floor(Math.random() * 30) + 50
      performance.activeUsers = Math.floor(Math.random() * 20) + 15
      performance.totalRequests += Math.floor(Math.random() * 100) + 50
    }

    // 컴포넌트 마운트 시
    onMounted(() => {
      // 초기 상태 확인
      updateSystemHealth()
      
      // 다크모드 초기 설정
      const savedDarkMode = localStorage.getItem('darkMode')
      if (savedDarkMode) {
        isDarkMode.value = JSON.parse(savedDarkMode)
      }

      // 주기적 업데이트 (30초마다)
      setInterval(() => {
        updateSystemHealth()
        updatePerformanceMetrics()
      }, 30000)
    })

    return {
      // 상태
      showMetrics,
      isDarkMode,
      systemVersion,
      buildNumber,
      systemHealth,
      aiFeatures,
      performance,

      // 계산된 속성
      aiStatus,

      // 메서드
      getStatusText,
      toggleMetrics,
      showSystemInfo,
      openFeedback,
      toggleTheme
    }
  }
}
</script>

<style scoped>
.app-footer {
  background: #f8fafc;
  border-top: 1px solid #e2e8f0;
  margin-top: auto;
}

.footer-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 3rem 2rem;
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 4rem;
}

.footer-left {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 2rem;
}

.company-info .logo-section {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.company-name {
  font-size: 1.25rem;
  font-weight: 700;
  color: #1e293b;
}

.company-description {
  color: #64748b;
  line-height: 1.6;
  margin: 0;
}

.quick-links h4,
.module-links h4,
.support-links h4,
.system-status h4,
.ai-features h4,
.performance-metrics h4 {
  font-size: 0.875rem;
  font-weight: 600;
  color: #374151;
  margin: 0 0 1rem 0;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.links-grid {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.links-grid a {
  color: #64748b;
  text-decoration: none;
  font-size: 0.875rem;
  transition: color 0.2s ease;
}

.links-grid a:hover {
  color: #3b82f6;
}

.footer-right {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.status-items {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.status-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 0.875rem;
}

.status-indicator {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  flex-shrink: 0;
}

.status-indicator.healthy {
  background: #10b981;
}

.status-indicator.warning {
  background: #f59e0b;
}

.status-indicator.error {
  background: #ef4444;
}

.status-indicator.connecting {
  background: #6b7280;
  animation: pulse 2s infinite;
}

.status-text {
  margin-left: auto;
  color: #64748b;
  font-size: 0.75rem;
}

.feature-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.feature-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 0.875rem;
}

.feature-status {
  margin-left: auto;
  font-size: 0.75rem;
}

.metrics-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
}

.metric-item {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.metric-label {
  font-size: 0.75rem;
  color: #64748b;
}

.metric-value {
  font-size: 0.875rem;
  font-weight: 600;
  color: #1e293b;
}

.footer-bottom {
  background: #f1f5f9;
  border-top: 1px solid #e2e8f0;
}

.footer-bottom-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 1rem 2rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 0.875rem;
}

.copyright {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #64748b;
}

.separator {
  color: #cbd5e1;
}

.version-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.version-badge {
  background: #3b82f6;
  color: white;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 500;
}

.build-info {
  color: #64748b;
  font-size: 0.75rem;
}

.metrics-toggle {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  border: none;
  background: none;
  color: #64748b;
  cursor: pointer;
  border-radius: 4px;
  transition: all 0.2s ease;
}

.metrics-toggle:hover {
  background: #e2e8f0;
  color: #3b82f6;
}

.footer-actions {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.action-button {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border: none;
  background: none;
  color: #64748b;
  cursor: pointer;
  border-radius: 6px;
  transition: all 0.2s ease;
}

.action-button:hover {
  background: #e2e8f0;
  color: #3b82f6;
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
@media (max-width: 1024px) {
  .footer-container {
    grid-template-columns: 1fr;
    gap: 2rem;
  }
  
  .footer-left {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .footer-container {
    padding: 2rem 1rem;
  }
  
  .footer-left {
    grid-template-columns: 1fr;
  }
  
  .footer-bottom-content {
    padding: 1rem;
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }
  
  .copyright {
    flex-direction: column;
    gap: 0.25rem;
  }
  
  .metrics-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 640px) {
  .version-info {
    flex-direction: column;
    gap: 0.5rem;
    align-items: center;
  }
  
  .footer-actions {
    justify-content: center;
  }
}

/* 다크모드 지원 */
[data-theme="dark"] .app-footer {
  background: #1e293b;
  border-top-color: #475569;
}

[data-theme="dark"] .company-name {
  color: #f1f5f9;
}

[data-theme="dark"] .company-description {
  color: #cbd5e1;
}

[data-theme="dark"] .links-grid a {
  color: #cbd5e1;
}

[data-theme="dark"] .links-grid a:hover {
  color: #60a5fa;
}

[data-theme="dark"] .footer-bottom {
  background: #334155;
  border-top-color: #475569;
}

[data-theme="dark"] .copyright {
  color: #cbd5e1;
}

[data-theme="dark"] .metric-value {
  color: #f1f5f9;
}
</style>