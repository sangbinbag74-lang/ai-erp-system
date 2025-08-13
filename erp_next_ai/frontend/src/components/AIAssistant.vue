<template>
  <!-- AI 어시스턴트 플로팅 창 -->
  <div class="ai-assistant-floating" :class="{ expanded: isExpanded }">
    <div class="ai-header" @click="toggleExpand">
      <div class="ai-avatar-small">
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"></path>
        </svg>
      </div>
      <span class="ai-title-small">AI 어시스턴트</span>
      <svg class="w-4 h-4 ai-toggle-icon" :class="{ rotated: isExpanded }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
      </svg>
      <div class="ai-status" :class="statusColor">
        <div class="status-dot"></div>
        <span class="status-text">{{ statusText }}</span>
      </div>
    </div>

    <div v-if="isExpanded" class="ai-content">
      <!-- 현재 페이지 컨텍스트 -->
      <div class="ai-context-bar" v-if="currentContext">
        <div class="context-info">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
          </svg>
          <span>{{ currentContext }} 페이지에서 도움을 드릴게요</span>
        </div>
      </div>

      <!-- AI 제안사항 -->
      <div class="ai-suggestions" v-if="suggestions.length && !hasMessages">
        <div class="suggestions-header">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
          </svg>
          <span>추천 질문</span>
        </div>
        <div class="suggestions-list">
          <button 
            v-for="suggestion in suggestions" 
            :key="suggestion.id"
            @click="useSuggestion(suggestion)"
            class="suggestion-item"
          >
            {{ suggestion.text }}
          </button>
        </div>
      </div>

      <div class="ai-chat-area">
        <div class="ai-messages" ref="messagesContainer">
          <div v-for="message in messages" :key="message.id" class="ai-message" :class="message.type">
            <div class="message-content" v-html="formatMessage(message.content)"></div>
            <div class="message-time">{{ message.time }}</div>
          </div>
          
          <!-- 타이핑 인디케이터 -->
          <div v-if="isTyping" class="ai-message ai typing-indicator">
            <div class="message-content">
              <div class="typing-dots">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="ai-input-area">
        <!-- 빠른 액션 버튼들 -->
        <div class="quick-actions" v-if="quickActions.length">
          <button 
            v-for="action in quickActions" 
            :key="action.id"
            @click="executeQuickAction(action)"
            class="quick-action-btn"
            :title="action.description"
          >
            <component :is="action.icon" class="w-4 h-4" />
          </button>
        </div>

        <div class="ai-input-container">
          <textarea
            v-model="currentInput"
            @keydown.enter.exact.prevent="sendMessage"
            @keydown.shift.enter="addNewLine"
            :placeholder="inputPlaceholder"
            class="ai-input"
            rows="2"
            :disabled="isTyping"
          ></textarea>
          <button 
            @click="sendMessage" 
            class="ai-send-btn" 
            :disabled="!currentInput.trim() || isTyping"
          >
            <svg v-if="!isTyping" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"></path>
            </svg>
            <svg v-else class="w-5 h-5 animate-spin" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="m4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, nextTick, onMounted } from 'vue'
import { useRoute } from 'vue-router'

// Props
const props = defineProps({
  context: {
    type: String,
    default: ''
  }
})

// 상태 관리
const isExpanded = ref(false)
const currentInput = ref('')
const messages = ref([])
const isTyping = ref(false)
const messagesContainer = ref(null)
const route = useRoute()

// 현재 페이지 컨텍스트
const currentContext = computed(() => {
  if (props.context) return props.context
  
  const routeNames = {
    'AIDashboard': '대시보드',
    'Accounts': '회계 관리',
    'Sales': '영업 관리',
    'Purchase': '구매 관리',
    'Stock': '재고 관리',
    'Manufacturing': '제조 관리',
    'Assets': '자산 관리',
    'Quality': '품질 관리',
    'HR': '인사 관리',
    'Projects': '프로젝트 관리',
    'CRM': '고객관계관리',
    'Support': '고객지원',
    'Website': '웹사이트 관리'
  }
  
  return routeNames[route.name] || '시스템'
})

// AI 상태
const statusColor = ref('online')
const statusText = computed(() => {
  switch (statusColor.value) {
    case 'online': return '온라인'
    case 'busy': return '처리중'
    case 'offline': return '오프라인'
    default: return '준비됨'
  }
})

