<template>
  <div class="accounts min-h-screen bg-white">
    <!-- 헤더 -->
    <div class="bg-white border-b border-gray-200 p-6">
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-3xl font-bold text-gray-900 mb-2">회계 관리</h1>
          <p class="text-gray-600">재무 제표, 계정 관리 및 회계 자동화</p>
        </div>
        <div class="flex space-x-3">
          <button 
            @click="editMode = !editMode" 
            class="px-4 py-2 text-sm font-medium rounded-md border"
            :class="editMode ? 'bg-blue-600 text-white border-blue-600' : 'bg-white text-gray-700 border-gray-300 hover:bg-gray-50'"
          >
            {{ editMode ? '편집 완료' : '편집 모드' }}
          </button>
          <button class="px-4 py-2 bg-blue-600 text-white text-sm font-medium rounded-md hover:bg-blue-700">
            새 거래 등록
          </button>
        </div>
      </div>
    </div>

    <!-- 메인 콘텐츠 -->
    <div class="p-6">
      <!-- 재무 현황 카드 -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div class="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm font-medium text-gray-500">총 자산</p>
              <p class="text-2xl font-bold text-gray-900" :contenteditable="editMode">₩12.5B</p>
            </div>
            <div class="p-3 bg-blue-50 rounded-full">
              <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
              </svg>
            </div>
          </div>
          <div class="mt-4 flex items-center text-sm">
            <span class="text-green-500 font-medium" :contenteditable="editMode">+8.2%</span>
            <span class="text-gray-500 ml-2">전월 대비</span>
          </div>
        </div>

        <div class="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm font-medium text-gray-500">총 부채</p>
              <p class="text-2xl font-bold text-gray-900" :contenteditable="editMode">₩3.8B</p>
            </div>
            <div class="p-3 bg-red-50 rounded-full">
              <svg class="w-6 h-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
          </div>
          <div class="mt-4 flex items-center text-sm">
            <span class="text-red-500 font-medium" :contenteditable="editMode">+2.1%</span>
            <span class="text-gray-500 ml-2">증가</span>
          </div>
        </div>

        <div class="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm font-medium text-gray-500">당기순이익</p>
              <p class="text-2xl font-bold text-gray-900" :contenteditable="editMode">₩2.1B</p>
            </div>
            <div class="p-3 bg-green-50 rounded-full">
              <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
              </svg>
            </div>
          </div>
          <div class="mt-4 flex items-center text-sm">
            <span class="text-green-500 font-medium" :contenteditable="editMode">+15.7%</span>
            <span class="text-gray-500 ml-2">개선</span>
          </div>
        </div>

        <div class="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm font-medium text-gray-500">현금흐름</p>
              <p class="text-2xl font-bold text-gray-900" :contenteditable="editMode">₩850M</p>
            </div>
            <div class="p-3 bg-purple-50 rounded-full">
              <svg class="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1" />
              </svg>
            </div>
          </div>
          <div class="mt-4 flex items-center text-sm">
            <span class="text-green-500 font-medium" :contenteditable="editMode">+5.3%</span>
            <span class="text-gray-500 ml-2">양호</span>
          </div>
        </div>
      </div>

      <!-- 메인 콘텐츠 그리드 -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <!-- 최근 거래 내역 -->
        <div class="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <div class="flex items-center justify-between mb-6">
            <h3 class="text-lg font-semibold text-gray-900">최근 거래 내역</h3>
            <div class="flex space-x-2">
              <button 
                @click="editTransactions = !editTransactions" 
                class="px-3 py-1.5 text-sm bg-blue-600 text-white rounded-md hover:bg-blue-700"
              >
                {{ editTransactions ? '저장' : '수정' }}
              </button>
              <button class="px-3 py-1.5 text-sm bg-gray-100 text-gray-700 rounded-md hover:bg-gray-200">
                전체 보기
              </button>
            </div>
          </div>
          
          <div class="space-y-4">
            <div v-for="transaction in transactions" :key="transaction.id" class="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
              <div class="flex-1">
                <div class="font-medium text-gray-900" :contenteditable="editTransactions">{{ transaction.description }}</div>
                <div class="text-sm text-gray-500" :contenteditable="editTransactions">{{ transaction.account }} • {{ transaction.date }}</div>
              </div>
              <div class="text-right">
                <div class="font-medium" :class="transaction.type === 'credit' ? 'text-green-600' : 'text-red-600'" :contenteditable="editTransactions">
                  {{ transaction.type === 'credit' ? '+' : '-' }}{{ transaction.amount }}
                </div>
                <div class="text-sm text-gray-500" :contenteditable="editTransactions">{{ transaction.reference }}</div>
              </div>
            </div>
          </div>
        </div>

        <!-- 계정별 잔액 -->
        <div class="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <div class="flex items-center justify-between mb-6">
            <h3 class="text-lg font-semibold text-gray-900">계정별 잔액</h3>
            <button 
              @click="editAccounts = !editAccounts" 
              class="px-3 py-1.5 text-sm bg-blue-600 text-white rounded-md hover:bg-blue-700"
            >
              {{ editAccounts ? '저장' : '수정' }}
            </button>
          </div>
          
          <div class="space-y-3">
            <div v-for="account in accounts" :key="account.id" class="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
              <div class="flex-1">
                <div class="font-medium text-gray-900" :contenteditable="editAccounts">{{ account.name }}</div>
                <div class="text-sm text-gray-500" :contenteditable="editAccounts">{{ account.type }} • {{ account.code }}</div>
              </div>
              <div class="text-right">
                <div class="font-medium text-gray-900" :contenteditable="editAccounts">{{ account.balance }}</div>
                <div class="text-sm" :class="account.change >= 0 ? 'text-green-500' : 'text-red-500'" :contenteditable="editAccounts">
                  {{ account.change >= 0 ? '+' : '' }}{{ account.change }}%
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 예산 vs 실적 -->
        <div class="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <div class="flex items-center justify-between mb-6">
            <h3 class="text-lg font-semibold text-gray-900">예산 vs 실적</h3>
            <button 
              @click="editBudget = !editBudget" 
              class="px-3 py-1.5 text-sm bg-blue-600 text-white rounded-md hover:bg-blue-700"
            >
              {{ editBudget ? '저장' : '수정' }}
            </button>
          </div>
          
          <div class="space-y-4">
            <div v-for="budget in budgetItems" :key="budget.id" class="p-4 bg-gray-50 rounded-lg">
              <div class="flex justify-between items-center mb-2">
                <h4 class="font-medium text-gray-900" :contenteditable="editBudget">{{ budget.category }}</h4>
                <span class="text-sm text-gray-500" :contenteditable="editBudget">{{ budget.period }}</span>
              </div>
              <div class="space-y-2">
                <div class="flex justify-between text-sm">
                  <span class="text-gray-600">예산:</span>
                  <span class="text-gray-900" :contenteditable="editBudget">{{ budget.budgeted }}</span>
                </div>
                <div class="flex justify-between text-sm">
                  <span class="text-gray-600">실적:</span>
                  <span class="text-gray-900" :contenteditable="editBudget">{{ budget.actual }}</span>
                </div>
                <div class="w-full bg-gray-200 rounded-full h-2">
                  <div class="h-2 rounded-full" :class="budget.variance >= 0 ? 'bg-green-500' : 'bg-red-500'" :style="{ width: Math.abs(budget.variance) + '%' }"></div>
                </div>
                <div class="text-xs text-gray-500">차이: {{ budget.variance >= 0 ? '+' : '-' }}{{ Math.abs(budget.variance) }}%</div>
              </div>
            </div>
          </div>
        </div>

        <!-- 세무 신고 현황 -->
        <div class="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <div class="flex items-center justify-between mb-6">
            <h3 class="text-lg font-semibold text-gray-900">세무 신고 현황</h3>
            <button 
              @click="editTax = !editTax" 
              class="px-3 py-1.5 text-sm bg-blue-600 text-white rounded-md hover:bg-blue-700"
            >
              {{ editTax ? '저장' : '수정' }}
            </button>
          </div>
          
          <div class="space-y-3">
            <div v-for="tax in taxReports" :key="tax.id" class="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
              <div class="flex-1">
                <div class="font-medium text-gray-900" :contenteditable="editTax">{{ tax.type }}</div>
                <div class="text-sm text-gray-600" :contenteditable="editTax">신고기한: {{ tax.dueDate }}</div>
              </div>
              <div class="text-right">
                <span class="px-2 py-1 text-xs font-medium rounded-full" :class="tax.statusClass">
                  {{ tax.status }}
                </span>
                <div class="text-sm text-gray-500 mt-1" :contenteditable="editTax">{{ tax.amount }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- AI 회계 분석 -->
      <div class="mt-8 bg-gradient-to-r from-blue-50 to-indigo-50 p-6 rounded-lg border border-blue-200">
        <div class="flex items-start space-x-3">
          <div class="p-2 bg-blue-100 rounded-lg">
            <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 002 2h2a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v14a2 2 0 002 2z" />
            </svg>
          </div>
          <div class="flex-1">
            <h4 class="font-semibold text-gray-900 mb-2">AI 재무 인사이트</h4>
            <div class="space-y-2 text-sm text-gray-700" :contenteditable="editMode">
              <p>• 매출채권 회전율이 전분기 대비 15% 개선되었습니다. 현금흐름 안정화에 긍정적입니다</p>
              <p>• 광고비 지출이 예산을 12% 초과했습니다. ROI 검토가 필요합니다</p>
              <p>• 법인세 추정액이 전년 대비 8% 증가했습니다. 절세 전략을 검토하세요</p>
              <p>• 재고자산 회전일수가 늘어나고 있습니다. 재고 관리 최적화를 권장합니다</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- AI 어시스턴트 -->
    <AIAssistant context="회계 관리" />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import AIAssistant from '@/components/AIAssistant.vue'

// 편집 모드 상태
const editMode = ref(false)
const editTransactions = ref(false)
const editAccounts = ref(false)
const editBudget = ref(false)
const editTax = ref(false)

// 거래 내역 데이터
const transactions = ref([
  {
    id: 1,
    description: '제품 매출',
    account: '매출',
    date: '2024-01-15',
    type: 'credit',
    amount: '₩5,250,000',
    reference: 'INV-001'
  },
  {
    id: 2,
    description: '사무용품 구매',
    account: '소모품비',
    date: '2024-01-14',
    type: 'debit',
    amount: '₩150,000',
    reference: 'PUR-045'
  },
  {
    id: 3,
    description: '급여 지급',
    account: '급여',
    date: '2024-01-10',
    type: 'debit',
    amount: '₩12,500,000',
    reference: 'PAY-001'
  },
  {
    id: 4,
    description: '은행 이자 수입',
    account: '이자수익',
    date: '2024-01-08',
    type: 'credit',
    amount: '₩45,000',
    reference: 'INT-001'
  }
])

// 계정 잔액 데이터
const accounts = ref([
  {
    id: 1,
    name: '현금',
    type: '자산',
    code: '1001',
    balance: '₩2,450,000',
    change: 5.2
  },
  {
    id: 2,
    name: '매출채권',
    type: '자산',
    code: '1201',
    balance: '₩8,750,000',
    change: -2.1
  },
  {
    id: 3,
    name: '매입채무',
    type: '부채',
    code: '2001',
    balance: '₩3,200,000',
    change: 1.8
  },
  {
    id: 4,
    name: '미지급금',
    type: '부채',
    code: '2101',
    balance: '₩1,850,000',
    change: -5.4
  }
])

// 예산 데이터
const budgetItems = ref([
  {
    id: 1,
    category: '매출',
    period: '2024년 1월',
    budgeted: '₩50,000,000',
    actual: '₩52,500,000',
    variance: 5
  },
  {
    id: 2,
    category: '마케팅비',
    period: '2024년 1월',
    budgeted: '₩3,000,000',
    actual: '₩3,360,000',
    variance: -12
  },
  {
    id: 3,
    category: '인건비',
    period: '2024년 1월',
    budgeted: '₩15,000,000',
    actual: '₩14,750,000',
    variance: 1.7
  }
])

// 세무 신고 데이터
const taxReports = ref([
  {
    id: 1,
    type: '부가가치세',
    dueDate: '2024-01-25',
    status: '준비중',
    statusClass: 'bg-yellow-100 text-yellow-800',
    amount: '₩1,250,000'
  },
  {
    id: 2,
    type: '원천세',
    dueDate: '2024-01-10',
    status: '완료',
    statusClass: 'bg-green-100 text-green-800',
    amount: '₩850,000'
  },
  {
    id: 3,
    type: '법인세 중간신고',
    dueDate: '2024-01-31',
    status: '대기',
    statusClass: 'bg-gray-100 text-gray-800',
    amount: '₩5,200,000'
  }
])
</script>