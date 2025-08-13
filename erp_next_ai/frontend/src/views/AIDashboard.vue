<template>
  <div class="ai-dashboard">
    <!-- AI 상태 헤더 -->
    <div class="ai-status-header">
      <div class="ai-status-content">
        <div class="ai-avatar">
          <div class="ai-core-indicator" :class="aiStatus">
            <Icon name="heroicons:cpu-chip" class="w-8 h-8" />
          </div>
        </div>
        <div class="ai-info">
          <h1 class="ai-title">ERPNext AGI System</h1>
          <p class="ai-subtitle">{{ aiStatusText }} • {{ tasksCompleted }} 작업 완료 • {{ efficiency }}% 효율성</p>
        </div>
        <div class="ai-controls">
          <button @click="toggleAIMode" class="ai-mode-btn" :class="aiMode">
            <Icon :name="aiModeIcon" class="w-5 h-5" />
            {{ aiModeText }}
          </button>
          <button @click="openAITerminal" class="ai-terminal-btn">
            <Icon name="heroicons:command-line" class="w-5 h-5" />
            AI Terminal
          </button>
        </div>
      </div>
    </div>

    <!-- AI 자연어 명령 입력 -->
    <div class="ai-command-center">
      <div class="command-input-container">
        <div class="command-prefix">
          <Icon name="heroicons:sparkles" class="w-6 h-6 text-ai-primary" />
          <span>AGI Command</span>
        </div>
        <textarea
          v-model="naturalLanguageCommand"
          @keydown.enter.ctrl="executeAICommand"
          placeholder="자연어로 ERP 작업을 명령하세요... 예: '지난 달 재무 보고서를 불러와서 수익 부분을 10% 증가로 수정하고 이유를 설명해줘'"
          class="command-input"
          rows="3"
        ></textarea>
        <div class="command-actions">
          <div class="command-suggestions">
            <button 
              v-for="suggestion in commandSuggestions" 
              :key="suggestion.id"
              @click="useCommandSuggestion(suggestion.command)"
              class="suggestion-chip"
            >
              {{ suggestion.label }}
            </button>
          </div>
          <button 
            @click="executeAICommand"
            :disabled="!naturalLanguageCommand.trim() || aiProcessing"
            class="execute-btn"
          >
            <Icon v-if="aiProcessing" name="heroicons:arrow-path" class="w-5 h-5 animate-spin" />
            <Icon v-else name="heroicons:play" class="w-5 h-5" />
            {{ aiProcessing ? '실행 중...' : 'Execute' }}
          </button>
        </div>
      </div>
    </div>

    <!-- AI 실행 결과 -->
    <div v-if="aiExecutionResult" class="ai-execution-result">
      <div class="result-header">
        <Icon name="heroicons:check-circle" class="w-6 h-6 text-ai-success" />
        <span>AI 실행 완료</span>
        <span class="execution-time">{{ aiExecutionResult.execution_time }}초</span>
      </div>
      <div class="result-content">
        <div class="result-explanation">
          <h3>실행 결과</h3>
          <p>{{ aiExecutionResult.explanation }}</p>
        </div>
        <div v-if="aiExecutionResult.actions_taken" class="actions-taken">
          <h4>수행된 작업들</h4>
          <ul>
            <li v-for="action in aiExecutionResult.actions_taken" :key="action">
              <Icon name="heroicons:arrow-right" class="w-4 h-4" />
              {{ action }}
            </li>
          </ul>
        </div>
        <div v-if="aiExecutionResult.files_affected" class="files-affected">
          <h4>영향받은 파일들</h4>
          <div class="file-list">
            <div v-for="file in aiExecutionResult.files_affected" :key="file.path" class="file-item">
              <Icon name="heroicons:document" class="w-4 h-4" />
              <span>{{ file.path }}</span>
              <span class="file-action">{{ file.action }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- AGI 워크플로 모니터링 -->
    <div class="workflow-monitor">
      <div class="monitor-header">
        <h2>자율 워크플로 모니터링</h2>
        <div class="monitor-controls">
          <button @click="pauseAllWorkflows" class="control-btn">
            <Icon name="heroicons:pause" class="w-4 h-4" />
            모든 워크플로 일시정지
          </button>
        </div>
      </div>

      <div class="active-workflows">
        <div v-for="workflow in activeWorkflows" :key="workflow.id" class="workflow-card">
          <div class="workflow-header">
            <div class="workflow-info">
              <h3>{{ workflow.name }}</h3>
              <span class="workflow-status" :class="workflow.status">{{ workflow.status }}</span>
            </div>
            <div class="workflow-progress">
              <div class="progress-bar">
                <div class="progress-fill" :style="{ width: workflow.progress + '%' }"></div>
              </div>
              <span>{{ workflow.progress }}%</span>
            </div>
          </div>
          
          <div class="workflow-steps">
            <div v-for="step in workflow.steps" :key="step.id" class="step-item" :class="step.status">
              <Icon :name="getStepIcon(step.status)" class="w-4 h-4" />
              <span>{{ step.description }}</span>
              <span v-if="step.duration" class="step-duration">{{ step.duration }}s</span>
            </div>
          </div>
          
          <div class="workflow-actions">
            <button @click="viewWorkflowDetails(workflow.id)" class="detail-btn">
              상세 보기
            </button>
            <button @click="stopWorkflow(workflow.id)" class="stop-btn">
              중지
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- ERPNext 모듈 현황 -->
    <div class="erp-modules-grid">
      <div v-for="module in erpModules" :key="module.name" class="module-card">
        <div class="module-header">
          <div class="module-icon" :style="{ background: module.color }">
            <Icon :name="module.icon" class="w-6 h-6 text-white" />
          </div>
          <div class="module-info">
            <h3>{{ module.name }}</h3>
            <p>{{ module.description }}</p>
          </div>
          <div class="module-ai-status">
            <Icon v-if="module.ai_enabled" name="heroicons:sparkles" class="w-5 h-5 text-ai-primary" />
            <span>{{ module.ai_enabled ? 'AI 활성' : 'AI 비활성' }}</span>
          </div>
        </div>
        
        <div class="module-stats">
          <div class="stat-item">
            <span class="stat-label">총 레코드</span>
            <span class="stat-value">{{ formatNumber(module.total_records) }}</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">오늘 생성</span>
            <span class="stat-value">{{ module.today_created }}</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">AI 처리</span>
            <span class="stat-value">{{ module.ai_processed }}</span>
          </div>
        </div>
        
        <div class="module-ai-insights">
          <h4>AI 인사이트</h4>
          <ul>
            <li v-for="insight in module.ai_insights" :key="insight">
              <Icon name="heroicons:lightbulb" class="w-4 h-4" />
              {{ insight }}
            </li>
          </ul>
        </div>
        
        <div class="module-actions">
          <button @click="openModule(module.name)" class="primary-btn">
            <Icon name="heroicons:arrow-top-right-on-square" class="w-4 h-4" />
            모듈 열기
          </button>
          <button @click="runAIAnalysis(module.name)" class="ai-btn">
            <Icon name="heroicons:cpu-chip" class="w-4 h-4" />
            AI 분석
          </button>
        </div>
      </div>
    </div>

    <!-- 파일 관리 센터 -->
    <div class="file-management-center">
      <div class="center-header">
        <h2>AI 파일 관리 센터</h2>
        <div class="file-upload-zone" @drop="handleFileDrop" @dragover.prevent>
          <Icon name="heroicons:cloud-arrow-up" class="w-8 h-8" />
          <span>파일을 드롭하거나 클릭하여 AI 분석</span>
          <input type="file" multiple @change="handleFileUpload" class="hidden" ref="fileInput">
        </div>
      </div>
      
      <div class="recent-files">
        <h3>최근 AI 처리 파일</h3>
        <div class="file-grid">
          <div v-for="file in recentFiles" :key="file.id" class="file-card">
            <div class="file-icon">
              <Icon :name="getFileIcon(file.type)" class="w-6 h-6" />
            </div>
            <div class="file-info">
              <h4>{{ file.name }}</h4>
              <p>{{ file.ai_summary }}</p>
              <span class="file-date">{{ formatDate(file.processed_at) }}</span>
            </div>
            <div class="file-actions">
              <button @click="reopenFile(file)" class="reopen-btn">
                <Icon name="heroicons:arrow-path" class="w-4 h-4" />
                재분석
              </button>
              <button @click="explainFile(file)" class="explain-btn">
                <Icon name="heroicons:chat-bubble-left-ellipsis" class="w-4 h-4" />
                설명
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- AI 학습 및 개선 센터 -->
    <div class="ai-learning-center">
      <div class="learning-header">
        <h2>AI 학습 및 자율 개선</h2>
        <div class="learning-stats">
          <div class="stat">
            <span class="label">학습된 패턴</span>
            <span class="value">{{ aiLearningStats.patterns_learned }}</span>
          </div>
          <div class="stat">
            <span class="label">정확도 개선</span>
            <span class="value">+{{ aiLearningStats.accuracy_improvement }}%</span>
          </div>
          <div class="stat">
            <span class="label">자동화 수준</span>
            <span class="value">{{ aiLearningStats.automation_level }}%</span>
          </div>
        </div>
      </div>
      
      <div class="learning-visualization">
        <h3>AI 성능 트렌드</h3>
        <div class="chart-container">
          <!-- Chart.js 차트가 여기에 렌더링됩니다 -->
          <canvas ref="performanceChart" width="400" height="200"></canvas>
        </div>
      </div>
      
      <div class="improvement-suggestions">
        <h3>AI 개선 제안</h3>
        <div class="suggestion-list">
          <div v-for="suggestion in aiImprovements" :key="suggestion.id" class="suggestion-item">
            <div class="suggestion-header">
              <Icon name="heroicons:lightbulb" class="w-5 h-5 text-ai-warning" />
              <h4>{{ suggestion.title }}</h4>
              <span class="impact-level" :class="suggestion.impact">{{ suggestion.impact }}</span>
            </div>
            <p>{{ suggestion.description }}</p>
            <div class="suggestion-actions">
              <button @click="implementSuggestion(suggestion.id)" class="implement-btn">
                구현하기
              </button>
              <button @click="dismissSuggestion(suggestion.id)" class="dismiss-btn">
                무시하기
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { Icon } from '@iconify/vue'
import { useAI } from '@/composables/useAI'
import { useNotification } from '@/composables/useNotification'

// AI 상태 관리
const aiStatus = ref('active')
const aiMode = ref('autonomous')
const tasksCompleted = ref(1247)
const efficiency = ref(94)
const aiProcessing = ref(false)

// 자연어 명령
const naturalLanguageCommand = ref('')
const aiExecutionResult = ref(null)

// AI 상태 컴포넌트
const aiStatusText = computed(() => {
  const statusMap = {
    'active': '활성 상태 • 모든 시스템 정상',
    'learning': '학습 중 • 새로운 패턴 분석',
    'processing': '처리 중 • 대용량 작업 실행',
    'idle': '대기 중 • 명령 대기',
    'error': '오류 발생 • 복구 중'
  }
  return statusMap[aiStatus.value] || '알 수 없음'
})

const aiModeText = computed(() => {
  const modeMap = {
    'autonomous': '완전 자율',
    'assisted': '보조 모드',
    'manual': '수동 제어'
  }
  return modeMap[aiMode.value]
})

const aiModeIcon = computed(() => {
  const iconMap = {
    'autonomous': 'heroicons:bolt',
    'assisted': 'heroicons:hand-raised',
    'manual': 'heroicons:cog-6-tooth'
  }
  return iconMap[aiMode.value]
})

// 명령 제안
const commandSuggestions = ref([
  { id: 1, label: '📊 월간 보고서', command: '이번 달 모든 모듈의 월간 보고서를 생성하고 주요 KPI를 분석해서 경영진용 요약 보고서를 만들어줘' },
  { id: 2, label: '📦 재고 최적화', command: '현재 재고 상황을 분석하고 부족한 품목은 자동 주문하고 과잉 재고는 할인 판매 제안해줘' },
  { id: 3, label: '💰 수익 예측', command: '과거 3년 데이터를 기반으로 다음 분기 수익을 예측하고 목표 달성을 위한 액션 플랜을 수립해줘' },
  { id: 4, label: '👥 직원 성과', command: '모든 직원의 성과 데이터를 분석하고 개별 피드백과 팀별 개선 방안을 제시해줘' }
])

// 활성 워크플로
const activeWorkflows = ref([
  {
    id: 1,
    name: '자동 재고 관리',
    status: 'running',
    progress: 75,
    steps: [
      { id: 1, description: '재고 데이터 분석', status: 'completed', duration: 2.3 },
      { id: 2, description: '부족 품목 식별', status: 'completed', duration: 1.8 },
      { id: 3, description: '공급업체 연락', status: 'running', duration: null },
      { id: 4, description: '주문서 생성', status: 'pending', duration: null }
    ]
  },
  {
    id: 2,
    name: '월간 재무 보고서 생성',
    status: 'running',
    progress: 45,
    steps: [
      { id: 1, description: '데이터 수집', status: 'completed', duration: 5.2 },
      { id: 2, description: '분석 및 계산', status: 'running', duration: null },
      { id: 3, description: '차트 생성', status: 'pending', duration: null },
      { id: 4, description: '보고서 작성', status: 'pending', duration: null }
    ]
  }
])

// ERP 모듈
const erpModules = ref([
  {
    name: 'Accounts',
    description: '회계 및 재무 관리',
    icon: 'heroicons:calculator',
    color: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    ai_enabled: true,
    total_records: 15420,
    today_created: 23,
    ai_processed: 156,
    ai_insights: [
      '현금 흐름이 지난달 대비 15% 개선됨',
      '미수금 회수율이 평균보다 8% 높음',
      '비용 절감 기회 3건 발견'
    ]
  },
  {
    name: 'Sales',
    description: '영업 및 판매 관리',
    icon: 'heroicons:chart-bar-square',
    color: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
    ai_enabled: true,
    total_records: 8945,
    today_created: 47,
    ai_processed: 89,
    ai_insights: [
      '이번 주 판매 목표 달성률 112%',
      '상위 고객 3명이 추가 주문 예정',
      '신제품 판매 트렌드 상승세'
    ]
  },
  {
    name: 'Purchase',
    description: '구매 및 조달 관리',
    icon: 'heroicons:shopping-cart',
    color: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
    ai_enabled: true,
    total_records: 5632,
    today_created: 12,
    ai_processed: 34,
    ai_insights: [
      '공급업체 A의 납기 지연 패턴 감지',
      '원자재 가격 15% 인상 예상',
      '대체 공급업체 2곳 추천 가능'
    ]
  },
  {
    name: 'Stock',
    description: '재고 및 창고 관리',
    icon: 'heroicons:cube',
    color: 'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)',
    ai_enabled: true,
    total_records: 12784,
    today_created: 68,
    ai_processed: 203,
    ai_insights: [
      '재고 회전율 최적화로 20% 비용 절감',
      '계절성 수요 패턴 분석 완료',
      '안전 재고 수준 자동 조정 제안'
    ]
  },
  {
    name: 'HR',
    description: '인사 및 급여 관리',
    icon: 'heroicons:users',
    color: 'linear-gradient(135deg, #fa709a 0%, #fee140 100%)',
    ai_enabled: true,
    total_records: 892,
    today_created: 3,
    ai_processed: 15,
    ai_insights: [
      '직원 만족도 85% 유지',
      '이직률 예측 모델 정확도 92%',
      '성과 평가 자동화 완료'
    ]
  },
  {
    name: 'Projects',
    description: '프로젝트 관리',
    icon: 'heroicons:folder',
    color: 'linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)',
    ai_enabled: true,
    total_records: 156,
    today_created: 2,
    ai_processed: 8,
    ai_insights: [
      '프로젝트 완료율 94% 달성',
      '리소스 배분 최적화 제안',
      '지연 위험 프로젝트 2건 감지'
    ]
  }
])

// 최근 파일
const recentFiles = ref([
  {
    id: 1,
    name: '2024년_Q3_재무보고서.xlsx',
    type: 'excel',
    ai_summary: '3분기 매출 15% 증가, 순이익 마진 개선',
    processed_at: new Date(Date.now() - 3600000)
  },
  {
    id: 2,
    name: '고객_만족도_조사.pdf',
    type: 'pdf',
    ai_summary: '전체 만족도 4.2/5, 배송 부분 개선 필요',
    processed_at: new Date(Date.now() - 7200000)
  },
  {
    id: 3,
    name: '재고_현황_리포트.csv',
    type: 'csv',
    ai_summary: '15개 품목 재주문 필요, 3개 품목 과잉재고',
    processed_at: new Date(Date.now() - 10800000)
  }
])

// AI 학습 통계
const aiLearningStats = ref({
  patterns_learned: 1247,
  accuracy_improvement: 12.5,
  automation_level: 87
})

// AI 개선 제안
const aiImprovements = ref([
  {
    id: 1,
    title: '워크플로 자동화 확장',
    description: '반복적인 승인 프로세스를 AI가 자동으로 처리하도록 확장할 수 있습니다.',
    impact: 'high'
  },
  {
    id: 2,
    title: '예측 모델 정확도 향상',
    description: '추가 데이터 소스를 활용하여 수요 예측 정확도를 15% 향상시킬 수 있습니다.',
    impact: 'medium'
  },
  {
    id: 3,
    title: '실시간 대시보드 업데이트',
    description: '실시간 데이터 스트리밍을 통해 대시보드 업데이트 속도를 개선할 수 있습니다.',
    impact: 'low'
  }
])

// 컴포저블 사용
const { processAIRequest } = useAI()
const { showNotification } = useNotification()

// 메서드
const toggleAIMode = () => {
  const modes = ['autonomous', 'assisted', 'manual']
  const currentIndex = modes.indexOf(aiMode.value)
  aiMode.value = modes[(currentIndex + 1) % modes.length]
  
  showNotification(`AI 모드가 ${aiModeText.value}로 변경되었습니다.`, 'info')
}

const executeAICommand = async () => {
  if (!naturalLanguageCommand.value.trim()) return
  
  aiProcessing.value = true
  
  try {
    const result = await processAIRequest(naturalLanguageCommand.value, {
      mode: 'agi',
      user_context: 'dashboard'
    })
    
    aiExecutionResult.value = result
    tasksCompleted.value++
    
    showNotification('AI 명령이 성공적으로 실행되었습니다.', 'success')
    
  } catch (error) {
    showNotification('AI 명령 실행 중 오류가 발생했습니다.', 'error')
    console.error('AI 명령 실행 오류:', error)
  } finally {
    aiProcessing.value = false
    naturalLanguageCommand.value = ''
  }
}

const useCommandSuggestion = (command) => {
  naturalLanguageCommand.value = command
}

const getStepIcon = (status) => {
  const iconMap = {
    'completed': 'heroicons:check-circle',
    'running': 'heroicons:arrow-path',
    'pending': 'heroicons:clock',
    'failed': 'heroicons:x-circle'
  }
  return iconMap[status] || 'heroicons:question-mark-circle'
}

const getFileIcon = (type) => {
  const iconMap = {
    'excel': 'heroicons:table-cells',
    'pdf': 'heroicons:document-text',
    'csv': 'heroicons:document-chart-bar',
    'image': 'heroicons:photo'
  }
  return iconMap[type] || 'heroicons:document'
}

const formatNumber = (num) => {
  return new Intl.NumberFormat('ko-KR').format(num)
}

const formatDate = (date) => {
  return new Intl.DateTimeFormat('ko-KR', {
    hour: '2-digit',
    minute: '2-digit',
    month: 'short',
    day: 'numeric'
  }).format(date)
}

// 라이프사이클
onMounted(() => {
  // AI 상태 모니터링 시작
  setInterval(() => {
    // 실시간 AI 상태 업데이트
  }, 5000)
  
  // 차트 초기화
  // initializePerformanceChart()
})
</script>

<style scoped>
.ai-dashboard {
  min-height: 100vh;
  background: var(--bg-primary);
  padding: 2rem;
  color: var(--text-primary);
}

/* AI 상태 헤더 */
.ai-status-header {
  background: var(--gradient-primary);
  border-radius: var(--border-radius-lg);
  padding: 2rem;
  margin-bottom: 2rem;
  box-shadow: var(--shadow-lg);
}

.ai-status-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 1.5rem;
}

