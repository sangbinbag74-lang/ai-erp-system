<template>
  <div class="ai-copilot" :class="{ 'expanded': isExpanded, 'collapsed': !isExpanded }">
    <!-- 토글 버튼 -->
    <button 
      @click="toggleExpanded"
      class="toggle-btn"
      :title="isExpanded ? 'AI 어시스턴트 숨기기' : 'AI 어시스턴트 열기'"
    >
      <Icon :name="isExpanded ? 'heroicons:chevron-left' : 'heroicons:chat-bubble-left-ellipsis'" />
    </button>

    <!-- AI 어시스턴트 패널 -->
    <div class="copilot-panel" v-show="isExpanded">
      <!-- 헤더 -->
      <div class="panel-header">
        <div class="header-info">
          <div class="avatar">
            <Icon name="heroicons:cpu-chip" class="w-6 h-6 text-primary-600" />
          </div>
          <div>
            <h3 class="title">AI 어시스턴트</h3>
            <p class="subtitle">ERP 업무를 도와드립니다</p>
          </div>
        </div>
        <div class="header-actions">
          <button @click="clearChat" class="action-btn" title="대화 내용 지우기">
            <Icon name="heroicons:trash" class="w-4 h-4" />
          </button>
        </div>
      </div>

      <!-- 상태 표시 -->
      <div class="status-bar">
        <div class="status-item" :class="connectionStatus">
          <div class="status-dot"></div>
          <span class="status-text">{{ statusText }}</span>
        </div>
        <div class="ai-capabilities">
          <span class="capability-badge">파일 관리</span>
          <span class="capability-badge">자동화</span>
          <span class="capability-badge">분석</span>
        </div>
      </div>

      <!-- 채팅 메시지 -->
      <div class="chat-messages" ref="messagesContainer">
        <div v-if="messages.length === 0" class="empty-state">
          <Icon name="heroicons:lightbulb" class="w-12 h-12 text-gray-400 mx-auto mb-4" />
          <h4 class="text-gray-600 font-medium mb-2">안녕하세요! 👋</h4>
          <p class="text-gray-500 text-sm mb-4">ERP 업무를 도와드릴 AI 어시스턴트입니다.</p>
          <div class="quick-actions">
            <button 
              v-for="suggestion in quickSuggestions" 
              :key="suggestion.id"
              @click="sendMessage(suggestion.message)"
              class="suggestion-btn"
            >
              {{ suggestion.label }}
            </button>
          </div>
        </div>

        <div 
          v-for="message in messages" 
          :key="message.id"
          class="message"
          :class="message.type"
        >
          <div class="message-avatar">
            <Icon 
              :name="message.type === 'user' ? 'heroicons:user' : 'heroicons:cpu-chip'"
              class="w-5 h-5"
            />
          </div>
          <div class="message-content">
            <div class="message-text" v-html="formatMessage(message.content)"></div>
            <div class="message-time">{{ formatTime(message.timestamp) }}</div>
            
            <!-- AI 작업 결과 -->
            <div v-if="message.result && message.type === 'ai'" class="ai-result">
              <div class="result-header">
                <Icon name="heroicons:cog" class="w-4 h-4" />
                <span>작업 결과</span>
              </div>
              <div class="result-content">
                <pre>{{ JSON.stringify(message.result, null, 2) }}</pre>
              </div>
            </div>
          </div>
        </div>

        <!-- 로딩 표시 -->
        <div v-if="isProcessing" class="message ai loading">
          <div class="message-avatar">
            <div class="spinner w-5 h-5"></div>
          </div>
          <div class="message-content">
            <div class="typing-indicator">
              <span></span>
              <span></span>
              <span></span>
            </div>
            <div class="message-time">처리 중...</div>
          </div>
        </div>
      </div>

      <!-- 입력 영역 -->
      <div class="chat-input">
        <div class="input-container">
          <textarea
            v-model="currentMessage"
            @keydown="handleKeydown"
            placeholder="ERP 업무에 대해 무엇이든 물어보세요... (Shift+Enter로 전송)"
            class="message-textarea"
            rows="1"
            :disabled="isProcessing"
            ref="messageInput"
          ></textarea>
          <button 
            @click="sendCurrentMessage"
            :disabled="!currentMessage.trim() || isProcessing"
            class="send-btn"
          >
            <Icon name="heroicons:paper-airplane" class="w-5 h-5" />
          </button>
        </div>
        <div class="input-footer">
          <div class="file-actions">
            <input 
              type="file" 
              ref="fileInput" 
              @change="handleFileUpload" 
              multiple
              style="display: none"
            >
            <button @click="$refs.fileInput.click()" class="file-btn">
              <Icon name="heroicons:paper-clip" class="w-4 h-4" />
              파일 첨부
            </button>
          </div>
          <div class="ai-mode">
            <select v-model="aiMode" class="mode-select">
              <option value="assistant">어시스턴트</option>
              <option value="analyst">분석가</option>
              <option value="automation">자동화</option>
            </select>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, onMounted, nextTick, watch } from 'vue'
