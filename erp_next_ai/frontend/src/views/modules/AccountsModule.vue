<template>
  <div class="accounts-module">
    <!-- 모듈 헤더 -->
    <div class="module-header">
      <div class="header-content">
        <div class="module-title">
          <Icon name="heroicons:calculator" class="w-8 h-8 text-ai-primary" />
          <div>
            <h1>회계 관리</h1>
            <p>AI 기반 자동 회계 처리 및 재무 분석</p>
          </div>
        </div>
        <div class="header-actions">
          <button @click="openAIAssistant" class="ai-assist-btn">
            <Icon name="heroicons:sparkles" class="w-5 h-5" />
            AI 회계 어시스턴트
          </button>
          <button @click="generateReport" class="generate-btn">
            <Icon name="heroicons:document-chart-bar" class="w-5 h-5" />
            보고서 생성
          </button>
        </div>
      </div>
      
      <!-- AI 실시간 인사이트 바 -->
      <div class="ai-insights-bar">
        <div class="insight-item" v-for="insight in realtimeInsights" :key="insight.id">
          <Icon :name="insight.icon" class="w-5 h-5" :class="insight.color" />
          <span>{{ insight.text }}</span>
          <button @click="exploreInsight(insight)" class="explore-btn">
            <Icon name="heroicons:arrow-top-right-on-square" class="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>

    <!-- AI 자연어 명령 영역 -->
    <div class="ai-command-section">
      <div class="command-container">
        <Icon name="heroicons:cpu-chip" class="w-6 h-6 text-ai-primary" />
        <textarea
          v-model="aiCommand"
          @keydown.enter.ctrl="executeAccountsAI"
          placeholder="회계 관련 자연어 명령... 예: '이번 달 손익계산서를 생성하고 주요 변동사항을 분석해줘'"
          class="ai-command-input"
          rows="2"
        ></textarea>
        <button 
          @click="executeAccountsAI"
          :disabled="!aiCommand.trim() || processing"
          class="ai-execute-btn"
        >
          <Icon v-if="processing" name="heroicons:arrow-path" class="w-5 h-5 animate-spin" />
          <Icon v-else name="heroicons:play" class="w-5 h-5" />
        </button>
      </div>
    </div>

    <!-- 대시보드 카드들 -->
    <div class="dashboard-cards">
      <!-- 재무 현황 카드 -->
      <div class="card financial-overview">
        <div class="card-header">
          <h3>재무 현황</h3>
          <div class="card-actions">
            <button @click="refreshFinancials" class="refresh-btn">
              <Icon name="heroicons:arrow-path" class="w-4 h-4" />
            </button>
            <button @click="analyzeFinancials" class="analyze-btn">
              <Icon name="heroicons:sparkles" class="w-4 h-4" />
              AI 분석
            </button>
          </div>
        </div>
        
        <div class="financial-metrics">
          <div class="metric">
            <div class="metric-label">총 자산</div>
            <div class="metric-value">{{ formatCurrency(financialData.totalAssets) }}</div>
            <div class="metric-change" :class="financialData.assetChange >= 0 ? 'positive' : 'negative'">
              <Icon :name="financialData.assetChange >= 0 ? 'heroicons:arrow-trending-up' : 'heroicons:arrow-trending-down'" class="w-4 h-4" />
              {{ Math.abs(financialData.assetChange) }}%
            </div>
          </div>
          
          <div class="metric">
            <div class="metric-label">총 부채</div>
            <div class="metric-value">{{ formatCurrency(financialData.totalLiabilities) }}</div>
            <div class="metric-change" :class="financialData.liabilityChange <= 0 ? 'positive' : 'negative'">
              <Icon :name="financialData.liabilityChange <= 0 ? 'heroicons:arrow-trending-down' : 'heroicons:arrow-trending-up'" class="w-4 h-4" />
              {{ Math.abs(financialData.liabilityChange) }}%
            </div>
          </div>
          
          <div class="metric">
            <div class="metric-label">자본</div>
            <div class="metric-value">{{ formatCurrency(financialData.equity) }}</div>
            <div class="metric-change" :class="financialData.equityChange >= 0 ? 'positive' : 'negative'">
              <Icon :name="financialData.equityChange >= 0 ? 'heroicons:arrow-trending-up' : 'heroicons:arrow-trending-down'" class="w-4 h-4" />
              {{ Math.abs(financialData.equityChange) }}%
            </div>
          </div>
          
          <div class="metric">
            <div class="metric-label">순이익</div>
            <div class="metric-value">{{ formatCurrency(financialData.netIncome) }}</div>
            <div class="metric-change" :class="financialData.incomeChange >= 0 ? 'positive' : 'negative'">
              <Icon :name="financialData.incomeChange >= 0 ? 'heroicons:arrow-trending-up' : 'heroicons:arrow-trending-down'" class="w-4 h-4" />
              {{ Math.abs(financialData.incomeChange) }}%
            </div>
          </div>
        </div>
        
        <div class="ai-financial-insights">
          <h4>AI 재무 분석</h4>
          <div class="insights-list">
            <div v-for="insight in financialInsights" :key="insight.id" class="insight-item">
              <Icon :name="insight.type === 'warning' ? 'heroicons:exclamation-triangle' : 'heroicons:lightbulb'" 
                    class="w-4 h-4" 
                    :class="insight.type === 'warning' ? 'text-ai-warning' : 'text-ai-success'" />
              <span>{{ insight.text }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 현금 흐름 카드 -->
      <div class="card cash-flow">
        <div class="card-header">
          <h3>현금 흐름</h3>
          <div class="period-selector">
            <select v-model="selectedPeriod" @change="updateCashFlow">
              <option value="week">이번 주</option>
              <option value="month">이번 달</option>
              <option value="quarter">이번 분기</option>
              <option value="year">올해</option>
            </select>
          </div>
        </div>
        
        <div class="cash-flow-chart">
          <canvas ref="cashFlowChart" width="400" height="200"></canvas>
        </div>
        
        <div class="cash-flow-summary">
          <div class="flow-item inflow">
            <Icon name="heroicons:arrow-down-circle" class="w-5 h-5 text-ai-success" />
            <div>
              <div class="flow-label">현금 유입</div>
              <div class="flow-amount">{{ formatCurrency(cashFlowData.inflow) }}</div>
            </div>
          </div>
          
          <div class="flow-item outflow">
            <Icon name="heroicons:arrow-up-circle" class="w-5 h-5 text-ai-error" />
            <div>
              <div class="flow-label">현금 유출</div>
              <div class="flow-amount">{{ formatCurrency(cashFlowData.outflow) }}</div>
            </div>
          </div>
          
          <div class="flow-item net">
            <Icon name="heroicons:equals" class="w-5 h-5 text-ai-primary" />
            <div>
              <div class="flow-label">순 현금 흐름</div>
              <div class="flow-amount" :class="cashFlowData.net >= 0 ? 'positive' : 'negative'">
                {{ formatCurrency(cashFlowData.net) }}
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 미수금/미지급금 카드 -->
      <div class="card receivables-payables">
        <div class="card-header">
          <h3>미수금 · 미지급금</h3>
          <button @click="optimizeCollections" class="optimize-btn">
            <Icon name="heroicons:sparkles" class="w-4 h-4" />
            AI 최적화
          </button>
        </div>
        
        <div class="ap-ar-summary">
          <div class="ar-section">
            <h4>미수금 (A/R)</h4>
            <div class="amount-display">
              <span class="amount">{{ formatCurrency(arData.total) }}</span>
              <span class="count">({{ arData.count }}건)</span>
            </div>
            <div class="aging-breakdown">
              <div class="aging-item" v-for="aging in arData.aging" :key="aging.period">
                <span class="period">{{ aging.period }}</span>
                <span class="amount">{{ formatCurrency(aging.amount) }}</span>
                <div class="progress-bar">
                  <div class="progress-fill" :style="{ width: aging.percentage + '%' }"></div>
                </div>
              </div>
            </div>
            <div class="ai-suggestions">
              <h5>AI 수금 제안</h5>
              <ul>
                <li v-for="suggestion in arSuggestions" :key="suggestion.id">
                  <Icon name="heroicons:lightbulb" class="w-4 h-4 text-ai-warning" />
                  {{ suggestion.text }}
                  <button @click="implementSuggestion(suggestion)" class="implement-btn">실행</button>
                </li>
              </ul>
            </div>
          </div>
          
          <div class="ap-section">
            <h4>미지급금 (A/P)</h4>
            <div class="amount-display">
              <span class="amount">{{ formatCurrency(apData.total) }}</span>
              <span class="count">({{ apData.count }}건)</span>
            </div>
            <div class="aging-breakdown">
              <div class="aging-item" v-for="aging in apData.aging" :key="aging.period">
                <span class="period">{{ aging.period }}</span>
                <span class="amount">{{ formatCurrency(aging.amount) }}</span>
                <div class="progress-bar">
                  <div class="progress-fill" :style="{ width: aging.percentage + '%' }"></div>
                </div>
              </div>
            </div>
            <div class="payment-schedule">
              <h5>AI 결제 계획</h5>
              <div class="schedule-list">
                <div v-for="payment in paymentSchedule" :key="payment.id" class="schedule-item">
                  <div class="payment-date">{{ formatDate(payment.date) }}</div>
                  <div class="payment-amount">{{ formatCurrency(payment.amount) }}</div>
                  <div class="payment-priority" :class="payment.priority">{{ payment.priority }}</div>
                  <button @click="schedulePayment(payment)" class="schedule-btn">예약</button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 계정 과목 관리 -->
    <div class="chart-of-accounts">
      <div class="section-header">
        <h2>계정 과목</h2>
        <div class="section-actions">
          <button @click="addAccount" class="add-btn">
            <Icon name="heroicons:plus" class="w-4 h-4" />
            계정 추가
          </button>
          <button @click="importAccounts" class="import-btn">
            <Icon name="heroicons:arrow-down-tray" class="w-4 h-4" />
            일괄 가져오기
          </button>
          <button @click="analyzeAccounts" class="analyze-btn">
            <Icon name="heroicons:sparkles" class="w-4 h-4" />
            AI 분석
          </button>
        </div>
      </div>
      
      <div class="accounts-tree">
        <div v-for="accountGroup in accountsTree" :key="accountGroup.id" class="account-group">
          <div class="group-header" @click="toggleGroup(accountGroup.id)">
            <Icon :name="accountGroup.expanded ? 'heroicons:minus' : 'heroicons:plus'" class="w-4 h-4" />
            <Icon :name="accountGroup.icon" class="w-5 h-5" />
            <span class="group-name">{{ accountGroup.name }}</span>
            <span class="group-balance">{{ formatCurrency(accountGroup.balance) }}</span>
            <div class="ai-health-indicator" :class="accountGroup.aiHealth">
              <Icon name="heroicons:circle" class="w-3 h-3" />
            </div>
          </div>
          
          <div v-if="accountGroup.expanded" class="group-accounts">
            <div v-for="account in accountGroup.accounts" :key="account.id" class="account-item">
              <div class="account-info">
                <span class="account-code">{{ account.code }}</span>
                <span class="account-name">{{ account.name }}</span>
                <span class="account-type">{{ account.type }}</span>
              </div>
              <div class="account-balance">{{ formatCurrency(account.balance) }}</div>
              <div class="account-actions">
                <button @click="viewAccount(account)" class="view-btn">
                  <Icon name="heroicons:eye" class="w-4 h-4" />
                </button>
                <button @click="editAccount(account)" class="edit-btn">
                  <Icon name="heroicons:pencil" class="w-4 h-4" />
                </button>
                <button @click="analyzeAccount(account)" class="ai-analyze-btn">
                  <Icon name="heroicons:sparkles" class="w-4 h-4" />
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 거래 내역 -->
    <div class="transactions-section">
      <div class="section-header">
        <h2>최근 거래</h2>
        <div class="transaction-filters">
          <input 
            v-model="transactionSearch" 
            type="text" 
            placeholder="거래 검색..." 
            class="search-input"
          >
          <select v-model="transactionFilter" class="filter-select">
            <option value="all">모든 거래</option>
            <option value="income">수입</option>
            <option value="expense">지출</option>
            <option value="transfer">이체</option>
          </select>
          <button @click="createTransaction" class="create-btn">
            <Icon name="heroicons:plus" class="w-4 h-4" />
            거래 생성
          </button>
        </div>
      </div>
      
      <div class="transactions-table">
        <div class="table-header">
          <div class="col-date">날짜</div>
          <div class="col-description">설명</div>
          <div class="col-account">계정</div>
          <div class="col-amount">금액</div>
          <div class="col-status">상태</div>
          <div class="col-actions">작업</div>
        </div>
        
        <div class="table-body">
          <div v-for="transaction in filteredTransactions" :key="transaction.id" class="transaction-row">
            <div class="col-date">{{ formatDate(transaction.date) }}</div>
            <div class="col-description">
              <div class="transaction-desc">{{ transaction.description }}</div>
              <div v-if="transaction.aiGenerated" class="ai-badge">AI 생성</div>
            </div>
            <div class="col-account">{{ transaction.account }}</div>
            <div class="col-amount" :class="transaction.type">
              {{ formatCurrency(transaction.amount) }}
            </div>
            <div class="col-status">
              <span class="status-badge" :class="transaction.status">{{ transaction.status }}</span>
            </div>
            <div class="col-actions">
              <button @click="editTransaction(transaction)" class="edit-btn">
                <Icon name="heroicons:pencil" class="w-4 h-4" />
              </button>
              <button @click="duplicateTransaction(transaction)" class="duplicate-btn">
                <Icon name="heroicons:square-2-stack" class="w-4 h-4" />
              </button>
              <button @click="analyzeTransaction(transaction)" class="analyze-btn">
                <Icon name="heroicons:sparkles" class="w-4 h-4" />
              </button>
            </div>
          </div>
        </div>
      </div>
      
      <div class="table-pagination">
        <button @click="previousPage" :disabled="currentPage === 1" class="page-btn">
          <Icon name="heroicons:chevron-left" class="w-4 h-4" />
        </button>
        <span class="page-info">{{ currentPage }} / {{ totalPages }}</span>
        <button @click="nextPage" :disabled="currentPage === totalPages" class="page-btn">
          <Icon name="heroicons:chevron-right" class="w-4 h-4" />
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { Icon } from '@iconify/vue'
import { useAI } from '@/composables/useAI'
import { useNotification } from '@/composables/useNotification'

// 반응형 데이터
const aiCommand = ref('')
const processing = ref(false)
const selectedPeriod = ref('month')
const transactionSearch = ref('')
const transactionFilter = ref('all')
const currentPage = ref(1)
const itemsPerPage = 10

// 재무 데이터
const financialData = ref({
  totalAssets: 15420000,
  assetChange: 8.5,
  totalLiabilities: 8950000,
  liabilityChange: -2.3,
  equity: 6470000,
  equityChange: 12.7,
  netIncome: 2340000,
  incomeChange: 15.2
})

// 현금 흐름 데이터
const cashFlowData = ref({
  inflow: 5650000,
  outflow: 4230000,
  net: 1420000
})

// 미수금 데이터
const arData = ref({
  total: 3240000,
  count: 45,
  aging: [
    { period: '30일 이내', amount: 1890000, percentage: 58 },
    { period: '31-60일', amount: 810000, percentage: 25 },
    { period: '61-90일', amount: 380000, percentage: 12 },
    { period: '90일 초과', amount: 160000, percentage: 5 }
  ]
})

// 미지급금 데이터
const apData = ref({
  total: 2180000,
  count: 32,
  aging: [
    { period: '30일 이내', amount: 1520000, percentage: 70 },
    { period: '31-60일', amount: 480000, percentage: 22 },
    { period: '61-90일', amount: 150000, percentage: 7 },
    { period: '90일 초과', amount: 30000, percentage: 1 }
  ]
})

// 실시간 AI 인사이트
const realtimeInsights = ref([
  {
    id: 1,
    text: '현금 흐름이 지난달 대비 15% 개선되었습니다',
    icon: 'heroicons:arrow-trending-up',
    color: 'text-ai-success'
  },
  {
    id: 2,
    text: '90일 초과 미수금이 증가하고 있습니다',
    icon: 'heroicons:exclamation-triangle',
    color: 'text-ai-warning'
  },
  {
    id: 3,
    text: '이번 분기 매출 목표 달성률 112%',
    icon: 'heroicons:chart-bar',
    color: 'text-ai-primary'
  }
])

// 재무 AI 인사이트
const financialInsights = ref([
  {
    id: 1,
    type: 'insight',
    text: '부채비율이 안정적인 수준을 유지하고 있습니다'
  },
  {
    id: 2,
    type: 'warning',
    text: '운전자본 회전율이 다소 낮아지고 있어 주의가 필요합니다'
  },
  {
    id: 3,
    type: 'insight',
    text: '순이익률이 업계 평균보다 3.2% 높습니다'
  }
])

// 계정 과목 트리
const accountsTree = ref([
  {
    id: 1,
    name: '자산',
    icon: 'heroicons:building-office',
    balance: 15420000,
    aiHealth: 'good',
    expanded: true,
    accounts: [
      { id: 11, code: '1100', name: '현금및현금성자산', type: '유동자산', balance: 2340000 },
      { id: 12, code: '1200', name: '매출채권', type: '유동자산', balance: 3240000 },
      { id: 13, code: '1300', name: '재고자산', type: '유동자산', balance: 4580000 },
      { id: 14, code: '1400', name: '유형자산', type: '비유동자산', balance: 5260000 }
    ]
  },
  {
    id: 2,
    name: '부채',
    icon: 'heroicons:credit-card',
    balance: 8950000,
    aiHealth: 'warning',
    expanded: false,
    accounts: []
  },
  {
    id: 3,
    name: '자본',
    icon: 'heroicons:banknotes',
    balance: 6470000,
    aiHealth: 'good',
    expanded: false,
    accounts: []
  },
  {
    id: 4,
    name: '수익',
    icon: 'heroicons:arrow-trending-up',
    balance: 12680000,
    aiHealth: 'excellent',
    expanded: false,
    accounts: []
  },
  {
    id: 5,
    name: '비용',
    icon: 'heroicons:arrow-trending-down',
    balance: 10340000,
    aiHealth: 'good',
    expanded: false,
    accounts: []
  }
])

// 거래 내역
const transactions = ref([
  {
    id: 1,
    date: new Date(Date.now() - 86400000),
    description: '제품 판매 - ABC 회사',
    account: '매출',
    amount: 1500000,
    type: 'income',
    status: '완료',
    aiGenerated: false
  },
  {
    id: 2,
    date: new Date(Date.now() - 172800000),
    description: '사무용품 구매',
    account: '사무비',
    amount: -85000,
    type: 'expense',
    status: '완료',
    aiGenerated: true
  },
  {
    id: 3,
    date: new Date(Date.now() - 259200000),
    description: '급여 지급',
    account: '급여비',
    amount: -3200000,
    type: 'expense',
    status: '완료',
    aiGenerated: true
  }
])

// 컴퓨티드
const filteredTransactions = computed(() => {
  let filtered = transactions.value

  if (transactionSearch.value) {
    const search = transactionSearch.value.toLowerCase()
    filtered = filtered.filter(t => 
      t.description.toLowerCase().includes(search) ||
      t.account.toLowerCase().includes(search)
    )
  }

  if (transactionFilter.value !== 'all') {
    filtered = filtered.filter(t => t.type === transactionFilter.value)
  }

  return filtered.slice(
    (currentPage.value - 1) * itemsPerPage,
    currentPage.value * itemsPerPage
  )
})

const totalPages = computed(() => {
  return Math.ceil(transactions.value.length / itemsPerPage)
})

// AI 관련 제안들
const arSuggestions = ref([
  {
    id: 1,
    text: 'ABC 회사에 3일 내 결제 요청 이메일 발송'
  },
  {
    id: 2,
    text: '90일 초과 채권에 대해 할인 제안'
  }
])

const paymentSchedule = ref([
  {
    id: 1,
    date: new Date(Date.now() + 86400000 * 3),
    amount: 850000,
    priority: 'high'
  },
  {
    id: 2,
    date: new Date(Date.now() + 86400000 * 7),
    amount: 1200000,
    priority: 'medium'
  }
])

// 컴포저블
const { processAIRequest } = useAI()
const { showNotification } = useNotification()

// 메서드
const formatCurrency = (amount) => {
  return new Intl.NumberFormat('ko-KR', {
    style: 'currency',
    currency: 'KRW'
  }).format(amount)
}

const formatDate = (date) => {
  return new Intl.DateTimeFormat('ko-KR', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  }).format(date)
}

