<template>
  <div class="about">
    <div class="info-card">
      <h2>🔧 시스템 정보</h2>
      
      <div class="tech-stack">
        <h3>기술 스택</h3>
        <div class="stack-grid">
          <div class="stack-item">
            <h4>Frontend</h4>
            <ul>
              <li>Vue.js 3.3.8</li>
              <li>Vite 4.5.0</li>
              <li>Vue Router</li>
              <li>Pinia (상태관리)</li>
            </ul>
          </div>
          <div class="stack-item">
            <h4>Backend</h4>
            <ul>
              <li>ERPNext 15.0.0</li>
              <li>Frappe Framework</li>
              <li>FastAPI</li>
              <li>Python 3.9+</li>
            </ul>
          </div>
          <div class="stack-item">
            <h4>AI & ML</h4>
            <ul>
              <li>OpenAI GPT</li>
              <li>Anthropic Claude</li>
              <li>LangChain</li>
              <li>scikit-learn</li>
            </ul>
          </div>
          <div class="stack-item">
            <h4>배포 & 인프라</h4>
            <ul>
              <li>Vercel (Frontend)</li>
              <li>Railway (Backend)</li>
              <li>PostgreSQL</li>
              <li>Redis</li>
            </ul>
          </div>
        </div>
      </div>
      
      <div class="deployment-info">
        <h3>배포 정보</h3>
        <div class="info-grid">
          <div class="info-item">
            <span class="label">환경:</span>
            <span class="value">{{ environment }}</span>
          </div>
          <div class="info-item">
            <span class="label">빌드 시간:</span>
            <span class="value">{{ buildTime }}</span>
          </div>
          <div class="info-item">
            <span class="label">버전:</span>
            <span class="value">v1.0.0</span>
          </div>
          <div class="info-item">
            <span class="label">API URL:</span>
            <span class="value">{{ apiUrl }}</span>
          </div>
        </div>
      </div>
      
      <div class="next-steps">
        <h3>다음 단계</h3>
        <ol>
          <li>Railway에서 Backend 배포</li>
          <li>환경변수 설정 (API 키 등)</li>
          <li>데이터베이스 연결 설정</li>
          <li>도메인 연결 (선택사항)</li>
          <li>SSL 인증서 설정</li>
        </ol>
      </div>
      
      <router-link to="/" class="btn-back">🏠 홈으로 돌아가기</router-link>
    </div>
  </div>
</template>

<script>
import { computed } from 'vue'

export default {
  name: 'About',
  setup() {
    const environment = computed(() => {
      return import.meta.env.VITE_APP_ENV || 'development'
    })
    
    const buildTime = computed(() => {
      return new Date().toLocaleString('ko-KR')
    })
    
    const apiUrl = computed(() => {
      return import.meta.env.VITE_API_URL || 'http://localhost:8000'
    })
    
    return {
      environment,
      buildTime,
      apiUrl
    }
  }
}
</script>

<style scoped>
.about {
  max-width: 900px;
  margin: 0 auto;
}

.info-card {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  border: 1px solid #e1e5e9;
}

.tech-stack {
  margin: 2rem 0;
}

.stack-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-top: 1rem;
}

.stack-item {
  background: #f8f9fa;
  padding: 1.5rem;
  border-radius: 8px;
  border: 1px solid #dee2e6;
}

.stack-item h4 {
  color: #495057;
  margin-bottom: 1rem;
  font-size: 1.1rem;
}

.stack-item ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.stack-item li {
  padding: 0.25rem 0;
  color: #6c757d;
}

.deployment-info {
  margin: 2rem 0;
  padding: 1.5rem;
  background: #e3f2fd;
  border-radius: 8px;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-top: 1rem;
}

.info-item {
  display: flex;
  justify-content: space-between;
  padding: 0.5rem 0;
}

.label {
  font-weight: bold;
  color: #1976d2;
}

.value {
  color: #424242;
  font-family: 'Courier New', monospace;
}

.next-steps {
  margin: 2rem 0;
  padding: 1.5rem;
  background: #fff3e0;
  border-radius: 8px;
  border-left: 4px solid #ff9800;
}

.next-steps ol {
  margin: 1rem 0 0 0;
  padding-left: 1.5rem;
}

.next-steps li {
  padding: 0.5rem 0;
  color: #e65100;
}

.btn-back {
  display: inline-block;
  background: #28a745;
  color: white;
  padding: 0.75rem 1.5rem;
  border-radius: 6px;
  text-decoration: none;
  font-size: 1rem;
  transition: background-color 0.2s;
  margin-top: 1rem;
}

.btn-back:hover {
  background: #1e7e34;
}
</style>