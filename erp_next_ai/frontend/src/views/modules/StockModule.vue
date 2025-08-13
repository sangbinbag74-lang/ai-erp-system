<template>
  <div class="stock-module min-h-screen" style="background: var(--bg-primary); color: var(--text-primary);">
    <!-- 헤더 -->
    <div class="header-section p-6 border-b" style="border-color: var(--border-primary); background: var(--bg-secondary);">
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-3xl font-bold bg-gradient-to-r from-purple-400 to-cyan-400 bg-clip-text text-transparent">
            재고 관리 (Stock Management)
          </h1>
          <p class="text-gray-400 mt-2">AI 기반 재고 예측 및 자동 발주 시스템</p>
        </div>
        <div class="flex items-center space-x-4">
          <div class="agi-status px-4 py-2 rounded-lg" style="background: var(--bg-tertiary); border: 1px solid var(--ai-primary);">
            <span class="text-sm">AGI 상태: </span>
            <span class="text-green-400 font-semibold">{{ agiStatus }}</span>
          </div>
          <button 
            @click="refreshDashboard"
            class="bg-purple-600 hover:bg-purple-700 px-4 py-2 rounded-lg transition-all duration-300 text-white"
            style="box-shadow: var(--glow-primary);"
          >
            새로고침
          </button>
        </div>
      </div>
    </div>

    <!-- AI 명령어 섹션 -->
    <div class="ai-command-section p-6" style="background: var(--bg-secondary); border-bottom: 1px solid var(--border-primary);">
      <div class="max-w-4xl">
        <h3 class="text-lg font-semibold mb-3 text-purple-400">AI 재고 어시스턴트</h3>
        <div class="flex space-x-4">
          <textarea 
            v-model="aiCommand"
            placeholder="재고 관련 자연어 명령을 입력하세요... 예: '부족한 재고 자동 주문해줘', '재고 회전율 분석해줘', '창고별 재고 현황 보여줘'"
            class="flex-1 p-4 rounded-lg resize-none transition-all duration-300"
            style="background: var(--bg-tertiary); border: 1px solid var(--border-secondary); color: var(--text-primary); min-height: 80px;"
            @focus="$event.target.style.borderColor = 'var(--ai-primary)'"
            @blur="$event.target.style.borderColor = 'var(--border-secondary)'"
          ></textarea>
          <div class="flex flex-col space-y-2">
            <button 
              @click="executeAICommand"
              :disabled="!aiCommand.trim()"
              class="bg-gradient-to-r from-purple-500 to-cyan-600 hover:from-purple-600 hover:to-cyan-700 disabled:opacity-50 px-6 py-3 rounded-lg transition-all duration-300 text-white font-medium"
              style="box-shadow: var(--glow-primary);"
            >
              실행
            </button>
            <button 
              @click="clearAICommand"
              class="bg-gray-600 hover:bg-gray-700 px-6 py-3 rounded-lg transition-all duration-300 text-white"
            >
              초기화
            </button>
          </div>
        </div>
        
        <!-- AI 응답 영역 -->
        <div v-if="aiResponse" class="mt-4 p-4 rounded-lg" style="background: var(--bg-tertiary); border: 1px solid var(--ai-accent);">
          <h4 class="font-semibold text-purple-400 mb-2">AI 분석 결과:</h4>
          <div class="whitespace-pre-wrap" style="color: var(--text-secondary);">{{ aiResponse }}</div>
        </div>
      </div>
    </div>

    <!-- 대시보드 카드들 -->
    <div class="dashboard-cards p-6 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      <!-- 총 재고 가치 -->
      <div class="dashboard-card p-6 rounded-xl transition-all duration-300 hover:scale-105" 
           style="background: var(--bg-secondary); border: 1px solid var(--border-secondary);"
           @mouseenter="$event.target.style.boxShadow = 'var(--glow-primary)'"
           @mouseleave="$event.target.style.boxShadow = 'none'">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm font-medium" style="color: var(--text-secondary);">총 재고 가치</p>
            <p class="text-2xl font-bold text-purple-400">{{ formatCurrency(totalStockValue) }}</p>
            <p class="text-xs mt-1" :class="stockValueGrowth >= 0 ? 'text-green-400' : 'text-red-400'">
              {{ stockValueGrowth >= 0 ? '+' : '' }}{{ stockValueGrowth }}% 전월 대비
            </p>
          </div>
          <div class="text-purple-400 text-3xl">📦</div>
        </div>
      </div>

      <!-- 재고 회전율 -->
      <div class="dashboard-card p-6 rounded-xl transition-all duration-300 hover:scale-105" 
           style="background: var(--bg-secondary); border: 1px solid var(--border-secondary);"
           @mouseenter="$event.target.style.boxShadow = 'var(--glow-secondary)'"
           @mouseleave="$event.target.style.boxShadow = 'none'">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm font-medium" style="color: var(--text-secondary);">재고 회전율</p>
            <p class="text-2xl font-bold text-cyan-400">{{ stockTurnoverRate }}x</p>
            <p class="text-xs mt-1 text-green-400">업계 평균 초과</p>
          </div>
          <div class="text-cyan-400 text-3xl">🔄</div>
        </div>
      </div>

      <!-- 창고 수 -->
      <div class="dashboard-card p-6 rounded-xl transition-all duration-300 hover:scale-105" 
           style="background: var(--bg-secondary); border: 1px solid var(--border-secondary);"
           @mouseenter="$event.target.style.boxShadow = 'var(--glow-accent)'"
           @mouseleave="$event.target.style.boxShadow = 'none'">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm font-medium" style="color: var(--text-secondary);">운영 창고</p>
            <p class="text-2xl font-bold text-green-400">{{ totalWarehouses }}</p>
            <p class="text-xs mt-1 text-green-400">{{ warehouseUtilization }}% 평균 가동률</p>
          </div>
          <div class="text-green-400 text-3xl">🏭</div>
        </div>
      </div>

      <!-- 자동 발주 건수 -->
      <div class="dashboard-card p-6 rounded-xl transition-all duration-300 hover:scale-105" 
           style="background: var(--bg-secondary); border: 1px solid var(--border-secondary);"
           @mouseenter="$event.target.style.boxShadow = 'var(--glow-primary)'"
           @mouseleave="$event.target.style.boxShadow = 'none'">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm font-medium" style="color: var(--text-secondary);">AI 자동 발주</p>
            <p class="text-2xl font-bold text-orange-400">{{ autoOrderCount }}</p>
            <p class="text-xs mt-1 text-green-400">{{ autoOrderAccuracy }}% 정확도</p>
          </div>
          <div class="text-orange-400 text-3xl">🤖</div>
        </div>
      </div>
    </div>

    <!-- 메인 콘텐츠 영역 -->
    <div class="main-content p-6 grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- 실시간 재고 현황 -->
      <div class="inventory-status p-6 rounded-xl" style="background: var(--bg-secondary); border: 1px solid var(--border-secondary);">
        <h3 class="text-xl font-semibold mb-4 text-purple-400">실시간 재고 현황</h3>
        <div class="space-y-4">
          <div v-for="category in inventoryCategories" :key="category.name" 
               class="category-item p-4 rounded-lg transition-all duration-300 hover:scale-102"
               style="background: var(--bg-tertiary); border: 1px solid var(--border-primary);">
            <div class="flex items-center justify-between mb-2">
              <h4 class="font-medium text-white">{{ category.name }}</h4>
              <span class="text-sm px-2 py-1 rounded" 
                    :style="`background: ${category.status === 'optimal' ? '#10b981' : category.status === 'low' ? '#f59e0b' : '#ef4444'}20; 
                             color: ${category.status === 'optimal' ? '#10b981' : category.status === 'low' ? '#f59e0b' : '#ef4444'};`">
                {{ category.status === 'optimal' ? '적정' : category.status === 'low' ? '부족' : '과다' }}
              </span>
            </div>
            <div class="grid grid-cols-2 gap-4 text-sm">
              <div>
                <span style="color: var(--text-tertiary);">현재 재고:</span>
                <span class="ml-2 font-medium text-white">{{ category.currentStock.toLocaleString() }}개</span>
              </div>
              <div>
                <span style="color: var(--text-tertiary);">재고 가치:</span>
                <span class="ml-2 font-medium text-green-400">{{ formatCurrency(category.value) }}</span>
              </div>
            </div>
            <div class="mt-2 grid grid-cols-2 gap-4 text-sm">
              <div>
                <span style="color: var(--text-tertiary);">회전율:</span>
                <span class="ml-2 font-medium text-cyan-400">{{ category.turnoverRate }}x</span>
              </div>
              <div>
                <span style="color: var(--text-tertiary);">AI 예측:</span>
                <span class="ml-2 font-medium text-purple-400">{{ category.forecast }}일분</span>
              </div>
            </div>
            <div class="mt-3">
              <div class="w-full h-2 rounded-full" style="background: var(--bg-hover);">
                <div class="h-full rounded-full transition-all duration-500" 
                     :style="`width: ${category.stockLevel}%; background: ${category.status === 'optimal' ? '#10b981' : category.status === 'low' ? '#f59e0b' : '#ef4444'};`">
                </div>
              </div>
              <div class="flex justify-between mt-1 text-xs" style="color: var(--text-tertiary);">
                <span>최소</span>
                <span>적정</span>
                <span>최대</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 창고별 현황 -->
      <div class="warehouse-status p-6 rounded-xl" style="background: var(--bg-secondary); border: 1px solid var(--border-secondary);">
        <h3 class="text-xl font-semibold mb-4 text-cyan-400">창고별 현황</h3>
        <div class="space-y-4">
          <div v-for="warehouse in warehouses" :key="warehouse.id"
               class="warehouse-item p-4 rounded-lg transition-all duration-300 hover:scale-102 cursor-pointer"
               style="background: var(--bg-tertiary); border: 1px solid var(--border-primary);"
               @click="viewWarehouseDetails(warehouse)">
            <div class="flex items-center justify-between mb-2">
              <h4 class="font-medium text-white">{{ warehouse.name }}</h4>
              <div class="flex items-center space-x-2">
                <span class="text-xs px-2 py-1 rounded" 
                      :style="`background: ${warehouse.utilizationRate >= 80 ? '#ef4444' : warehouse.utilizationRate >= 60 ? '#f59e0b' : '#10b981'}20; 
                               color: ${warehouse.utilizationRate >= 80 ? '#ef4444' : warehouse.utilizationRate >= 60 ? '#f59e0b' : '#10b981'};`">
                  {{ warehouse.utilizationRate }}%
                </span>
                <span class="text-xs" style="color: var(--text-tertiary);">
                  {{ warehouse.temperature }}°C
                </span>
              </div>
            </div>
            <div class="grid grid-cols-2 gap-4 text-sm mb-2">
              <div>
                <span style="color: var(--text-tertiary);">총 용량:</span>
                <span class="ml-2 font-medium text-white">{{ warehouse.totalCapacity.toLocaleString() }}㎡</span>
              </div>
              <div>
                <span style="color: var(--text-tertiary);">사용량:</span>
                <span class="ml-2 font-medium text-cyan-400">{{ warehouse.usedCapacity.toLocaleString() }}㎡</span>
              </div>
            </div>
            <div class="grid grid-cols-2 gap-4 text-sm">
              <div>
                <span style="color: var(--text-tertiary);">총 품목:</span>
                <span class="ml-2 font-medium text-purple-400">{{ warehouse.itemCount.toLocaleString() }}개</span>
              </div>
              <div>
                <span style="color: var(--text-tertiary);">AI 효율성:</span>
                <span class="ml-2 font-medium text-green-400">{{ warehouse.aiEfficiency }}%</span>
              </div>
            </div>
            <div class="mt-3 flex items-center justify-between">
              <span class="text-xs" style="color: var(--text-tertiary);">위치: {{ warehouse.location }}</span>
              <span class="text-xs px-2 py-1 rounded" 
                    :style="`background: ${warehouse.status === 'active' ? '#10b981' : warehouse.status === 'maintenance' ? '#f59e0b' : '#ef4444'}20; 
                             color: ${warehouse.status === 'active' ? '#10b981' : warehouse.status === 'maintenance' ? '#f59e0b' : '#ef4444'};`">
                {{ warehouse.status === 'active' ? '운영중' : warehouse.status === 'maintenance' ? '점검중' : '중단' }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 재고 관리 및 예측 -->
    <div class="management-section p-6 grid grid-cols-1 xl:grid-cols-3 gap-6">
      <!-- 재고 부족 알림 -->
      <div class="low-stock-alerts p-6 rounded-xl" style="background: var(--bg-secondary); border: 1px solid var(--border-secondary);">
        <h3 class="text-xl font-semibold mb-4 text-red-400">재고 부족 알림</h3>
        <div class="space-y-3 max-h-64 overflow-y-auto">
          <div v-for="alert in lowStockAlerts" :key="alert.id"
               class="alert-item p-3 rounded-lg transition-all duration-300 hover:scale-102 cursor-pointer"
               style="background: var(--bg-tertiary); border: 1px solid var(--border-primary);"
               @click="autoOrder(alert)">
            <div class="flex items-center justify-between mb-2">
              <h4 class="font-medium text-white">{{ alert.itemName }}</h4>
              <span class="text-xs px-2 py-1 rounded" 
                    :style="`background: ${alert.urgency === 'critical' ? '#ef4444' : alert.urgency === 'high' ? '#f59e0b' : '#3b82f6'}20; 
                             color: ${alert.urgency === 'critical' ? '#ef4444' : alert.urgency === 'high' ? '#f59e0b' : '#3b82f6'};`">
                {{ alert.urgency === 'critical' ? '긴급' : alert.urgency === 'high' ? '높음' : '보통' }}
              </span>
            </div>
            <div class="grid grid-cols-2 gap-2 text-sm">
              <div>
                <span style="color: var(--text-tertiary);">현재:</span>
                <span class="ml-1 font-medium text-red-400">{{ alert.currentStock }}</span>
              </div>
              <div>
                <span style="color: var(--text-tertiary);">최소:</span>
                <span class="ml-1 font-medium text-orange-400">{{ alert.minStock }}</span>
              </div>
            </div>
            <div class="mt-2 text-sm">
              <span style="color: var(--text-tertiary);">예상 소진:</span>
              <span class="ml-2 font-medium text-white">{{ alert.estimatedRunout }}</span>
            </div>
            <div class="mt-2">
              <span class="text-xs" style="color: var(--text-tertiary);">
                AI 권장 주문량: {{ alert.recommendedQuantity }}개
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- AI 재고 예측 -->
      <div class="inventory-forecast p-6 rounded-xl" style="background: var(--bg-secondary); border: 1px solid var(--border-secondary);">
        <h3 class="text-xl font-semibold mb-4 text-green-400">AI 재고 예측</h3>
        <div class="space-y-4">
          <div v-for="forecast in inventoryForecasts" :key="forecast.period"
               class="forecast-item p-3 rounded-lg"
               style="background: var(--bg-tertiary); border: 1px solid var(--border-primary);">
            <div class="flex items-center justify-between mb-2">
              <span class="text-sm font-medium text-white">{{ forecast.period }}</span>
              <span class="text-sm font-bold" :style="`color: ${forecast.trend === 'increase' ? '#10b981' : forecast.trend === 'decrease' ? '#ef4444' : '#f59e0b'};`">
                {{ forecast.trend === 'increase' ? '↗️' : forecast.trend === 'decrease' ? '↘️' : '➡️' }} {{ forecast.change }}%
              </span>
            </div>
            <div class="grid grid-cols-2 gap-2 text-sm">
              <div>
                <span style="color: var(--text-tertiary);">예상 수요:</span>
                <span class="ml-1 font-medium text-white">{{ forecast.demand.toLocaleString() }}</span>
              </div>
              <div>
                <span style="color: var(--text-tertiary);">권장 재고:</span>
                <span class="ml-1 font-medium text-green-400">{{ forecast.recommendedStock.toLocaleString() }}</span>
              </div>
            </div>
            <div class="mt-2">
              <div class="w-full h-1.5 rounded-full" style="background: var(--bg-hover);">
                <div class="h-full rounded-full transition-all duration-500" 
                     :style="`width: ${forecast.confidence}%; background: ${forecast.trend === 'increase' ? '#10b981' : forecast.trend === 'decrease' ? '#ef4444' : '#f59e0b'};`">
                </div>
              </div>
              <div class="flex justify-between mt-1 text-xs" style="color: var(--text-tertiary);">
                <span>신뢰도: {{ forecast.confidence }}%</span>
                <span>정확도: {{ forecast.accuracy }}%</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 자동 발주 현황 -->
      <div class="auto-ordering p-6 rounded-xl" style="background: var(--bg-secondary); border: 1px solid var(--border-secondary);">
        <h3 class="text-xl font-semibold mb-4 text-purple-400">AI 자동 발주 현황</h3>
        <div class="space-y-3 max-h-64 overflow-y-auto">
          <div v-for="order in autoOrders" :key="order.id"
               class="order-item p-3 rounded-lg transition-all duration-300 hover:scale-102"
               style="background: var(--bg-tertiary); border: 1px solid var(--border-primary);">
            <div class="flex items-center justify-between mb-2">
              <h4 class="font-medium text-white">{{ order.itemName }}</h4>
              <span class="text-xs px-2 py-1 rounded" 
                    :style="`background: ${order.status === 'completed' ? '#10b981' : order.status === 'pending' ? '#f59e0b' : '#3b82f6'}20; 
                             color: ${order.status === 'completed' ? '#10b981' : order.status === 'pending' ? '#f59e0b' : '#3b82f6'};`">
                {{ order.status === 'completed' ? '완료' : order.status === 'pending' ? '대기' : '진행중' }}
              </span>
            </div>
            <div class="grid grid-cols-2 gap-2 text-sm">
              <div>
                <span style="color: var(--text-tertiary);">주문량:</span>
                <span class="ml-1 font-medium text-white">{{ order.quantity.toLocaleString() }}개</span>
              </div>
              <div>
                <span style="color: var(--text-tertiary);">금액:</span>
                <span class="ml-1 font-medium text-green-400">{{ formatCurrency(order.amount) }}</span>
              </div>
            </div>
            <div class="mt-2 text-sm">
              <span style="color: var(--text-tertiary);">공급업체:</span>
              <span class="ml-2 font-medium text-cyan-400">{{ order.supplier }}</span>
            </div>
            <div class="mt-2 flex justify-between items-center">
              <span class="text-xs" style="color: var(--text-tertiary);">{{ order.orderDate }}</span>
              <span class="text-xs" style="color: var(--text-tertiary);">
                AI 신뢰도: {{ order.aiConfidence }}%
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 재고 분석 및 인사이트 -->
    <div class="insights-section p-6">
      <div class="insights-grid grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- 재고 회전 분석 -->
        <div class="turnover-analysis p-6 rounded-xl" style="background: var(--bg-secondary); border: 1px solid var(--border-secondary);">
          <h3 class="text-xl font-semibold mb-4 text-cyan-400">재고 회전 분석</h3>
          <div class="analysis-chart p-4 rounded-lg" style="background: var(--bg-tertiary);">
            <div class="space-y-3">
              <div v-for="category in turnoverAnalysis" :key="category.name" 
                   class="category-analysis p-3 rounded-lg" style="background: var(--bg-hover);">
                <div class="flex items-center justify-between mb-2">
                  <span class="text-sm font-medium text-white">{{ category.name }}</span>
                  <span class="text-sm font-bold" :style="`color: ${category.color};`">
                    {{ category.turnoverRate }}x
                  </span>
                </div>
                <div class="grid grid-cols-2 gap-4 text-sm">
                  <div>
                    <span style="color: var(--text-tertiary);">일일 판매:</span>
                    <span class="ml-2 font-medium text-white">{{ category.dailySales }}</span>
                  </div>
                  <div>
                    <span style="color: var(--text-tertiary);">평균 재고:</span>
                    <span class="ml-2 font-medium text-cyan-400">{{ category.avgInventory }}</span>
                  </div>
                </div>
                <div class="mt-2">
                  <div class="w-full h-2 rounded-full" style="background: var(--bg-primary);">
                    <div class="h-full rounded-full transition-all duration-500" 
                         :style="`width: ${(category.turnoverRate / 10) * 100}%; background: ${category.color};`">
                    </div>
                  </div>
                  <div class="flex justify-between mt-1 text-xs" style="color: var(--text-tertiary);">
                    <span>{{ category.status }}</span>
                    <span>목표: {{ category.target }}x</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- AI 재고 인사이트 -->
        <div class="inventory-insights p-6 rounded-xl" style="background: var(--bg-secondary); border: 1px solid var(--border-secondary);">
          <h3 class="text-xl font-semibold mb-4 text-purple-400">AI 재고 인사이트</h3>
          <div class="insights-list space-y-3">
            <div v-for="insight in stockInsights" :key="insight.id"
                 class="insight-item p-4 rounded-lg transition-all duration-300 hover:scale-102"
                 style="background: var(--bg-tertiary); border: 1px solid var(--border-primary);">
              <div class="flex items-start space-x-3">
                <div class="insight-icon p-2 rounded-full" 
                     :style="`background: ${insight.color}20; color: ${insight.color};`">
                  {{ insight.icon }}
                </div>
                <div class="flex-1">
                  <h4 class="font-medium text-white mb-1">{{ insight.title }}</h4>
                  <p class="text-sm mb-2" style="color: var(--text-secondary);">{{ insight.description }}</p>
                  <div class="flex items-center justify-between">
                    <span class="text-xs px-2 py-1 rounded" 
                          :style="`background: ${insight.impact === 'high' ? '#ef4444' : insight.impact === 'medium' ? '#f59e0b' : '#10b981'}20; 
                                   color: ${insight.impact === 'high' ? '#ef4444' : insight.impact === 'medium' ? '#f59e0b' : '#10b981'};`">
                      {{ insight.impact === 'high' ? '높은 영향' : insight.impact === 'medium' ? '보통 영향' : '낮은 영향' }}
                    </span>
                    <span class="text-xs" style="color: var(--text-tertiary);">
                      예상 절약: {{ formatCurrency(insight.potentialSavings) }}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import { useAI } from '@/composables/useAI'

export default {
  name: 'StockModule',
  setup() {
    const { executeAIRequest, formatResponse } = useAI()
    
    // 반응형 데이터
    const agiStatus = ref('활성화됨')
    const aiCommand = ref('')
    const aiResponse = ref('')
    
    // 대시보드 메트릭
    const totalStockValue = ref(3750000000)
    const stockValueGrowth = ref(5.8)
    const stockTurnoverRate = ref(6.8)
    const totalWarehouses = ref(8)
    const warehouseUtilization = ref(78.5)
    const autoOrderCount = ref(156)
    const autoOrderAccuracy = ref(94.2)
    
    // 재고 카테고리
    const inventoryCategories = ref([
      { 
        name: '원자재', 
        currentStock: 85600, 
        value: 1280000000, 
        turnoverRate: 8.2, 
        forecast: 45, 
        status: 'optimal', 
        stockLevel: 75 
      },
      { 
        name: '반제품', 
        currentStock: 12400, 
        value: 950000000, 
        turnoverRate: 5.6, 
        forecast: 62, 
        status: 'low', 
        stockLevel: 35 
      },
      { 
        name: '완제품', 
        currentStock: 8900, 
        value: 1150000000, 
        turnoverRate: 12.3, 
        forecast: 28, 
        status: 'optimal', 
        stockLevel: 85 
      },
      { 
        name: '부품', 
        currentStock: 156000, 
        value: 370000000, 
        turnoverRate: 6.9, 
        forecast: 52, 
        status: 'excess', 
        stockLevel: 95 
      }
    ])
    
    // 창고 현황
    const warehouses = ref([
      {
        id: 1,
        name: '중앙 창고 A',
        totalCapacity: 15000,
        usedCapacity: 12750,
        utilizationRate: 85,
        itemCount: 45600,
        temperature: 22,
        location: '서울 강서구',
        status: 'active',
        aiEfficiency: 92
      },
      {
        id: 2,
        name: '냉동 창고 B',
        totalCapacity: 8000,
        usedCapacity: 5600,
        utilizationRate: 70,
        itemCount: 12800,
        temperature: -18,
        location: '경기 평택시',
        status: 'active',
        aiEfficiency: 89
      },
      {
        id: 3,
        name: '물류 창고 C',
        totalCapacity: 12000,
        usedCapacity: 9360,
        utilizationRate: 78,
        itemCount: 28900,
        temperature: 18,
        location: '부산 사하구',
        status: 'maintenance',
        aiEfficiency: 86
      }
    ])
    
    // 재고 부족 알림
    const lowStockAlerts = ref([
      {
        id: 1,
        itemName: '프리미엄 원자재 A',
        currentStock: 85,
        minStock: 200,
        urgency: 'critical',
        estimatedRunout: '2일',
        recommendedQuantity: 500
      },
      {
        id: 2,
        itemName: '핵심 부품 B',
        currentStock: 150,
        minStock: 300,
        urgency: 'high',
        estimatedRunout: '5일',
        recommendedQuantity: 800
      },
      {
        id: 3,
        itemName: '포장재 C',
        currentStock: 800,
        minStock: 1000,
        urgency: 'medium',
        estimatedRunout: '1주일',
        recommendedQuantity: 2000
      }
    ])
    
    // 재고 예측
    const inventoryForecasts = ref([
      {
        period: '다음 주',
        demand: 12800,
        recommendedStock: 15600,
        trend: 'increase',
        change: 15.2,
        confidence: 92,
        accuracy: 88
      },
      {
        period: '다음 월',
        demand: 48500,
        recommendedStock: 58200,
        trend: 'increase',
        change: 8.7,
        confidence: 87,
        accuracy: 85
      },
      {
        period: '다음 분기',
        demand: 156000,
        recommendedStock: 187200,
        trend: 'stable',
        change: 2.1,
        confidence: 79,
        accuracy: 82
      }
    ])
    
    // 자동 발주 현황
    const autoOrders = ref([
      {
        id: 1,
        itemName: '고급 원자재 X',
        quantity: 1500,
        amount: 45000000,
        supplier: '글로벌소재(주)',
        status: 'completed',
        orderDate: '2024-01-15',
        aiConfidence: 95
      },
      {
        id: 2,
        itemName: '특수 부품 Y',
        quantity: 800,
        amount: 28000000,
        supplier: '프리미엄부품',
        status: 'processing',
        orderDate: '2024-01-16',
        aiConfidence: 89
      },
      {
        id: 3,
        itemName: '포장재료 Z',
        quantity: 5000,
        amount: 12500000,
        supplier: '스마트팩키징',
        status: 'pending',
        orderDate: '2024-01-17',
        aiConfidence: 87
      }
    ])
    
    // 회전율 분석
    const turnoverAnalysis = ref([
      {
        name: '고회전 품목',
        turnoverRate: 15.6,
        dailySales: 850,
        avgInventory: 5400,
        target: 12.0,
        status: '우수',
        color: '#10b981'
      },
      {
        name: '중회전 품목',
        turnoverRate: 8.2,
        dailySales: 420,
        avgInventory: 5100,
        target: 8.0,
        status: '양호',
        color: '#3b82f6'
      },
      {
        name: '저회전 품목',
        turnoverRate: 3.1,
        dailySales: 125,
        avgInventory: 4000,
        target: 6.0,
        status: '개선필요',
        color: '#f59e0b'
      },
      {
        name: '재고 과다',
        turnoverRate: 1.2,
        dailySales: 45,
        avgInventory: 3700,
        target: 4.0,
        status: '위험',
        color: '#ef4444'
      }
    ])
    
    // 재고 인사이트
    const stockInsights = ref([
      {
        id: 1,
        title: '계절성 수요 변화 감지',
        description: '겨울 제품 수요가 평소보다 20% 높게 예측됩니다. 미리 재고를 확보하는 것이 좋습니다.',
        impact: 'high',
        potentialSavings: 85000000,
        icon: '❄️',
        color: '#3b82f6'
      },
      {
        id: 2,
        title: '재고 과다 품목 발견',
        description: '특정 부품의 재고가 6개월 치 수요량을 초과했습니다. 할인 판매를 검토하세요.',
        impact: 'medium',
        potentialSavings: 45000000,
        icon: '📦',
        color: '#f59e0b'
      },
      {
        id: 3,
        title: '공급업체 리스크 예측',
        description: '주요 공급업체의 배송 지연 가능성이 높습니다. 대체 공급업체 준비가 필요합니다.',
        impact: 'high',
        potentialSavings: 120000000,
        icon: '⚠️',
        color: '#ef4444'
      },
      {
        id: 4,
        title: '자동 발주 최적화',
        description: 'AI 학습을 통해 발주 정확도를 5% 개선할 수 있습니다.',
        impact: 'medium',
        potentialSavings: 35000000,
        icon: '🤖',
        color: '#10b981'
      }
    ])
    
    // 메서드
    const formatCurrency = (amount) => {
      return new Intl.NumberFormat('ko-KR', {
        style: 'currency',
        currency: 'KRW',
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
      }).format(amount)
    }
    
    const executeAICommand = async () => {
      if (!aiCommand.value.trim()) return
      
      try {
        aiResponse.value = '처리 중...'
        
        // AI 요청 실행
        const response = await executeAIRequest(aiCommand.value, 'stock')
        aiResponse.value = formatResponse(response)
        
        // 성공적인 실행 후 관련 데이터 업데이트
        await updateDashboardData()
        
      } catch (error) {
        aiResponse.value = `오류가 발생했습니다: ${error.message}`
      }
    }
    
    const clearAICommand = () => {
      aiCommand.value = ''
      aiResponse.value = ''
    }
    
    const refreshDashboard = async () => {
      agiStatus.value = '업데이트 중...'
      
      // 실제 데이터 새로고침 로직
      setTimeout(() => {
        agiStatus.value = '활성화됨'
        // 데이터 업데이트
        updateDashboardData()
      }, 1000)
    }
    
    const updateDashboardData = async () => {
      // 실시간 데이터 업데이트 시뮬레이션
      totalStockValue.value += Math.floor(Math.random() * 100000000)
      autoOrderCount.value += Math.floor(Math.random() * 5)
      stockTurnoverRate.value = Math.round((stockTurnoverRate.value + Math.random() * 0.5 - 0.25) * 10) / 10
    }
    
    const viewWarehouseDetails = (warehouse) => {
      aiResponse.value = `창고 상세 현황:
      
