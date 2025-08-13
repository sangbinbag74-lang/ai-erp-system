<template>
  <div class="crm-module min-h-screen" style="background: var(--bg-primary); color: var(--text-primary);">
    <!-- 헤더 -->
    <div class="header-section p-6 border-b" style="border-color: var(--border-primary); background: var(--bg-secondary);">
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-3xl font-bold bg-gradient-to-r from-rose-400 to-purple-400 bg-clip-text text-transparent">
            고객 관계 관리 (Customer Relationship Management)
          </h1>
          <p class="text-gray-400 mt-2">AI 기반 고객 분석 및 관계 최적화</p>
        </div>
        <div class="flex items-center space-x-4">
          <div class="agi-status px-4 py-2 rounded-lg" style="background: var(--bg-tertiary); border: 1px solid var(--ai-primary);">
            <span class="text-sm">AGI 상태: </span>
            <span class="text-green-400 font-semibold">{{ agiStatus }}</span>
          </div>
          <button 
            @click="refreshDashboard"
            class="bg-rose-600 hover:bg-rose-700 px-4 py-2 rounded-lg transition-all duration-300 text-white"
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
        <h3 class="text-lg font-semibold mb-3 text-rose-400">AI CRM 어시스턴트</h3>
        <div class="flex space-x-4">
          <textarea 
            v-model="aiCommand"
            placeholder="CRM 관련 자연어 명령을 입력하세요... 예: '고객 이탈 위험 분석해줘', '최적 마케팅 타겟 찾아줘', '고객 생애가치 예측해줘'"
            class="flex-1 p-4 rounded-lg resize-none transition-all duration-300"
            style="background: var(--bg-tertiary); border: 1px solid var(--border-secondary); color: var(--text-primary); min-height: 80px;"
            @focus="$event.target.style.borderColor = 'var(--ai-primary)'"
            @blur="$event.target.style.borderColor = 'var(--border-secondary)'"
          ></textarea>
          <div class="flex flex-col space-y-2">
            <button 
              @click="executeAICommand"
              :disabled="!aiCommand.trim()"
              class="bg-gradient-to-r from-rose-500 to-purple-600 hover:from-rose-600 hover:to-purple-700 disabled:opacity-50 px-6 py-3 rounded-lg transition-all duration-300 text-white font-medium"
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
      <!-- 총 고객 수 -->
      <div class="dashboard-card p-6 rounded-xl transition-all duration-300 hover:scale-105" 
           style="background: var(--bg-secondary); border: 1px solid var(--border-secondary);"
           @mouseenter="$event.target.style.boxShadow = 'var(--glow-primary)'"
           @mouseleave="$event.target.style.boxShadow = 'none'">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm font-medium" style="color: var(--text-secondary);">총 고객 수</p>
            <p class="text-2xl font-bold text-rose-400">{{ totalCustomers.toLocaleString() }}</p>
            <p class="text-xs mt-1" :class="customerGrowth >= 0 ? 'text-green-400' : 'text-red-400'">
              {{ customerGrowth >= 0 ? '+' : '' }}{{ customerGrowth }}% 전월 대비
            </p>
          </div>
          <div class="text-rose-400 text-3xl">👥</div>
        </div>
      </div>

      <!-- 고객 생애가치 -->
      <div class="dashboard-card p-6 rounded-xl transition-all duration-300 hover:scale-105" 
           style="background: var(--bg-secondary); border: 1px solid var(--border-secondary);"
           @mouseenter="$event.target.style.boxShadow = 'var(--glow-secondary)'"
           @mouseleave="$event.target.style.boxShadow = 'none'">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm font-medium" style="color: var(--text-secondary);">평균 고객 생애가치</p>
            <p class="text-2xl font-bold text-purple-400">{{ formatCurrency(avgLifetimeValue) }}</p>
            <p class="text-xs mt-1 text-green-400">{{ lifetimeValueTrend }}% 증가</p>
          </div>
          <div class="text-purple-400 text-3xl">💎</div>
        </div>
      </div>

      <!-- 고객 만족도 -->
      <div class="dashboard-card p-6 rounded-xl transition-all duration-300 hover:scale-105" 
           style="background: var(--bg-secondary); border: 1px solid var(--border-secondary);"
           @mouseenter="$event.target.style.boxShadow = 'var(--glow-accent)'"
           @mouseleave="$event.target.style.boxShadow = 'none'">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm font-medium" style="color: var(--text-secondary);">고객 만족도</p>
            <p class="text-2xl font-bold text-yellow-400">{{ customerSatisfaction }}/5</p>
            <p class="text-xs mt-1 text-green-400">{{ satisfactionTrend }}% 향상</p>
          </div>
          <div class="text-yellow-400 text-3xl">⭐</div>
        </div>
      </div>

      <!-- AI 예측 정확도 -->
      <div class="dashboard-card p-6 rounded-xl transition-all duration-300 hover:scale-105" 
           style="background: var(--bg-secondary); border: 1px solid var(--border-secondary);"
           @mouseenter="$event.target.style.boxShadow = 'var(--glow-primary)'"
           @mouseleave="$event.target.style.boxShadow = 'none'">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm font-medium" style="color: var(--text-secondary);">AI 예측 정확도</p>
            <p class="text-2xl font-bold text-green-400">{{ aiPredictionAccuracy }}%</p>
            <p class="text-xs mt-1 text-green-400">{{ predictionTrend }}% 개선</p>
          </div>
          <div class="text-green-400 text-3xl">🎯</div>
        </div>
      </div>
    </div>

    <!-- 메인 콘텐츠 영역 -->
    <div class="main-content p-6 grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- 고객 세그먼트 분석 -->
      <div class="customer-segments p-6 rounded-xl" style="background: var(--bg-secondary); border: 1px solid var(--border-secondary);">
        <h3 class="text-xl font-semibold mb-4 text-rose-400">AI 고객 세그먼트 분석</h3>
        <div class="space-y-4">
          <div v-for="segment in customerSegments" :key="segment.name" 
               class="segment-item p-4 rounded-lg transition-all duration-300 hover:scale-102 cursor-pointer"
               style="background: var(--bg-tertiary); border: 1px solid var(--border-primary);"
               @click="viewSegmentDetails(segment)">
            <div class="flex items-center justify-between mb-2">
              <h4 class="font-medium text-white">{{ segment.name }}</h4>
              <span class="text-sm px-2 py-1 rounded" 
                    :style="`background: ${segment.color}20; color: ${segment.color};`">
                {{ segment.percentage }}%
              </span>
            </div>
            <div class="grid grid-cols-2 gap-4 text-sm">
              <div>
                <span style="color: var(--text-tertiary);">고객 수:</span>
                <span class="ml-2 font-medium text-white">{{ segment.customerCount.toLocaleString() }}명</span>
              </div>
              <div>
                <span style="color: var(--text-tertiary);">평균 구매액:</span>
                <span class="ml-2 font-medium text-cyan-400">{{ formatCurrency(segment.avgPurchase) }}</span>
              </div>
            </div>
            <div class="mt-2 grid grid-cols-2 gap-4 text-sm">
              <div>
                <span style="color: var(--text-tertiary);">생애가치:</span>
                <span class="ml-2 font-medium text-green-400">{{ formatCurrency(segment.lifetimeValue) }}</span>
              </div>
              <div>
                <span style="color: var(--text-tertiary);">이탈 위험:</span>
                <span class="ml-2 font-medium" :class="segment.churnRisk < 20 ? 'text-green-400' : segment.churnRisk < 50 ? 'text-yellow-400' : 'text-red-400'">
                  {{ segment.churnRisk }}%
                </span>
              </div>
            </div>
            <div class="mt-3">
              <div class="w-full h-2 rounded-full" style="background: var(--bg-hover);">
                <div class="h-full rounded-full transition-all duration-500" 
                     :style="`width: ${segment.percentage}%; background: ${segment.color};`">
                </div>
              </div>
              <div class="mt-1 text-xs" style="color: var(--text-tertiary);">
                AI 추천 전략: {{ segment.strategy }}
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 고객 활동 분석 -->
      <div class="customer-activity p-6 rounded-xl" style="background: var(--bg-secondary); border: 1px solid var(--border-secondary);">
        <h3 class="text-xl font-semibold mb-4 text-purple-400">고객 활동 분석</h3>
        <div class="space-y-4">
          <div v-for="customer in topCustomers" :key="customer.id"
               class="customer-item p-4 rounded-lg transition-all duration-300 hover:scale-102 cursor-pointer"
               style="background: var(--bg-tertiary); border: 1px solid var(--border-primary);"
               @click="viewCustomerDetails(customer)">
            <div class="flex items-center justify-between mb-2">
              <div class="flex items-center space-x-3">
                <div class="w-10 h-10 rounded-full flex items-center justify-center" 
                     :style="`background: ${customer.color}20; color: ${customer.color};`">
                  {{ customer.name.charAt(0) }}
                </div>
                <div>
                  <h4 class="font-medium text-white">{{ customer.name }}</h4>
                  <p class="text-xs" style="color: var(--text-tertiary);">{{ customer.company }}</p>
                </div>
              </div>
              <span class="text-sm px-2 py-1 rounded" 
                    :style="`background: ${customer.tier === 'VIP' ? '#ef4444' : customer.tier === 'Premium' ? '#f59e0b' : '#10b981'}20; 
                             color: ${customer.tier === 'VIP' ? '#ef4444' : customer.tier === 'Premium' ? '#f59e0b' : '#10b981'};`">
                {{ customer.tier }}
              </span>
            </div>
            <div class="grid grid-cols-2 gap-4 text-sm">
              <div>
                <span style="color: var(--text-tertiary);">총 구매액:</span>
                <span class="ml-2 font-medium text-white">{{ formatCurrency(customer.totalPurchase) }}</span>
              </div>
              <div>
                <span style="color: var(--text-tertiary);">최근 활동:</span>
                <span class="ml-2 font-medium text-cyan-400">{{ customer.lastActivity }}</span>
              </div>
            </div>
            <div class="mt-2 grid grid-cols-2 gap-4 text-sm">
              <div>
                <span style="color: var(--text-tertiary);">만족도:</span>
                <span class="ml-2 font-medium text-yellow-400">{{ customer.satisfaction }}/5</span>
              </div>
              <div>
                <span style="color: var(--text-tertiary);">AI 점수:</span>
                <span class="ml-2 font-medium text-purple-400">{{ customer.aiScore }}/100</span>
              </div>
            </div>
            <div class="mt-2">
              <span class="text-xs" style="color: var(--text-tertiary);">
                AI 예측: {{ customer.aiPrediction }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- CRM 관리 및 분석 -->
    <div class="crm-management-section p-6 grid grid-cols-1 xl:grid-cols-3 gap-6">
      <!-- 이탈 위험 고객 -->
      <div class="churn-risk p-6 rounded-xl" style="background: var(--bg-secondary); border: 1px solid var(--border-secondary);">
        <h3 class="text-xl font-semibold mb-4 text-red-400">이탈 위험 고객</h3>
        <div class="space-y-3 max-h-64 overflow-y-auto">
          <div v-for="customer in churnRiskCustomers" :key="customer.id"
               class="risk-customer-item p-3 rounded-lg transition-all duration-300 hover:scale-102 cursor-pointer"
               style="background: var(--bg-tertiary); border: 1px solid var(--border-primary);"
               @click="viewChurnAnalysis(customer)">
            <div class="flex items-center justify-between mb-2">
              <h4 class="font-medium text-white">{{ customer.name }}</h4>
              <span class="text-xs px-2 py-1 rounded" 
                    :style="`background: ${customer.riskLevel === 'high' ? '#ef4444' : customer.riskLevel === 'medium' ? '#f59e0b' : '#3b82f6'}20; 
                             color: ${customer.riskLevel === 'high' ? '#ef4444' : customer.riskLevel === 'medium' ? '#f59e0b' : '#3b82f6'};`">
                {{ customer.riskLevel === 'high' ? '높음' : customer.riskLevel === 'medium' ? '보통' : '낮음' }}
              </span>
            </div>
            <div class="grid grid-cols-2 gap-2 text-sm">
              <div>
                <span style="color: var(--text-tertiary);">이탈 확률:</span>
                <span class="ml-1 font-medium text-red-400">{{ customer.churnProbability }}%</span>
              </div>
              <div>
                <span style="color: var(--text-tertiary);">가치:</span>
                <span class="ml-1 font-medium text-green-400">{{ formatCurrency(customer.value) }}</span>
              </div>
            </div>
            <div class="mt-2 text-sm">
              <span style="color: var(--text-tertiary);">마지막 구매:</span>
              <span class="ml-2 font-medium text-white">{{ customer.lastPurchase }}</span>
            </div>
            <div class="mt-2">
              <span class="text-xs" style="color: var(--text-tertiary);">
                AI 제안: {{ customer.retentionStrategy }}
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- 마케팅 기회 -->
      <div class="marketing-opportunities p-6 rounded-xl" style="background: var(--bg-secondary); border: 1px solid var(--border-secondary);">
        <h3 class="text-xl font-semibold mb-4 text-green-400">AI 마케팅 기회</h3>
        <div class="space-y-3 max-h-64 overflow-y-auto">
          <div v-for="opportunity in marketingOpportunities" :key="opportunity.id"
               class="opportunity-item p-3 rounded-lg transition-all duration-300 hover:scale-102"
               style="background: var(--bg-tertiary); border: 1px solid var(--border-primary);">
            <div class="flex items-center justify-between mb-2">
              <h4 class="font-medium text-white">{{ opportunity.title }}</h4>
              <span class="text-xs px-2 py-1 rounded" 
                    :style="`background: ${opportunity.potential === 'high' ? '#10b981' : opportunity.potential === 'medium' ? '#f59e0b' : '#3b82f6'}20; 
                             color: ${opportunity.potential === 'high' ? '#10b981' : opportunity.potential === 'medium' ? '#f59e0b' : '#3b82f6'};`">
                {{ opportunity.potential === 'high' ? '높음' : opportunity.potential === 'medium' ? '보통' : '낮음' }}
              </span>
            </div>
            <p class="text-sm mb-2" style="color: var(--text-secondary);">{{ opportunity.description }}</p>
            <div class="grid grid-cols-2 gap-2 text-sm">
              <div>
                <span style="color: var(--text-tertiary);">대상 고객:</span>
                <span class="ml-1 font-medium text-white">{{ opportunity.targetCount }}명</span>
              </div>
              <div>
                <span style="color: var(--text-tertiary);">예상 수익:</span>
                <span class="ml-1 font-medium text-green-400">{{ formatCurrency(opportunity.expectedRevenue) }}</span>
              </div>
            </div>
            <div class="mt-2">
              <span class="text-xs" style="color: var(--text-tertiary);">
                성공 확률: {{ opportunity.successRate }}% | ROI: {{ opportunity.roi }}%
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- 고객 피드백 분석 -->
      <div class="feedback-analysis p-6 rounded-xl" style="background: var(--bg-secondary); border: 1px solid var(--border-secondary);">
        <h3 class="text-xl font-semibold mb-4 text-blue-400">AI 피드백 분석</h3>
        <div class="space-y-4">
          <div v-for="feedback in customerFeedbacks" :key="feedback.id"
               class="feedback-item p-3 rounded-lg"
               style="background: var(--bg-tertiary); border: 1px solid var(--border-primary);">
            <div class="flex items-center justify-between mb-2">
              <span class="text-sm font-medium text-white">{{ feedback.category }}</span>
              <span class="text-sm font-bold" :class="feedback.sentiment === 'positive' ? 'text-green-400' : feedback.sentiment === 'neutral' ? 'text-yellow-400' : 'text-red-400'">
                {{ feedback.sentiment === 'positive' ? '긍정' : feedback.sentiment === 'neutral' ? '중립' : '부정' }}
              </span>
            </div>
            <div class="grid grid-cols-2 gap-2 text-sm">
              <div>
                <span style="color: var(--text-tertiary);">피드백 수:</span>
                <span class="ml-1 font-medium text-white">{{ feedback.count }}건</span>
              </div>
              <div>
                <span style="color: var(--text-tertiary);">점수:</span>
                <span class="ml-1 font-medium text-cyan-400">{{ feedback.score }}/5</span>
              </div>
            </div>
            <div class="mt-2">
              <div class="w-full h-1.5 rounded-full" style="background: var(--bg-hover);">
                <div class="h-full rounded-full transition-all duration-500" 
                     :style="`width: ${(feedback.score / 5) * 100}%; background: ${feedback.sentiment === 'positive' ? '#10b981' : feedback.sentiment === 'neutral' ? '#f59e0b' : '#ef4444'};`">
                </div>
              </div>
              <div class="flex justify-between mt-1 text-xs" style="color: var(--text-tertiary);">
                <span>트렌드: {{ feedback.trend }}</span>
                <span>개선 필요도: {{ feedback.improvementNeeded }}%</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- CRM 인사이트 및 예측 -->
    <div class="insights-section p-6">
      <div class="insights-grid grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- 고객 여정 분석 -->
        <div class="customer-journey p-6 rounded-xl" style="background: var(--bg-secondary); border: 1px solid var(--border-secondary);">
          <h3 class="text-xl font-semibold mb-4 text-rose-400">고객 여정 분석</h3>
          <div class="journey-stages space-y-4">
            <div v-for="stage in customerJourney" :key="stage.name"
                 class="stage-item p-4 rounded-lg"
                 style="background: var(--bg-tertiary); border: 1px solid var(--border-primary);">
              <div class="flex items-center justify-between mb-2">
                <span class="text-sm font-medium text-white">{{ stage.name }}</span>
                <span class="text-sm font-bold" :style="`color: ${stage.color};`">
                  {{ stage.conversionRate }}%
                </span>
              </div>
              <div class="grid grid-cols-2 gap-4 text-sm">
                <div>
                  <span style="color: var(--text-tertiary);">고객 수:</span>
                  <span class="ml-2 font-medium text-white">{{ stage.customerCount.toLocaleString() }}명</span>
                </div>
                <div>
                  <span style="color: var(--text-tertiary);">평균 시간:</span>
                  <span class="ml-2 font-medium text-cyan-400">{{ stage.avgTime }}</span>
                </div>
              </div>
              <div class="mt-2">
                <div class="w-full h-2 rounded-full" style="background: var(--bg-hover);">
                  <div class="h-full rounded-full transition-all duration-500" 
                       :style="`width: ${stage.conversionRate}%; background: ${stage.color};`">
                  </div>
                </div>
                <div class="flex justify-between mt-1 text-xs" style="color: var(--text-tertiary);">
                  <span>전환율</span>
                  <span>개선 포인트: {{ stage.improvementPoint }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- AI CRM 인사이트 -->
        <div class="crm-insights p-6 rounded-xl" style="background: var(--bg-secondary); border: 1px solid var(--border-secondary);">
          <h3 class="text-xl font-semibold mb-4 text-purple-400">AI CRM 인사이트</h3>
          <div class="insights-list space-y-3">
            <div v-for="insight in crmInsights" :key="insight.id"
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
                      신뢰도: {{ insight.confidence }}%
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
  name: 'CRMModule',
  setup() {
    const { executeAIRequest, formatResponse } = useAI()
    
    // 반응형 데이터
    const agiStatus = ref('활성화됨')
    const aiCommand = ref('')
    const aiResponse = ref('')
    
    // 대시보드 메트릭
    const totalCustomers = ref(15847)
    const customerGrowth = ref(12.3)
    const avgLifetimeValue = ref(2850000)
    const lifetimeValueTrend = ref(18.7)
    const customerSatisfaction = ref(4.2)
    const satisfactionTrend = ref(8.5)
    const aiPredictionAccuracy = ref(91.8)
    const predictionTrend = ref(6.9)
    
    // 고객 세그먼트
    const customerSegments = ref([
      {
        name: 'VIP 고객',
        percentage: 15,
        customerCount: 2377,
        avgPurchase: 8500000,
        lifetimeValue: 45000000,
        churnRisk: 12,
        color: '#ef4444',
        strategy: '개인 맞춤 서비스 강화'
      },
      {
        name: '충성 고객',
        percentage: 35,
        customerCount: 5546,
        avgPurchase: 3200000,
        lifetimeValue: 18500000,
        churnRisk: 18,
        color: '#10b981',
        strategy: '리워드 프로그램 확대'
      },
      {
        name: '일반 고객',
        percentage: 40,
        customerCount: 6339,
        avgPurchase: 1200000,
        lifetimeValue: 8500000,
        churnRisk: 35,
        color: '#3b82f6',
        strategy: '가치 제안 강화'
      },
      {
        name: '신규 고객',
        percentage: 10,
        customerCount: 1585,
        avgPurchase: 580000,
        lifetimeValue: 3200000,
        churnRisk: 45,
        color: '#f59e0b',
        strategy: '온보딩 프로세스 개선'
      }
    ])
    
    // 상위 고객
    const topCustomers = ref([
      {
        id: 1,
        name: '김대기업',
        company: '글로벌테크(주)',
        totalPurchase: 125000000,
        lastActivity: '2일 전',
        satisfaction: 4.8,
        aiScore: 95,
        tier: 'VIP',
        color: '#ef4444',
        aiPrediction: '장기 파트너십 가능성 높음'
      },
      {
        id: 2,
        name: '이중견기업',
        company: '스마트솔루션',
        totalPurchase: 85000000,
        lastActivity: '1주 전',
        satisfaction: 4.5,
        aiScore: 88,
        tier: 'Premium',
        color: '#f59e0b',
        aiPrediction: '추가 구매 가능성 높음'
      },
      {
        id: 3,
        name: '박벤처',
        company: '혁신스타트업',
        totalPurchase: 45000000,
        lastActivity: '3일 전',
        satisfaction: 4.3,
        aiScore: 82,
        tier: 'Standard',
        color: '#10b981',
        aiPrediction: '성장 잠재력 우수'
      },
      {
        id: 4,
        name: '최제조업',
        company: '전통제조(주)',
        totalPurchase: 65000000,
        lastActivity: '5일 전',
        satisfaction: 4.1,
        aiScore: 79,
        tier: 'Premium',
        color: '#3b82f6',
        aiPrediction: '디지털 전환 지원 필요'
      }
    ])
    
    // 이탈 위험 고객
    const churnRiskCustomers = ref([
      {
        id: 1,
        name: '위험고객A',
        churnProbability: 78,
        value: 25000000,
        lastPurchase: '3개월 전',
        riskLevel: 'high',
        retentionStrategy: '개인 상담 및 특별 할인'
      },
      {
        id: 2,
        name: '위험고객B',
        churnProbability: 65,
        value: 18000000,
        lastPurchase: '2개월 전',
        riskLevel: 'medium',
        retentionStrategy: '신제품 소개 및 데모'
      },
      {
        id: 3,
        name: '위험고객C',
        churnProbability: 52,
        value: 12000000,
        lastPurchase: '1개월 전',
        riskLevel: 'medium',
        retentionStrategy: '고객 만족도 조사'
      }
    ])
    
    // 마케팅 기회
    const marketingOpportunities = ref([
      {
        id: 1,
        title: '크로스셀링 기회',
        description: 'AI가 식별한 추가 제품 구매 가능성이 높은 고객군',
        targetCount: 1250,
        expectedRevenue: 185000000,
        successRate: 67,
        roi: 340,
        potential: 'high'
      },
      {
        id: 2,
        title: '업셀링 캠페인',
        description: '상위 제품으로 업그레이드 가능성이 높은 기존 고객',
        targetCount: 890,
        expectedRevenue: 125000000,
        successRate: 54,
        roi: 280,
        potential: 'medium'
      },
      {
        id: 3,
        title: '재구매 촉진',
        description: '구매 주기 분석을 통한 적정 시점 리마케팅',
        targetCount: 2100,
        expectedRevenue: 95000000,
        successRate: 42,
        roi: 220,
        potential: 'medium'
      }
    ])
    
    // 고객 피드백
    const customerFeedbacks = ref([
      {
        id: 1,
        category: '제품 품질',
        count: 1250,
        score: 4.3,
        sentiment: 'positive',
        trend: '상승',
        improvementNeeded: 15
      },
      {
        id: 2,
        category: '고객 서비스',
        count: 980,
        score: 3.8,
        sentiment: 'neutral',
        trend: '안정',
        improvementNeeded: 35
      },
      {
        id: 3,
        category: '배송 서비스',
        count: 750,
        score: 4.1,
        sentiment: 'positive',
        trend: '상승',
        improvementNeeded: 20
      },
      {
        id: 4,
        category: '가격 경쟁력',
        count: 650,
        score: 3.2,
        sentiment: 'negative',
        trend: '하락',
        improvementNeeded: 55
      }
    ])
    
    // 고객 여정
    const customerJourney = ref([
      {
        name: '인지',
        customerCount: 50000,
        conversionRate: 15,
        avgTime: '2주',
        color: '#8b5cf6',
        improvementPoint: '브랜드 인지도 개선'
      },
      {
        name: '관심',
        customerCount: 7500,
        conversionRate: 35,
        avgTime: '1주',
        color: '#3b82f6',
        improvementPoint: '콘텐츠 마케팅 강화'
      },
      {
        name: '검토',
        customerCount: 2625,
        conversionRate: 60,
        avgTime: '3일',
        color: '#f59e0b',
        improvementPoint: '제품 데모 개선'
      },
      {
        name: '구매',
        customerCount: 1575,
        conversionRate: 85,
        avgTime: '1일',
        color: '#10b981',
        improvementPoint: '결제 프로세스 간소화'
      },
      {
        name: '재구매',
        customerCount: 1339,
        conversionRate: 70,
        avgTime: '6개월',
        color: '#ef4444',
        improvementPoint: '고객 관계 관리 강화'
      }
    ])
    
    // CRM 인사이트
    const crmInsights = ref([
      {
        id: 1,
        title: '고객 행동 패턴 변화 감지',
        description: '코로나19 이후 온라인 구매 패턴이 45% 증가했습니다. 디지털 채널 강화가 필요합니다.',
        impact: 'high',
        confidence: 94,
        icon: '📊',
        color: '#3b82f6'
      },
      {
        id: 2,
        title: '계절성 수요 예측',
        description: '연말 프로모션 시즌에 특정 제품군의 수요가 180% 증가할 것으로 예상됩니다.',
        impact: 'high',
        confidence: 87,
        icon: '📈',
        color: '#10b981'
      },
      {
        id: 3,
        title: '고객 세그먼트 진화',
        description: '신규 고객의 30%가 모바일 우선 사용자로 분류됩니다. 모바일 경험 개선이 필요합니다.',
        impact: 'medium',
        confidence: 82,
        icon: '📱',
        color: '#f59e0b'
      },
      {
        id: 4,
        title: '피드백 분석 인사이트',
        description: 'AI 텍스트 분석 결과, 고객들이 가장 중요하게 생각하는 요소는 "신속한 대응"입니다.',
        impact: 'medium',
        confidence: 79,
        icon: '💬',
        color: '#8b5cf6'
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
        const response = await executeAIRequest(aiCommand.value, 'crm')
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
      totalCustomers.value += Math.floor(Math.random() * 20)
      avgLifetimeValue.value += Math.floor(Math.random() * 100000)
      customerSatisfaction.value = Math.round((customerSatisfaction.value + Math.random() * 0.2 - 0.1) * 10) / 10
    }
    
    const viewSegmentDetails = (segment) => {
      aiResponse.value = `고객 세그먼트 상세 분석:
      