const executeAccountsAI = async () => {
  if (!aiCommand.value.trim()) return
  
  processing.value = true
  
  try {
    const result = await processAIRequest(aiCommand.value, {
      module: 'accounts',
      context: 'financial_management'
    })
    
    showNotification('AI 회계 명령이 실행되었습니다.', 'success')
    aiCommand.value = ''
    
  } catch (error) {
    showNotification('AI 명령 실행 중 오류가 발생했습니다.', 'error')
  } finally {
    processing.value = false
  }
}

const toggleGroup = (groupId) => {
  const group = accountsTree.value.find(g => g.id === groupId)
  if (group) {
    group.expanded = !group.expanded
  }
}

const previousPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--
  }
}

const nextPage = () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value++
  }
}

// 라이프사이클
onMounted(() => {
  // 실시간 데이터 업데이트
  setInterval(() => {
    // 실시간 업데이트 로직
  }, 30000)
})
</script>

<style scoped>
.accounts-module {
  padding: 2rem;
  background: var(--bg-primary);
  min-height: 100vh;
  color: var(--text-primary);
}

/* 모듈 헤더 */
.module-header {
  margin-bottom: 2rem;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.module-title {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.module-title h1 {
  font-size: 2rem;
  font-weight: 700;
  margin: 0;
  background: var(--gradient-primary);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.module-title p {
  margin: 0.5rem 0 0 0;
  color: var(--text-secondary);
}

.header-actions {
  display: flex;
  gap: 1rem;
}

.ai-assist-btn, .generate-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 1rem 1.5rem;
  border-radius: var(--border-radius);
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.ai-assist-btn {
  background: var(--gradient-primary);
  border: none;
  color: white;
}

.generate-btn {
  background: var(--bg-secondary);
  border: 1px solid var(--border-primary);
  color: var(--text-primary);
}

.ai-assist-btn:hover, .generate-btn:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

/* AI 인사이트 바 */
.ai-insights-bar {
  display: flex;
  gap: 1rem;
  padding: 1rem;
  background: var(--bg-secondary);
  border-radius: var(--border-radius);
  border: 1px solid var(--border-primary);
  overflow-x: auto;
}

.ai-insights-bar .insight-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  background: var(--bg-tertiary);
  border-radius: var(--border-radius);
  white-space: nowrap;
  min-width: fit-content;
}

.explore-btn {
  background: none;
  border: none;
  color: var(--ai-primary);
  cursor: pointer;
  padding: 0.25rem;
  border-radius: 4px;
  transition: background 0.2s;
}

.explore-btn:hover {
  background: var(--bg-hover);
}

/* AI 명령 섹션 */
.ai-command-section {
  margin-bottom: 2rem;
}

.command-container {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1.5rem;
  background: var(--bg-secondary);
  border-radius: var(--border-radius-lg);
  border: 1px solid var(--border-primary);
}

.ai-command-input {
  flex: 1;
  background: var(--bg-tertiary);
  border: 1px solid var(--border-secondary);
  border-radius: var(--border-radius);
  padding: 1rem;
  color: var(--text-primary);
  resize: vertical;
  min-height: 80px;
}

.ai-command-input:focus {
  outline: none;
  border-color: var(--ai-primary);
  box-shadow: var(--glow-primary);
}

.ai-execute-btn {
  padding: 1rem;
  background: var(--gradient-primary);
  border: none;
  border-radius: var(--border-radius);
  color: white;
  cursor: pointer;
  transition: all 0.3s ease;
}

.ai-execute-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: var(--glow-primary);
}

.ai-execute-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* 대시보드 카드들 */
.dashboard-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 2rem;
  margin-bottom: 3rem;
}

