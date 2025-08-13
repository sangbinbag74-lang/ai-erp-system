<template>
  <div class="purchase-module min-h-screen" style="background: var(--bg-primary); color: var(--text-primary);">
    <!-- 헤더 -->
    <div class="header-section p-6 border-b" style="border-color: var(--border-primary); background: var(--bg-secondary);">
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-3xl font-bold bg-gradient-to-r from-green-400 to-blue-400 bg-clip-text text-transparent">
            구매 관리 (Purchase Management)
          </h1>
          <p class="text-gray-400 mt-2">AI 기반 구매 최적화 및 공급업체 관리</p>
        </div>
        <div class="flex items-center space-x-4">
          <div class="agi-status px-4 py-2 rounded-lg" style="background: var(--bg-tertiary); border: 1px solid var(--ai-primary);">
            <span class="text-sm">AGI 상태: </span>
            <span class="text-green-400 font-semibold">{{ agiStatus }}</span>
          </div>
          <button 
            @click="refreshDashboard"
            class="bg-green-600 hover:bg-green-700 px-4 py-2 rounded-lg transition-all duration-300 text-white"
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
        <h3 class="text-lg font-semibold mb-3 text-green-400">AI 구매 어시스턴트</h3>
        <div class="flex space-x-4">
          <textarea 
            v-model="aiCommand"
            placeholder="구매 관련 자연어 명령을 입력하세요... 예: '최적 공급업체 찾아줘', '재고 부족 품목 주문해줘', '구매 비용 분석해줘'"
            class="flex-1 p-4 rounded-lg resize-none transition-all duration-300"
            style="background: var(--bg-tertiary); border: 1px solid var(--border-secondary); color: var(--text-primary); min-height: 80px;"
            @focus="$event.target.style.borderColor = 'var(--ai-primary)'"
            @blur="$event.target.style.borderColor = 'var(--border-secondary)'"
          ></textarea>
          <div class="flex flex-col space-y-2">
            <button 
              @click="executeAICommand"
              :disabled="!aiCommand.trim()"
              class="bg-gradient-to-r from-green-500 to-blue-600 hover:from-green-600 hover:to-blue-700 disabled:opacity-50 px-6 py-3 rounded-lg transition-all duration-300 text-white font-medium"
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
      <!-- 총 구매액 -->
      <div class="dashboard-card p-6 rounded-xl transition-all duration-300 hover:scale-105" 
           style="background: var(--bg-secondary); border: 1px solid var(--border-secondary);"
           @mouseenter="$event.target.style.boxShadow = 'var(--glow-primary)'"
           @mouseleave="$event.target.style.boxShadow = 'none'">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm font-medium" style="color: var(--text-secondary);">총 구매액</p>
            <p class="text-2xl font-bold text-green-400">{{ formatCurrency(totalPurchaseAmount) }}</p>
            <p class="text-xs mt-1" :class="purchaseGrowth >= 0 ? 'text-green-400' : 'text-red-400'">
              {{ purchaseGrowth >= 0 ? '+' : '' }}{{ purchaseGrowth }}% 전월 대비
            </p>
          </div>
          <div class="text-green-400 text-3xl">💰</div>
        </div>
      </div>

      <!-- 활성 주문 -->
      <div class="dashboard-card p-6 rounded-xl transition-all duration-300 hover:scale-105" 
           style="background: var(--bg-secondary); border: 1px solid var(--border-secondary);"
           @mouseenter="$event.target.style.boxShadow = 'var(--glow-secondary)'"
           @mouseleave="$event.target.style.boxShadow = 'none'">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm font-medium" style="color: var(--text-secondary);">활성 주문</p>
            <p class="text-2xl font-bold text-blue-400">{{ activeOrders }}</p>
            <p class="text-xs mt-1 text-green-400">{{ onTimeDelivery }}% 정시 배송률</p>
          </div>
          <div class="text-blue-400 text-3xl">📦</div>
        </div>
      </div>

      <!-- 공급업체 수 -->
      <div class="dashboard-card p-6 rounded-xl transition-all duration-300 hover:scale-105" 
           style="background: var(--bg-secondary); border: 1px solid var(--border-secondary);"
           @mouseenter="$event.target.style.boxShadow = 'var(--glow-accent)'"
           @mouseleave="$event.target.style.boxShadow = 'none'">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm font-medium" style="color: var(--text-secondary);">활성 공급업체</p>
            <p class="text-2xl font-bold text-purple-400">{{ activeSuppliers }}</p>
            <p class="text-xs mt-1 text-green-400">평균 평점 {{ averageRating }}점</p>
          </div>
          <div class="text-purple-400 text-3xl">🏢</div>
        </div>
      </div>

      <!-- 비용 절감 -->
      <div class="dashboard-card p-6 rounded-xl transition-all duration-300 hover:scale-105" 
           style="background: var(--bg-secondary); border: 1px solid var(--border-secondary);"
           @mouseenter="$event.target.style.boxShadow = 'var(--glow-primary)'"
           @mouseleave="$event.target.style.boxShadow = 'none'">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm font-medium" style="color: var(--text-secondary);">AI 비용 절감</p>
            <p class="text-2xl font-bold text-orange-400">{{ formatCurrency(costSavings) }}</p>
            <p class="text-xs mt-1 text-green-400">{{ savingsPercentage }}% 절약</p>
          </div>
          <div class="text-orange-400 text-3xl">💡</div>
        </div>
      </div>
    </div>

    <!-- 메인 콘텐츠 영역 -->
    <div class="main-content p-6 grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- 구매 워크플로 -->
      <div class="workflow-section p-6 rounded-xl" style="background: var(--bg-secondary); border: 1px solid var(--border-secondary);">
        <h3 class="text-xl font-semibold mb-4 text-green-400">AI 구매 워크플로</h3>
        <div class="space-y-4">
          <div v-for="stage in purchaseWorkflow" :key="stage.name" 
               class="workflow-stage p-4 rounded-lg transition-all duration-300 hover:scale-102"
               style="background: var(--bg-tertiary); border: 1px solid var(--border-primary);">
            <div class="flex items-center justify-between mb-2">
              <h4 class="font-medium text-white">{{ stage.name }}</h4>
              <span class="text-sm px-2 py-1 rounded" 
                    :style="`background: ${stage.color}20; color: ${stage.color};`">
                {{ stage.count }}건
              </span>
            </div>
            <div class="flex items-center justify-between">
              <span class="text-sm" style="color: var(--text-secondary);">
                평균 처리시간: {{ stage.avgTime }}
              </span>
              <div class="w-16 h-2 rounded-full" style="background: var(--bg-hover);">
                <div class="h-full rounded-full transition-all duration-300" 
                     :style="`width: ${stage.efficiency}%; background: ${stage.color};`">
                </div>
              </div>
            </div>
            <div class="mt-2">
              <span class="text-xs" style="color: var(--text-tertiary);">
                AI 자동화율: {{ stage.automation }}%
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- 공급업체 성과 분석 -->
      <div class="supplier-analysis p-6 rounded-xl" style="background: var(--bg-secondary); border: 1px solid var(--border-secondary);">
        <h3 class="text-xl font-semibold mb-4 text-blue-400">AI 공급업체 성과 분석</h3>
        <div class="space-y-4">
          <div v-for="supplier in topSuppliers" :key="supplier.name"
               class="supplier-item p-4 rounded-lg transition-all duration-300 hover:scale-102 cursor-pointer"
               style="background: var(--bg-tertiary); border: 1px solid var(--border-primary);"
               @click="viewSupplierDetails(supplier)">
            <div class="flex items-center justify-between mb-2">
              <h4 class="font-medium text-white">{{ supplier.name }}</h4>
              <div class="flex items-center space-x-2">
                <span class="text-sm px-2 py-1 rounded" 
                      :style="`background: ${supplier.rating >= 4.5 ? '#10b981' : supplier.rating >= 4.0 ? '#f59e0b' : '#ef4444'}20; 
                               color: ${supplier.rating >= 4.5 ? '#10b981' : supplier.rating >= 4.0 ? '#f59e0b' : '#ef4444'};`">
                  ⭐ {{ supplier.rating }}
                </span>
              </div>
            </div>
            <div class="grid grid-cols-2 gap-4 text-sm">
              <div>
                <span style="color: var(--text-tertiary);">총 주문액:</span>
                <span class="ml-2 font-medium text-white">{{ formatCurrency(supplier.totalOrders) }}</span>
              </div>
              <div>
                <span style="color: var(--text-tertiary);">정시 배송률:</span>
                <span class="ml-2 font-medium text-green-400">{{ supplier.onTimeRate }}%</span>
              </div>
            </div>
            <div class="mt-2 grid grid-cols-2 gap-4 text-sm">
              <div>
                <span style="color: var(--text-tertiary);">품질 점수:</span>
                <span class="ml-2 font-medium text-purple-400">{{ supplier.qualityScore }}/100</span>
              </div>
              <div>
                <span style="color: var(--text-tertiary);">비용 경쟁력:</span>
                <span class="ml-2 font-medium text-blue-400">{{ supplier.costCompetitiveness }}</span>
              </div>
            </div>
            <div class="mt-2">
              <span class="text-xs" style="color: var(--text-tertiary);">
                AI 추천도: {{ supplier.aiRecommendation }}% | 리스크 레벨: {{ supplier.riskLevel }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 구매 활동 및 재고 관리 -->
    <div class="activities-section p-6 grid grid-cols-1 xl:grid-cols-3 gap-6">
      <!-- 최근 구매 활동 -->
      <div class="recent-activities p-6 rounded-xl" style="background: var(--bg-secondary); border: 1px solid var(--border-secondary);">
        <h3 class="text-xl font-semibold mb-4 text-green-400">최근 구매 활동</h3>
        <div class="space-y-3 max-h-64 overflow-y-auto">
          <div v-for="activity in recentActivities" :key="activity.id"
               class="activity-item p-3 rounded-lg transition-all duration-300 hover:scale-102"
               style="background: var(--bg-tertiary); border: 1px solid var(--border-primary);">
            <div class="flex items-start space-x-3">
              <div class="activity-icon p-2 rounded-full" 
                   :style="`background: ${activity.color}20; color: ${activity.color};`">
                {{ activity.icon }}
              </div>
              <div class="flex-1">
                <p class="text-sm font-medium text-white">{{ activity.title }}</p>
                <p class="text-xs mt-1" style="color: var(--text-tertiary);">{{ activity.description }}</p>
                <p class="text-xs mt-1" style="color: var(--text-secondary);">{{ activity.time }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 재고 부족 알림 -->
      <div class="inventory-alerts p-6 rounded-xl" style="background: var(--bg-secondary); border: 1px solid var(--border-secondary);">
        <h3 class="text-xl font-semibold mb-4 text-red-400">AI 재고 부족 알림</h3>
        <div class="space-y-3 max-h-64 overflow-y-auto">
          <div v-for="alert in inventoryAlerts" :key="alert.id"
               class="alert-item p-3 rounded-lg transition-all duration-300 hover:scale-102 cursor-pointer"
               style="background: var(--bg-tertiary); border: 1px solid var(--border-primary);"
               @click="createPurchaseOrder(alert)">
            <div class="flex items-center justify-between mb-2">
              <h4 class="font-medium text-white">{{ alert.itemName }}</h4>
              <span class="text-xs px-2 py-1 rounded" 
                    :style="`background: ${alert.priority === 'critical' ? '#ef4444' : alert.priority === 'high' ? '#f59e0b' : '#3b82f6'}20; 
                             color: ${alert.priority === 'critical' ? '#ef4444' : alert.priority === 'high' ? '#f59e0b' : '#3b82f6'};`">
                {{ alert.priority === 'critical' ? '긴급' : alert.priority === 'high' ? '높음' : '보통' }}
              </span>
            </div>
            <div class="grid grid-cols-2 gap-2 text-sm">
              <div>
                <span style="color: var(--text-tertiary);">현재 재고:</span>
                <span class="ml-2 font-medium text-red-400">{{ alert.currentStock }}</span>
              </div>
              <div>
                <span style="color: var(--text-tertiary);">최소 재고:</span>
                <span class="ml-2 font-medium text-orange-400">{{ alert.minStock }}</span>
              </div>
            </div>
            <div class="mt-2">
              <span class="text-xs" style="color: var(--text-tertiary);">
                AI 추천 주문량: {{ alert.recommendedOrder }}개 | 예상 소진: {{ alert.estimatedDepletion }}
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- 비용 최적화 제안 -->
      <div class="cost-optimization p-6 rounded-xl" style="background: var(--bg-secondary); border: 1px solid var(--border-secondary);">
        <h3 class="text-xl font-semibold mb-4 text-purple-400">AI 비용 최적화 제안</h3>
        <div class="space-y-4">
          <div v-for="optimization in costOptimizations" :key="optimization.id"
               class="optimization-item p-3 rounded-lg"
               style="background: var(--bg-tertiary); border: 1px solid var(--border-primary);">
            <div class="flex items-center justify-between mb-2">
              <span class="text-sm font-medium text-white">{{ optimization.title }}</span>
              <span class="text-sm font-bold text-green-400">
                {{ formatCurrency(optimization.savings) }}
              </span>
            </div>
            <p class="text-xs mb-2" style="color: var(--text-secondary);">{{ optimization.description }}</p>
            <div class="flex items-center justify-between">
              <span class="text-xs px-2 py-1 rounded" 
                    :style="`background: ${optimization.difficulty === 'easy' ? '#10b981' : optimization.difficulty === 'medium' ? '#f59e0b' : '#ef4444'}20; 
                             color: ${optimization.difficulty === 'easy' ? '#10b981' : optimization.difficulty === 'medium' ? '#f59e0b' : '#ef4444'};`">
                {{ optimization.difficulty === 'easy' ? '쉬움' : optimization.difficulty === 'medium' ? '보통' : '어려움' }}
              </span>
              <span class="text-xs" style="color: var(--text-tertiary);">
                예상 ROI: {{ optimization.roi }}%
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 구매 분석 및 예측 -->
    <div class="analytics-section p-6">
      <div class="analytics-grid grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- 구매 패턴 분석 -->
        <div class="purchase-patterns p-6 rounded-xl" style="background: var(--bg-secondary); border: 1px solid var(--border-secondary);">
          <h3 class="text-xl font-semibold mb-4 text-blue-400">AI 구매 패턴 분석</h3>
          <div class="patterns-chart p-4 rounded-lg" style="background: var(--bg-tertiary);">
            <div class="space-y-3">
              <div v-for="pattern in purchasePatterns" :key="pattern.category" 
                   class="pattern-item p-3 rounded-lg" style="background: var(--bg-hover);">
                <div class="flex items-center justify-between mb-2">
                  <span class="text-sm font-medium text-white">{{ pattern.category }}</span>
                  <span class="text-sm font-bold" :style="`color: ${pattern.color};`">
                    {{ pattern.percentage }}%
                  </span>
                </div>
                <div class="w-full h-2 rounded-full" style="background: var(--bg-primary);">
                  <div class="h-full rounded-full transition-all duration-500" 
                       :style="`width: ${pattern.percentage}%; background: ${pattern.color};`">
                  </div>
                </div>
                <div class="flex items-center justify-between mt-1">
                  <span class="text-xs" style="color: var(--text-tertiary);">{{ formatCurrency(pattern.amount) }}</span>
                  <span class="text-xs" :class="pattern.trend === 'up' ? 'text-green-400' : pattern.trend === 'down' ? 'text-red-400' : 'text-gray-400'">
                    {{ pattern.trend === 'up' ? '↗️' : pattern.trend === 'down' ? '↘️' : '➡️' }} {{ pattern.change }}%
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- AI 구매 예측 -->
        <div class="purchase-forecast p-6 rounded-xl" style="background: var(--bg-secondary); border: 1px solid var(--border-secondary);">
          <h3 class="text-xl font-semibold mb-4 text-green-400">AI 구매 예측 및 인사이트</h3>
          <div class="forecast-data space-y-4">
            <div class="forecast-summary p-4 rounded-lg" style="background: var(--bg-tertiary);">
              <div class="flex items-center justify-between mb-2">
                <span class="text-sm" style="color: var(--text-secondary);">다음 분기 예상 구매액</span>
                <span class="text-lg font-bold text-green-400">{{ formatCurrency(forecastAmount) }}</span>
              </div>
              <div class="text-xs" style="color: var(--text-tertiary);">
                현재 트렌드 기준 {{ ((forecastAmount - totalPurchaseAmount) / totalPurchaseAmount * 100).toFixed(1) }}% 증가 예상
              </div>
            </div>
            
            <div class="insights-list space-y-3">
              <div v-for="insight in purchaseInsights" :key="insight.id"
                   class="insight-item p-3 rounded-lg"
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
                      <span class="text-xs" style="color: var(--text-tertiary);">신뢰도: {{ insight.confidence }}%</span>
                    </div>
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
  name: 'PurchaseModule',
  setup() {
    const { executeAIRequest, formatResponse } = useAI()
    
    // 반응형 데이터
    const agiStatus = ref('활성화됨')
    const aiCommand = ref('')
    const aiResponse = ref('')
    
    // 대시보드 메트릭
    const totalPurchaseAmount = ref(1850000000)
    const purchaseGrowth = ref(8.3)
    const activeOrders = ref(89)
    const onTimeDelivery = ref(94.2)
    const activeSuppliers = ref(67)
    const averageRating = ref(4.3)
    const costSavings = ref(125000000)
    const savingsPercentage = ref(6.8)
    
    // 예측 데이터
    const forecastAmount = ref(2100000000)
    
    // 구매 워크플로
    const purchaseWorkflow = ref([
      { name: '구매 요청', count: 23, avgTime: '2시간', efficiency: 92, automation: 85, color: '#3b82f6' },
      { name: '견적 수집', count: 15, avgTime: '1일', efficiency: 88, automation: 70, color: '#8b5cf6' },
      { name: '승인 대기', count: 8, avgTime: '4시간', efficiency: 85, automation: 95, color: '#f59e0b' },
      { name: '주문 발주', count: 12, avgTime: '30분', efficiency: 98, automation: 100, color: '#10b981' },
      { name: '배송 추적', count: 34, avgTime: '실시간', efficiency: 96, automation: 100, color: '#06b6d4' }
    ])
    
    // 상위 공급업체
    const topSuppliers = ref([
      { 
        name: '글로벌 소재(주)', 
        rating: 4.8, 
        totalOrders: 450000000, 
        onTimeRate: 96.5,
        qualityScore: 92,
        costCompetitiveness: 'A+',
        aiRecommendation: 95,
        riskLevel: '낮음'
      },
      { 
        name: '프리미엄 부품', 
        rating: 4.6, 
        totalOrders: 320000000, 
        onTimeRate: 94.2,
        qualityScore: 89,
        costCompetitiveness: 'A',
        aiRecommendation: 87,
        riskLevel: '낮음'
      },
      { 
        name: '스마트 공급사', 
        rating: 4.3, 
        totalOrders: 280000000, 
        onTimeRate: 91.8,
        qualityScore: 85,
        costCompetitiveness: 'B+',
        aiRecommendation: 78,
        riskLevel: '보통'
      }
    ])
    
    // 최근 활동
    const recentActivities = ref([
      { id: 1, title: '긴급 주문 승인', description: '생산라인 부품 - 24시간 내 배송 요청', time: '15분 전', icon: '🚨', color: '#ef4444' },
      { id: 2, title: '신규 견적 접수', description: '고급 원자재 - 3개 업체 견적 비교', time: '2시간 전', icon: '📋', color: '#3b82f6' },
      { id: 3, title: 'AI 최적화 완료', description: '월간 구매 패턴 분석 및 추천', time: '4시간 전', icon: '🤖', color: '#10b981' },
      { id: 4, title: '배송 지연 알림', description: '해외 부품 배송 3일 지연 예상', time: '6시간 전', icon: '📦', color: '#f59e0b' }
    ])
    
    // 재고 부족 알림
    const inventoryAlerts = ref([
      { 
        id: 1, 
        itemName: '핵심 부품 A', 
        currentStock: 45, 
        minStock: 100, 
        priority: 'critical',
        recommendedOrder: 500,
        estimatedDepletion: '3일'
      },
      { 
        id: 2, 
        itemName: '원자재 B', 
        currentStock: 120, 
        minStock: 200, 
        priority: 'high',
        recommendedOrder: 800,
        estimatedDepletion: '1주일'
      },
      { 
        id: 3, 
        itemName: '소모품 C', 
        currentStock: 300, 
        minStock: 500, 
        priority: 'medium',
        recommendedOrder: 1000,
        estimatedDepletion: '2주일'
      }
    ])
    
    // 비용 최적화 제안
    const costOptimizations = ref([
      {
        id: 1,
        title: '대량 구매 할인',
        description: '월 단위 통합 주문으로 5-10% 할인 가능',
        savings: 45000000,
        difficulty: 'easy',
        roi: 250
      },
      {
        id: 2,
        title: '공급업체 재협상',
        description: '상위 3개 업체와 장기 계약 협상',
        savings: 78000000,
        difficulty: 'medium',
        roi: 180
      },
      {
        id: 3,
        title: '자동화 시스템 도입',
        description: '구매 프로세스 완전 자동화',
        savings: 95000000,
        difficulty: 'hard',
        roi: 320
      }
    ])
    
    // 구매 패턴
    const purchasePatterns = ref([
      { category: '원자재', percentage: 35, amount: 647500000, color: '#3b82f6', trend: 'up', change: 8.2 },
      { category: '부품/소재', percentage: 28, amount: 518000000, color: '#10b981', trend: 'up', change: 12.5 },
      { category: '장비/기계', percentage: 20, amount: 370000000, color: '#f59e0b', trend: 'down', change: -3.1 },
      { category: '소모품', percentage: 12, amount: 222000000, color: '#8b5cf6', trend: 'stable', change: 1.8 },
      { category: '기타', percentage: 5, amount: 92500000, color: '#06b6d4', trend: 'up', change: 15.3 }
    ])
    
    // 구매 인사이트
    const purchaseInsights = ref([
      {
        id: 1,
        title: '계절성 수요 증가 예측',
        description: '4분기 원자재 수요가 평균 대비 25% 증가할 것으로 예상됩니다.',
        impact: 'high',
        confidence: 89,
        icon: '📈',
        color: '#ef4444'
      },
      {
        id: 2,
        title: '공급업체 리스크 감지',
        description: '주요 공급업체의 재정 상태 변화가 감지되었습니다.',
        impact: 'medium',
        confidence: 76,
        icon: '⚠️',
        color: '#f59e0b'
      },
      {
        id: 3,
        title: '신규 공급업체 발견',
        description: '품질과 가격 경쟁력을 모두 만족하는 신규 업체를 발견했습니다.',
        impact: 'medium',
        confidence: 82,
        icon: '🆕',
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
        const response = await executeAIRequest(aiCommand.value, 'purchase')
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
      totalPurchaseAmount.value += Math.floor(Math.random() * 50000000)
      activeOrders.value += Math.floor(Math.random() * 3)
      onTimeDelivery.value = Math.round((onTimeDelivery.value + Math.random() * 2 - 1) * 10) / 10
    }
    
    const viewSupplierDetails = (supplier) => {
      aiResponse.value = `공급업체 상세 분석:
      