세그먼트: ${segment.name}
전체 고객 대비 비율: ${segment.percentage}%
고객 수: ${segment.customerCount.toLocaleString()}명

구매 행동 분석:
- 평균 구매액: ${formatCurrency(segment.avgPurchase)}
- 생애가치: ${formatCurrency(segment.lifetimeValue)}
- 이탈 위험도: ${segment.churnRisk}%

AI 세그먼트 특성:
${segment.name === 'VIP 고객' ? '- 최고 가치 고객으로 개인화된 서비스 필요' : 
  segment.name === '충성 고객' ? '- 안정적인 수익원으로 관계 유지 중요' :
  segment.name === '일반 고객' ? '- 상위 세그먼트로 전환 가능성 보유' : 
  '- 조기 이탈 방지 및 관계 구축 필요'}

추천 마케팅 전략: ${segment.strategy}

구체적 액션 플랜:
1. ${segment.churnRisk > 30 ? '이탈 방지 프로그램 우선 실행' : '업셀링/크로스셀링 기회 발굴'}
2. ${segment.avgPurchase > 5000000 ? '프리미엄 서비스 제공' : '가치 인식 개선 캠페인'}
3. ${segment.percentage > 30 ? '세그먼트 내 하위 분류 검토' : '세그먼트 확대 전략 수립'}`
    }
    
    const viewCustomerDetails = (customer) => {
      aiResponse.value = `고객 상세 프로필:
      