import { Icon } from '@iconify/vue'
import { useAI } from '@/composables/useAI'
import { useNotification } from '@/composables/useNotification'

export default {
  name: 'AICopilot',
  components: {
    Icon
  },
  setup() {
    const isExpanded = ref(false)
    const isProcessing = ref(false)
    const currentMessage = ref('')
    const aiMode = ref('assistant')
    const messages = ref([])
    const messagesContainer = ref(null)
    const messageInput = ref(null)
    const fileInput = ref(null)

    const { processAIRequest } = useAI()
    const { showNotification } = useNotification()

    // 연결 상태
    const connectionStatus = ref('connected')
    const statusText = ref('연결됨')

    // 빠른 제안사항
    const quickSuggestions = ref([
      { id: 1, label: '💰 매출 현황 분석해줘', message: '이번 달 매출 현황을 분석해서 보고서를 만들어줘' },
      { id: 2, label: '📦 재고 부족 상품 확인', message: '재고가 부족한 상품들을 찾아서 주문 제안해줘' },
      { id: 3, label: '👥 신규 고객 등록 도움', message: '신규 고객을 등록하는 방법을 알려줘' },
      { id: 4, label: '📊 대시보드 데이터 설명', message: '현재 대시보드에 표시된 데이터를 설명해줘' }
    ])

    // 메시지 전송
    const sendMessage = async (message) => {
      if (!message.trim()) return

      const userMessage = {
        id: Date.now(),
        type: 'user',
        content: message,
        timestamp: new Date()
      }

      messages.value.push(userMessage)
      currentMessage.value = ''
      isProcessing.value = true

      // 스크롤 하단으로
      await nextTick()
      scrollToBottom()

      try {
        const response = await processAIRequest(message, {
          mode: aiMode.value,
          context: getCurrentContext()
        })

        const aiMessage = {
          id: Date.now() + 1,
          type: 'ai',
          content: response.response,
          result: response.result,
          timestamp: new Date()
        }

        messages.value.push(aiMessage)

      } catch (error) {
        console.error('AI 처리 오류:', error)
        
        const errorMessage = {
          id: Date.now() + 1,
          type: 'ai',
          content: '죄송합니다. 요청을 처리하는 중에 오류가 발생했습니다. 다시 시도해 주세요.',
          timestamp: new Date()
        }

        messages.value.push(errorMessage)
        showNotification('AI 처리 중 오류가 발생했습니다.', 'error')
      } finally {
        isProcessing.value = false
        await nextTick()
        scrollToBottom()
      }
    }

    const sendCurrentMessage = () => {
      sendMessage(currentMessage.value)
    }

    // 키보드 이벤트 처리
    const handleKeydown = (e) => {
      if (e.key === 'Enter' && e.shiftKey) {
        e.preventDefault()
        sendCurrentMessage()
      }
    }

    // 파일 업로드
    const handleFileUpload = (e) => {
      const files = Array.from(e.target.files)
      if (files.length > 0) {
        const fileMessage = `다음 파일들을 분석해줘: ${files.map(f => f.name).join(', ')}`
        sendMessage(fileMessage)
      }
    }

    // 패널 토글
    const toggleExpanded = () => {
      isExpanded.value = !isExpanded.value
      if (isExpanded.value) {
        nextTick(() => {
          messageInput.value?.focus()
        })
      }
    }

    // 채팅 내용 지우기
    const clearChat = () => {
      if (confirm('대화 내용을 모두 지우시겠습니까?')) {
        messages.value = []
      }
    }

    // 메시지 포맷팅
    const formatMessage = (content) => {
      return content
        .replace(/\n/g, '<br>')
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.*?)\*/g, '<em>$1</em>')
        .replace(/`(.*?)`/g, '<code>$1</code>')
    }

    // 시간 포맷팅
    const formatTime = (timestamp) => {
      return new Date(timestamp).toLocaleTimeString('ko-KR', {
        hour: '2-digit',
        minute: '2-digit'
      })
    }

    // 스크롤 하단으로
    const scrollToBottom = () => {
      if (messagesContainer.value) {
        messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
      }
    }

    // 현재 컨텍스트 가져오기
    const getCurrentContext = () => {
      return {
        currentPath: window.location.pathname,
        userAgent: navigator.userAgent,
        timestamp: new Date().toISOString()
      }
    }

    // 컴포넌트 마운트 시
    onMounted(() => {
      // 초기 상태 설정
      connectionStatus.value = 'connected'
      statusText.value = '연결됨'
    })

    return {
      // 상태
      isExpanded,
      isProcessing,
      currentMessage,
      aiMode,
      messages,
      connectionStatus,
      statusText,
      quickSuggestions,

      // 참조
      messagesContainer,
      messageInput,
      fileInput,

      // 메서드
      toggleExpanded,
      sendMessage,
      sendCurrentMessage,
      handleKeydown,
      handleFileUpload,
      clearChat,
      formatMessage,
      formatTime
    }
  }
}
</script>