.card {
  background: var(--bg-secondary);
  border-radius: var(--border-radius-lg);
  padding: 2rem;
  border: 1px solid var(--border-primary);
  transition: all 0.3s ease;
}

.card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-lg);
  border-color: var(--ai-primary);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.card-header h3 {
  margin: 0;
  font-size: 1.25rem;
  color: var(--ai-primary);
}

.card-actions {
  display: flex;
  gap: 0.5rem;
}

.refresh-btn, .analyze-btn, .optimize-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: var(--bg-tertiary);
  border: 1px solid var(--border-secondary);
  border-radius: var(--border-radius);
  color: var(--text-primary);
  cursor: pointer;
  font-size: 0.875rem;
  transition: all 0.3s ease;
}

.refresh-btn:hover, .analyze-btn:hover, .optimize-btn:hover {
  background: var(--ai-primary);
  color: white;
}

/* 재무 메트릭 */
.financial-metrics {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.metric {
  padding: 1rem;
  background: var(--bg-tertiary);
  border-radius: var(--border-radius);
  text-align: center;
}

.metric-label {
  font-size: 0.875rem;
  color: var(--text-secondary);
  margin-bottom: 0.5rem;
}

.metric-value {
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 0.5rem;
}

.metric-change {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.25rem;
  font-size: 0.875rem;
  font-weight: 500;
}

.metric-change.positive {
  color: var(--ai-success);
}

.metric-change.negative {
  color: var(--ai-error);
}

/* AI 재무 인사이트 */
.ai-financial-insights h4 {
  margin: 0 0 1rem 0;
  color: var(--ai-primary);
  font-size: 1rem;
}

.insights-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.insights-list .insight-item {
  display: flex;
  align-items: flex-start;
  gap: 0.5rem;
  padding: 0.75rem;
  background: var(--bg-elevated);
  border-radius: var(--border-radius);
  font-size: 0.875rem;
}

/* 현금 흐름 */
.period-selector select {
  background: var(--bg-tertiary);
  border: 1px solid var(--border-secondary);
  border-radius: var(--border-radius);
  padding: 0.5rem;
  color: var(--text-primary);
}

.cash-flow-chart {
  margin: 1.5rem 0;
  padding: 1rem;
  background: var(--bg-tertiary);
  border-radius: var(--border-radius);
}

.cash-flow-summary {
  display: flex;
  justify-content: space-between;
  gap: 1rem;
}

.flow-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex: 1;
  padding: 1rem;
  background: var(--bg-tertiary);
  border-radius: var(--border-radius);
}

