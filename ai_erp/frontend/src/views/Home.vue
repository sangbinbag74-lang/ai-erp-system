<template>
  <div class="home">
    <div class="welcome-card">
      <h2>🎉 AI ERP 시스템에 오신 것을 환영합니다!</h2>
      <p>Vercel 배포가 성공적으로 완료되었습니다.</p>
      
      <div class="features">
        <h3>주요 기능</h3>
        <ul>
          <li>🤖 AI 기반 업무 자동화</li>
          <li>📊 실시간 데이터 분석</li>
          <li>🌍 한국어 완벽 지원</li>
          <li>☁️ 클라우드 스토리지 연동</li>
          <li>📱 반응형 웹 디자인</li>
        </ul>
      </div>
      
      <div class="status">
        <h3>시스템 상태</h3>
        <div class="status-item">
          <span class="status-label">Frontend:</span>
          <span class="status-value success">✅ 배포 완료 (Vercel)</span>
        </div>
        <div class="status-item">
          <span class="status-label">Backend:</span>
          <span class="status-value pending">⏳ 설정 필요 (Railway)</span>
        </div>
        <div class="status-item">
          <span class="status-label">API 연결:</span>
          <span class="status-value" :class="apiStatus">{{ apiMessage }}</span>
        </div>
      </div>
      
      <div class="actions">
        <button @click="testApi" class="btn-primary">API 테스트</button>
        <router-link to="/about" class="btn-secondary">시스템 정보</router-link>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'

export default {
  name: 'Home',
  setup() {
    const apiStatus = ref('pending')
    const apiMessage = ref('⏳ 연결 대기중...')
    
    const testApi = async () => {
      try {
        apiStatus.value = 'pending'
        
        // API URL from environment variable
        const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
        apiMessage.value = `⏳ API 연결 테스트 중... (${apiUrl})`
        
        const response = await fetch(`${apiUrl}/api/health`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
          },
        })
        
        if (response.ok) {
          const data = await response.json()
          apiStatus.value = 'success'
          apiMessage.value = '✅ API 연결 성공!'
          console.log('API Response:', data)
        } else {
          throw new Error(`HTTP ${response.status}: ${response.statusText}`)
        }
      } catch (error) {
        apiStatus.value = 'error'
        apiMessage.value = `❌ API 연결 실패: ${error.message}`
        console.error('API Error:', error)
      }
    }
    
    onMounted(() => {
      // 페이지 로드 시 자동으로 API 테스트
      setTimeout(testApi, 1000)
    })
    
    return {
      apiStatus,
      apiMessage,
      testApi
    }
  }
}
</script>

<style scoped>
.home {
  max-width: 800px;
  margin: 0 auto;
}

.welcome-card {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  border: 1px solid #e1e5e9;
}

.welcome-card h2 {
  color: #2c3e50;
  margin-bottom: 1rem;
}

.features {
  margin: 2rem 0;
  padding: 1.5rem;
  background: #f8f9fa;
  border-radius: 8px;
}

.features ul {
  list-style: none;
  padding: 0;
}

.features li {
  padding: 0.5rem 0;
  font-size: 1.1rem;
}

.status {
  margin: 2rem 0;
}

.status-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 0;
  border-bottom: 1px solid #eee;
}

.status-label {
  font-weight: bold;
  color: #495057;
}

.status-value {
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.9rem;
}

.status-value.success {
  background: #d4edda;
  color: #155724;
}

.status-value.pending {
  background: #fff3cd;
  color: #856404;
}

.status-value.error {
  background: #f8d7da;
  color: #721c24;
}

.actions {
  display: flex;
  gap: 1rem;
  margin-top: 2rem;
}

.btn-primary {
  background: #007bff;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 6px;
  cursor: pointer;
  text-decoration: none;
  font-size: 1rem;
  transition: background-color 0.2s;
}

.btn-primary:hover {
  background: #0056b3;
}

.btn-secondary {
  background: #6c757d;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 6px;
  cursor: pointer;
  text-decoration: none;
  font-size: 1rem;
  transition: background-color 0.2s;
}

.btn-secondary:hover {
  background: #545b62;
}
</style>