// 입력 플레이스홀더 (페이지별 맞춤)
const inputPlaceholder = computed(() => {
  const placeholders = {
    '대시보드': '전체 시스템에 대해 질문하세요...',
    '회계 관리': '재무 데이터나 회계 업무에 대해 질문하세요...',
    '영업 관리': '매출, 고객, 주문에 대해 질문하세요...',
    '구매 관리': '구매 주문, 공급업체에 대해 질문하세요...',
    '재고 관리': '재고 현황, 입출고에 대해 질문하세요...',
    '제조 관리': '생산 계획, 품질에 대해 질문하세요...',
    '자산 관리': '자산 현황, 감가상각에 대해 질문하세요...',
    '품질 관리': '품질 검사, 기준에 대해 질문하세요...',
    '인사 관리': '직원, 급여, 근태에 대해 질문하세요...',
    '프로젝트 관리': '프로젝트 진행상황에 대해 질문하세요...',
    '고객관계관리': '고객 정보, 영업기회에 대해 질문하세요...',
    '고객지원': '티켓, 문의사항에 대해 질문하세요...',
    '웹사이트 관리': 'SEO, 콘텐츠에 대해 질문하세요...'
  }
  
  return placeholders[currentContext.value] || 'AI에게 도움을 요청하세요...'
})

// 페이지별 제안사항
const suggestions = computed(() => {
  const pageSuggestions = {
    '대시보드': [
      { id: 1, text: '오늘의 중요한 알림 요약해줘' },
      { id: 2, text: '시스템 성능 상태 확인해줘' },
      { id: 3, text: '이번 주 주요 지표 분석해줘' },
      { id: 4, text: '할 일 우선순위를 정해줘' }
    ],
    '회계 관리': [
      { id: 1, text: '이번 달 손익 현황 분석해줘' },
      { id: 2, text: '현금흐름 예측해줘' },
      { id: 3, text: '세무신고 일정 확인해줘' },
      { id: 4, text: '예산 대비 실적 검토해줘' }
    ],
    '영업 관리': [
      { id: 1, text: '이번 달 매출 목표 달성률은?' },
      { id: 2, text: '신규 고객 현황 보여줘' },
      { id: 3, text: '상위 고객 분석해줘' },
      { id: 4, text: '영업 파이프라인 검토해줘' }
    ],
    '구매 관리': [
      { id: 1, text: '미결제 구매주문 확인해줘' },
      { id: 2, text: '공급업체별 성과 분석해줘' },
      { id: 3, text: '구매비용 절감 방안 제시해줘' },
      { id: 4, text: '재고 부족 품목 주문 생성해줘' }
    ]
  }
  
  return pageSuggestions[currentContext.value] || []
})

// 빠른 액션 버튼들
const quickActions = ref([
  { 
    id: 'search', 
    icon: 'MagnifyingGlassIcon', 
    description: '검색', 
    action: 'search' 
  },
  { 
    id: 'report', 
    icon: 'DocumentChartBarIcon', 
    description: '보고서 생성', 
    action: 'generate_report' 
  },
  { 
    id: 'export', 
    icon: 'ArrowDownTrayIcon', 
    description: '데이터 내보내기', 
    action: 'export_data' 
  }
])

// 메시지가 있는지 확인
const hasMessages = computed(() => messages.value.length > 0)

// 메서드들
const toggleExpand = () => {
  isExpanded.value = !isExpanded.value
  if (isExpanded.value) {
    nextTick(() => scrollToBottom())
  }
}

const sendMessage = async () => {
  if (!currentInput.value.trim() || isTyping.value) return
  
  const userMessage = currentInput.value.trim()
  currentInput.value = ''
  
  // 사용자 메시지 추가
  messages.value.push({
    id: Date.now(),
    type: 'user',
    content: userMessage,
    time: new Date().toLocaleTimeString('ko-KR', { hour: '2-digit', minute: '2-digit' })
  })
  
  // 스크롤 및 타이핑 시작
  nextTick(() => scrollToBottom())
  isTyping.value = true
  statusColor.value = 'busy'
  
  // AI 응답 시뮬레이션
  setTimeout(() => {
    const contextualResponse = generateContextualResponse(userMessage)
    
    messages.value.push({
      id: Date.now() + 1,
      type: 'ai',
      content: contextualResponse,
      time: new Date().toLocaleTimeString('ko-KR', { hour: '2-digit', minute: '2-digit' })
    })
    
    isTyping.value = false
    statusColor.value = 'online'
    nextTick(() => scrollToBottom())
  }, 1500 + Math.random() * 1000)
}

const useSuggestion = (suggestion) => {
  currentInput.value = suggestion.text
  sendMessage()
}