업체명: ${supplier.name}
평점: ${supplier.rating}/5.0
총 주문액: ${formatCurrency(supplier.totalOrders)}
정시 배송률: ${supplier.onTimeRate}%
품질 점수: ${supplier.qualityScore}/100
비용 경쟁력: ${supplier.costCompetitiveness}

AI 종합 평가:
- 추천도: ${supplier.aiRecommendation}%
- 리스크 레벨: ${supplier.riskLevel}
- 장기 파트너십 적합성: ${supplier.aiRecommendation >= 85 ? '매우 높음' : supplier.aiRecommendation >= 70 ? '높음' : '보통'}

추천 액션:
1. ${supplier.aiRecommendation >= 85 ? '우선 파트너로 지정' : '성과 모니터링 강화'}
2. ${supplier.onTimeRate >= 95 ? '배송 일정 최적화 협의' : '배송 개선 방안 논의'}
3. ${supplier.qualityScore >= 90 ? '품질 인증 파트너 등록' : '품질 관리 체계 점검'}`
    }
    
    const createPurchaseOrder = (alert) => {
      aiResponse.value = `자동 구매 주문 생성:
      
품목: ${alert.itemName}
현재 재고: ${alert.currentStock}개
최소 재고: ${alert.minStock}개
부족량: ${alert.minStock - alert.currentStock}개