.ai-avatar {
  position: relative;
}

.ai-core-indicator {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  position: relative;
  overflow: hidden;
}

.ai-core-indicator.active {
  background: radial-gradient(circle, var(--ai-primary) 0%, var(--ai-accent) 100%);
  box-shadow: var(--glow-primary);
  animation: pulse-glow 2s infinite;
}

.ai-title {
  font-size: 2.5rem;
  font-weight: 700;
  margin: 0;
  background: linear-gradient(45deg, #ffffff, #e0e0e0);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  letter-spacing: -0.02em;
}

.ai-subtitle {
  margin: 0.5rem 0 0 0;
  opacity: 0.9;
  font-size: 1.1rem;
}

.ai-controls {
  display: flex;
  gap: 1rem;
}

.ai-mode-btn, .ai-terminal-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 1rem 1.5rem;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: var(--border-radius);
  color: white;
  font-weight: 500;
  transition: all 0.3s ease;
  cursor: pointer;
}

.ai-mode-btn:hover, .ai-terminal-btn:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: translateY(-2px);
}

.ai-mode-btn.autonomous {
  background: rgba(0, 255, 135, 0.2);
  border-color: var(--ai-success);
}

/* AI 명령 센터 */
.ai-command-center {
  background: var(--bg-secondary);
  border-radius: var(--border-radius-lg);
  padding: 2rem;
  margin-bottom: 2rem;
  border: 1px solid var(--border-primary);
}