<style scoped>
.ai-copilot {
  position: fixed;
  left: 0;
  top: 64px; /* 헤더 높이만큼 */
  bottom: 0;
  z-index: 50;
  transition: all 0.3s ease-in-out;
}

.ai-copilot.expanded {
  width: 380px;
}

.ai-copilot.collapsed {
  width: 60px;
}

.toggle-btn {
  position: absolute;
  right: -12px;
  top: 50%;
  transform: translateY(-50%);
  width: 24px;
  height: 48px;
  background: white;
  border: 1px solid #e2e8f0;
  border-left: none;
  border-radius: 0 12px 12px 0;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #64748b;
  cursor: pointer;
  transition: all 0.2s ease;
  z-index: 51;
}

.toggle-btn:hover {
  background: #f8fafc;
  color: #3b82f6;
}

.copilot-panel {
  width: 100%;
  height: 100%;
  background: white;
  border-right: 1px solid #e2e8f0;
  box-shadow: 2px 0 8px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
}

.panel-header {
  padding: 1rem;
  border-bottom: 1px solid #e2e8f0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: linear-gradient(135deg, #3b82f6 0%, #6366f1 100%);
  color: white;
}

.header-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
}

.title {
  font-size: 0.9rem;
  font-weight: 600;
  margin: 0;
}

.subtitle {
  font-size: 0.75rem;
  opacity: 0.9;
  margin: 0;
}

.action-btn {
  padding: 0.5rem;
  background: rgba(255, 255, 255, 0.1);
  border: none;
  border-radius: 6px;
  color: white;
  cursor: pointer;
  transition: background 0.2s ease;
}

.action-btn:hover {
  background: rgba(255, 255, 255, 0.2);
}

.status-bar {
  padding: 0.75rem 1rem;
  background: #f8fafc;
  border-bottom: 1px solid #e2e8f0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.status-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.75rem;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #10b981;
}

.status-item.disconnected .status-dot {
  background: #ef4444;
}

.status-item.connecting .status-dot {
  background: #f59e0b;
  animation: pulse 2s infinite;
}

.ai-capabilities {
  display: flex;
  gap: 0.25rem;
  flex-wrap: wrap;
}

