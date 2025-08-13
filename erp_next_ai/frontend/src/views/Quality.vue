<template>
  <div class="quality min-h-screen bg-white">
    <!-- 헤더 -->
    <div class="bg-white border-b border-gray-200 p-6">
      <h1 class="text-3xl font-bold text-gray-900 mb-2">품질 관리</h1>
      <p class="text-gray-600">품질 검사, 기준 관리 및 품질 보증 시스템</p>
    </div>

    <!-- 메인 콘텐츠 -->
    <div class="p-6">
      <!-- 통계 카드 -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div class="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm font-medium text-gray-500">품질 지수</p>
              <p class="text-2xl font-bold text-gray-900">97.8%</p>
            </div>
            <div class="p-3 bg-green-50 rounded-full">
              <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
          </div>
          <div class="mt-4 flex items-center text-sm">
            <span class="text-green-500 font-medium">+1.2%</span>
            <span class="text-gray-500 ml-2">전월 대비</span>
          </div>
        </div>

        <div class="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm font-medium text-gray-500">불량률</p>
              <p class="text-2xl font-bold text-gray-900">2.2%</p>
            </div>
            <div class="p-3 bg-red-50 rounded-full">
              <svg class="w-6 h-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
          </div>
          <div class="mt-4 flex items-center text-sm">
            <span class="text-green-500 font-medium">-0.3%</span>
            <span class="text-gray-500 ml-2">개선됨</span>
          </div>
        </div>

        <div class="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm font-medium text-gray-500">검사 완료</p>
              <p class="text-2xl font-bold text-gray-900">1,247</p>
            </div>
            <div class="p-3 bg-blue-50 rounded-full">
              <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" />
              </svg>
            </div>
          </div>
          <div class="mt-4 flex items-center text-sm">
            <span class="text-blue-500 font-medium">87건</span>
            <span class="text-gray-500 ml-2">오늘</span>
          </div>
        </div>

        <div class="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm font-medium text-gray-500">재검사</p>
              <p class="text-2xl font-bold text-gray-900">23</p>
            </div>
            <div class="p-3 bg-yellow-50 rounded-full">
              <svg class="w-6 h-6 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
              </svg>
            </div>
          </div>
          <div class="mt-4 flex items-center text-sm">
            <span class="text-yellow-500 font-medium">-12건</span>
            <span class="text-gray-500 ml-2">감소</span>
          </div>
        </div>
      </div>

      <!-- 메인 콘텐츠 그리드 -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <!-- 검사 현황 -->
        <div class="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <div class="flex items-center justify-between mb-6">
            <h3 class="text-lg font-semibold text-gray-900">검사 현황</h3>
            <div class="flex space-x-2">
              <button class="px-3 py-1.5 text-sm bg-blue-600 text-white rounded-md hover:bg-blue-700" @click="editInspections = !editInspections">
                {{ editInspections ? '저장' : '수정' }}
              </button>
              <button class="px-3 py-1.5 text-sm bg-gray-100 text-gray-700 rounded-md hover:bg-gray-200">
                새 검사
              </button>
            </div>
          </div>
          
          <div class="space-y-4">
            <div v-for="inspection in inspectionList" :key="inspection.id" class="p-4 bg-gray-50 rounded-lg">
              <div class="flex items-center justify-between mb-2">
                <h4 class="font-medium text-gray-900" :contenteditable="editInspections">{{ inspection.product }}</h4>
                <span class="px-2 py-1 text-xs font-medium rounded-full" :class="inspection.statusClass">
                  {{ inspection.status }}
                </span>
              </div>
              <div class="grid grid-cols-2 gap-4 text-sm">
                <div>
                  <span class="text-gray-500">배치번호:</span>
                  <span class="ml-1 text-gray-900" :contenteditable="editInspections">{{ inspection.batchNo }}</span>
                </div>
                <div>
                  <span class="text-gray-500">검사자:</span>
                  <span class="ml-1 text-gray-900" :contenteditable="editInspections">{{ inspection.inspector }}</span>
                </div>
                <div>
                  <span class="text-gray-500">수량:</span>
                  <span class="ml-1 text-gray-900" :contenteditable="editInspections">{{ inspection.quantity }}</span>
                </div>
                <div>
                  <span class="text-gray-500">검사일:</span>
                  <span class="ml-1 text-gray-900" :contenteditable="editInspections">{{ inspection.date }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 품질 기준 -->
        <div class="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <div class="flex items-center justify-between mb-6">
            <h3 class="text-lg font-semibold text-gray-900">품질 기준</h3>
            <div class="flex space-x-2">
              <button class="px-3 py-1.5 text-sm bg-blue-600 text-white rounded-md hover:bg-blue-700" @click="editStandards = !editStandards">
                {{ editStandards ? '저장' : '수정' }}
              </button>
              <button class="px-3 py-1.5 text-sm bg-gray-100 text-gray-700 rounded-md hover:bg-gray-200">
                기준 추가
              </button>
            </div>
          </div>
          
          <div class="space-y-4">
            <div v-for="standard in qualityStandards" :key="standard.id" class="p-4 bg-gray-50 rounded-lg">
              <div class="flex items-center justify-between mb-3">
                <h4 class="font-medium text-gray-900" :contenteditable="editStandards">{{ standard.name }}</h4>
                <span class="px-2 py-1 text-xs font-medium bg-blue-100 text-blue-800 rounded-full">
                  {{ standard.category }}
                </span>
              </div>
              <div class="space-y-2 text-sm">
                <div class="flex justify-between">
                  <span class="text-gray-500">기준값:</span>
                  <span class="text-gray-900" :contenteditable="editStandards">{{ standard.targetValue }}</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-gray-500">허용 범위:</span>
                  <span class="text-gray-900" :contenteditable="editStandards">{{ standard.tolerance }}</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-gray-500">측정 방법:</span>
                  <span class="text-gray-900" :contenteditable="editStandards">{{ standard.method }}</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-gray-500">검사 빈도:</span>
                  <span class="text-gray-900" :contenteditable="editStandards">{{ standard.frequency }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 불량 분석 -->
        <div class="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <div class="flex items-center justify-between mb-6">
            <h3 class="text-lg font-semibold text-gray-900">불량 분석</h3>
            <button class="px-3 py-1.5 text-sm bg-blue-600 text-white rounded-md hover:bg-blue-700" @click="editDefects = !editDefects">
              {{ editDefects ? '저장' : '수정' }}
            </button>
          </div>
          
          <div class="space-y-4">
            <div v-for="defect in defectAnalysis" :key="defect.id" class="p-4 bg-gray-50 rounded-lg">
              <div class="flex items-center justify-between mb-2">
                <h4 class="font-medium text-gray-900" :contenteditable="editDefects">{{ defect.type }}</h4>
                <span class="text-sm font-medium text-red-600">{{ defect.count }}건</span>
              </div>
              <div class="space-y-2">
                <div class="flex justify-between text-sm">
                  <span class="text-gray-500">주요 원인:</span>
                  <span class="text-gray-900" :contenteditable="editDefects">{{ defect.cause }}</span>
                </div>
                <div class="flex justify-between text-sm">
                  <span class="text-gray-500">비용 영향:</span>
                  <span class="text-gray-900" :contenteditable="editDefects">{{ defect.cost }}</span>
                </div>
                <div class="w-full bg-gray-200 rounded-full h-2">
                  <div class="bg-red-500 h-2 rounded-full" :style="{ width: defect.percentage + '%' }"></div>
                </div>
                <div class="text-xs text-gray-500">전체 불량의 {{ defect.percentage }}%</div>
              </div>
            </div>
          </div>
        </div>

        <!-- 개선 조치 -->
        <div class="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <div class="flex items-center justify-between mb-6">
            <h3 class="text-lg font-semibold text-gray-900">개선 조치</h3>
            <div class="flex space-x-2">
              <button class="px-3 py-1.5 text-sm bg-blue-600 text-white rounded-md hover:bg-blue-700" @click="editActions = !editActions">
                {{ editActions ? '저장' : '수정' }}
              </button>
              <button class="px-3 py-1.5 text-sm bg-gray-100 text-gray-700 rounded-md hover:bg-gray-200">
                조치 추가
              </button>
            </div>
          </div>
          
          <div class="space-y-3">
            <div v-for="action in correctiveActions" :key="action.id" class="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
              <div class="flex-1">
                <div class="font-medium text-gray-900" :contenteditable="editActions">{{ action.description }}</div>
                <div class="text-sm text-gray-600" :contenteditable="editActions">담당: {{ action.assignee }}</div>
                <div class="text-sm text-gray-500" :contenteditable="editActions">기한: {{ action.dueDate }}</div>
              </div>
              <div class="text-right">
                <span class="px-2 py-1 text-xs font-medium rounded-full" :class="action.priorityClass">
                  {{ action.priority }}
                </span>
                <div class="text-sm text-gray-500 mt-1">{{ action.progress }}% 완료</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 품질 인증 및 감사 -->
      <div class="mt-8 grid grid-cols-1 lg:grid-cols-2 gap-8">
        <!-- 품질 인증 -->
        <div class="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <div class="flex items-center justify-between mb-6">
            <h3 class="text-lg font-semibold text-gray-900">품질 인증</h3>
            <button class="px-3 py-1.5 text-sm bg-blue-600 text-white rounded-md hover:bg-blue-700" @click="editCertifications = !editCertifications">
              {{ editCertifications ? '저장' : '수정' }}
            </button>
          </div>
          
          <div class="space-y-4">
            <div v-for="cert in certifications" :key="cert.id" class="p-4 bg-gray-50 rounded-lg">
              <div class="flex items-center justify-between mb-2">
                <h4 class="font-medium text-gray-900" :contenteditable="editCertifications">{{ cert.name }}</h4>
                <span class="px-2 py-1 text-xs font-medium rounded-full" :class="cert.statusClass">
                  {{ cert.status }}
                </span>
              </div>
              <div class="text-sm text-gray-600 mb-1" :contenteditable="editCertifications">발급기관: {{ cert.issuer }}</div>
              <div class="text-sm text-gray-600 mb-2" :contenteditable="editCertifications">유효기간: {{ cert.validUntil }}</div>
              <div class="text-sm text-gray-500" :contenteditable="editCertifications">갱신 예정: {{ cert.renewalDue }}</div>
            </div>
          </div>
        </div>

        <!-- 품질 감사 -->
        <div class="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <div class="flex items-center justify-between mb-6">
            <h3 class="text-lg font-semibold text-gray-900">품질 감사</h3>
            <button class="px-3 py-1.5 text-sm bg-blue-600 text-white rounded-md hover:bg-blue-700" @click="editAudits = !editAudits">
              {{ editAudits ? '저장' : '수정' }}
            </button>
          </div>
          
          <div class="space-y-4">
            <div v-for="audit in qualityAudits" :key="audit.id" class="p-4 bg-gray-50 rounded-lg">
              <div class="flex items-center justify-between mb-2">
                <h4 class="font-medium text-gray-900" :contenteditable="editAudits">{{ audit.type }}</h4>
                <span class="text-sm font-medium text-gray-600">{{ audit.score }}점</span>
              </div>
              <div class="text-sm text-gray-600 mb-1" :contenteditable="editAudits">감사자: {{ audit.auditor }}</div>
              <div class="text-sm text-gray-600 mb-2" :contenteditable="editAudits">감사일: {{ audit.date }}</div>
              <div class="text-sm text-gray-500" :contenteditable="editAudits">주요 발견사항: {{ audit.findings }}</div>
            </div>
          </div>
        </div>
      </div>

      <!-- AI 품질 분석 -->
      <div class="mt-8 bg-gradient-to-r from-green-50 to-blue-50 p-6 rounded-lg border border-green-200">
        <div class="flex items-start space-x-3">
          <div class="p-2 bg-green-100 rounded-lg">
            <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 002 2h2a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v14a2 2 0 002 2z" />
            </svg>
          </div>
          <div class="flex-1">
            <h4 class="font-semibold text-gray-900 mb-2">AI 품질 인사이트</h4>
            <div class="space-y-2 text-sm text-gray-700" :contenteditable="editInspections">
              <p>• 생산라인 B에서 오전 시간대 불량률이 높습니다. 장비 예열 시간을 늘려보세요</p>
              <p>• 원자재 공급업체 A의 품질이 최근 3주간 하락 추세입니다</p>
              <p>• 검사 간격을 2시간에서 1.5시간으로 줄이면 불량 조기 발견률을 30% 높일 수 있습니다</p>
              <p>• ISO 9001 갱신을 위해 문서 업데이트가 필요합니다 (90일 남음)</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const editInspections = ref(false)
const editStandards = ref(false)
const editDefects = ref(false)
const editActions = ref(false)
const editCertifications = ref(false)
const editAudits = ref(false)

const inspectionList = ref([
  {
    id: 1,
    product: '스마트폰 케이스',
    batchNo: 'B2024-001',
    inspector: '김검사',
    quantity: '500개',
    date: '2024-01-15',
    status: '합격',
    statusClass: 'bg-green-100 text-green-800'
  },
  {
    id: 2,
    product: 'USB 케이블',
    batchNo: 'B2024-002',
    inspector: '박품질',
    quantity: '1000개',
    date: '2024-01-15',
    status: '재검사',
    statusClass: 'bg-yellow-100 text-yellow-800'
  },
  {
    id: 3,
    product: '무선 충전기',
    batchNo: 'B2024-003',
    inspector: '이테스트',
    quantity: '200개',
    date: '2024-01-14',
    status: '진행중',
    statusClass: 'bg-blue-100 text-blue-800'
  }
])

const qualityStandards = ref([
  {
    id: 1,
    name: '외관 검사',
    category: '시각적',
    targetValue: '무결점',
    tolerance: '±0%',
    method: '육안 검사',
    frequency: '전수 검사'
  },
  {
    id: 2,
    name: '치수 정밀도',
    category: '물리적',
    targetValue: '±0.1mm',
    tolerance: '±0.05mm',
    method: '캘리퍼 측정',
    frequency: '10% 샘플링'
  },
  {
    id: 3,
    name: '전기적 성능',
    category: '전기적',
    targetValue: '5V ±5%',
    tolerance: '±2%',
    method: '멀티미터',
    frequency: '배치당 5개'
  }
])

const defectAnalysis = ref([
  {
    id: 1,
    type: '표면 결함',
    count: 42,
    cause: '금형 마모',
    cost: '₩2.1M',
    percentage: 35
  },
  {
    id: 2,
    type: '치수 불량',
    count: 28,
    cause: '온도 변화',
    cost: '₩1.4M',
    percentage: 23
  },
  {
    id: 3,
    type: '전기적 불량',
    count: 18,
    cause: '소재 불량',
    cost: '₩900K',
    percentage: 15
  }
])

const correctiveActions = ref([
  {
    id: 1,
    description: '금형 교체 및 예방 정비',
    assignee: '김기술',
    dueDate: '2024-01-25',
    priority: '높음',
    priorityClass: 'bg-red-100 text-red-800',
    progress: 60
  },
  {
    id: 2,
    description: '온도 관리 시스템 개선',
    assignee: '박환경',
    dueDate: '2024-01-30',
    priority: '보통',
    priorityClass: 'bg-yellow-100 text-yellow-800',
    progress: 30
  },
  {
    id: 3,
    description: '공급업체 품질 점검',
    assignee: '이구매',
    dueDate: '2024-01-20',
    priority: '높음',
    priorityClass: 'bg-red-100 text-red-800',
    progress: 80
  }
])

const certifications = ref([
  {
    id: 1,
    name: 'ISO 9001:2015',
    issuer: 'KAB 한국인정원',
    validUntil: '2025-03-15',
    renewalDue: '2025-01-15',
    status: '유효',
    statusClass: 'bg-green-100 text-green-800'
  },
  {
    id: 2,
    name: 'ISO 14001:2015',
    issuer: 'KAB 한국인정원',
    validUntil: '2024-08-20',
    renewalDue: '2024-06-20',
    status: '갱신필요',
    statusClass: 'bg-yellow-100 text-yellow-800'
  },
  {
    id: 3,
    name: 'OHSAS 18001',
    issuer: '로이드코리아',
    validUntil: '2024-12-10',
    renewalDue: '2024-10-10',
    status: '유효',
    statusClass: 'bg-green-100 text-green-800'
  }
])

const qualityAudits = ref([
  {
    id: 1,
    type: '내부 감사',
    auditor: '품질팀',
    date: '2024-01-10',
    score: 92,
    findings: '전반적으로 우수, 일부 문서 업데이트 필요'
  },
  {
    id: 2,
    type: '공급업체 감사',
    auditor: '외부 감사원',
    date: '2024-01-05',
    score: 85,
    findings: '품질 관리 체계 강화 권고'
  },
  {
    id: 3,
    type: '고객 감사',
    auditor: 'ABC전자',
    date: '2023-12-20',
    score: 96,
    findings: '품질 수준 매우 만족'
  }
])
</script>