.flow-label {
  font-size: 0.875rem;
  color: var(--text-secondary);
}

.flow-amount {
  font-weight: 600;
  font-size: 1.125rem;
}

.flow-amount.positive {
  color: var(--ai-success);
}

.flow-amount.negative {
  color: var(--ai-error);
}

/* 미수금/미지급금 */
.ap-ar-summary {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
}

.ar-section h4, .ap-section h4 {
  margin: 0 0 1rem 0;
  color: var(--ai-primary);
}

.amount-display {
  display: flex;
  align-items: baseline;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.amount-display .amount {
  font-size: 1.5rem;
  font-weight: 600;
}

.amount-display .count {
  color: var(--text-secondary);
  font-size: 0.875rem;
}

.aging-breakdown {
  margin-bottom: 1.5rem;
}

.aging-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 0;
  border-bottom: 1px solid var(--border-primary);
}

.aging-item:last-child {
  border-bottom: none;
}

.progress-bar {
  width: 60px;
  height: 6px;
  background: var(--bg-primary);
  border-radius: 3px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: var(--gradient-primary);
  transition: width 0.3s ease;
}

/* AI 제안 */
.ai-suggestions h5, .payment-schedule h5 {
  margin: 0 0 1rem 0;
  color: var(--ai-accent);
  font-size: 0.875rem;
}

