<template>
  <div class="analytics">
    <div class="page-header">
      <h1>🤖 AI 분석</h1>
      <button @click="generateAnalysis" class="btn-primary">🔄 새 분석 생성</button>
    </div>

    <div class="analysis-grid">
      <div class="analysis-card">
        <h3>📈 매출 트렌드 분석</h3>
        <div class="chart-placeholder">
          <div class="fake-chart">
            <div class="bar" style="height: 60%"></div>
            <div class="bar" style="height: 80%"></div>
            <div class="bar" style="height: 45%"></div>
            <div class="bar" style="height: 90%"></div>
            <div class="bar" style="height: 70%"></div>
          </div>
        </div>
        <p><strong>AI 분석:</strong> 지난 3개월간 매출이 15% 증가했습니다. 전자제품 카테고리가 주요 성장 동력입니다.</p>
      </div>

      <div class="analysis-card">
        <h3>🎯 고객 세그먼트 분석</h3>
        <div class="pie-chart">
          <div class="segment segment1" data-label="기업 고객 (60%)"></div>
          <div class="segment segment2" data-label="개인 고객 (25%)"></div>
          <div class="segment segment3" data-label="정부 기관 (15%)"></div>
        </div>
        <p><strong>AI 추천:</strong> 기업 고객 비중이 높습니다. B2B 마케팅에 더 집중하세요.</p>
      </div>

      <div class="analysis-card">
        <h3>🔮 미래 예측</h3>
        <div class="prediction-box">
          <div class="prediction-item">
            <span class="metric">다음 달 예상 매출</span>
            <span class="value">₩{{ formatNumber(predictedSales) }}</span>
          </div>
          <div class="prediction-item">
            <span class="metric">고객 증가율</span>
            <span class="value">+{{ customerGrowth }}%</span>
          </div>
          <div class="prediction-item">
            <span class="metric">재고 회전율</span>
            <span class="value">{{ inventoryTurnover }}회</span>
          </div>
        </div>
        <p><strong>AI 인사이트:</strong> 현재 추세가 계속되면 분기 목표를 달성할 확률이 88%입니다.</p>
      </div>

      <div class="analysis-card">
        <h3>🚨 위험 요소 분석</h3>
        <div class="risk-list">
          <div class="risk-item low">
            <span class="risk-icon">🟢</span>
            <span>현금 흐름: 안정적</span>
          </div>
          <div class="risk-item medium">
            <span class="risk-icon">🟡</span>
            <span>재고 부족: 3개 상품 주의</span>
          </div>
          <div class="risk-item high">
            <span class="risk-icon">🔴</span>
            <span>고객 이탈률: 증가 추세</span>
          </div>
        </div>
        <p><strong>AI 추천:</strong> 고객 만족도 조사를 통해 이탈 원인을 파악하세요.</p>
      </div>
    </div>

    <div class="ai-chat">
      <h2>💬 AI 어시스턴트와 대화</h2>
      <div class="chat-container">
        <div class="chat-messages">
          <div v-for="message in chatMessages" :key="message.id" :class="['message', message.type]">
            <div class="message-content">{{ message.content }}</div>
            <div class="message-time">{{ message.time }}</div>
          </div>
        </div>
        <div class="chat-input">
          <input 
            v-model="newMessage" 
            @keyup.enter="sendMessage"
            placeholder="AI에게 질문하세요... (예: 이번 달 매출 분석해줘)"
            class="message-input"
          >
          <button @click="sendMessage" class="send-btn">전송</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'