AI 추천 주문량: ${alert.recommendedOrder}개
우선순위: ${alert.priority === 'critical' ? '긴급' : alert.priority === 'high' ? '높음' : '보통'}
예상 소진 시점: ${alert.estimatedDepletion}

최적 공급업체: ${topSuppliers.value[0].name}
예상 단가: ${formatCurrency(Math.floor(Math.random() * 100000 + 50000))}
총 주문 금액: ${formatCurrency(alert.recommendedOrder * Math.floor(Math.random() * 100000 + 50000))}
예상 배송일: ${Math.floor(Math.random() * 7 + 3)}일 후

자동 주문을 진행하시겠습니까?`
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
      totalPurchaseAmount,
      purchaseGrowth,
      activeOrders,
      onTimeDelivery,
      activeSuppliers,
      averageRating,
      costSavings,
      savingsPercentage,
      forecastAmount,
      
      // 데이터
      purchaseWorkflow,
      topSuppliers,
      recentActivities,
      inventoryAlerts,
      costOptimizations,
      purchasePatterns,
      purchaseInsights,
      
      // 메서드
      formatCurrency,
      executeAICommand,
      clearAICommand,
      refreshDashboard,
      viewSupplierDetails,
      createPurchaseOrder
    }
  }
}
</script>

<style scoped>
.purchase-module {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

.dashboard-card:hover {
  transform: translateY(-2px);
}

.workflow-stage:hover,
.supplier-item:hover,
.activity-item:hover,
.alert-item:hover,
.optimization-item:hover,
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
  
  .activities-section {
    grid-template-columns: 1fr;
  }
  
  .analytics-section .analytics-grid {
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