.ai-suggestions ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.ai-suggestions li {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem;
  background: var(--bg-elevated);
  border-radius: var(--border-radius);
  margin-bottom: 0.5rem;
  font-size: 0.875rem;
}

.implement-btn {
  margin-left: auto;
  padding: 0.25rem 0.75rem;
  background: var(--ai-success);
  border: none;
  border-radius: 12px;
  color: white;
  font-size: 0.75rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.implement-btn:hover {
  transform: translateY(-1px);
  box-shadow: var(--shadow-sm);
}

/* 결제 일정 */
.schedule-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.schedule-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0.75rem;
  background: var(--bg-elevated);
  border-radius: var(--border-radius);
  font-size: 0.875rem;
}

.payment-priority {
  padding: 0.25rem 0.5rem;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 500;
}

.payment-priority.high {
  background: var(--ai-error);
  color: white;
}

.payment-priority.medium {
  background: var(--ai-warning);
  color: white;
}

.payment-priority.low {
  background: var(--ai-info);
  color: white;
}

.schedule-btn {
  margin-left: auto;
  padding: 0.25rem 0.75rem;
  background: var(--ai-primary);
  border: none;
  border-radius: 12px;
  color: white;
  font-size: 0.75rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.schedule-btn:hover {
  transform: translateY(-1px);
}

/* 계정 과목 관리 */
.chart-of-accounts, .transactions-section {
  background: var(--bg-secondary);
  border-radius: var(--border-radius-lg);
  padding: 2rem;
  margin-bottom: 2rem;
  border: 1px solid var(--border-primary);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.section-header h2 {
  margin: 0;
  color: var(--ai-primary);
}

.section-actions, .transaction-filters {
  display: flex;
  gap: 1rem;
  align-items: center;
  flex-wrap: wrap;
}

.add-btn, .import-btn, .create-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  background: var(--ai-primary);
  border: none;
  border-radius: var(--border-radius);
  color: white;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.add-btn:hover, .import-btn:hover, .create-btn:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

/* 계정 트리 */
.accounts-tree {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.account-group {
  border: 1px solid var(--border-primary);
  border-radius: var(--border-radius);
  overflow: hidden;
}

.group-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: var(--bg-tertiary);
  cursor: pointer;
  transition: all 0.3s ease;
}

.group-header:hover {
  background: var(--bg-elevated);
}

.group-name {
  flex: 1;
  font-weight: 600;
}

.group-balance {
  font-weight: 600;
  color: var(--ai-primary);
}

.ai-health-indicator {
  width: 12px;
  height: 12px;
  border-radius: 50%;
}

.ai-health-indicator.excellent {
  color: var(--ai-success);
}

.ai-health-indicator.good {
  color: var(--ai-primary);
}

.ai-health-indicator.warning {
  color: var(--ai-warning);
}

.ai-health-indicator.poor {
  color: var(--ai-error);
}

.group-accounts {
  background: var(--bg-primary);
}

.account-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0.75rem 1rem 0.75rem 3rem;
  border-bottom: 1px solid var(--border-primary);
  transition: all 0.3s ease;
}

.account-item:last-child {
  border-bottom: none;
}

.account-item:hover {
  background: var(--bg-secondary);
}

.account-info {
  display: flex;
  gap: 1rem;
  flex: 1;
}

.account-code {
  font-family: monospace;
  color: var(--text-secondary);
  min-width: 60px;
}

.account-name {
  flex: 1;
}

.account-type {
  color: var(--text-secondary);
  font-size: 0.875rem;
}

.account-balance {
  font-weight: 600;
  color: var(--ai-primary);
  min-width: 120px;
  text-align: right;
}

.account-actions {
  display: flex;
  gap: 0.5rem;
}

.view-btn, .edit-btn, .ai-analyze-btn {
  padding: 0.5rem;
  background: var(--bg-tertiary);
  border: 1px solid var(--border-secondary);
  border-radius: var(--border-radius);
  color: var(--text-secondary);
  cursor: pointer;
  transition: all 0.3s ease;
}

.view-btn:hover, .edit-btn:hover, .ai-analyze-btn:hover {
  color: var(--ai-primary);
  border-color: var(--ai-primary);
}

/* 거래 테이블 */
.search-input, .filter-select {
  padding: 0.75rem;
  background: var(--bg-tertiary);
  border: 1px solid var(--border-secondary);
  border-radius: var(--border-radius);
  color: var(--text-primary);
}

.transactions-table {
  margin: 1.5rem 0;
}

.table-header, .transaction-row {
  display: grid;
  grid-template-columns: 100px 1fr 120px 120px 80px 120px;
  gap: 1rem;
  align-items: center;
  padding: 1rem;
  border-bottom: 1px solid var(--border-primary);
}

.table-header {
  background: var(--bg-tertiary);
  font-weight: 600;
  color: var(--text-secondary);
  border-radius: var(--border-radius) var(--border-radius) 0 0;
}

.transaction-row {
  transition: all 0.3s ease;
}

.transaction-row:hover {
  background: var(--bg-tertiary);
}

.transaction-desc {
  font-weight: 500;
}

.ai-badge {
  display: inline-block;
  padding: 0.25rem 0.5rem;
  background: var(--ai-primary);
  color: white;
  border-radius: 12px;
  font-size: 0.75rem;
  margin-top: 0.25rem;
}

.col-amount.income {
  color: var(--ai-success);
  font-weight: 600;
}

.col-amount.expense {
  color: var(--ai-error);
  font-weight: 600;
}

.status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 500;
}