.capability-badge {
  padding: 0.125rem 0.5rem;
  background: #dbeafe;
  color: #1d4ed8;
  font-size: 0.625rem;
  border-radius: 12px;
  font-weight: 500;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 1rem;
  scroll-behavior: smooth;
}

.empty-state {
  text-align: center;
  padding: 2rem 1rem;
}

.quick-actions {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-top: 1rem;
}

.suggestion-btn {
  padding: 0.75rem;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  text-align: left;
  cursor: pointer;
  font-size: 0.8rem;
  transition: all 0.2s ease;
}

.suggestion-btn:hover {
  background: #f1f5f9;
  border-color: #cbd5e1;
  transform: translateY(-1px);
}

.message {
  display: flex;
  gap: 0.75rem;
  margin-bottom: 1rem;
}

.message.user {
  flex-direction: row-reverse;
}

.message-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.message.user .message-avatar {
  background: #3b82f6;
  color: white;
}

.message.ai .message-avatar {
  background: #f1f5f9;
  color: #64748b;
}

.message-content {
  flex: 1;
  min-width: 0;
}

.message.user .message-content {
  text-align: right;
}

.message-text {
  background: #f8fafc;
  padding: 0.75rem 1rem;
  border-radius: 12px;
  font-size: 0.85rem;
  line-height: 1.5;
  word-wrap: break-word;
}

.message.user .message-text {
  background: #3b82f6;
  color: white;
  border-bottom-right-radius: 4px;
}

.message.ai .message-text {
  border-bottom-left-radius: 4px;
}

.message-time {
  font-size: 0.7rem;
  color: #64748b;
  margin-top: 0.25rem;
}

.ai-result {
  margin-top: 0.5rem;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  overflow: hidden;
}

.result-header {
  padding: 0.5rem 0.75rem;
  background: #f8fafc;
  border-bottom: 1px solid #e2e8f0;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.75rem;
  font-weight: 500;
}

.result-content {
  padding: 0.75rem;
  background: #1e293b;
  color: #e2e8f0;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.7rem;
  overflow-x: auto;
}

.typing-indicator {
  display: flex;
  gap: 0.25rem;
  padding: 0.75rem 1rem;
}

.typing-indicator span {
  width: 6px;
  height: 6px;
  background: #94a3b8;
  border-radius: 50%;
  animation: typing 1.4s infinite ease-in-out;
}

.typing-indicator span:nth-child(2) {
  animation-delay: 0.2s;
}

.typing-indicator span:nth-child(3) {
  animation-delay: 0.4s;
}

.chat-input {
  border-top: 1px solid #e2e8f0;
  background: white;
}

.input-container {
  padding: 1rem;
  display: flex;
  gap: 0.75rem;
  align-items: end;
}

.message-textarea {
  flex: 1;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 0.75rem;
  font-size: 0.85rem;
  resize: none;
  outline: none;
  transition: border-color 0.2s ease;
  max-height: 120px;
  min-height: 40px;
}

.message-textarea:focus {
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.message-textarea:disabled {
  background: #f8fafc;
  opacity: 0.6;
}

.send-btn {
  padding: 0.75rem;
  background: #3b82f6;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.send-btn:enabled:hover {
  background: #2563eb;
  transform: translateY(-1px);
}

.send-btn:disabled {
  background: #94a3b8;
  cursor: not-allowed;
  transform: none;
}

.input-footer {
  padding: 0 1rem 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.file-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 0.75rem;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  font-size: 0.75rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.file-btn:hover {
  background: #f1f5f9;
}

.mode-select {
  padding: 0.375rem 0.5rem;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  font-size: 0.75rem;
  background: white;
  cursor: pointer;
}

@keyframes typing {
  0%, 60%, 100% {
    transform: translateY(0);
  }
  30% {
    transform: translateY(-10px);
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

.spinner {
  border: 2px solid #f3f4f6;
  border-top: 2px solid #3b82f6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* 스크롤바 스타일링 */
.chat-messages::-webkit-scrollbar {
  width: 4px;
}

.chat-messages::-webkit-scrollbar-track {
  background: #f1f5f9;
}

.chat-messages::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 2px;
}

.chat-messages::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}
</style>