창고명: ${warehouse.name}
위치: ${warehouse.location}
운영 상태: ${warehouse.status === 'active' ? '정상 운영' : warehouse.status === 'maintenance' ? '정기 점검' : '운영 중단'}

용량 정보:
- 총 용량: ${warehouse.totalCapacity.toLocaleString()}㎡
- 사용 용량: ${warehouse.usedCapacity.toLocaleString()}㎡
- 가동률: ${warehouse.utilizationRate}%
- 여유 공간: ${(warehouse.totalCapacity - warehouse.usedCapacity).toLocaleString()}㎡

운영 정보:
- 총 품목 수: ${warehouse.itemCount.toLocaleString()}개
- 현재 온도: ${warehouse.temperature}°C
- AI 효율성: ${warehouse.aiEfficiency}%

AI 추천 액션:
${warehouse.utilizationRate >= 85 ? '- 용량 확장 또는 재배치 검토 필요' : '- 현재 운영 상태 양호'}
${warehouse.temperature !== 22 ? '- 특수 환경 관리 품목 포함' : '- 일반 보관 환경'}
- 효율성 개선 가능: ${100 - warehouse.aiEfficiency}%`
    }
    
    const autoOrder = (alert) => {
      aiResponse.value = `AI 자동 발주 실행:
      
