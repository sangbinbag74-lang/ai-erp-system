<template>
  <div class="assets min-h-screen bg-white">
    <!-- 헤더 -->
    <div class="bg-white border-b border-gray-200 p-6">
      <h1 class="text-3xl font-bold text-gray-900 mb-2">자산 관리</h1>
      <p class="text-gray-600">고정자산, 감가상각 및 자산 추적 관리</p>
    </div>

    <!-- 메인 콘텐츠 -->
    <div class="p-6">
      <!-- 통계 카드 -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div class="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm font-medium text-gray-500">총 자산 가치</p>
              <p class="text-2xl font-bold text-gray-900">₩2.4B</p>
            </div>
            <div class="p-3 bg-green-50 rounded-full">
              <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
              </svg>
            </div>
          </div>
          <div class="mt-4 flex items-center text-sm">
            <span class="text-green-500 font-medium">+5.2%</span>
            <span class="text-gray-500 ml-2">전년 대비</span>
          </div>
        </div>

        <div class="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm font-medium text-gray-500">활성 자산</p>
              <p class="text-2xl font-bold text-gray-900">1,247</p>
            </div>
            <div class="p-3 bg-blue-50 rounded-full">
              <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
              </svg>
            </div>
          </div>
          <div class="mt-4 flex items-center text-sm">
            <span class="text-blue-500 font-medium">23개</span>
            <span class="text-gray-500 ml-2">신규 등록</span>
          </div>
        </div>

        <div class="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm font-medium text-gray-500">월 감가상각</p>
              <p class="text-2xl font-bold text-gray-900">₩45M</p>
            </div>
            <div class="p-3 bg-orange-50 rounded-full">
              <svg class="w-6 h-6 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 17h8m0 0V9m0 8l-8-8-4 4-6-6" />
              </svg>
            </div>
          </div>
          <div class="mt-4 flex items-center text-sm">
            <span class="text-orange-500 font-medium">₩2.1M</span>
            <span class="text-gray-500 ml-2">전월 대비</span>
          </div>
        </div>

        <div class="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm font-medium text-gray-500">유지보수 예정</p>
              <p class="text-2xl font-bold text-gray-900">38</p>
            </div>
            <div class="p-3 bg-purple-50 rounded-full">
              <svg class="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
            </div>
          </div>
          <div class="mt-4 flex items-center text-sm">
            <span class="text-purple-500 font-medium">7일 이내</span>
            <span class="text-gray-500 ml-2">긴급</span>
          </div>
        </div>
      </div>

      <!-- 메인 콘텐츠 그리드 -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <!-- 자산 목록 -->
        <div class="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <div class="flex items-center justify-between mb-6">
            <h3 class="text-lg font-semibold text-gray-900">자산 목록</h3>
            <div class="flex space-x-2">
              <button class="px-3 py-1.5 text-sm bg-blue-600 text-white rounded-md hover:bg-blue-700" @click="editAssets = !editAssets">
                {{ editAssets ? '저장' : '수정' }}
              </button>
              <button class="px-3 py-1.5 text-sm bg-gray-100 text-gray-700 rounded-md hover:bg-gray-200">
                새 자산
              </button>
            </div>
          </div>
          
          <div class="space-y-4">
            <div v-for="asset in assetList" :key="asset.id" class="p-4 bg-gray-50 rounded-lg">
              <div class="flex items-center justify-between mb-2">
                <h4 class="font-medium text-gray-900" :contenteditable="editAssets">{{ asset.name }}</h4>
                <span class="px-2 py-1 text-xs font-medium rounded-full" :class="asset.statusClass">
                  {{ asset.status }}
                </span>
              </div>
              <div class="grid grid-cols-2 gap-4 text-sm">
                <div>
                  <span class="text-gray-500">카테고리:</span>
                  <span class="ml-1 text-gray-900" :contenteditable="editAssets">{{ asset.category }}</span>
                </div>
                <div>
                  <span class="text-gray-500">구매가:</span>
                  <span class="ml-1 text-gray-900" :contenteditable="editAssets">{{ asset.purchaseValue }}</span>
                </div>
                <div>
                  <span class="text-gray-500">현재가치:</span>
                  <span class="ml-1 text-gray-900" :contenteditable="editAssets">{{ asset.currentValue }}</span>
                </div>
                <div>
                  <span class="text-gray-500">구매일:</span>
                  <span class="ml-1 text-gray-900" :contenteditable="editAssets">{{ asset.purchaseDate }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 감가상각 현황 -->
        <div class="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <div class="flex items-center justify-between mb-6">
            <h3 class="text-lg font-semibold text-gray-900">감가상각 현황</h3>
            <button class="px-3 py-1.5 text-sm bg-blue-600 text-white rounded-md hover:bg-blue-700" @click="editDepreciation = !editDepreciation">
              {{ editDepreciation ? '저장' : '수정' }}
            </button>
          </div>
          
          <div class="space-y-4">
            <div v-for="item in depreciationList" :key="item.id" class="p-4 bg-gray-50 rounded-lg">
              <div class="flex items-center justify-between mb-3">
                <h4 class="font-medium text-gray-900" :contenteditable="editDepreciation">{{ item.asset }}</h4>
                <span class="text-sm text-gray-500" :contenteditable="editDepreciation">{{ item.method }}</span>
              </div>
              <div class="space-y-2">
                <div class="flex justify-between text-sm">
                  <span class="text-gray-500">월 상각액:</span>
                  <span class="text-gray-900" :contenteditable="editDepreciation">{{ item.monthlyAmount }}</span>
                </div>
                <div class="flex justify-between text-sm">
                  <span class="text-gray-500">누적 상각:</span>
                  <span class="text-gray-900" :contenteditable="editDepreciation">{{ item.accumulated }}</span>
                </div>
                <div class="flex justify-between text-sm">
                  <span class="text-gray-500">잔존가치:</span>
                  <span class="text-gray-900" :contenteditable="editDepreciation">{{ item.residualValue }}</span>
                </div>
                <div class="w-full bg-gray-200 rounded-full h-2">
                  <div class="bg-orange-500 h-2 rounded-full" :style="{ width: item.progress + '%' }"></div>
                </div>
                <div class="text-xs text-gray-500">{{ item.progress }}% 상각됨</div>
              </div>
            </div>
          </div>
        </div>

        <!-- 유지보수 일정 -->
        <div class="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <div class="flex items-center justify-between mb-6">
            <h3 class="text-lg font-semibold text-gray-900">유지보수 일정</h3>
            <div class="flex space-x-2">
              <button class="px-3 py-1.5 text-sm bg-blue-600 text-white rounded-md hover:bg-blue-700" @click="editMaintenance = !editMaintenance">
                {{ editMaintenance ? '저장' : '수정' }}
              </button>
              <button class="px-3 py-1.5 text-sm bg-gray-100 text-gray-700 rounded-md hover:bg-gray-200">
                일정 추가
              </button>
            </div>
          </div>
          
          <div class="space-y-3">
            <div v-for="maintenance in maintenanceSchedule" :key="maintenance.id" class="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
              <div class="flex-1">
                <div class="font-medium text-gray-900" :contenteditable="editMaintenance">{{ maintenance.asset }}</div>
                <div class="text-sm text-gray-600" :contenteditable="editMaintenance">{{ maintenance.type }}</div>
                <div class="text-sm text-gray-500" :contenteditable="editMaintenance">담당: {{ maintenance.assignee }}</div>
              </div>
              <div class="text-right">
                <div class="text-sm font-medium text-gray-900" :contenteditable="editMaintenance">{{ maintenance.date }}</div>
                <span class="px-2 py-1 text-xs font-medium rounded-full" :class="maintenance.priorityClass">
                  {{ maintenance.priority }}
                </span>
              </div>
            </div>
          </div>
        </div>

        <!-- 자산 위치 추적 -->
        <div class="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <div class="flex items-center justify-between mb-6">
            <h3 class="text-lg font-semibold text-gray-900">자산 위치 추적</h3>
            <button class="px-3 py-1.5 text-sm bg-blue-600 text-white rounded-md hover:bg-blue-700" @click="editLocation = !editLocation">
              {{ editLocation ? '저장' : '수정' }}
            </button>
          </div>
          
          <div class="space-y-4">
            <div v-for="location in assetLocations" :key="location.id" class="p-4 bg-gray-50 rounded-lg">
              <div class="flex items-center justify-between mb-2">
                <h4 class="font-medium text-gray-900" :contenteditable="editLocation">{{ location.asset }}</h4>
                <span class="px-2 py-1 text-xs font-medium bg-blue-100 text-blue-800 rounded-full">
                  {{ location.building }}
                </span>
              </div>
              <div class="text-sm text-gray-600 mb-1" :contenteditable="editLocation">위치: {{ location.room }}</div>
              <div class="text-sm text-gray-600 mb-2" :contenteditable="editLocation">담당자: {{ location.custodian }}</div>
              <div class="text-sm text-gray-500" :contenteditable="editLocation">최근 확인: {{ location.lastVerified }}</div>
            </div>
          </div>
        </div>
      </div>

      <!-- AI 분석 및 권장사항 -->
      <div class="mt-8 bg-gradient-to-r from-purple-50 to-pink-50 p-6 rounded-lg border border-purple-200">
        <div class="flex items-start space-x-3">
          <div class="p-2 bg-purple-100 rounded-lg">
            <svg class="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
          </div>
          <div class="flex-1">
            <h4 class="font-semibold text-gray-900 mb-2">AI 자산 분석</h4>
            <div class="space-y-2 text-sm text-gray-700" :contenteditable="editAssets">
              <p>• 생산라인 A의 장비들이 예상보다 빠르게 감가상각되고 있습니다. 교체 계획을 검토하세요</p>
              <p>• IT 장비 중 3년 이상 된 자산들의 유지보수 비용이 증가하고 있습니다</p>
              <p>• 사무용 가구의 활용률이 낮은 층이 있습니다. 재배치를 고려해보세요</p>
              <p>• 예방적 유지보수를 통해 연간 ₩15M의 비용을 절약할 수 있습니다</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const editAssets = ref(false)
const editDepreciation = ref(false)
const editMaintenance = ref(false)
const editLocation = ref(false)

const assetList = ref([
  {
    id: 1,
    name: '생산라인 A - CNC 기계',
    category: '제조장비',
    purchaseValue: '₩850M',
    currentValue: '₩680M',
    purchaseDate: '2020-03-15',
    status: '활성',
    statusClass: 'bg-green-100 text-green-800'
  },
  {
    id: 2,
    name: '사무용 컴퓨터 (20대)',
    category: 'IT장비',
    purchaseValue: '₩40M',
    currentValue: '₩24M',
    purchaseDate: '2022-01-10',
    status: '활성',
    statusClass: 'bg-green-100 text-green-800'
  },
  {
    id: 3,
    name: '배송 트럭 (3대)',
    category: '차량',
    purchaseValue: '₩180M',
    currentValue: '₩135M',
    purchaseDate: '2021-08-20',
    status: '활성',
    statusClass: 'bg-green-100 text-green-800'
  },
  {
    id: 4,
    name: '냉장 보관 시설',
    category: '건물/시설',
    purchaseValue: '₩120M',
    currentValue: '₩100M',
    purchaseDate: '2019-11-05',
    status: '유지보수',
    statusClass: 'bg-yellow-100 text-yellow-800'
  }
])

const depreciationList = ref([
  {
    id: 1,
    asset: 'CNC 기계',
    method: '정액법',
    monthlyAmount: '₩2.1M',
    accumulated: '₹170M',
    residualValue: '₩680M',
    progress: 20
  },
  {
    id: 2,
    asset: '사무용 컴퓨터',
    method: '가속상각',
    monthlyAmount: '₩800K',
    accumulated: '₩16M',
    residualValue: '₩24M',
    progress: 40
  },
  {
    id: 3,
    asset: '배송 트럭',
    method: '정액법',
    monthlyAmount: '₩1.9M',
    accumulated: '₩45M',
    residualValue: '₩135M',
    progress: 25
  }
])

const maintenanceSchedule = ref([
  {
    id: 1,
    asset: 'CNC 기계 #001',
    type: '정기점검',
    date: '2024-01-20',
    assignee: '김기술',
    priority: '높음',
    priorityClass: 'bg-red-100 text-red-800'
  },
  {
    id: 2,
    asset: '배송 트럭 #002',
    type: '오일 교환',
    date: '2024-01-25',
    assignee: '박정비',
    priority: '보통',
    priorityClass: 'bg-yellow-100 text-yellow-800'
  },
  {
    id: 3,
    asset: '냉장 보관 시설',
    type: '냉각 시스템 점검',
    date: '2024-01-18',
    assignee: '이냉동',
    priority: '긴급',
    priorityClass: 'bg-red-100 text-red-800'
  }
])

const assetLocations = ref([
  {
    id: 1,
    asset: 'CNC 기계 #001',
    building: '공장동',
    room: '1층 생산라인 A',
    custodian: '김생산',
    lastVerified: '2024-01-10'
  },
  {
    id: 2,
    asset: '서버 랙',
    building: '본사',
    room: '지하 1층 서버실',
    custodian: 'IT팀',
    lastVerified: '2024-01-12'
  },
  {
    id: 3,
    asset: '회의실 프로젝터',
    building: '본사',
    room: '3층 대회의실',
    custodian: '총무팀',
    lastVerified: '2024-01-08'
  }
])
</script>