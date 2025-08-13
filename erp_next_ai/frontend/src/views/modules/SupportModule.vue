<template>
  <div class="support-module min-h-screen" style="background: var(--bg-primary); color: var(--text-primary);">
    <!-- 헤더 -->
    <div class="header-section p-6 border-b" style="border-color: var(--border-primary); background: var(--bg-secondary);">
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-3xl font-bold bg-gradient-to-r from-cyan-400 to-blue-400 bg-clip-text text-transparent">
            고객 지원 (Customer Support)
          </h1>
          <p class="text-gray-400 mt-2">AI 기반 고객 지원 및 자동 티켓 처리</p>
        </div>
        <div class="flex items-center space-x-4">
          <div class="agi-status px-4 py-2 rounded-lg" style="background: var(--bg-tertiary); border: 1px solid var(--ai-primary);">
            <span class="text-sm">AGI 상태: </span>
            <span class="text-green-400 font-semibold">{{ agiStatus }}</span>
          </div>
          <button 
            @click="refreshDashboard"
            class="bg-cyan-600 hover:bg-cyan-700 px-4 py-2 rounded-lg transition-all duration-300 text-white"
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
        <h3 class="text-lg font-semibold mb-3 text-cyan-400">AI 지원 어시스턴트</h3>
        <div class="flex space-x-4">
          <textarea 
            v-model="aiCommand"
            placeholder="지원 관련 자연어 명령을 입력하세요... 예: '티켓 우선순위 분석해줘', '고객 만족도 개선 방안 제시해줘', '응답 시간 최적화해줘'"
            class="flex-1 p-4 rounded-lg resize-none transition-all duration-300"
            style="background: var(--bg-tertiary); border: 1px solid var(--border-secondary); color: var(--text-primary); min-height: 80px;"
            @focus="$event.target.style.borderColor = 'var(--ai-primary)'"
            @blur="$event.target.style.borderColor = 'var(--border-secondary)'"
          ></textarea>
          <div class="flex flex-col space-y-2">
            <button 
              @click="executeAICommand"
              :disabled="!aiCommand.trim()"
              class="bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-600 hover:to-blue-700 disabled:opacity-50 px-6 py-3 rounded-lg transition-all duration-300 text-white font-medium"
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
      <!-- 총 티켓 수 -->
      <div class="dashboard-card p-6 rounded-xl transition-all duration-300 hover:scale-105" 
           style="background: var(--bg-secondary); border: 1px solid var(--border-secondary);"
           @mouseenter="$event.target.style.boxShadow = 'var(--glow-primary)'"
           @mouseleave="$event.target.style.boxShadow = 'none'">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm font-medium" style="color: var(--text-secondary);">총 티켓 수</p>
            <p class="text-2xl font-bold text-cyan-400">{{ totalTickets }}</p>
            <p class="text-xs mt-1" :class="ticketGrowth >= 0 ? 'text-red-400' : 'text-green-400'">
              {{ ticketGrowth >= 0 ? '+' : '' }}{{ ticketGrowth }}% 전월 대비
            </p>
          </div>
          <div class="text-cyan-400 text-3xl">🎫</div>
        </div>
      </div>

      <!-- 평균 응답 시간 -->
      <div class="dashboard-card p-6 rounded-xl transition-all duration-300 hover:scale-105" 
           style="background: var(--bg-secondary); border: 1px solid var(--border-secondary);"
           @mouseenter="$event.target.style.boxShadow = 'var(--glow-secondary)'"
           @mouseleave="$event.target.style.boxShadow = 'none'">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm font-medium" style="color: var(--text-secondary);">평균 응답 시간</p>
            <p class="text-2xl font-bold text-blue-400">{{ avgResponseTime }}h</p>
            <p class="text-xs mt-1 text-green-400">{{ responseTimeImprovement }}% 개선</p>
          </div>
          <div class="text-blue-400 text-3xl">⏱️</div>
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
          <div class="text-yellow-400 text-3xl">😊</div>
        </div>
      </div>

      <!-- AI 해결률 -->
      <div class="dashboard-card p-6 rounded-xl transition-all duration-300 hover:scale-105" 
           style="background: var(--bg-secondary); border: 1px solid var(--border-secondary);"
           @mouseenter="$event.target.style.boxShadow = 'var(--glow-primary)'"
           @mouseleave="$event.target.style.boxShadow = 'none'">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm font-medium" style="color: var(--text-secondary);">AI 자동 해결률</p>
            <p class="text-2xl font-bold text-green-400">{{ aiResolutionRate }}%</p>
            <p class="text-xs mt-1 text-green-400">{{ aiImprovementRate }}% 증가</p>
          </div>
          <div class="text-green-400 text-3xl">🤖</div>
        </div>
      </div>
    </div>

    <!-- 메인 콘텐츠 영역 -->
    <div class="main-content p-6 grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- 티켓 대시보드 -->
      <div class="ticket-dashboard p-6 rounded-xl" style="background: var(--bg-secondary); border: 1px solid var(--border-secondary);">
        <h3 class="text-xl font-semibold mb-4 text-cyan-400">실시간 티켓 현황</h3>
        <div class="space-y-4">
          <div v-for="ticket in recentTickets" :key="ticket.id" 
               class="ticket-item p-4 rounded-lg transition-all duration-300 hover:scale-102 cursor-pointer"
               style="background: var(--bg-tertiary); border: 1px solid var(--border-primary);"
               @click="viewTicketDetails(ticket)">
            <div class="flex items-center justify-between mb-2">
              <h4 class="font-medium text-white">{{ ticket.title }}</h4>
              <div class="flex items-center space-x-2">
                <span class="text-sm px-2 py-1 rounded" 
                      :style="`background: ${ticket.priority === 'urgent' ? '#ef4444' : ticket.priority === 'high' ? '#f59e0b' : ticket.priority === 'medium' ? '#3b82f6' : '#10b981'}20; 
                               color: ${ticket.priority === 'urgent' ? '#ef4444' : ticket.priority === 'high' ? '#f59e0b' : ticket.priority === 'medium' ? '#3b82f6' : '#10b981'};`">
                  {{ ticket.priority === 'urgent' ? '긴급' : ticket.priority === 'high' ? '높음' : ticket.priority === 'medium' ? '보통' : '낮음' }}
                </span>
                <span class="text-xs px-2 py-1 rounded" 
                      :style="`background: ${ticket.status === 'open' ? '#3b82f6' : ticket.status === 'in-progress' ? '#f59e0b' : '#10b981'}20; 
                               color: ${ticket.status === 'open' ? '#3b82f6' : ticket.status === 'in-progress' ? '#f59e0b' : '#10b981'};`">
                  {{ ticket.status === 'open' ? '대기' : ticket.status === 'in-progress' ? '진행중' : '완료' }}
                </span>
              </div>
            </div>
            <div class="grid grid-cols-2 gap-4 text-sm">
              <div>
                <span style="color: var(--text-tertiary);">고객:</span>
                <span class="ml-2 font-medium text-white">{{ ticket.customer }}</span>
              </div>
              <div>
                <span style="color: var(--text-tertiary);">담당자:</span>
                <span class="ml-2 font-medium text-cyan-400">{{ ticket.assignee || 'AI 자동 배정' }}</span>
              </div>
            </div>
            <div class="mt-2 grid grid-cols-2 gap-4 text-sm">
              <div>
                <span style="color: var(--text-tertiary);">생성일:</span>
                <span class="ml-2 font-medium text-white">{{ ticket.createdAt }}</span>
              </div>
              <div>
                <span style="color: var(--text-tertiary);">AI 분류:</span>
                <span class="ml-2 font-medium text-purple-400">{{ ticket.aiCategory }}</span>
              </div>
            </div>
            <div class="mt-3">
              <p class="text-sm" style="color: var(--text-secondary);">{{ ticket.description }}</p>
              <div class="mt-2">
                <span class="text-xs" style="color: var(--text-tertiary);">
                  AI 예상 해결 시간: {{ ticket.aiEstimatedTime }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 지원팀 성과 -->
      <div class="team-performance p-6 rounded-xl" style="background: var(--bg-secondary); border: 1px solid var(--border-secondary);">
        <h3 class="text-xl font-semibold mb-4 text-blue-400">지원팀 성과 분석</h3>
        <div class="space-y-4">
          <div v-for="agent in supportAgents" :key="agent.id"
               class="agent-item p-4 rounded-lg transition-all duration-300 hover:scale-102 cursor-pointer"
               style="background: var(--bg-tertiary); border: 1px solid var(--border-primary);"
               @click="viewAgentDetails(agent)">
            <div class="flex items-center justify-between mb-2">
              <div class="flex items-center space-x-3">
                <div class="w-10 h-10 rounded-full flex items-center justify-center" 
                     :style="`background: ${agent.color}20; color: ${agent.color};`">
                  {{ agent.name.charAt(0) }}
                </div>
                <div>
                  <h4 class="font-medium text-white">{{ agent.name }}</h4>
                  <p class="text-xs" style="color: var(--text-tertiary);">{{ agent.role }}</p>
                </div>
              </div>
              <div class="flex items-center space-x-2">
                <span class="text-sm px-2 py-1 rounded" 
                      :style="`background: ${agent.performance >= 90 ? '#10b981' : agent.performance >= 80 ? '#f59e0b' : '#ef4444'}20; 
                               color: ${agent.performance >= 90 ? '#10b981' : agent.performance >= 80 ? '#f59e0b' : '#ef4444'};`">
                  {{ agent.performance }}%
                </span>
              </div>
            </div>
            <div class="grid grid-cols-2 gap-4 text-sm">
              <div>
                <span style="color: var(--text-tertiary);">처리 티켓:</span>
                <span class="ml-2 font-medium text-white">{{ agent.ticketsHandled }}개</span>
              </div>
              <div>
                <span style="color: var(--text-tertiary);">평균 응답:</span>
                <span class="ml-2 font-medium text-cyan-400">{{ agent.avgResponseTime }}h</span>
              </div>
            </div>
            <div class="mt-2 grid grid-cols-2 gap-4 text-sm">
              <div>
                <span style="color: var(--text-tertiary);">고객 평점:</span>
                <span class="ml-2 font-medium text-yellow-400">{{ agent.customerRating }}/5</span>
              </div>
              <div>
                <span style="color: var(--text-tertiary);">AI 협업 점수:</span>
                <span class="ml-2 font-medium text-purple-400">{{ agent.aiCollaboration }}/100</span>
              </div>
            </div>
            <div class="mt-3">
              <div class="w-full h-2 rounded-full" style="background: var(--bg-hover);">
                <div class="h-full rounded-full transition-all duration-500" 
                     :style="`width: ${agent.performance}%; background: ${agent.performance >= 90 ? '#10b981' : agent.performance >= 80 ? '#f59e0b' : '#ef4444'};`">
                </div>
              </div>
              <div class="flex justify-between mt-1 text-xs" style="color: var(--text-tertiary);">
                <span>성과 지표</span>
                <span>전문 분야: {{ agent.specialization }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 지원 관리 및 분석 -->
    <div class="support-management-section p-6 grid grid-cols-1 xl:grid-cols-3 gap-6">
      <!-- FAQ 및 지식 베이스 -->
      <div class="knowledge-base p-6 rounded-xl" style="background: var(--bg-secondary); border: 1px solid var(--border-secondary);">
        <h3 class="text-xl font-semibold mb-4 text-green-400">AI 지식 베이스</h3>
        <div class="space-y-3 max-h-64 overflow-y-auto">
          <div v-for="article in knowledgeBase" :key="article.id"
               class="article-item p-3 rounded-lg transition-all duration-300 hover:scale-102 cursor-pointer"
               style="background: var(--bg-tertiary); border: 1px solid var(--border-primary);"
               @click="viewArticleDetails(article)">
            <div class="flex items-center justify-between mb-2">
              <h4 class="font-medium text-white">{{ article.title }}</h4>
              <span class="text-xs px-2 py-1 rounded" 
                    :style="`background: ${article.helpfulness >= 90 ? '#10b981' : article.helpfulness >= 70 ? '#f59e0b' : '#ef4444'}20; 
                             color: ${article.helpfulness >= 90 ? '#10b981' : article.helpfulness >= 70 ? '#f59e0b' : '#ef4444'};`">
                {{ article.helpfulness }}%
              </span>
            </div>
            <div class="grid grid-cols-2 gap-2 text-sm">
              <div>
                <span style="color: var(--text-tertiary);">조회수:</span>
                <span class="ml-1 font-medium text-white">{{ article.views.toLocaleString() }}</span>
              </div>
              <div>
                <span style="color: var(--text-tertiary);">카테고리:</span>
                <span class="ml-1 font-medium text-cyan-400">{{ article.category }}</span>
              </div>
            </div>
            <div class="mt-2 text-sm">
              <span style="color: var(--text-tertiary);">마지막 업데이트:</span>
              <span class="ml-2 font-medium text-white">{{ article.lastUpdated }}</span>
            </div>
            <div class="mt-2">
              <span class="text-xs" style="color: var(--text-tertiary);">
                AI 추천 빈도: {{ article.aiRecommendations }}회
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- 자동화 현황 -->
      <div class="automation-status p-6 rounded-xl" style="background: var(--bg-secondary); border: 1px solid var(--border-secondary);">
        <h3 class="text-xl font-semibold mb-4 text-purple-400">AI 자동화 현황</h3>
        <div class="space-y-4">
          <div v-for="automation in automationMetrics" :key="automation.name"
               class="automation-item p-3 rounded-lg"
               style="background: var(--bg-tertiary); border: 1px solid var(--border-primary);">
            <div class="flex items-center justify-between mb-2">
              <span class="text-sm font-medium text-white">{{ automation.name }}</span>
              <span class="text-sm font-bold" :style="`color: ${automation.color};`">
                {{ automation.rate }}%
              </span>
            </div>
            <div class="grid grid-cols-2 gap-2 text-sm">
              <div>
                <span style="color: var(--text-tertiary);">처리량:</span>
                <span class="ml-1 font-medium text-white">{{ automation.processed }}건</span>
              </div>
              <div>
                <span style="color: var(--text-tertiary);">정확도:</span>
                <span class="ml-1 font-medium text-green-400">{{ automation.accuracy }}%</span>
              </div>
            </div>
            <div class="mt-2">
              <div class="w-full h-1.5 rounded-full" style="background: var(--bg-hover);">
                <div class="h-full rounded-full transition-all duration-500" 
                     :style="`width: ${automation.rate}%; background: ${automation.color};`">
                </div>
              </div>
              <div class="flex justify-between mt-1 text-xs" style="color: var(--text-tertiary);">
                <span>자동화율</span>
                <span>절약 시간: {{ automation.timeSaved }}h</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 고객 피드백 -->
      <div class="customer-feedback p-6 rounded-xl" style="background: var(--bg-secondary); border: 1px solid var(--border-secondary);">
        <h3 class="text-xl font-semibold mb-4 text-orange-400">실시간 고객 피드백</h3>
        <div class="space-y-3 max-h-64 overflow-y-auto">
          <div v-for="feedback in customerFeedbacks" :key="feedback.id"
               class="feedback-item p-3 rounded-lg transition-all duration-300 hover:scale-102"
               style="background: var(--bg-tertiary); border: 1px solid var(--border-primary);">
            <div class="flex items-center justify-between mb-2">
              <h4 class="font-medium text-white">{{ feedback.customer }}</h4>
              <div class="flex items-center space-x-1">
                <span v-for="n in 5" :key="n" 
                      :class="n <= feedback.rating ? 'text-yellow-400' : 'text-gray-600'">⭐</span>
              </div>
            </div>
            <p class="text-sm mb-2" style="color: var(--text-secondary);">{{ feedback.comment }}</p>
            <div class="grid grid-cols-2 gap-2 text-sm">
              <div>
                <span style="color: var(--text-tertiary);">티켓 ID:</span>
                <span class="ml-1 font-medium text-white">#{{ feedback.ticketId }}</span>
              </div>
              <div>
                <span style="color: var(--text-tertiary);">처리자:</span>
                <span class="ml-1 font-medium text-cyan-400">{{ feedback.agent }}</span>
              </div>
            </div>
            <div class="mt-2">
              <span class="text-xs" style="color: var(--text-tertiary);">
                {{ feedback.timestamp }} | AI 감정 분석: {{ feedback.sentiment }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 지원 인사이트 및 예측 -->
    <div class="insights-section p-6">
      <div class="insights-grid grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- 지원 트렌드 분석 -->
        <div class="support-trends p-6 rounded-xl" style="background: var(--bg-secondary); border: 1px solid var(--border-secondary);">
          <h3 class="text-xl font-semibold mb-4 text-cyan-400">지원 트렌드 분석</h3>
          <div class="trends-chart space-y-4">
            <div v-for="trend in supportTrends" :key="trend.category"
                 class="trend-item p-4 rounded-lg"
                 style="background: var(--bg-tertiary); border: 1px solid var(--border-primary);">
              <div class="flex items-center justify-between mb-2">
                <span class="text-sm font-medium text-white">{{ trend.category }}</span>
                <span class="text-sm font-bold" :class="trend.change >= 0 ? 'text-red-400' : 'text-green-400'">
                  {{ trend.change >= 0 ? '+' : '' }}{{ trend.change }}%
                </span>
              </div>
              <div class="grid grid-cols-2 gap-4 text-sm">
                <div>
                  <span style="color: var(--text-tertiary);">이번 달:</span>
                  <span class="ml-2 font-medium text-white">{{ trend.currentMonth }}건</span>
                </div>
                <div>
                  <span style="color: var(--text-tertiary);">지난 달:</span>
                  <span class="ml-2 font-medium text-cyan-400">{{ trend.lastMonth }}건</span>
                </div>
              </div>
              <div class="mt-2">
                <div class="w-full h-2 rounded-full" style="background: var(--bg-hover);">
                  <div class="h-full rounded-full transition-all duration-500" 
                       :style="`width: ${(trend.currentMonth / (trend.currentMonth + trend.lastMonth)) * 100}%; background: ${trend.change >= 0 ? '#ef4444' : '#10b981'};`">
                  </div>
                </div>
                <div class="flex justify-between mt-1 text-xs" style="color: var(--text-tertiary);">
                  <span>{{ trend.description }}</span>
                  <span>AI 예측: {{ trend.aiPrediction }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- AI 지원 인사이트 -->
        <div class="support-insights p-6 rounded-xl" style="background: var(--bg-secondary); border: 1px solid var(--border-secondary);">
          <h3 class="text-xl font-semibold mb-4 text-blue-400">AI 지원 인사이트</h3>
          <div class="insights-list space-y-3">
            <div v-for="insight in supportInsights" :key="insight.id"
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
                    <span class="text-xs" style="color: var(--text-tertiary);">
                      효과 예상: {{ insight.expectedImpact }}%
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
  name: 'SupportModule',
  setup() {
    const { executeAIRequest, formatResponse } = useAI()
    
    // 반응형 데이터
    const agiStatus = ref('활성화됨')
    const aiCommand = ref('')
    const aiResponse = ref('')
    
    // 대시보드 메트릭
    const totalTickets = ref(1847)
    const ticketGrowth = ref(-8.3) // 음수는 좋은 것 (티켓 감소)
    const avgResponseTime = ref(2.4)
    const responseTimeImprovement = ref(15.7)
    const customerSatisfaction = ref(4.3)
    const satisfactionTrend = ref(12.5)
    const aiResolutionRate = ref(67.8)
    const aiImprovementRate = ref(23.4)
    
    // 최근 티켓
    const recentTickets = ref([
      {
        id: 1,
        title: '로그인 문제 해결 요청',
        customer: '김고객',
        assignee: null,
        priority: 'medium',
        status: 'open',
        createdAt: '2024-01-20',
        aiCategory: '인증/보안',
        description: '2단계 인증 설정 후 로그인이 안 됩니다.',
        aiEstimatedTime: '1-2시간'
      },
      {
        id: 2,
        title: '데이터 동기화 오류',
        customer: '이기업',
        assignee: '박지원',
        priority: 'high',
        status: 'in-progress',
        createdAt: '2024-01-20',
        aiCategory: '시스템/기술',
        description: '클라우드 동기화가 12시간째 중단되었습니다.',
        aiEstimatedTime: '2-4시간'
      },
      {
        id: 3,
        title: '기능 사용법 문의',
        customer: '최사용자',
        assignee: 'AI 봇',
        priority: 'low',
        status: 'resolved',
        createdAt: '2024-01-19',
        aiCategory: '사용법/교육',
        description: '새로운 보고서 기능 사용 방법을 알고 싶습니다.',
        aiEstimatedTime: '즉시 해결'
      },
      {
        id: 4,
        title: '결제 관련 문의',
        customer: '정회사',
        assignee: '김상담',
        priority: 'urgent',
        status: 'open',
        createdAt: '2024-01-20',
        aiCategory: '결제/청구',
        description: '청구서에 잘못된 금액이 표시되고 있습니다.',
        aiEstimatedTime: '1시간 이내'
      }
    ])
    
    // 지원팀 에이전트
    const supportAgents = ref([
      {
        id: 1,
        name: '김전문가',
        role: '수석 지원 엔지니어',
        ticketsHandled: 156,
        avgResponseTime: 1.8,
        customerRating: 4.8,
        performance: 95,
        aiCollaboration: 92,
        specialization: '기술 이슈',
        color: '#10b981'
      },
      {
        id: 2,
        name: '이상담사',
        role: '고객 성공 매니저',
        ticketsHandled: 203,
        avgResponseTime: 2.1,
        customerRating: 4.6,
        performance: 88,
        aiCollaboration: 89,
        specialization: '고객 관리',
        color: '#3b82f6'
      },
      {
        id: 3,
        name: '박해결사',
        role: '기술 지원 전문가',
        ticketsHandled: 134,
        avgResponseTime: 2.5,
        customerRating: 4.4,
        performance: 85,
        aiCollaboration: 87,
        specialization: '시스템 문제',
        color: '#f59e0b'
      },
      {
        id: 4,
        name: '최도우미',
        role: '신입 지원 담당자',
        ticketsHandled: 87,
        avgResponseTime: 3.2,
        customerRating: 4.1,
        performance: 76,
        aiCollaboration: 94,
        specialization: '일반 문의',
        color: '#8b5cf6'
      }
    ])
    
    // 지식 베이스
    const knowledgeBase = ref([
      {
        id: 1,
        title: '로그인 문제 해결 가이드',
        category: '인증',
        views: 15847,
        helpfulness: 94,
        lastUpdated: '2024-01-15',
        aiRecommendations: 342
      },
      {
        id: 2,
        title: '데이터 백업 및 복원',
        category: '데이터',
        views: 12563,
        helpfulness: 89,
        lastUpdated: '2024-01-10',
        aiRecommendations: 187
      },
      {
        id: 3,
        title: '결제 및 요금제 변경',
        category: '결제',
        views: 9876,
        helpfulness: 87,
        lastUpdated: '2024-01-18',
        aiRecommendations: 234
      },
      {
        id: 4,
        title: 'API 연동 가이드',
        category: '개발',
        views: 7654,
        helpfulness: 92,
        lastUpdated: '2024-01-12',
        aiRecommendations: 156
      }
    ])
    
    // 자동화 지표
    const automationMetrics = ref([
      {
        name: '1차 응답 자동화',
        rate: 85,
        processed: 1247,
        accuracy: 92,
        timeSaved: 312,
        color: '#10b981'
      },
      {
        name: '티켓 분류 자동화',
        rate: 94,
        processed: 1568,
        accuracy: 89,
        timeSaved: 187,
        color: '#3b82f6'
      },
      {
        name: 'FAQ 자동 답변',
        rate: 73,
        processed: 892,
        accuracy: 95,
        timeSaved: 445,
        color: '#f59e0b'
      },
      {
        name: '에스컬레이션 판단',
        rate: 67,
        processed: 534,
        accuracy: 87,
        timeSaved: 223,
        color: '#8b5cf6'
      }
    ])
    
    // 고객 피드백
    const customerFeedbacks = ref([
      {
        id: 1,
        customer: '김만족',
        ticketId: '2024-0120-001',
        rating: 5,
        comment: '매우 빠르고 정확한 해결책을 제공해주셔서 감사합니다.',
        agent: '김전문가',
        timestamp: '2시간 전',
        sentiment: '매우 긍정'
      },
      {
        id: 2,
        customer: '이감사',
        ticketId: '2024-0119-045',
        rating: 4,
        comment: '친절한 응대였지만 해결 시간이 조금 길었습니다.',
        agent: 'AI 봇 + 박해결사',
        timestamp: '4시간 전',
        sentiment: '긍정'
      },
      {
        id: 3,
        customer: '박칭찬',
        ticketId: '2024-0119-032',
        rating: 5,
        comment: 'AI가 즉시 답변해주어서 매우 편리했습니다.',
        agent: 'AI 봇',
        timestamp: '6시간 전',
        sentiment: '매우 긍정'
      }
    ])
    
    // 지원 트렌드
    const supportTrends = ref([
      {
        category: '기술 문의',
        currentMonth: 456,
        lastMonth: 523,
        change: -12.8,
        description: '시스템 안정성 개선 효과',
        aiPrediction: '지속 감소'
      },
      {
        category: '사용법 문의',
        currentMonth: 234,
        lastMonth: 198,
        change: 18.2,
        description: '신기능 출시 영향',
        aiPrediction: '일시적 증가'
      },
      {
        category: '결제 문의',
        currentMonth: 123,
        lastMonth: 134,
        change: -8.2,
        description: '결제 프로세스 개선',
        aiPrediction: '안정화'
      },
      {
        category: '계정 문제',
        currentMonth: 89,
        lastMonth: 156,
        change: -43.0,
        description: '보안 강화 및 자동화',
        aiPrediction: '대폭 감소'
      }
    ])
    
    // 지원 인사이트
    const supportInsights = ref([
      {
        id: 1,
        title: 'AI 챗봇 성능 급상승',
        description: '지난 월 대비 AI 자동 해결률이 23% 증가했습니다. FAQ 학습 모델 개선이 효과를 보고 있습니다.',
        priority: 'high',
        expectedImpact: 35,
        icon: '🤖',
        color: '#10b981'
      },
      {
        id: 2,
        title: '반복 문의 패턴 감지',
        description: '신규 기능 관련 동일한 문의가 증가하고 있습니다. 추가 가이드 문서 작성이 필요합니다.',
        priority: 'medium',
        expectedImpact: 25,
        icon: '🔄',
        color: '#f59e0b'
      },
      {
        id: 3,
        title: '고객 만족도 상승 트렌드',
        description: '평균 응답 시간 단축과 AI 지원으로 고객 만족도가 12% 향상되었습니다.',
        priority: 'medium',
        expectedImpact: 20,
        icon: '📈',
        color: '#3b82f6'
      },
      {
        id: 4,
        title: '프로액티브 지원 기회',
        description: 'AI가 시스템 로그를 분석해 잠재적 문제를 사전 감지하고 있습니다.',
        priority: 'high',
        expectedImpact: 45,
        icon: '🛡️',
        color: '#8b5cf6'
      }
    ])
    
    // 메서드
    const executeAICommand = async () => {
      if (!aiCommand.value.trim()) return
      
      try {
        aiResponse.value = '처리 중...'
        
        // AI 요청 실행
        const response = await executeAIRequest(aiCommand.value, 'support')
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
      totalTickets.value += Math.floor(Math.random() * 10 - 5) // 티켓 수는 감소할 수도 있음
      avgResponseTime.value = Math.max(1.0, Math.round((avgResponseTime.value + Math.random() * 0.4 - 0.2) * 10) / 10)
      aiResolutionRate.value = Math.min(100, Math.round((aiResolutionRate.value + Math.random() * 2 - 1) * 10) / 10)
    }
    
    const viewTicketDetails = (ticket) => {
      aiResponse.value = `티켓 상세 분석:
      