.command-input-container {
  position: relative;
}

.command-prefix {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 1rem;
  font-weight: 600;
  color: var(--ai-primary);
}

.command-input {
  width: 100%;
  background: var(--bg-tertiary);
  border: 2px solid var(--border-secondary);
  border-radius: var(--border-radius);
  padding: 1rem;
  color: var(--text-primary);
  font-size: 1.1rem;
  resize: vertical;
  min-height: 120px;
  transition: all 0.3s ease;
}

.command-input:focus {
  outline: none;
  border-color: var(--ai-primary);
  box-shadow: var(--glow-primary);
}

.command-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 1rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.command-suggestions {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.suggestion-chip {
  padding: 0.5rem 1rem;
  background: var(--bg-elevated);
  border: 1px solid var(--border-secondary);
  border-radius: 20px;
  color: var(--text-secondary);
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.suggestion-chip:hover {
  background: var(--ai-primary);
  color: white;
  transform: translateY(-1px);
}

.execute-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 1rem 2rem;
  background: var(--gradient-primary);
  border: none;
  border-radius: var(--border-radius);
  color: white;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.execute-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: var(--glow-primary);
}

.execute-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* AI 실행 결과 */
.ai-execution-result {
  background: var(--bg-secondary);
  border: 1px solid var(--ai-success);
  border-radius: var(--border-radius-lg);
  padding: 2rem;
  margin-bottom: 2rem;
  box-shadow: 0 0 20px rgba(0, 255, 135, 0.1);
}

.result-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.5rem;
  font-weight: 600;
}