.status-badge.완료 {
  background: var(--ai-success);
  color: white;
}

.status-badge.대기 {
  background: var(--ai-warning);
  color: white;
}

.col-actions {
  display: flex;
  gap: 0.5rem;
}

.edit-btn, .duplicate-btn, .analyze-btn {
  padding: 0.5rem;
  background: var(--bg-elevated);
  border: 1px solid var(--border-secondary);
  border-radius: var(--border-radius);
  color: var(--text-secondary);
  cursor: pointer;
  transition: all 0.3s ease;
}

.edit-btn:hover, .duplicate-btn:hover, .analyze-btn:hover {
  color: var(--ai-primary);
  border-color: var(--ai-primary);
}

/* 페이지네이션 */
.table-pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  margin-top: 1.5rem;
}

.page-btn {
  padding: 0.5rem;
  background: var(--bg-tertiary);
  border: 1px solid var(--border-secondary);
  border-radius: var(--border-radius);
  color: var(--text-primary);
  cursor: pointer;
  transition: all 0.3s ease;
}

.page-btn:hover:not(:disabled) {
  background: var(--ai-primary);
  color: white;
}

.page-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.page-info {
  color: var(--text-secondary);
  font-size: 0.875rem;
}

/* 반응형 */
@media (max-width: 768px) {
  .accounts-module {
    padding: 1rem;
  }
  
  .dashboard-cards {
    grid-template-columns: 1fr;
  }
  
  .financial-metrics {
    grid-template-columns: 1fr;
  }
  
  .ap-ar-summary {
    grid-template-columns: 1fr;
  }
  
  .cash-flow-summary {
    flex-direction: column;
  }
  
  .table-header, .transaction-row {
    grid-template-columns: 1fr;
    gap: 0.5rem;
  }
  
  .table-header {
    display: none;
  }
  
  .transaction-row {
    display: flex;
    flex-direction: column;
    text-align: left;
  }
}
</style>