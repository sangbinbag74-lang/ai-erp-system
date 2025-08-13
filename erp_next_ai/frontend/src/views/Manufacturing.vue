<template>
  <div class="manufacturing min-h-screen bg-white">
    <!-- 헤더 -->
    <div class="bg-white border-b border-gray-200 p-6">
      <h1 class="text-3xl font-bold text-gray-900 mb-2">제조</h1>
      <p class="text-gray-600">생산 계획 및 제조 프로세스 관리</p>
    </div>

    <!-- 메인 콘텐츠 -->
    <div class="p-6">
      <!-- 통계 카드 -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div class="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm font-medium text-gray-500">총 생산량</p>
              <p class="text-2xl font-bold text-gray-900">12,450</p>
            </div>
            <div class="p-3 bg-blue-50 rounded-full">
              <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 7.172V5l-1-1z" />
              </svg>
            </div>
          </div>
          <div class="mt-4 flex items-center text-sm">
            <span class="text-green-500 font-medium">+8.3%</span>
            <span class="text-gray-500 ml-2">전월 대비</span>
          </div>
        </div>

        <div class="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm font-medium text-gray-500">진행 중인 작업</p>
              <p class="text-2xl font-bold text-gray-900">42</p>
            </div>
            <div class="p-3 bg-orange-50 rounded-full">
              <svg class="w-6 h-6 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
          </div>
          <div class="mt-4 flex items-center text-sm">
            <span class="text-blue-500 font-medium">5개</span>
            <span class="text-gray-500 ml-2">새로운 작업</span>
          </div>
        </div>

        <div class="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm font-medium text-gray-500">완료율</p>
              <p class="text-2xl font-bold text-gray-900">94.5%</p>
            </div>
            <div class="p-3 bg-green-50 rounded-full">
              <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
          </div>
          <div class="mt-4 flex items-center text-sm">
            <span class="text-green-500 font-medium">+2.1%</span>
            <span class="text-gray-500 ml-2">개선됨</span>
          </div>
        </div>

        <div class="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm font-medium text-gray-500">불량률</p>
              <p class="text-2xl font-bold text-gray-900">2.3%</p>
            </div>
            <div class="p-3 bg-red-50 rounded-full">
              <svg class="w-6 h-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
          </div>
          <div class="mt-4 flex items-center text-sm">
            <span class="text-red-500 font-medium">-0.5%</span>
            <span class="text-gray-500 ml-2">감소</span>
          </div>
        </div>
      </div>

      <!-- 메인 콘텐츠 그리드 -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <!-- 생산 계획 -->
        <div class="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <div class="flex items-center justify-between mb-6">
            <h3 class="text-lg font-semibold text-gray-900">생산 계획</h3>
            <div class="flex space-x-2">
              <button class="px-3 py-1.5 text-sm bg-blue-600 text-white rounded-md hover:bg-blue-700" @click="editMode = !editMode">
                {{ editMode ? '저장' : '수정' }}
              </button>
              <button class="px-3 py-1.5 text-sm bg-gray-100 text-gray-700 rounded-md hover:bg-gray-200">
                새 계획
              </button>
            </div>
          </div>
          
          <div class="space-y-4">
            <div v-for="plan in productionPlans" :key="plan.id" class="p-4 bg-gray-50 rounded-lg">
              <div class="flex items-center justify-between mb-2">
                <h4 class="font-medium text-gray-900" :contenteditable="editMode">{{ plan.product }}</h4>
                <span class="px-2 py-1 text-xs font-medium bg-blue-100 text-blue-800 rounded-full">{{ plan.status }}</span>
              </div>
              <div class="text-sm text-gray-600 mb-2" :contenteditable="editMode">목표량: {{ plan.target }}개</div>
              <div class="text-sm text-gray-600 mb-3" :contenteditable="editMode">예상 완료: {{ plan.dueDate }}</div>
              <div class="w-full bg-gray-200 rounded-full h-2">
                <div class="bg-blue-600 h-2 rounded-full" :style="{ width: plan.progress + '%' }"></div>
              </div>
              <div class="text-xs text-gray-500 mt-1">{{ plan.progress }}% 완료</div>
            </div>
          </div>
        </div>

        <!-- 작업 현황 -->
        <div class="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <div class="flex items-center justify-between mb-6">
            <h3 class="text-lg font-semibold text-gray-900">작업 현황</h3>
            <div class="flex space-x-2">
              <button class="px-3 py-1.5 text-sm bg-blue-600 text-white rounded-md hover:bg-blue-700" @click="editWorkOrders = !editWorkOrders">
                {{ editWorkOrders ? '저장' : '수정' }}
              </button>
              <button class="px-3 py-1.5 text-sm bg-gray-100 text-gray-700 rounded-md hover:bg-gray-200">
                새 작업
              </button>
            </div>
          </div>
          
          <div class="space-y-3">
            <div v-for="order in workOrders" :key="order.id" class="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
              <div class="flex-1">
                <div class="font-medium text-gray-900" :contenteditable="editWorkOrders">{{ order.number }}</div>
                <div class="text-sm text-gray-600" :contenteditable="editWorkOrders">{{ order.product }}</div>
                <div class="text-sm text-gray-500" :contenteditable="editWorkOrders">라인: {{ order.line }}</div>
              </div>
              <div class="text-right">
                <span class="px-2 py-1 text-xs font-medium rounded-full" :class="order.statusClass">
                  {{ order.status }}
                </span>
                <div class="text-sm text-gray-500 mt-1" :contenteditable="editWorkOrders">{{ order.quantity }}</div>
              </div>
            </div>
          </div>
        </div>

        <!-- 자재 소비 -->
        <div class="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <div class="flex items-center justify-between mb-6">
            <h3 class="text-lg font-semibold text-gray-900">자재 소비</h3>
            <button class="px-3 py-1.5 text-sm bg-blue-600 text-white rounded-md hover:bg-blue-700" @click="editMaterials = !editMaterials">
              {{ editMaterials ? '저장' : '수정' }}
            </button>
          </div>
          
          <div class="space-y-4">
            <div v-for="material in materials" :key="material.id" class="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
              <div class="flex-1">
                <div class="font-medium text-gray-900" :contenteditable="editMaterials">{{ material.name }}</div>
                <div class="text-sm text-gray-600" :contenteditable="editMaterials">코드: {{ material.code }}</div>
              </div>
              <div class="text-right">
                <div class="font-medium text-gray-900" :contenteditable="editMaterials">{{ material.consumed }}</div>
                <div class="text-sm text-gray-500">소비량</div>
              </div>
            </div>
          </div>
        </div>

        <!-- 품질 관리 -->
        <div class="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <div class="flex items-center justify-between mb-6">
            <h3 class="text-lg font-semibold text-gray-900">품질 관리</h3>
            <button class="px-3 py-1.5 text-sm bg-blue-600 text-white rounded-md hover:bg-blue-700" @click="editQuality = !editQuality">
              {{ editQuality ? '저장' : '수정' }}
            </button>
          </div>
          
          <div class="space-y-4">
            <div v-for="check in qualityChecks" :key="check.id" class="p-3 bg-gray-50 rounded-lg">
              <div class="flex items-center justify-between mb-2">
                <div class="font-medium text-gray-900" :contenteditable="editQuality">{{ check.item }}</div>
                <span class="px-2 py-1 text-xs font-medium rounded-full" :class="check.resultClass">
                  {{ check.result }}
                </span>
              </div>
              <div class="text-sm text-gray-600" :contenteditable="editQuality">검사자: {{ check.inspector }}</div>
              <div class="text-sm text-gray-500" :contenteditable="editQuality">{{ check.date }}</div>
            </div>
          </div>
        </div>
      </div>

      <!-- AI 추천 -->
      <div class="mt-8 bg-gradient-to-r from-blue-50 to-purple-50 p-6 rounded-lg border border-blue-200">
        <div class="flex items-start space-x-3">
          <div class="p-2 bg-blue-100 rounded-lg">
            <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
            </svg>
          </div>
          <div class="flex-1">
            <h4 class="font-semibold text-gray-900 mb-2">AI 최적화 제안</h4>
            <div class="space-y-2 text-sm text-gray-700" :contenteditable="editMode">
              <p>• 라인 B의 생산 효율성을 15% 개선할 수 있는 스케줄 조정을 제안합니다</p>
              <p>• 자재 A-001의 재고가 부족합니다. 3일 내 보충이 필요합니다</p>
              <p>• 품질 검사 주기를 조정하여 불량률을 1.2%까지 낮출 수 있습니다</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const editMode = ref(false)