티켓 ID: #${ticket.id}
제목: ${ticket.title}
고객: ${ticket.customer}
우선순위: ${ticket.priority === 'urgent' ? '긴급' : ticket.priority === 'high' ? '높음' : ticket.priority === 'medium' ? '보통' : '낮음'}
상태: ${ticket.status === 'open' ? '대기 중' : ticket.status === 'in-progress' ? '처리 중' : '해결 완료'}

AI 분석 결과:
- 카테고리: ${ticket.aiCategory}
- 예상 해결 시간: ${ticket.aiEstimatedTime}
- 복잡도: ${ticket.priority === 'urgent' ? '높음' : ticket.priority === 'high' ? '보통' : '낮음'}

고객 정보:
- 이름: ${ticket.customer}
- 과거 티켓 수: ${Math.floor(Math.random() * 20 + 5)}건
- 평균 만족도: ${(Math.random() * 1.5 + 3.5).toFixed(1)}/5

추천 액션:
1. ${ticket.status === 'open' ? ticket.assignee ? `담당자 ${ticket.assignee}에게 즉시 배정` : 'AI가 최적 담당자 자동 배정 중' : '현재 처리 진행 상황 모니터링'}
2. ${ticket.priority === 'urgent' ? '1시간 내 첫 응답 필수' : ticket.priority === 'high' ? '4시간 내 응답 권장' : '24시간 내 응답'}
3. ${ticket.aiCategory === '사용법/교육' ? '관련 FAQ 문서 자동 제안' : ticket.aiCategory === '시스템/기술' ? '시스템 로그 자동 분석' : '전문가 에스컬레이션 고려'}

