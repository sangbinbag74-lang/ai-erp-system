<template>
  <div class="sales-module min-h-screen" style="background: var(--bg-primary); color: var(--text-primary);">
    <!-- 헤더 -->
    <div class="header-section p-6 border-b" style="border-color: var(--border-primary); background: var(--bg-secondary);">
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-3xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
            영업 관리 (Sales Management)
          </h1>
          <p class="text-gray-400 mt-2">AI 기반 영업 프로세스 최적화 및 매출 예측</p>
        </div>
        <div class="flex items-center space-x-4">
          <div class="agi-status px-4 py-2 rounded-lg" style="background: var(--bg-tertiary); border: 1px solid var(--ai-primary);">
            <span class="text-sm">AGI 상태: </span>
            <span class="text-green-400 font-semibold">{{ agiStatus }}</span>
          </div>
          <button 
            @click="refreshDashboard"
            class="bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded-lg transition-all duration-300 text-white"
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
        <h3 class="text-lg font-semibold mb-3 text-blue-400">AI 영업 어시스턴트</h3>
        <div class="flex space-x-4">
          <textarea 
            v-model="aiCommand"
            placeholder="영업 관련 자연어 명령을 입력하세요... 예: '이번 분기 매출 예측해줘', '새로운 리드 분석해줘', '고객 세그먼트별 매출 보여줘'"
            class="flex-1 p-4 rounded-lg resize-none transition-all duration-300"
            style="background: var(--bg-tertiary); border: 1px solid var(--border-secondary); color: var(--text-primary); min-height: 80px;"
            @focus="$event.target.style.borderColor = 'var(--ai-primary)'"
            @blur="$event.target.style.borderColor = 'var(--border-secondary)'"
          ></textarea>
          <div class="flex flex-col space-y-2">
            <button 
              @click="executeAICommand"
              :disabled="!aiCommand.trim()"
              class="bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 disabled:opacity-50 px-6 py-3 rounded-lg transition-all duration-300 text-white font-medium"
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
      <!-- 총 매출 -->
      <div class="dashboard-card p-6 rounded-xl transition-all duration-300 hover:scale-105" 
           style="background: var(--bg-secondary); border: 1px solid var(--border-secondary);"
           @mouseenter="$event.target.style.boxShadow = 'var(--glow-primary)'"
           @mouseleave="$event.target.style.boxShadow = 'none'">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm font-medium" style="color: var(--text-secondary);">총 매출</p>
            <p class="text-2xl font-bold text-blue-400">{{ formatCurrency(totalRevenue) }}</p>
            <p class="text-xs mt-1" :class="revenueGrowth >= 0 ? 'text-green-400' : 'text-red-400'">
              {{ revenueGrowth >= 0 ? '+' : '' }}{{ revenueGrowth }}% 전월 대비
            </p>
          </div>
          <div class="text-blue-400 text-3xl">💰</div>
        </div>
      </div>

      <!-- 신규 리드 -->
      <div class="dashboard-card p-6 rounded-xl transition-all duration-300 hover:scale-105" 
           style="background: var(--bg-secondary); border: 1px solid var(--border-secondary);"
           @mouseenter="$event.target.style.boxShadow = 'var(--glow-secondary)'"
           @mouseleave="$event.target.style.boxShadow = 'none'">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm font-medium" style="color: var(--text-secondary);">신규 리드</p>
            <p class="text-2xl font-bold text-orange-400">{{ newLeads }}</p>
            <p class="text-xs mt-1 text-green-400">+{{ leadsGrowth }}% 지난주 대비</p>
          </div>
          <div class="text-orange-400 text-3xl">🎯</div>
        </div>
      </div>

      <!-- 전환율 -->
      <div class="dashboard-card p-6 rounded-xl transition-all duration-300 hover:scale-105" 
           style="background: var(--bg-secondary); border: 1px solid var(--border-secondary);"
           @mouseenter="$event.target.style.boxShadow = 'var(--glow-accent)'"
           @mouseleave="$event.target.style.boxShadow = 'none'">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm font-medium" style="color: var(--text-secondary);">리드 전환율</p>
            <p class="text-2xl font-bold text-purple-400">{{ conversionRate }}%</p>
            <p class="text-xs mt-1 text-green-400">업계 평균 15% 초과</p>
          </div>
          <div class="text-purple-400 text-3xl">📈</div>
        </div>
      </div>

      <!-- 평균 거래 규모 -->
      <div class="dashboard-card p-6 rounded-xl transition-all duration-300 hover:scale-105" 
           style="background: var(--bg-secondary); border: 1px solid var(--border-secondary);"
           @mouseenter="$event.target.style.boxShadow = 'var(--glow-primary)'"
           @mouseleave="$event.target.style.boxShadow = 'none'">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm font-medium" style="color: var(--text-secondary);">평균 거래액</p>
            <p class="text-2xl font-bold text-green-400">{{ formatCurrency(avgDealSize) }}</p>
            <p class="text-xs mt-1 text-green-400">+{{ dealSizeGrowth }}% 증가</p>
          </div>
          <div class="text-green-400 text-3xl">💎</div>
        </div>
      </div>
    </div>

    <!-- 메인 콘텐츠 영역 -->
    <div class="main-content p-6 grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- 영업 파이프라인 -->
      <div class="pipeline-section p-6 rounded-xl" style="background: var(--bg-secondary); border: 1px solid var(--border-secondary);">
        <h3 class="text-xl font-semibold mb-4 text-blue-400">AI 영업 파이프라인</h3>
        <div class="space-y-4">
          <div v-for="stage in pipelineStages" :key="stage.name" 
               class="pipeline-stage p-4 rounded-lg transition-all duration-300 hover:scale-102"
               style="background: var(--bg-tertiary); border: 1px solid var(--border-primary);">
            <div class="flex items-center justify-between mb-2">
              <h4 class="font-medium text-white">{{ stage.name }}</h4>
              <span class="text-sm px-2 py-1 rounded" 
                    :style="`background: ${stage.color}20; color: ${stage.color};`">
                {{ stage.count }}개
              </span>
            </div>
            <div class="flex items-center justify-between">
              <span class="text-sm" style="color: var(--text-secondary);">
                {{ formatCurrency(stage.value) }}
              </span>
              <div class="w-16 h-2 rounded-full" style="background: var(--bg-hover);">
                <div class="h-full rounded-full transition-all duration-300" 
                     :style="`width: ${stage.probability}%; background: ${stage.color};`">
                </div>
              </div>
            </div>
            <div class="mt-2">
              <span class="text-xs" style="color: var(--text-tertiary);">
                AI 예측 성공률: {{ stage.probability }}%
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- 고객 세그먼트 분석 -->
      <div class="customer-analysis p-6 rounded-xl" style="background: var(--bg-secondary); border: 1px solid var(--border-secondary);">
        <h3 class="text-xl font-semibold mb-4 text-purple-400">AI 고객 세그먼트 분석</h3>
        <div class="space-y-4">
          <div v-for="segment in customerSegments" :key="segment.name"
               class="segment-item p-4 rounded-lg transition-all duration-300 hover:scale-102"
               style="background: var(--bg-tertiary); border: 1px solid var(--border-primary);">
            <div class="flex items-center justify-between mb-2">
              <h4 class="font-medium text-white">{{ segment.name }}</h4>
              <div class="flex items-center space-x-2">
                <span class="text-sm px-2 py-1 rounded" 
                      :style="`background: ${segment.color}20; color: ${segment.color};`">
                  {{ segment.percentage }}%
                </span>
                <span class="text-xs" :style="`color: ${segment.color};`">
                  {{ segment.trend === 'up' ? '↗️' : segment.trend === 'down' ? '↘️' : '➡️' }}
                </span>
              </div>
            </div>
            <div class="grid grid-cols-2 gap-4 text-sm">
              <div>
                <span style="color: var(--text-tertiary);">평균 거래액:</span>
                <span class="ml-2 font-medium text-white">{{ formatCurrency(segment.avgValue) }}</span>
              </div>
              <div>
                <span style="color: var(--text-tertiary);">생애 가치:</span>
                <span class="ml-2 font-medium text-green-400">{{ formatCurrency(segment.lifetime) }}</span>
              </div>
            </div>
            <div class="mt-2">
              <span class="text-xs" style="color: var(--text-tertiary);">
                AI 추천 전략: {{ segment.strategy }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 영업 활동 및 기회 관리 -->
    <div class="activities-section p-6 grid grid-cols-1 xl:grid-cols-3 gap-6">
      <!-- 최근 영업 활동 -->
      <div class="recent-activities p-6 rounded-xl" style="background: var(--bg-secondary); border: 1px solid var(--border-secondary);">
        <h3 class="text-xl font-semibold mb-4 text-blue-400">최근 영업 활동</h3>
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

      <!-- 영업 기회 -->
      <div class="opportunities p-6 rounded-xl" style="background: var(--bg-secondary); border: 1px solid var(--border-secondary);">
        <h3 class="text-xl font-semibold mb-4 text-green-400">AI 예측 영업 기회</h3>
        <div class="space-y-3 max-h-64 overflow-y-auto">
          <div v-for="opportunity in salesOpportunities" :key="opportunity.id"
               class="opportunity-item p-3 rounded-lg transition-all duration-300 hover:scale-102 cursor-pointer"
               style="background: var(--bg-tertiary); border: 1px solid var(--border-primary);"
               @click="viewOpportunityDetails(opportunity)">
            <div class="flex items-center justify-between mb-2">
              <h4 class="font-medium text-white">{{ opportunity.company }}</h4>
              <span class="text-xs px-2 py-1 rounded" 
                    :style="`background: ${opportunity.priority === 'high' ? '#ef4444' : opportunity.priority === 'medium' ? '#f59e0b' : '#10b981'}20; 
                             color: ${opportunity.priority === 'high' ? '#ef4444' : opportunity.priority === 'medium' ? '#f59e0b' : '#10b981'};`">
                {{ opportunity.priority === 'high' ? '높음' : opportunity.priority === 'medium' ? '보통' : '낮음' }}
              </span>
            </div>
            <p class="text-sm mb-2" style="color: var(--text-secondary);">{{ opportunity.description }}</p>
            <div class="flex items-center justify-between">
              <span class="text-sm font-medium text-green-400">{{ formatCurrency(opportunity.value) }}</span>
              <span class="text-xs" style="color: var(--text-tertiary);">
                AI 성공률: {{ opportunity.aiScore }}%
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- 성과 지표 -->
      <div class="performance-metrics p-6 rounded-xl" style="background: var(--bg-secondary); border: 1px solid var(--border-secondary);">
        <h3 class="text-xl font-semibold mb-4 text-purple-400">AI 성과 지표</h3>
        <div class="space-y-4">
          <div v-for="metric in performanceMetrics" :key="metric.name"
               class="metric-item p-3 rounded-lg"
               style="background: var(--bg-tertiary); border: 1px solid var(--border-primary);">
            <div class="flex items-center justify-between mb-2">
              <span class="text-sm font-medium text-white">{{ metric.name }}</span>
              <span class="text-sm font-bold" :style="`color: ${metric.color};`">
                {{ metric.value }}{{ metric.unit }}
              </span>
            </div>
            <div class="w-full h-2 rounded-full" style="background: var(--bg-hover);">
              <div class="h-full rounded-full transition-all duration-500" 
                   :style="`width: ${metric.percentage}%; background: ${metric.color};`">
              </div>
            </div>
            <div class="flex items-center justify-between mt-1">
              <span class="text-xs" style="color: var(--text-tertiary);">목표: {{ metric.target }}{{ metric.unit }}</span>
              <span class="text-xs" :class="metric.change >= 0 ? 'text-green-400' : 'text-red-400'">
                {{ metric.change >= 0 ? '+' : '' }}{{ metric.change }}%
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 영업 예측 및 인사이트 -->
    <div class="insights-section p-6">
      <div class="insights-grid grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- AI 매출 예측 -->
        <div class="revenue-forecast p-6 rounded-xl" style="background: var(--bg-secondary); border: 1px solid var(--border-secondary);">
          <h3 class="text-xl font-semibold mb-4 text-blue-400">AI 매출 예측</h3>
          <div class="forecast-chart p-4 rounded-lg" style="background: var(--bg-tertiary);">
            <div class="flex items-center justify-between mb-4">
              <span class="text-sm" style="color: var(--text-secondary);">다음 분기 예상 매출</span>
              <span class="text-lg font-bold text-green-400">{{ formatCurrency(forecastRevenue) }}</span>
            </div>
            <div class="space-y-2">
              <div v-for="month in forecastData" :key="month.name" class="flex items-center justify-between">
                <span class="text-sm text-white">{{ month.name }}</span>
                <div class="flex items-center space-x-2">
                  <div class="w-20 h-2 rounded-full" style="background: var(--bg-hover);">
                    <div class="h-full rounded-full bg-gradient-to-r from-blue-400 to-green-400 transition-all duration-500" 
                         :style="`width: ${month.percentage}%;`">
                    </div>
                  </div>
                  <span class="text-sm font-medium text-green-400">{{ formatCurrency(month.value) }}</span>
                </div>
              </div>
            </div>
            <div class="mt-4 p-3 rounded-lg" style="background: var(--bg-hover);">
              <p class="text-sm" style="color: var(--text-secondary);">
                <span class="text-blue-400 font-medium">AI 분석:</span> 
                현재 트렌드 기준 95% 신뢰도로 {{ (((forecastRevenue - totalRevenue) / totalRevenue) * 100).toFixed(1) }}% 성장 예상
              </p>
            </div>
          </div>
        </div>

        <!-- AI 인사이트 -->
        <div class="ai-insights p-6 rounded-xl" style="background: var(--bg-secondary); border: 1px solid var(--border-secondary);">
          <h3 class="text-xl font-semibold mb-4 text-purple-400">AI 영업 인사이트</h3>
          <div class="insights-list space-y-3">
            <div v-for="insight in aiInsights" :key="insight.id"
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
                          :style="`background: ${insight.priority === 'critical' ? '#ef4444' : insight.priority === 'high' ? '#f59e0b' : '#3b82f6'}20; 
                                   color: ${insight.priority === 'critical' ? '#ef4444' : insight.priority === 'high' ? '#f59e0b' : '#3b82f6'};`">
                      {{ insight.priority === 'critical' ? '긴급' : insight.priority === 'high' ? '높음' : '보통' }}
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
</template>

<script>
import { ref, reactive, onMounted, computed } from 'vue'
import { useAI } from '@/composables/useAI'

export default {
  name: 'SalesModule',
  setup() {
    const { executeAIRequest, formatResponse } = useAI()
    
    // 반응형 데이터
    const agiStatus = ref('활성화됨')
    const aiCommand = ref('')
    const aiResponse = ref('')
    
    // 대시보드 메트릭
    const totalRevenue = ref(2850000000)
    const revenueGrowth = ref(12.5)
    const newLeads = ref(147)
    const leadsGrowth = ref(23)
    const conversionRate = ref(18.7)
    const avgDealSize = ref(15750000)
    const dealSizeGrowth = ref(8.3)
    
    // 예측 데이터
    const forecastRevenue = ref(3200000000)
    const forecastData = ref([
      { name: '1월', value: 950000000, percentage: 85 },
      { name: '2월', value: 1050000000, percentage: 92 },
      { name: '3월', value: 1200000000, percentage: 100 }
    ])
    
    // 영업 파이프라인
    const pipelineStages = ref([
      { name: '리드 발굴', count: 89, value: 445000000, probability: 15, color: '#3b82f6' },
      { name: '자격 확인', count: 34, value: 510000000, probability: 35, color: '#8b5cf6' },
      { name: '제안서 작성', count: 18, value: 360000000, probability: 65, color: '#f59e0b' },
      { name: '협상', count: 12, value: 240000000, probability: 80, color: '#10b981' },
      { name: '계약 체결', count: 8, value: 180000000, probability: 95, color: '#06b6d4' }
    ])
    
    // 고객 세그먼트
    const customerSegments = ref([
      { 
        name: '대기업', 
        percentage: 35, 
        avgValue: 45000000, 
        lifetime: 180000000, 
        color: '#3b82f6',
        trend: 'up',
        strategy: '장기 파트너십 중심 접근'
      },
      { 
        name: '중견기업', 
        percentage: 45, 
        avgValue: 18000000, 
        lifetime: 72000000, 
        color: '#8b5cf6',
        trend: 'up',
        strategy: '맞춤형 솔루션 제공'
      },
      { 
        name: '중소기업', 
        percentage: 20, 
        avgValue: 8500000, 
        lifetime: 34000000, 
        color: '#10b981',
        trend: 'stable',
        strategy: '비용 효율성 강조'
      }
    ])
    
    // 최근 활동
    const recentActivities = ref([
      { id: 1, title: '신규 리드 등록', description: '(주)테크솔루션 - ERP 도입 문의', time: '10분 전', icon: '🎯', color: '#3b82f6' },
      { id: 2, title: '제안서 발송', description: '글로벌 제조(주) - 맞춤형 ERP 제안', time: '1시간 전', icon: '📝', color: '#8b5cf6' },
      { id: 3, title: '미팅 완료', description: '스마트팩토리(주) - 계약 협상', time: '3시간 전', icon: '🤝', color: '#10b981' },
      { id: 4, title: 'AI 분석 완료', description: '4분기 매출 예측 업데이트', time: '5시간 전', icon: '🤖', color: '#f59e0b' }
    ])
    
    // 영업 기회
    const salesOpportunities = ref([
      { 
        id: 1, 
        company: '(주)미래테크', 
        description: 'AI 통합 ERP 시스템 구축', 
        value: 85000000, 
        priority: 'high', 
        aiScore: 87 
      },
      { 
        id: 2, 
        company: '글로벌솔루션', 
        description: '클라우드 ERP 마이그레이션', 
        value: 62000000, 
        priority: 'medium', 
        aiScore: 73 
      },
      { 
        id: 3, 
        company: '스마트공장(주)', 
        description: 'IoT 연동 생산관리 시스템', 
        value: 95000000, 
        priority: 'high', 
        aiScore: 91 
      }
    ])
    
    // 성과 지표
    const performanceMetrics = ref([
      { name: '매출 목표 달성률', value: 92, unit: '%', target: 100, percentage: 92, color: '#10b981', change: 5.2 },
      { name: '신규 고객 획득', value: 23, unit: '개', target: 30, percentage: 77, color: '#3b82f6', change: 15.0 },
      { name: '고객 만족도', value: 4.7, unit: '/5', target: 4.5, percentage: 94, color: '#8b5cf6', change: 8.1 },
      { name: '영업 효율성', value: 87, unit: '%', target: 85, percentage: 87, color: '#f59e0b', change: 3.5 }
    ])
    
    // AI 인사이트
    const aiInsights = ref([
      {
        id: 1,
        title: '고가치 리드 발견',
        description: '대기업 세그먼트에서 3개의 고가치 리드가 감지되었습니다. 즉시 접촉을 권장합니다.',
        priority: 'critical',
        confidence: 94,
        icon: '🎯',
        color: '#ef4444'
      },
      {
        id: 2,
        title: '계절성 트렌드 예측',
        description: '연말 프로젝트 러시로 인해 12월 매출이 평균 대비 25% 증가할 것으로 예상됩니다.',
        priority: 'high',
        confidence: 87,
        icon: '📈',
        color: '#f59e0b'
      },
      {
        id: 3,
        title: '경쟁사 분석',
        description: '주요 경쟁사의 가격 정책 변화가 감지되었습니다. 대응 전략 수립이 필요합니다.',
        priority: 'medium',
        confidence: 79,
        icon: '🔍',
        color: '#3b82f6'
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
        const response = await executeAIRequest(aiCommand.value, 'sales')
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
      totalRevenue.value += Math.floor(Math.random() * 10000000)
      newLeads.value += Math.floor(Math.random() * 5)
      conversionRate.value = Math.round((conversionRate.value + Math.random() * 2 - 1) * 10) / 10
    }
    
    const viewOpportunityDetails = (opportunity) => {
      aiResponse.value = `영업 기회 상세 분석:
      
회사: ${opportunity.company}
예상 거래액: ${formatCurrency(opportunity.value)}
AI 성공 예측률: ${opportunity.aiScore}%
우선순위: ${opportunity.priority === 'high' ? '높음' : opportunity.priority === 'medium' ? '보통' : '낮음'}

추천 접근 전략:
1. 즉시 연락하여 니즈 파악
2. 맞춤형 제안서 작성
3. 기술 데모 일정 조율
4. 의사결정자와의 직접 미팅 요청

예상 성사 시기: ${Math.floor(Math.random() * 12 + 1)}개월 후`
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
      totalRevenue,
      revenueGrowth,
      newLeads,
      leadsGrowth,
      conversionRate,
      avgDealSize,
      dealSizeGrowth,
      forecastRevenue,
      forecastData,
      
      // 데이터
      pipelineStages,
      customerSegments,
      recentActivities,
      salesOpportunities,
      performanceMetrics,
      aiInsights,
      
      // 메서드
      formatCurrency,
      executeAICommand,
      clearAICommand,
      refreshDashboard,
      viewOpportunityDetails
    }
  }
}
</script>

<style scoped>
.sales-module {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

.dashboard-card:hover {
  transform: translateY(-2px);
}

.pipeline-stage:hover,
.segment-item:hover,
.activity-item:hover,
.opportunity-item:hover,
.metric-item:hover,
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