<template>
  <div class="sales min-h-screen bg-white">
    <!-- 헤더 -->
    <div class="bg-white border-b border-gray-200 p-6">
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-3xl font-bold text-gray-900 mb-2">영업 관리</h1>
          <p class="text-gray-600">고객 관리, 매출 분석 및 영업 프로세스 자동화</p>
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
            새 거래처 등록
          </button>
        </div>
      </div>
    </div>

    <!-- 메인 콘텐츠 -->
    <div class="p-6">
      <!-- 매출 현황 카드 -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div class="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm font-medium text-gray-500">월 매출</p>
              <p class="text-2xl font-bold text-gray-900" :contenteditable="editMode">₩1.25B</p>
            </div>
            <div class="p-3 bg-blue-50 rounded-full">
              <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
              </svg>
            </div>
          </div>
          <div class="mt-4 flex items-center text-sm">
            <span class="text-green-500 font-medium" :contenteditable="editMode">+12.5%</span>
            <span class="text-gray-500 ml-2">전월 대비</span>
          </div>
        </div>

        <div class="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm font-medium text-gray-500">신규 고객</p>
              <p class="text-2xl font-bold text-gray-900" :contenteditable="editMode">156</p>
            </div>
            <div class="p-3 bg-green-50 rounded-full">
              <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
              </svg>
            </div>
          </div>
          <div class="mt-4 flex items-center text-sm">
            <span class="text-green-500 font-medium" :contenteditable="editMode">+8.2%</span>
            <span class="text-gray-500 ml-2">증가</span>
          </div>
        </div>

        <div class="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm font-medium text-gray-500">거래 성공률</p>
              <p class="text-2xl font-bold text-gray-900" :contenteditable="editMode">67.8%</p>
            </div>
            <div class="p-3 bg-purple-50 rounded-full">
              <svg class="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
          </div>
          <div class="mt-4 flex items-center text-sm">
            <span class="text-green-500 font-medium" :contenteditable="editMode">+3.4%</span>
            <span class="text-gray-500 ml-2">개선</span>
          </div>
        </div>

        <div class="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm font-medium text-gray-500">평균 거래액</p>
              <p class="text-2xl font-bold text-gray-900" :contenteditable="editMode">₩8.5M</p>
            </div>
            <div class="p-3 bg-orange-50 rounded-full">
              <svg class="w-6 h-6 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1" />
              </svg>
            </div>
          </div>
          <div class="mt-4 flex items-center text-sm">
            <span class="text-orange-500 font-medium" :contenteditable="editMode">+5.7%</span>
            <span class="text-gray-500 ml-2">상승</span>
          </div>
        </div>
      </div>

      <!-- 메인 콘텐츠 그리드 -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <!-- 최근 주문 -->
        <div class="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <div class="flex items-center justify-between mb-6">
            <h3 class="text-lg font-semibold text-gray-900">최근 주문</h3>
            <div class="flex space-x-2">
              <button 
                @click="editOrders = !editOrders" 
                class="px-3 py-1.5 text-sm bg-blue-600 text-white rounded-md hover:bg-blue-700"
              >
                {{ editOrders ? '저장' : '수정' }}
              </button>
              <button class="px-3 py-1.5 text-sm bg-gray-100 text-gray-700 rounded-md hover:bg-gray-200">
                전체 보기
              </button>
            </div>
          </div>
          
          <div class="space-y-4">
            <div v-for="order in recentOrders" :key="order.id" class="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
              <div class="flex-1">
                <div class="font-medium text-gray-900" :contenteditable="editOrders">{{ order.customer }}</div>
                <div class="text-sm text-gray-500" :contenteditable="editOrders">{{ order.orderNo }} • {{ order.date }}</div>
                <div class="text-sm text-gray-600" :contenteditable="editOrders">{{ order.product }}</div>
              </div>
              <div class="text-right">
                <div class="font-medium text-gray-900" :contenteditable="editOrders">{{ order.amount }}</div>
                <span class="px-2 py-1 text-xs font-medium rounded-full" :class="order.statusClass">
                  {{ order.status }}
                </span>
              </div>
            </div>
          </div>
        </div>

        <!-- 고객 현황 -->
        <div class="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <div class="flex items-center justify-between mb-6">
            <h3 class="text-lg font-semibold text-gray-900">주요 고객</h3>
            <button 
              @click="editCustomers = !editCustomers" 
              class="px-3 py-1.5 text-sm bg-blue-600 text-white rounded-md hover:bg-blue-700"
            >
              {{ editCustomers ? '저장' : '수정' }}
            </button>
          </div>
          
          <div class="space-y-3">
            <div v-for="customer in topCustomers" :key="customer.id" class="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
              <div class="flex items-center space-x-3">
                <div class="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center">
                  <span class="text-blue-600 font-medium">{{ customer.name.charAt(0) }}</span>
                </div>
                <div>
                  <div class="font-medium text-gray-900" :contenteditable="editCustomers">{{ customer.name }}</div>
                  <div class="text-sm text-gray-500" :contenteditable="editCustomers">{{ customer.industry }}</div>
                </div>
              </div>
              <div class="text-right">
                <div class="font-medium text-gray-900" :contenteditable="editCustomers">{{ customer.revenue }}</div>
                <div class="text-sm text-gray-500" :contenteditable="editCustomers">{{ customer.orders }}건</div>
              </div>
            </div>
          </div>
        </div>

        <!-- 영업 파이프라인 -->
        <div class="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <div class="flex items-center justify-between mb-6">
            <h3 class="text-lg font-semibold text-gray-900">영업 파이프라인</h3>
            <button 
              @click="editPipeline = !editPipeline" 
              class="px-3 py-1.5 text-sm bg-blue-600 text-white rounded-md hover:bg-blue-700"
            >
              {{ editPipeline ? '저장' : '수정' }}
            </button>
          </div>
          
          <div class="space-y-4">
            <div v-for="stage in pipelineStages" :key="stage.id" class="p-4 bg-gray-50 rounded-lg">
              <div class="flex justify-between items-center mb-2">
                <h4 class="font-medium text-gray-900" :contenteditable="editPipeline">{{ stage.name }}</h4>
                <span class="text-sm text-gray-500" :contenteditable="editPipeline">{{ stage.count }}건</span>
              </div>
              <div class="space-y-2">
                <div class="flex justify-between text-sm">
                  <span class="text-gray-600">예상 매출:</span>
                  <span class="text-gray-900" :contenteditable="editPipeline">{{ stage.revenue }}</span>
                </div>
                <div class="w-full bg-gray-200 rounded-full h-2">
                  <div class="bg-blue-500 h-2 rounded-full" :style="{ width: stage.progress + '%' }"></div>
                </div>
                <div class="text-xs text-gray-500">성공 확률: {{ stage.progress }}%</div>
              </div>
            </div>
          </div>
        </div>

        <!-- 영업 성과 -->
        <div class="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <div class="flex items-center justify-between mb-6">
            <h3 class="text-lg font-semibold text-gray-900">영업 담당자 성과</h3>
            <button 
              @click="editPerformance = !editPerformance" 
              class="px-3 py-1.5 text-sm bg-blue-600 text-white rounded-md hover:bg-blue-700"
            >
              {{ editPerformance ? '저장' : '수정' }}
            </button>
          </div>
          
          <div class="space-y-3">
            <div v-for="rep in salesReps" :key="rep.id" class="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
              <div class="flex items-center space-x-3">
                <div class="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center">
                  <span class="text-green-600 font-medium text-sm">{{ rep.name.charAt(0) }}</span>
                </div>
                <div>
                  <div class="font-medium text-gray-900" :contenteditable="editPerformance">{{ rep.name }}</div>
                  <div class="text-sm text-gray-500" :contenteditable="editPerformance">{{ rep.position }}</div>
                </div>
              </div>
              <div class="text-right">
                <div class="font-medium text-gray-900" :contenteditable="editPerformance">{{ rep.sales }}</div>
                <div class="text-sm" :class="rep.target >= 100 ? 'text-green-500' : 'text-orange-500'" :contenteditable="editPerformance">
                  목표 {{ rep.target }}%
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- AI 영업 분석 -->
      <div class="mt-8 bg-gradient-to-r from-green-50 to-blue-50 p-6 rounded-lg border border-green-200">
        <div class="flex items-start space-x-3">
          <div class="p-2 bg-green-100 rounded-lg">
            <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
          </div>
          <div class="flex-1">
            <h4 class="font-semibold text-gray-900 mb-2">AI 영업 인사이트</h4>
            <div class="space-y-2 text-sm text-gray-700" :contenteditable="editMode">
              <p>• (주)테크솔루션과의 거래가 80% 성공 확률로 예측됩니다. 적극적 접촉을 권장합니다</p>
              <p>• IT 업계 고객들의 Q4 구매 패턴이 증가하고 있습니다. 마케팅 집중이 필요합니다</p>
              <p>• 김영업의 성과가 목표 대비 120% 달성 중입니다. 베스트 프랙티스 공유를 고려하세요</p>
              <p>• 제조업 세그먼트에서 평균 거래 주기가 15% 단축되었습니다</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- AI 어시스턴트 -->
    <AIAssistant context="영업 관리" />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import AIAssistant from '@/components/AIAssistant.vue'