예상 결과:
- 해결 가능성: ${85 + Math.floor(Math.random() * 15)}%
- 고객 만족도 예측: ${3.8 + Math.random() * 1.2}/5`
    }
    
    const viewAgentDetails = (agent) => {
      aiResponse.value = `지원 담당자 성과 분석:
      
담당자: ${agent.name}
역할: ${agent.role}
전문 분야: ${agent.specialization}

성과 지표:
- 전체 성과 점수: ${agent.performance}%
- 처리한 티켓 수: ${agent.ticketsHandled}개
- 평균 응답 시간: ${agent.avgResponseTime}시간
- 고객 평점: ${agent.customerRating}/5.0
- AI 협업 점수: ${agent.aiCollaboration}/100

AI 분석:
${agent.performance >= 90 ? '최우수 성과자로 멘토링 역할 적합' : agent.performance >= 80 ? '우수한 성과를 보이는 핵심 인력' : '추가 교육 및 지원이 필요한 상황'}
${agent.aiCollaboration >= 90 ? 'AI 도구 활용도가 매우 높음' : agent.aiCollaboration >= 80 ? 'AI 도구를 잘 활용하고 있음' : 'AI 협업 교육 필요'}

강점:
- ${agent.avgResponseTime < 2.5 ? '빠른 응답 속도' : '정확한 문제 해결'}
- ${agent.customerRating >= 4.5 ? '뛰어난 고객 만족도' : '전문적인 기술 지원'}
- ${agent.specialization}에 특화된 전문성