.execution-time {
  margin-left: auto;
  color: var(--text-secondary);
}

/* 워크플로 모니터링 */
.workflow-monitor {
  background: var(--bg-secondary);
  border-radius: var(--border-radius-lg);
  padding: 2rem;
  margin-bottom: 2rem;
  border: 1px solid var(--border-primary);
}

.monitor-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.workflow-card {
  background: var(--bg-tertiary);
  border-radius: var(--border-radius);
  padding: 1.5rem;
  margin-bottom: 1.5rem;
  border: 1px solid var(--border-secondary);
  transition: all 0.3s ease;
}

.workflow-card:hover {
  border-color: var(--ai-primary);
  box-shadow: var(--shadow-md);
}

.workflow-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.workflow-status {
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 500;
}

.workflow-status.running {
  background: var(--ai-primary);
  color: white;
}

.workflow-progress {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.progress-bar {
  width: 200px;
  height: 8px;
  background: var(--bg-primary);
  border-radius: 4px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: var(--gradient-primary);
  transition: width 0.3s ease;
}

.workflow-steps {
  margin: 1rem 0;
}

.step-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.5rem 0;
  color: var(--text-secondary);
}

.step-item.completed {
  color: var(--ai-success);
}

.step-item.running {
  color: var(--ai-primary);
}