// 편집 모드 상태
const editMode = ref(false)
const editOrders = ref(false)
const editCustomers = ref(false)
const editPipeline = ref(false)
const editPerformance = ref(false)

// 최근 주문 데이터
const recentOrders = ref([
  {
    id: 1,
    customer: '(주)테크솔루션',
    orderNo: 'SO-2024-001',
    date: '2024-01-15',
    product: 'ERP 시스템 라이선스',
    amount: '₩25,000,000',
    status: '확정',
    statusClass: 'bg-green-100 text-green-800'
  },
  {
    id: 2,
    customer: '스마트팩토리',
    orderNo: 'SO-2024-002',
    date: '2024-01-14',
    product: '제조관리 모듈',
    amount: '₩15,500,000',
    status: '진행중',
    statusClass: 'bg-blue-100 text-blue-800'
  },
  {
    id: 3,
    customer: '글로벌커머스',
    orderNo: 'SO-2024-003',
    date: '2024-01-12',
    product: '회계시스템',
    amount: '₩8,200,000',
    status: '검토중',
    statusClass: 'bg-yellow-100 text-yellow-800'
  }
])

// 주요 고객 데이터
const topCustomers = ref([
  {
    id: 1,
    name: '(주)테크솔루션',
    industry: 'IT서비스',
    revenue: '₩125M',
    orders: 15
  },
  {
    id: 2,
    name: '스마트팩토리',
    industry: '제조업',
    revenue: '₩98M',
    orders: 12
  },
  {
    id: 3,
    name: '글로벌커머스',
    industry: '유통업',
    revenue: '₩85M',
    orders: 8
  },
  {
    id: 4,
    name: '디지털이노베이션',
    industry: 'IT서비스',
    revenue: '₩72M',
    orders: 10
  }
])

// 영업 파이프라인 데이터
const pipelineStages = ref([
  {
    id: 1,
    name: '신규 리드',
    count: 24,
    revenue: '₩480M',
    progress: 15
  },
  {
    id: 2,
    name: '제안서 제출',
    count: 12,
    revenue: '₩360M',
    progress: 45
  },
  {
    id: 3,
    name: '협상 중',
    count: 8,
    revenue: '₩240M',
    progress: 70
  },
  {
    id: 4,
    name: '계약 검토',
    count: 5,
    revenue: '₩150M',
    progress: 85
  }
])

// 영업 담당자 성과 데이터
const salesReps = ref([
  {
    id: 1,
    name: '김영업',
    position: '수석 영업',
    sales: '₩185M',
    target: 120
  },
  {
    id: 2,
    name: '박세일즈',
    position: '선임 영업',
    sales: '₩142M',
    target: 95
  },
  {
    id: 3,
    name: '이마케팅',
    position: '영업 대리',
    sales: '₩98M',
    target: 88
  },
  {
    id: 4,
    name: '최비즈니스',
    position: '영업 사원',
    sales: '₩76M',
    target: 105
  }
])
</script>