품목명: ${alert.itemName}
현재 재고: ${alert.currentStock}개
최소 재고: ${alert.minStock}개
부족량: ${alert.minStock - alert.currentStock}개

AI 분석 결과:
- 긴급도: ${alert.urgency === 'critical' ? '긴급 (24시간 내 발주 필요)' : alert.urgency === 'high' ? '높음 (3일 내 발주 권장)' : '보통 (1주일 내 발주)'}
- 예상 소진: ${alert.estimatedRunout}
- 권장 주문량: ${alert.recommendedQuantity}개

최적 발주 계획:
- 주문량: ${alert.recommendedQuantity}개
- 예상 단가: ${formatCurrency(Math.floor(Math.random() * 50000 + 10000))}
- 총 금액: ${formatCurrency(alert.recommendedQuantity * Math.floor(Math.random() * 50000 + 10000))}
- 최적 공급업체: AI가 선정한 1순위 업체
- 예상 배송: ${Math.floor(Math.random() * 5 + 2)}일

자동 발주를 승인하시겠습니까?`
    }
    
    // 라이프사이클
    onMounted(() => {
      updateDashboardData()
    })
    
    return {
      // 상태
      agiStatus,
      aiCommand,
      aiResponse,
      
      // 메트릭
      totalStockValue,
      stockValueGrowth,
      stockTurnoverRate,
      totalWarehouses,
      warehouseUtilization,
      autoOrderCount,
      autoOrderAccuracy,
      
      // 데이터
      inventoryCategories,
      warehouses,
      lowStockAlerts,
      inventoryForecasts,
      autoOrders,
      turnoverAnalysis,
      stockInsights,
      
      // 메서드
      formatCurrency,
      executeAICommand,
      clearAICommand,
      refreshDashboard,
      viewWarehouseDetails,
      autoOrder
    }
  }
}
</script>

<style scoped>
.stock-module {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

.dashboard-card:hover {
  transform: translateY(-2px);
}

.category-item:hover,
.warehouse-item:hover,
.alert-item:hover,
.order-item:hover,
.insight-item:hover {
  transform: translateY(-1px);
}

.hover\:scale-102:hover {
  transform: scale(1.02);
}

/* 커스텀 스크롤바 */
.max-h-64::-webkit-scrollbar {
  width: 6px;
}

.max-h-64::-webkit-scrollbar-track {
  background: var(--bg-hover);
  border-radius: 3px;
}

.max-h-64::-webkit-scrollbar-thumb {
  background: var(--border-secondary);
  border-radius: 3px;
}

.max-h-64::-webkit-scrollbar-thumb:hover {
  background: var(--ai-primary);
}

/* 애니메이션 */
@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.7;
  }
}

.animate-pulse {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

/* 반응형 디자인 */
@media (max-width: 768px) {
  .dashboard-cards {
    grid-template-columns: 1fr;
  }
  
  .main-content {
    grid-template-columns: 1fr;
  }
  
  .management-section {
    grid-template-columns: 1fr;
  }
  
  .insights-section .insights-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 640px) {
  .header-section .flex {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
  
  .ai-command-section .flex {
    flex-direction: column;
  }
  
  .ai-command-section .flex-col {
    flex-direction: row;
    justify-content: space-between;
    width: 100%;
  }
}
</style>