고객명: ${customer.name}
소속: ${customer.company}
고객 등급: ${customer.tier}
AI 점수: ${customer.aiScore}/100

거래 현황:
- 총 구매액: ${formatCurrency(customer.totalPurchase)}
- 최근 활동: ${customer.lastActivity}
- 만족도: ${customer.satisfaction}/5.0

AI 종합 평가:
${customer.aiScore >= 90 ? '최우선 관리 대상 고객' : customer.aiScore >= 80 ? '핵심 고객으로 지속 관리 필요' : '잠재력 보유 고객으로 관심 필요'}
${customer.satisfaction >= 4.5 ? '매우 높은 만족도' : customer.satisfaction >= 4.0 ? '양호한 만족도' : '만족도 개선 필요'}

AI 예측: ${customer.aiPrediction}

맞춤 액션 플랜:
1. ${customer.tier === 'VIP' ? '전담 계정 매니저 배정' : customer.tier === 'Premium' ? '정기 소통 및 관리' : '잠재 가치 발굴'}
2. ${customer.satisfaction < 4.0 ? '만족도 개선 프로그램 참여' : '현재 서비스 수준 유지'}
3. ${customer.totalPurchase > 100000000 ? '전략적 파트너십 검토' : '추가 사업 기회 탐색'}

다음 액션 예정일: ${Math.floor(Math.random() * 14 + 1)}일 후`
    }
    
    const viewChurnAnalysis = (customer) => {
      aiResponse.value = `이탈 위험 고객 분석:
      