/* ERP 모듈 그리드 */
.erp-modules-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 2rem;
  margin-bottom: 2rem;
}

.module-card {
  background: var(--bg-secondary);
  border-radius: var(--border-radius-lg);
  padding: 2rem;
  border: 1px solid var(--border-primary);
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.module-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: var(--gradient-primary);
}

.module-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-lg);
  border-color: var(--ai-primary);
}

.module-header {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.module-icon {
  width: 48px;
  height: 48px;
  border-radius: var(--border-radius);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.module-info h3 {
  margin: 0 0 0.5rem 0;
  font-size: 1.25rem;
}

.module-info p {
  margin: 0;
  color: var(--text-secondary);
}

.module-ai-status {
  margin-left: auto;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: var(--ai-primary);
  font-size: 0.9rem;
}

.module-stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.stat-item {
  text-align: center;
  padding: 1rem;
  background: var(--bg-tertiary);
  border-radius: var(--border-radius);
}

.stat-label {
  display: block;
  color: var(--text-secondary);
  font-size: 0.8rem;
  margin-bottom: 0.5rem;
}

.stat-value {
  display: block;
  font-weight: 600;
  font-size: 1.25rem;
  color: var(--ai-primary);
}

.module-ai-insights {
  margin-bottom: 1.5rem;
}

.module-ai-insights h4 {
  margin: 0 0 1rem 0;
  font-size: 1rem;
  color: var(--ai-primary);
}

.module-ai-insights ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.module-ai-insights li {
  display: flex;
  align-items: flex-start;
  gap: 0.5rem;
  padding: 0.5rem 0;
  color: var(--text-secondary);
  font-size: 0.9rem;
}

.module-actions {
  display: flex;
  gap: 1rem;
}

.primary-btn, .ai-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  border-radius: var(--border-radius);
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  flex: 1;
  justify-content: center;
}

.primary-btn {
  background: var(--gradient-primary);
  border: none;
  color: white;
}

.ai-btn {
  background: var(--bg-elevated);
  border: 1px solid var(--border-secondary);
  color: var(--text-primary);
}

.primary-btn:hover, .ai-btn:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

/* 파일 관리 센터 */
.file-management-center {
  background: var(--bg-secondary);
  border-radius: var(--border-radius-lg);
  padding: 2rem;
  margin-bottom: 2rem;
  border: 1px solid var(--border-primary);
}

.center-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.file-upload-zone {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  padding: 2rem;
  border: 2px dashed var(--border-secondary);
  border-radius: var(--border-radius);
  cursor: pointer;
  transition: all 0.3s ease;
  min-width: 300px;
}

.file-upload-zone:hover {
  border-color: var(--ai-primary);
  background: var(--bg-tertiary);
}

.file-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1rem;
}