const executeQuickAction = (action) => {
  const actionMessages = {
    'search': '검색 기능을 실행합니다. 무엇을 찾고 싶으신가요?',
    'generate_report': `${currentContext.value}에 대한 보고서를 생성하고 있습니다...`,
    'export_data': `${currentContext.value} 데이터를 내보내는 중입니다...`
  }
  
  messages.value.push({
    id: Date.now(),
    type: 'ai',
    content: actionMessages[action.action] || '작업을 실행하고 있습니다...',
    time: new Date().toLocaleTimeString('ko-KR', { hour: '2-digit', minute: '2-digit' })
  })
  
  nextTick(() => scrollToBottom())
}

const generateContextualResponse = (userMessage) => {
  const contextualResponses = {
    '회계 관리': [
      '재무 데이터를 분석한 결과를 정리해드리겠습니다.',
      '회계 업무에 관한 답변을 준비했습니다.',
      '현재 재무 상황을 바탕으로 분석해드리겠습니다.'
    ],
    '영업 관리': [
      '영업 데이터를 확인하고 분석결과를 제공해드리겠습니다.',
      '고객 관리 측면에서 도움을 드리겠습니다.',
      '매출 현황을 바탕으로 인사이트를 제공해드리겠습니다.'
    ],
    '제조 관리': [
      '생산 계획과 품질 데이터를 검토하고 있습니다.',
      '제조 프로세스 최적화 방안을 검토해드리겠습니다.',
      '생산 현황을 바탕으로 분석해드리겠습니다.'
    ]
  }
  
  const responses = contextualResponses[currentContext.value] || [
    '요청사항을 처리하고 있습니다.',
    '데이터를 분석하고 답변을 준비하고 있습니다.',
    '최적의 솔루션을 찾아드리겠습니다.'
  ]
  
  const randomResponse = responses[Math.floor(Math.random() * responses.length)]
  
  return `**${userMessage}**에 대해 ${randomResponse}\n\n현재 ${currentContext.value} 모듈의 데이터를 바탕으로 상세한 분석을 진행하겠습니다. 잠시만 기다려주세요...`
}

const formatMessage = (content) => {
  return content.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/\n/g, '<br>')
}

const addNewLine = () => {
  currentInput.value += '\n'
}