고객명: ${customer.name}
이탈 확률: ${customer.churnProbability}%
고객 가치: ${formatCurrency(customer.value)}
위험 수준: ${customer.riskLevel === 'high' ? '높음' : customer.riskLevel === 'medium' ? '보통' : '낮음'}

위험 요인 분석:
- 마지막 구매: ${customer.lastPurchase}
- 구매 패턴 변화: ${customer.churnProbability > 70 ? '급격한 감소' : customer.churnProbability > 50 ? '점진적 감소' : '일시적 변화'}
- 서비스 이용률: ${customer.churnProbability > 60 ? '현저히 낮음' : '보통 수준'}

AI 추천 보유 전략: ${customer.retentionStrategy}

즉시 실행 가능한 액션:
1. ${customer.churnProbability > 70 ? '48시간 내 직접 연락' : '1주일 내 개인화된 제안'}
2. ${customer.value > 20000000 ? '임원급 미팅 주선' : '전문 상담사 배정'}
3. ${customer.lastPurchase.includes('개월') ? '특별 할인 및 인센티브 제공' : '신제품/서비스 소개'}

예상 보유 성공률: ${100 - customer.churnProbability + Math.floor(Math.random() * 20)}%
투자 대비 효과: ${Math.floor(customer.value / 1000000 * 2.5)}배`
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
      totalCustomers,
      customerGrowth,
      avgLifetimeValue,
      lifetimeValueTrend,
      customerSatisfaction,
      satisfactionTrend,
      aiPredictionAccuracy,
      predictionTrend,
      
      // 데이터
      customerSegments,
      topCustomers,
      churnRiskCustomers,
      marketingOpportunities,
      customerFeedbacks,
      customerJourney,
      crmInsights,
      
      // 메서드
      formatCurrency,
      executeAICommand,
      clearAICommand,
      refreshDashboard,
      viewSegmentDetails,
      viewCustomerDetails,
      viewChurnAnalysis
    }
  }
}
</script>

<style scoped>
.crm-module {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

.dashboard-card:hover {
  transform: translateY(-2px);
}

.segment-item:hover,
.customer-item:hover,
.risk-customer-item:hover,
.opportunity-item:hover,
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
  
  .crm-management-section {
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