.file-card {
  background: var(--bg-tertiary);
  border-radius: var(--border-radius);
  padding: 1.5rem;
  border: 1px solid var(--border-secondary);
  transition: all 0.3s ease;
}

.file-card:hover {
  border-color: var(--ai-primary);
  transform: translateY(-2px);
}

/* AI 학습 센터 */
.ai-learning-center {
  background: var(--bg-secondary);
  border-radius: var(--border-radius-lg);
  padding: 2rem;
  border: 1px solid var(--border-primary);
}

.learning-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.learning-stats {
  display: flex;
  gap: 2rem;
}

.learning-stats .stat {
  text-align: center;
}

.learning-stats .label {
  display: block;
  color: var(--text-secondary);
  font-size: 0.9rem;
  margin-bottom: 0.5rem;
}

.learning-stats .value {
  display: block;
  font-weight: 600;
  font-size: 1.5rem;
  color: var(--ai-primary);
}

.chart-container {
  background: var(--bg-tertiary);
  border-radius: var(--border-radius);
  padding: 1rem;
  margin-bottom: 2rem;
}

.suggestion-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.suggestion-item {
  background: var(--bg-tertiary);
  border-radius: var(--border-radius);
  padding: 1.5rem;
  border: 1px solid var(--border-secondary);
}