const editWorkOrders = ref(false)
const editMaterials = ref(false)
const editQuality = ref(false)

const productionPlans = ref([
  {
    id: 1,
    product: '스마트폰 케이스',
    target: 1000,
    progress: 75,
    status: '진행중',
    dueDate: '2024-01-25'
  },
  {
    id: 2,
    product: 'USB 케이블',
    target: 5000,
    progress: 45,
    status: '진행중',
    dueDate: '2024-01-30'
  },
  {
    id: 3,
    product: '무선 충전기',
    target: 500,
    progress: 90,
    status: '완료 예정',
    dueDate: '2024-01-20'
  }
])

const workOrders = ref([
  {
    id: 1,
    number: 'WO-2024-001',
    product: '스마트폰 케이스',
    line: 'Line A',
    status: '진행중',
    statusClass: 'bg-yellow-100 text-yellow-800',
    quantity: '750/1000'
  },
  {
    id: 2,
    number: 'WO-2024-002',
    product: 'USB 케이블',
    line: 'Line B',
    status: '대기',
    statusClass: 'bg-gray-100 text-gray-800',
    quantity: '0/5000'
  },
  {
    id: 3,
    number: 'WO-2024-003',
    product: '무선 충전기',
    line: 'Line C',
    status: '완료',
    statusClass: 'bg-green-100 text-green-800',
    quantity: '450/500'
  }
])

const materials = ref([
  {
    id: 1,
    name: '플라스틱 원료 A',
    code: 'MAT-001',
    consumed: '450kg'
  },
  {
    id: 2,
    name: '구리선',
    code: 'MAT-002',
    consumed: '2.3km'
  },
  {
    id: 3,
    name: '코일',
    code: 'MAT-003',
    consumed: '120개'
  }
])

const qualityChecks = ref([
  {
    id: 1,
    item: '스마트폰 케이스 배치 #001',
    result: '합격',
    resultClass: 'bg-green-100 text-green-800',
    inspector: '김품질',
    date: '2024-01-15 14:30'
  },
  {
    id: 2,
    item: 'USB 케이블 배치 #002',
    result: '재검사',
    resultClass: 'bg-yellow-100 text-yellow-800',
    inspector: '박검사',
    date: '2024-01-15 10:15'
  },
  {
    id: 3,
    item: '무선 충전기 배치 #003',
    result: '합격',
    resultClass: 'bg-green-100 text-green-800',
    inspector: '이테스트',
    date: '2024-01-14 16:45'
  }
])
</script>