const scrollToBottom = () => {
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

// 페이지 변경 감지
watch(currentContext, () => {
  // 새 페이지로 이동했을 때 컨텍스트 메시지 추가
  if (messages.value.length > 0) {
    messages.value.push({
      id: Date.now(),
      type: 'system',
      content: `${currentContext.value} 페이지로 이동했습니다. 이 페이지에 대해 도움이 필요하시면 언제든 말씀해주세요.`,
      time: new Date().toLocaleTimeString('ko-KR', { hour: '2-digit', minute: '2-digit' })
    })
    nextTick(() => scrollToBottom())
  }
})

// 초기 환영 메시지
onMounted(() => {
  messages.value.push({
    id: 1,
    type: 'ai',
    content: `안녕하세요! ${currentContext.value}에서 도움이 필요하시면 언제든 말씀해주세요. 아래 추천 질문을 클릭하거나 직접 질문해주세요.`,
    time: new Date().toLocaleTimeString('ko-KR', { hour: '2-digit', minute: '2-digit' })
  })
})
</script>

<style scoped>
.ai-assistant-floating {
  position: fixed;
  bottom: 24px;
  left: 24px;
  width: 380px;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 16px;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
  z-index: 1000;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  overflow: hidden;
}

.ai-assistant-floating:not(.expanded) {
  height: 72px;
}

.ai-assistant-floating.expanded {
  height: 600px;
}

.ai-header {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 18px 20px;
  cursor: pointer;
  border-bottom: 1px solid #f1f5f9;
  transition: all 0.2s;
  position: relative;
}

.ai-header:hover {
  background-color: #f8fafc;
}

.ai-assistant-floating:not(.expanded) .ai-header {
  border-bottom: none;
}

.ai-avatar-small {
  width: 36px;
  height: 36px;
  background: linear-gradient(135deg, #3b82f6, #8b5cf6);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.ai-title-small {
  flex: 1;
  font-size: 16px;
  font-weight: 600;
  color: #1e293b;
}

.ai-toggle-icon {
  transition: transform 0.3s;
  color: #64748b;
}

.ai-toggle-icon.rotated {
  transform: rotate(180deg);
}

.ai-status {
  position: absolute;
  top: 16px;
  right: 16px;
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: #64748b;
}

.status-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  transition: all 0.2s;
}

.ai-status.online .status-dot {
  background-color: #10b981;
  box-shadow: 0 0 0 2px rgba(16, 185, 129, 0.2);
}

.ai-status.busy .status-dot {
  background-color: #f59e0b;
  animation: pulse 1.5s infinite;
}

.ai-status.offline .status-dot {
  background-color: #ef4444;
}

.ai-content {
  display: flex;
  flex-direction: column;
  height: calc(600px - 73px);
}

.ai-context-bar {
  padding: 12px 20px;
  background: linear-gradient(135deg, #f1f5f9, #e2e8f0);
  border-bottom: 1px solid #e2e8f0;
}

.context-info {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: #475569;
}

.ai-suggestions {
  padding: 16px 20px;
  border-bottom: 1px solid #f1f5f9;
}

.suggestions-header {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  font-weight: 500;
  color: #64748b;
  margin-bottom: 12px;
}

.suggestions-list {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.suggestion-item {
  padding: 8px 12px;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 13px;
  color: #475569;
  text-align: left;
  transition: all 0.2s;
  cursor: pointer;
}

.suggestion-item:hover {
  background: #f1f5f9;
  border-color: #cbd5e1;
  color: #334155;
}

.ai-chat-area {
  flex: 1;
  overflow: hidden;
}

.ai-messages {
  height: 100%;
  overflow-y: auto;
  padding: 16px 20px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.ai-message {
  max-width: 85%;
  word-wrap: break-word;
}

.ai-message.user {
  align-self: flex-end;
}

.ai-message.system {
  align-self: center;
  max-width: 100%;
}

.ai-message.user .message-content {
  background: #3b82f6;
  color: white;
  padding: 10px 14px;
  border-radius: 16px 16px 4px 16px;
  font-size: 14px;
  line-height: 1.5;
}

.ai-message.ai .message-content {
  background: #f8fafc;
  color: #334155;
  padding: 10px 14px;
  border-radius: 16px 16px 16px 4px;
  font-size: 14px;
  line-height: 1.5;
  border: 1px solid #e2e8f0;
}

.ai-message.system .message-content {
  background: #fef3c7;
  color: #92400e;
  padding: 8px 12px;
  border-radius: 12px;
  font-size: 13px;
  text-align: center;
  border: 1px solid #fde68a;
}

.message-time {
  font-size: 11px;
  color: #94a3b8;
  margin-top: 4px;
}

.ai-message.user .message-time {
  text-align: right;
}

.ai-message.ai .message-time {
  text-align: left;
}

.ai-message.system .message-time {
  text-align: center;
}

.typing-indicator .message-content {
  display: flex;
  align-items: center;
  padding: 12px 16px;
}

.typing-dots {
  display: flex;
  gap: 4px;
}

.typing-dots span {
  width: 6px;
  height: 6px;
  background-color: #94a3b8;
  border-radius: 50%;
  animation: typing 1.4s infinite ease-in-out;
}

.typing-dots span:nth-child(1) { animation-delay: -0.32s; }
.typing-dots span:nth-child(2) { animation-delay: -0.16s; }

.ai-input-area {
  border-top: 1px solid #e2e8f0;
  padding: 16px 20px;
  background: white;
}

.quick-actions {
  display: flex;
  gap: 8px;
  margin-bottom: 12px;
}

.quick-action-btn {
  padding: 6px;
  background: #f1f5f9;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  color: #64748b;
  transition: all 0.2s;
}

.quick-action-btn:hover {
  background: #e2e8f0;
  color: #475569;
}

.ai-input-container {
  display: flex;
  gap: 10px;
}

.ai-input {
  flex: 1;
  padding: 10px 14px;
  border: 1px solid #d1d5db;
  border-radius: 12px;
  font-size: 14px;
  resize: none;
  min-height: 40px;
  max-height: 100px;
  transition: all 0.2s;
}

.ai-input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.ai-send-btn {
  padding: 8px;
  background: #3b82f6;
  color: white;
  border-radius: 10px;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.ai-send-btn:hover:not(:disabled) {
  background: #2563eb;
  transform: translateY(-1px);
}

.ai-send-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

@keyframes pulse {
  0%, 100% { transform: scale(1); opacity: 1; }
  50% { transform: scale(1.1); opacity: 0.8; }
}

@keyframes typing {
  0%, 80%, 100% { transform: scale(0); }
  40% { transform: scale(1); }
}

/* 스크롤바 스타일링 */
.ai-messages::-webkit-scrollbar {
  width: 6px;
}

.ai-messages::-webkit-scrollbar-track {
  background: #f1f5f9;
  border-radius: 3px;
}

.ai-messages::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 3px;
}

.ai-messages::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}
</style>