.suggestion-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;
}

.impact-level {
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 500;
  margin-left: auto;
}

.impact-level.high {
  background: var(--ai-error);
  color: white;
}

.impact-level.medium {
  background: var(--ai-warning);
  color: white;
}

.impact-level.low {
  background: var(--ai-info);
  color: white;
}

.suggestion-actions {
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
}

.implement-btn, .dismiss-btn {
  padding: 0.5rem 1rem;
  border-radius: var(--border-radius);
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.implement-btn {
  background: var(--ai-success);
  border: none;
  color: white;
}

.dismiss-btn {
  background: var(--bg-elevated);
  border: 1px solid var(--border-secondary);
  color: var(--text-secondary);
}

@keyframes pulse-glow {
  0%, 100% {
    box-shadow: var(--glow-primary);
  }
  50% {
    box-shadow: 0 0 30px rgba(0, 212, 255, 0.5);
  }
}

/* 반응형 */
@media (max-width: 768px) {
  .ai-dashboard {
    padding: 1rem;
  }
  
  .ai-status-content {
    flex-direction: column;
    text-align: center;
  }
  
  .ai-title {
    font-size: 2rem;
  }
  
  .erp-modules-grid {
    grid-template-columns: 1fr;
  }
  
  .command-actions {
    flex-direction: column;
    align-items: stretch;
  }
  
  .learning-stats {
    flex-direction: column;
    gap: 1rem;
  }
}
</style>