개선 제안:
1. ${agent.performance < 85 ? '성과 개선을 위한 추가 교육 프로그램 참여' : '현재 성과 수준 유지 및 경험 공유'}
2. ${agent.aiCollaboration < 85 ? 'AI 도구 활용 교육 강화' : 'AI 협업 베스트 프랙티스 전파'}
3. ${agent.avgResponseTime > 3.0 ? '응답 시간 단축 방안 모색' : '품질 유지하며 효율성 극대화'}

다음 달 목표:
- 티켓 처리량: ${agent.ticketsHandled + Math.floor(Math.random() * 30 + 10)}개
- 목표 성과 점수: ${Math.min(100, agent.performance + Math.floor(Math.random() * 10 + 2))}%`
    }
    
    const viewArticleDetails = (article) => {
      aiResponse.value = `지식 베이스 문서 분석:
      
문서 제목: ${article.title}
카테고리: ${article.category}
도움도: ${article.helpfulness}%

사용 통계:
- 총 조회수: ${article.views.toLocaleString()}회
- AI 추천 횟수: ${article.aiRecommendations}회
- 마지막 업데이트: ${article.lastUpdated}

AI 분석:
${article.helpfulness >= 90 ? '매우 유용한 문서로 고객들에게 높은 평가를 받음' : article.helpfulness >= 80 ? '유용한 문서이나 개선 여지 있음' : '내용 개선이 필요한 문서'}
${article.views > 10000 ? '높은 조회수로 인기 있는 주제' : '중간 수준의 관심도'}