export default {
  name: 'Analytics',
  setup() {
    const predictedSales = ref(143750000)
    const customerGrowth = ref(8.5)
    const inventoryTurnover = ref(4.2)
    const newMessage = ref('')
    
    const chatMessages = ref([
      {
        id: 1,
        type: 'ai',
        content: '안녕하세요! AI 분석 어시스턴트입니다. 비즈니스 데이터에 대해 궁금한 점이 있으시면 언제든 물어보세요.',
        time: '14:30'
      }
    ])
    
    const formatNumber = (num) => num.toLocaleString('ko-KR')
    
    const generateAnalysis = () => {
      // 새로운 분석 생성 시뮬레이션
      predictedSales.value = Math.floor(Math.random() * 50000000) + 120000000
      customerGrowth.value = (Math.random() * 10 + 5).toFixed(1)
      inventoryTurnover.value = (Math.random() * 2 + 3).toFixed(1)
    }
    
    const sendMessage = () => {
      if (!newMessage.value.trim()) return
      
      // 사용자 메시지 추가
      chatMessages.value.push({
        id: chatMessages.value.length + 1,
        type: 'user',
        content: newMessage.value,
        time: new Date().toLocaleTimeString('ko-KR', { hour: '2-digit', minute: '2-digit' })
      })
      
      // AI 응답 시뮬레이션 (2초 후)
      setTimeout(() => {
        const aiResponses = [
          '분석 결과를 확인하겠습니다. 현재 매출 추세는 양호하며, 전월 대비 12% 증가했습니다.',
          '고객 데이터를 분석한 결과, VIP 고객층의 구매 패턴이 변화하고 있습니다.',
          '재고 최적화를 위한 추천사항을 드리겠습니다. 전자제품 카테고리의 재주문이 필요합니다.',
          '예측 모델에 따르면, 다음 분기 성장률은 15-20% 범위로 예상됩니다.',
          '리스크 분석 결과, 현재 가장 주의해야 할 부분은 고객 이탈률 증가입니다.'
        ]
        
        chatMessages.value.push({
          id: chatMessages.value.length + 1,
          type: 'ai',
          content: aiResponses[Math.floor(Math.random() * aiResponses.length)],
          time: new Date().toLocaleTimeString('ko-KR', { hour: '2-digit', minute: '2-digit' })
        })
      }, 2000)
      
      newMessage.value = ''
    }
    
    return {
      predictedSales,
      customerGrowth,
      inventoryTurnover,
      newMessage,
      chatMessages,
      formatNumber,
      generateAnalysis,
      sendMessage
    }
  }
}
</script>

<style scoped>
.analytics {
  max-width: 1400px;
  margin: 0 auto;
  padding: 2rem;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.btn-primary {
  background: #3498db;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 6px;
  cursor: pointer;
}

.analysis-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 2rem;
  margin-bottom: 3rem;
}

.analysis-card {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}

.analysis-card h3 {
  margin: 0 0 1rem 0;
  color: #2c3e50;
}

.chart-placeholder {
  height: 200px;
  background: #f8f9fa;
  border-radius: 8px;
  margin: 1rem 0;
  display: flex;
  align-items: end;
  justify-content: center;
}

.fake-chart {
  display: flex;
  align-items: end;
  gap: 1rem;
  height: 80%;
  width: 80%;
}

.bar {
  background: linear-gradient(to top, #3498db, #2980b9);
  flex: 1;
  border-radius: 4px 4px 0 0;
  min-height: 20px;
}

.pie-chart {
  width: 200px;
  height: 200px;
  border-radius: 50%;
  background: conic-gradient(#3498db 0deg 216deg, #e74c3c 216deg 306deg, #f39c12 306deg 360deg);
  margin: 1rem auto;
}

.prediction-box {
  background: #f8f9fa;
  padding: 1rem;
  border-radius: 8px;
  margin: 1rem 0;
}

.prediction-item {
  display: flex;
  justify-content: space-between;
  padding: 0.5rem 0;
  border-bottom: 1px solid #eee;
}

.prediction-item:last-child {
  border-bottom: none;
}

.metric {
  color: #7f8c8d;
}

.value {
  font-weight: bold;
  color: #2c3e50;
}

.risk-list {
  margin: 1rem 0;
}

.risk-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem;
  margin: 0.5rem 0;
  border-radius: 6px;
}

.risk-item.low {
  background: #d5f4e6;
}

.risk-item.medium {
  background: #fff3cd;
}

.risk-item.high {
  background: #f8d7da;
}

.ai-chat {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
  overflow: hidden;
}

.ai-chat h2 {
  padding: 1.5rem;
  margin: 0;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.chat-container {
  height: 400px;
  display: flex;
  flex-direction: column;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 1rem;
}

.message {
  margin: 1rem 0;
  max-width: 70%;
}

.message.user {
  margin-left: auto;
}

.message.ai {
  margin-right: auto;
}

.message-content {
  padding: 0.75rem 1rem;
  border-radius: 18px;
  word-wrap: break-word;
}

.message.user .message-content {
  background: #3498db;
  color: white;
}

.message.ai .message-content {
  background: #f1f3f4;
  color: #2c3e50;
}

.message-time {
  font-size: 0.7rem;
  color: #7f8c8d;
  margin-top: 0.25rem;
  text-align: right;
}

.message.ai .message-time {
  text-align: left;
}

.chat-input {
  display: flex;
  padding: 1rem;
  border-top: 1px solid #eee;
}

.message-input {
  flex: 1;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 20px;
  outline: none;
}

.send-btn {
  background: #3498db;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 20px;
  margin-left: 0.5rem;
  cursor: pointer;
}
</style>