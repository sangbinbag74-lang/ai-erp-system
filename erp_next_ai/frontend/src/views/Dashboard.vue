<template>
  <div class="dashboard">
    <div class="dashboard-header">
      <h1 class="text-2xl font-bold text-gray-900">ERPNext AI 대시보드</h1>
      <p class="text-gray-600">AI 기반 ERP 시스템에 오신 것을 환영합니다</p>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
      <!-- 통계 카드들 -->
      <div class="bg-white p-6 rounded-lg shadow">
        <div class="flex items-center">
          <div class="p-2 bg-blue-100 rounded-lg">
            <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"></path>
            </svg>
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-600">총 고객</p>
            <p class="text-2xl font-semibold text-gray-900">1,234</p>
          </div>
        </div>
      </div>

      <div class="bg-white p-6 rounded-lg shadow">
        <div class="flex items-center">
          <div class="p-2 bg-green-100 rounded-lg">
            <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1"></path>
            </svg>
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-600">이번 달 매출</p>
            <p class="text-2xl font-semibold text-gray-900">₩45.2M</p>
          </div>
        </div>
      </div>

      <div class="bg-white p-6 rounded-lg shadow">
        <div class="flex items-center">
          <div class="p-2 bg-yellow-100 rounded-lg">
            <svg class="w-6 h-6 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10"></path>
            </svg>
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-600">재고 품목</p>
            <p class="text-2xl font-semibold text-gray-900">567</p>
          </div>
        </div>
      </div>

      <div class="bg-white p-6 rounded-lg shadow">
        <div class="flex items-center">
          <div class="p-2 bg-purple-100 rounded-lg">
            <svg class="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
            </svg>
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-600">미처리 주문</p>
            <p class="text-2xl font-semibold text-gray-900">23</p>
          </div>
        </div>
      </div>
    </div>

    <!-- 최근 활동 -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
      <div class="bg-white rounded-lg shadow">
        <div class="p-6 border-b">
          <h2 class="text-lg font-semibold text-gray-900">최근 판매 주문</h2>
        </div>
        <div class="p-6">
          <div class="space-y-4">
            <div class="flex items-center justify-between py-3 border-b border-gray-100">
              <div>
                <p class="font-medium text-gray-900">SO-2024-001</p>
                <p class="text-sm text-gray-600">ABC 주식회사</p>
              </div>
              <div class="text-right">
                <p class="font-medium text-gray-900">₩2,340,000</p>
                <p class="text-sm text-green-600">승인됨</p>
              </div>
            </div>
            <div class="flex items-center justify-between py-3 border-b border-gray-100">
              <div>
                <p class="font-medium text-gray-900">SO-2024-002</p>
                <p class="text-sm text-gray-600">XYZ 코퍼레이션</p>
              </div>
              <div class="text-right">
                <p class="font-medium text-gray-900">₩1,856,000</p>
                <p class="text-sm text-yellow-600">대기중</p>
              </div>
            </div>
            <div class="flex items-center justify-between py-3">
              <div>
                <p class="font-medium text-gray-900">SO-2024-003</p>
                <p class="text-sm text-gray-600">123 기업</p>
              </div>
              <div class="text-right">
                <p class="font-medium text-gray-900">₩945,000</p>
                <p class="text-sm text-blue-600">진행중</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-lg shadow">
        <div class="p-6 border-b">
          <h2 class="text-lg font-semibold text-gray-900">AI 인사이트</h2>
        </div>
        <div class="p-6">
          <div class="space-y-4">
            <div class="p-4 bg-blue-50 rounded-lg">
              <h3 class="font-medium text-blue-900">매출 예측</h3>
              <p class="text-sm text-blue-700 mt-1">다음 달 예상 매출: ₩52.8M (+17% 증가)</p>
            </div>
            <div class="p-4 bg-yellow-50 rounded-lg">
              <h3 class="font-medium text-yellow-900">재고 알림</h3>
              <p class="text-sm text-yellow-700 mt-1">5개 품목이 재주문 수준에 도달했습니다.</p>
            </div>
            <div class="p-4 bg-green-50 rounded-lg">
              <h3 class="font-medium text-green-900">고객 분석</h3>
              <p class="text-sm text-green-700 mt-1">VIP 고객 3명이 신규 주문을 검토 중입니다.</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

// 대시보드 데이터
const stats = ref({
  customers: 1234,
  revenue: 45200000,
  items: 567,
  orders: 23
})

onMounted(() => {
  // 실제 데이터는 API에서 가져와야 함
  console.log('Dashboard mounted')
})
</script>

<style scoped>
.dashboard {
  @apply p-6;
}

.dashboard-header {
  @apply mb-8;
}
</style>