활용 현황:
- 고객 자가 해결률: ${article.helpfulness * 0.8}%
- 지원팀 참조 빈도: ${article.aiRecommendations / 10}회/월
- 최근 30일 트렌드: ${Math.random() > 0.5 ? '증가' : '안정'}

개선 제안:
1. ${article.helpfulness < 85 ? '고객 피드백을 반영한 내용 개선' : '현재 품질 수준 유지'}
2. ${article.views > 15000 ? '관련 하위 주제 문서 추가 작성' : '검색 최적화로 접근성 개선'}
3. ${Date.now() - new Date(article.lastUpdated).getTime() > 30 * 24 * 60 * 60 * 1000 ? '최신 정보로 업데이트 필요' : '정기 검토 및 업데이트 일정 준수'}

관련 지표:
- 문서 활용으로 절약된 지원 시간: ${Math.floor(article.aiRecommendations * 0.5)}시간
- 고객 만족도 기여도: ${Math.floor(article.helpfulness * 0.05)}%
- ROI: ${Math.floor(article.views * 0.001)}%`
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
      totalTickets,
      ticketGrowth,
      avgResponseTime,
      responseTimeImprovement,
      customerSatisfaction,
      satisfactionTrend,
      aiResolutionRate,
      aiImprovementRate,
      
      // 데이터
      recentTickets,
      supportAgents,
      knowledgeBase,
      automationMetrics,
      customerFeedbacks,
      supportTrends,
      supportInsights,
      
      // 메서드
      executeAICommand,
      clearAICommand,
      refreshDashboard,
      viewTicketDetails,
      viewAgentDetails,
      viewArticleDetails
    }
  }
}
</script>

<style scoped>
.support-module {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

.dashboard-card:hover {
  transform: translateY(-2px);
}

.ticket-item:hover,
.agent-item:hover,
.article-item:hover,
.feedback-item:hover,
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
  
  .support-management-section {
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