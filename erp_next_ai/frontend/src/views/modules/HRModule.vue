<template>
  <div class="hr-module min-h-screen" style="background: var(--bg-primary); color: var(--text-primary);">
    <!-- 헤더 -->
    <div class="header-section p-6 border-b" style="border-color: var(--border-primary); background: var(--bg-secondary);">
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-3xl font-bold bg-gradient-to-r from-pink-400 to-orange-400 bg-clip-text text-transparent">
            인사 관리 (Human Resources)
          </h1>
          <p class="text-gray-400 mt-2">AI 기반 인재 관리 및 조직 최적화</p>
        </div>
        <div class="flex items-center space-x-4">
          <div class="agi-status px-4 py-2 rounded-lg" style="background: var(--bg-tertiary); border: 1px solid var(--ai-primary);">
            <span class="text-sm">AGI 상태: </span>
            <span class="text-green-400 font-semibold">{{ agiStatus }}</span>
          </div>
          <button 
            @click="refreshDashboard"
            class="bg-pink-600 hover:bg-pink-700 px-4 py-2 rounded-lg transition-all duration-300 text-white"
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
        <h3 class="text-lg font-semibold mb-3 text-pink-400">AI 인사 어시스턴트</h3>
        <div class="flex space-x-4">
          <textarea 
            v-model="aiCommand"
            placeholder="인사 관련 자연어 명령을 입력하세요... 예: '직원 성과 분석해줘', '최적 팀 구성 추천해줘', '급여 체계 분석해줘'"
            class="flex-1 p-4 rounded-lg resize-none transition-all duration-300"
            style="background: var(--bg-tertiary); border: 1px solid var(--border-secondary); color: var(--text-primary); min-height: 80px;"
            @focus="$event.target.style.borderColor = 'var(--ai-primary)'"
            @blur="$event.target.style.borderColor = 'var(--border-secondary)'"
          ></textarea>
          <div class="flex flex-col space-y-2">
            <button 
              @click="executeAICommand"
              :disabled="!aiCommand.trim()"
              class="bg-gradient-to-r from-pink-500 to-orange-600 hover:from-pink-600 hover:to-orange-700 disabled:opacity-50 px-6 py-3 rounded-lg transition-all duration-300 text-white font-medium"
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
      <!-- 총 직원 수 -->
      <div class="dashboard-card p-6 rounded-xl transition-all duration-300 hover:scale-105" 
           style="background: var(--bg-secondary); border: 1px solid var(--border-secondary);"
           @mouseenter="$event.target.style.boxShadow = 'var(--glow-primary)'"
           @mouseleave="$event.target.style.boxShadow = 'none'">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm font-medium" style="color: var(--text-secondary);">총 직원 수</p>
            <p class="text-2xl font-bold text-pink-400">{{ totalEmployees }}</p>
            <p class="text-xs mt-1" :class="employeeGrowth >= 0 ? 'text-green-400' : 'text-red-400'">
              {{ employeeGrowth >= 0 ? '+' : '' }}{{ employeeGrowth }}% 전년 대비
            </p>
          </div>
          <div class="text-pink-400 text-3xl">👥</div>
        </div>
      </div>

      <!-- 평균 만족도 -->
      <div class="dashboard-card p-6 rounded-xl transition-all duration-300 hover:scale-105" 
           style="background: var(--bg-secondary); border: 1px solid var(--border-secondary);"
           @mouseenter="$event.target.style.boxShadow = 'var(--glow-secondary)'"
           @mouseleave="$event.target.style.boxShadow = 'none'">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm font-medium" style="color: var(--text-secondary);">직원 만족도</p>
            <p class="text-2xl font-bold text-orange-400">{{ employeeSatisfaction }}/5</p>
            <p class="text-xs mt-1 text-green-400">{{ satisfactionTrend }}% 향상</p>
          </div>
          <div class="text-orange-400 text-3xl">😊</div>
        </div>
      </div>

      <!-- 이직률 -->
      <div class="dashboard-card p-6 rounded-xl transition-all duration-300 hover:scale-105" 
           style="background: var(--bg-secondary); border: 1px solid var(--border-secondary);"
           @mouseenter="$event.target.style.boxShadow = 'var(--glow-accent)'"
           @mouseleave="$event.target.style.boxShadow = 'none'">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm font-medium" style="color: var(--text-secondary);">연간 이직률</p>
            <p class="text-2xl font-bold text-yellow-400">{{ turnoverRate }}%</p>
            <p class="text-xs mt-1 text-green-400">업계 평균 이하</p>
          </div>
          <div class="text-yellow-400 text-3xl">📊</div>
        </div>
      </div>

      <!-- AI 추천 채용 -->
      <div class="dashboard-card p-6 rounded-xl transition-all duration-300 hover:scale-105" 
           style="background: var(--bg-secondary); border: 1px solid var(--border-secondary);"
           @mouseenter="$event.target.style.boxShadow = 'var(--glow-primary)'"
           @mouseleave="$event.target.style.boxShadow = 'none'">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm font-medium" style="color: var(--text-secondary);">AI 추천 채용</p>
            <p class="text-2xl font-bold text-green-400">{{ aiRecruitments }}</p>
            <p class="text-xs mt-1 text-green-400">{{ recruitmentAccuracy }}% 성공률</p>
          </div>
          <div class="text-green-400 text-3xl">🎯</div>
        </div>
      </div>
    </div>

    <!-- 메인 콘텐츠 영역 -->
    <div class="main-content p-6 grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- 조직 구조 -->
      <div class="organization-structure p-6 rounded-xl" style="background: var(--bg-secondary); border: 1px solid var(--border-secondary);">
        <h3 class="text-xl font-semibold mb-4 text-pink-400">AI 조직 분석</h3>
        <div class="space-y-4">
          <div v-for="department in departments" :key="department.name" 
               class="department-item p-4 rounded-lg transition-all duration-300 hover:scale-102 cursor-pointer"
               style="background: var(--bg-tertiary); border: 1px solid var(--border-primary);"
               @click="viewDepartmentDetails(department)">
            <div class="flex items-center justify-between mb-2">
              <h4 class="font-medium text-white">{{ department.name }}</h4>
              <span class="text-sm px-2 py-1 rounded" 
                    :style="`background: ${department.performance >= 85 ? '#10b981' : department.performance >= 70 ? '#f59e0b' : '#ef4444'}20; 
                             color: ${department.performance >= 85 ? '#10b981' : department.performance >= 70 ? '#f59e0b' : '#ef4444'};`">
                {{ department.performance }}%
              </span>
            </div>
            <div class="grid grid-cols-2 gap-4 text-sm">
              <div>
                <span style="color: var(--text-tertiary);">인원:</span>
                <span class="ml-2 font-medium text-white">{{ department.headcount }}명</span>
              </div>
              <div>
                <span style="color: var(--text-tertiary);">평균 경력:</span>
                <span class="ml-2 font-medium text-cyan-400">{{ department.avgExperience }}년</span>
              </div>
            </div>
            <div class="mt-2 grid grid-cols-2 gap-4 text-sm">
              <div>
                <span style="color: var(--text-tertiary);">만족도:</span>
                <span class="ml-2 font-medium text-orange-400">{{ department.satisfaction }}/5</span>
              </div>
              <div>
                <span style="color: var(--text-tertiary);">AI 효율성:</span>
                <span class="ml-2 font-medium text-green-400">{{ department.aiEfficiency }}%</span>
              </div>
            </div>
            <div class="mt-3">
              <div class="w-full h-2 rounded-full" style="background: var(--bg-hover);">
                <div class="h-full rounded-full transition-all duration-500" 
                     :style="`width: ${department.performance}%; background: ${department.performance >= 85 ? '#10b981' : department.performance >= 70 ? '#f59e0b' : '#ef4444'};`">
                </div>
              </div>
              <div class="flex justify-between mt-1 text-xs" style="color: var(--text-tertiary);">
                <span>성과 지표</span>
                <span>목표: {{ department.target }}%</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 직원 성과 분석 -->
      <div class="performance-analysis p-6 rounded-xl" style="background: var(--bg-secondary); border: 1px solid var(--border-secondary);">
        <h3 class="text-xl font-semibold mb-4 text-orange-400">직원 성과 분석</h3>
        <div class="space-y-4">
          <div v-for="employee in topPerformers" :key="employee.id"
               class="employee-item p-4 rounded-lg transition-all duration-300 hover:scale-102 cursor-pointer"
               style="background: var(--bg-tertiary); border: 1px solid var(--border-primary);"
               @click="viewEmployeeDetails(employee)">
            <div class="flex items-center justify-between mb-2">
              <div class="flex items-center space-x-3">
                <div class="w-10 h-10 rounded-full flex items-center justify-center" 
                     :style="`background: ${employee.color}20; color: ${employee.color};`">
                  {{ employee.name.charAt(0) }}
                </div>
                <div>
                  <h4 class="font-medium text-white">{{ employee.name }}</h4>
                  <p class="text-xs" style="color: var(--text-tertiary);">{{ employee.position }}</p>
                </div>
              </div>
              <span class="text-sm px-2 py-1 rounded" 
                    :style="`background: ${employee.performanceScore >= 90 ? '#10b981' : employee.performanceScore >= 80 ? '#f59e0b' : '#ef4444'}20; 
                             color: ${employee.performanceScore >= 90 ? '#10b981' : employee.performanceScore >= 80 ? '#f59e0b' : '#ef4444'};`">
                {{ employee.performanceScore }}점
              </span>
            </div>
            <div class="grid grid-cols-2 gap-4 text-sm">
              <div>
                <span style="color: var(--text-tertiary);">부서:</span>
                <span class="ml-2 font-medium text-white">{{ employee.department }}</span>
              </div>
              <div>
                <span style="color: var(--text-tertiary);">경력:</span>
                <span class="ml-2 font-medium text-cyan-400">{{ employee.experience }}년</span>
              </div>
            </div>
            <div class="mt-2 grid grid-cols-2 gap-4 text-sm">
              <div>
                <span style="color: var(--text-tertiary);">목표 달성:</span>
                <span class="ml-2 font-medium text-green-400">{{ employee.goalAchievement }}%</span>
              </div>
              <div>
                <span style="color: var(--text-tertiary);">AI 스킬 매칭:</span>
                <span class="ml-2 font-medium text-purple-400">{{ employee.skillMatch }}%</span>
              </div>
            </div>
            <div class="mt-2">
              <span class="text-xs" style="color: var(--text-tertiary);">
                AI 추천: {{ employee.aiRecommendation }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 인사 관리 및 분석 -->
    <div class="hr-management-section p-6 grid grid-cols-1 xl:grid-cols-3 gap-6">
      <!-- 채용 현황 -->
      <div class="recruitment-status p-6 rounded-xl" style="background: var(--bg-secondary); border: 1px solid var(--border-secondary);">
        <h3 class="text-xl font-semibold mb-4 text-green-400">AI 채용 현황</h3>
        <div class="space-y-3 max-h-64 overflow-y-auto">
          <div v-for="position in openPositions" :key="position.id"
               class="position-item p-3 rounded-lg transition-all duration-300 hover:scale-102 cursor-pointer"
               style="background: var(--bg-tertiary); border: 1px solid var(--border-primary);"
               @click="viewPositionDetails(position)">
            <div class="flex items-center justify-between mb-2">
              <h4 class="font-medium text-white">{{ position.title }}</h4>
              <span class="text-xs px-2 py-1 rounded" 
                    :style="`background: ${position.priority === 'urgent' ? '#ef4444' : position.priority === 'high' ? '#f59e0b' : '#3b82f6'}20; 
                             color: ${position.priority === 'urgent' ? '#ef4444' : position.priority === 'high' ? '#f59e0b' : '#3b82f6'};`">
                {{ position.priority === 'urgent' ? '긴급' : position.priority === 'high' ? '높음' : '보통' }}
              </span>
            </div>
            <div class="grid grid-cols-2 gap-2 text-sm">
              <div>
                <span style="color: var(--text-tertiary);">지원자:</span>
                <span class="ml-1 font-medium text-white">{{ position.applicants }}명</span>
              </div>
              <div>
                <span style="color: var(--text-tertiary);">AI 매칭:</span>
                <span class="ml-1 font-medium text-green-400">{{ position.aiMatches }}명</span>
              </div>
            </div>
            <div class="mt-2 text-sm">
              <span style="color: var(--text-tertiary);">부서:</span>
              <span class="ml-2 font-medium text-cyan-400">{{ position.department }}</span>
            </div>
            <div class="mt-2">
              <span class="text-xs" style="color: var(--text-tertiary);">
                예상 채용완료: {{ position.estimatedCompletion }}
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- 교육 및 개발 -->
      <div class="training-development p-6 rounded-xl" style="background: var(--bg-secondary); border: 1px solid var(--border-secondary);">
        <h3 class="text-xl font-semibold mb-4 text-blue-400">AI 교육 추천</h3>
        <div class="space-y-3 max-h-64 overflow-y-auto">
          <div v-for="training in trainingPrograms" :key="training.id"
               class="training-item p-3 rounded-lg transition-all duration-300 hover:scale-102"
               style="background: var(--bg-tertiary); border: 1px solid var(--border-primary);">
            <div class="flex items-center justify-between mb-2">
              <h4 class="font-medium text-white">{{ training.title }}</h4>
              <span class="text-xs px-2 py-1 rounded" 
                    :style="`background: ${training.urgency === 'high' ? '#ef4444' : training.urgency === 'medium' ? '#f59e0b' : '#10b981'}20; 
                             color: ${training.urgency === 'high' ? '#ef4444' : training.urgency === 'medium' ? '#f59e0b' : '#10b981'};`">
                {{ training.urgency === 'high' ? '필수' : training.urgency === 'medium' ? '권장' : '선택' }}
              </span>
            </div>
            <div class="grid grid-cols-2 gap-2 text-sm">
              <div>
                <span style="color: var(--text-tertiary);">대상자:</span>
                <span class="ml-1 font-medium text-white">{{ training.targetCount }}명</span>
              </div>
              <div>
                <span style="color: var(--text-tertiary);">완료율:</span>
                <span class="ml-1 font-medium text-green-400">{{ training.completionRate }}%</span>
              </div>
            </div>
            <div class="mt-2 text-sm">
              <span style="color: var(--text-tertiary);">기간:</span>
              <span class="ml-2 font-medium text-cyan-400">{{ training.duration }}</span>
            </div>
            <div class="mt-2">
              <span class="text-xs" style="color: var(--text-tertiary);">
                AI 예상 효과: {{ training.expectedImpact }}
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- 급여 및 복리후생 -->
      <div class="compensation-benefits p-6 rounded-xl" style="background: var(--bg-secondary); border: 1px solid var(--border-secondary);">
        <h3 class="text-xl font-semibold mb-4 text-purple-400">급여 분석</h3>
        <div class="space-y-4">
          <div v-for="salaryData in salaryAnalysis" :key="salaryData.level"
               class="salary-item p-3 rounded-lg"
               style="background: var(--bg-tertiary); border: 1px solid var(--border-primary);">
            <div class="flex items-center justify-between mb-2">
              <span class="text-sm font-medium text-white">{{ salaryData.level }}</span>
              <span class="text-sm font-bold text-green-400">
                {{ formatCurrency(salaryData.avgSalary) }}
              </span>
            </div>
            <div class="grid grid-cols-2 gap-2 text-sm">
              <div>
                <span style="color: var(--text-tertiary);">인원:</span>
                <span class="ml-1 font-medium text-white">{{ salaryData.count }}명</span>
              </div>
              <div>
                <span style="color: var(--text-tertiary);">시장 대비:</span>
                <span class="ml-1 font-medium" :class="salaryData.marketComparison >= 0 ? 'text-green-400' : 'text-red-400'">
                  {{ salaryData.marketComparison >= 0 ? '+' : '' }}{{ salaryData.marketComparison }}%
                </span>
              </div>
            </div>
            <div class="mt-2">
              <div class="w-full h-1.5 rounded-full" style="background: var(--bg-hover);">
                <div class="h-full rounded-full transition-all duration-500" 
                     :style="`width: ${Math.min(100, (salaryData.avgSalary / 150000000) * 100)}%; background: linear-gradient(to right, #10b981, #3b82f6);`">
                </div>
              </div>
              <div class="flex justify-between mt-1 text-xs" style="color: var(--text-tertiary);">
                <span>급여 범위</span>
                <span>경쟁력: {{ salaryData.competitiveness }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 인사 인사이트 및 예측 -->
    <div class="insights-section p-6">
      <div class="insights-grid grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- 조직 건강도 -->
        <div class="organization-health p-6 rounded-xl" style="background: var(--bg-secondary); border: 1px solid var(--border-secondary);">
          <h3 class="text-xl font-semibold mb-4 text-pink-400">조직 건강도 분석</h3>
          <div class="health-metrics space-y-4">
            <div v-for="metric in healthMetrics" :key="metric.name"
                 class="metric-item p-4 rounded-lg"
                 style="background: var(--bg-tertiary); border: 1px solid var(--border-primary);">
              <div class="flex items-center justify-between mb-2">
                <span class="text-sm font-medium text-white">{{ metric.name }}</span>
                <span class="text-sm font-bold" :style="`color: ${metric.color};`">
                  {{ metric.score }}/100
                </span>
              </div>
              <div class="w-full h-2 rounded-full" style="background: var(--bg-hover);">
                <div class="h-full rounded-full transition-all duration-500" 
                     :style="`width: ${metric.score}%; background: ${metric.color};`">
                </div>
              </div>
              <div class="flex items-center justify-between mt-2">
                <span class="text-xs" style="color: var(--text-tertiary);">{{ metric.description }}</span>
                <span class="text-xs" :class="metric.trend === 'up' ? 'text-green-400' : metric.trend === 'down' ? 'text-red-400' : 'text-gray-400'">
                  {{ metric.trend === 'up' ? '↗️' : metric.trend === 'down' ? '↘️' : '➡️' }} {{ metric.change }}%
                </span>
              </div>
            </div>
          </div>
        </div>

        <!-- AI 인사 인사이트 -->
        <div class="hr-insights p-6 rounded-xl" style="background: var(--bg-secondary); border: 1px solid var(--border-secondary);">
          <h3 class="text-xl font-semibold mb-4 text-orange-400">AI 인사 인사이트</h3>
          <div class="insights-list space-y-3">
            <div v-for="insight in hrInsights" :key="insight.id"
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
  name: 'HRModule',
  setup() {
    const { executeAIRequest, formatResponse } = useAI()
    
    // 반응형 데이터
    const agiStatus = ref('활성화됨')
    const aiCommand = ref('')
    const aiResponse = ref('')
    
    // 대시보드 메트릭
    const totalEmployees = ref(387)
    const employeeGrowth = ref(8.5)
    const employeeSatisfaction = ref(4.2)
    const satisfactionTrend = ref(7.3)
    const turnoverRate = ref(5.8)
    const aiRecruitments = ref(24)
    const recruitmentAccuracy = ref(89.2)
    
    // 부서별 현황
    const departments = ref([
      { 
        name: '개발팀', 
        headcount: 85, 
        avgExperience: 5.2, 
        satisfaction: 4.5, 
        performance: 92, 
        target: 90, 
        aiEfficiency: 94 
      },
      { 
        name: '영업팀', 
        headcount: 67, 
        avgExperience: 4.8, 
        satisfaction: 4.1, 
        performance: 88, 
        target: 85, 
        aiEfficiency: 87 
      },
      { 
        name: '마케팅팀', 
        headcount: 42, 
        avgExperience: 4.3, 
        satisfaction: 4.3, 
        performance: 85, 
        target: 80, 
        aiEfficiency: 91 
      },
      { 
        name: '운영팀', 
        headcount: 58, 
        avgExperience: 6.1, 
        satisfaction: 3.9, 
        performance: 78, 
        target: 85, 
        aiEfficiency: 82 
      },
      { 
        name: '인사팀', 
        headcount: 15, 
        avgExperience: 7.2, 
        satisfaction: 4.4, 
        performance: 89, 
        target: 85, 
        aiEfficiency: 95 
      }
    ])
    
    // 상위 성과자
    const topPerformers = ref([
      {
        id: 1,
        name: '김민수',
        position: '시니어 개발자',
        department: '개발팀',
        experience: 6,
        performanceScore: 95,
        goalAchievement: 125,
        skillMatch: 98,
        color: '#10b981',
        aiRecommendation: '팀 리더십 교육 추천'
      },
      {
        id: 2,
        name: '이수영',
        position: '영업 매니저',
        department: '영업팀',
        experience: 8,
        performanceScore: 92,
        goalAchievement: 118,
        skillMatch: 94,
        color: '#3b82f6',
        aiRecommendation: '전략 기획 역량 강화'
      },
      {
        id: 3,
        name: '박지훈',
        position: '마케팅 전문가',
        department: '마케팅팀',
        experience: 4,
        performanceScore: 89,
        goalAchievement: 112,
        skillMatch: 91,
        color: '#8b5cf6',
        aiRecommendation: '데이터 분석 스킬 향상'
      },
      {
        id: 4,
        name: '최혜진',
        position: '프로젝트 매니저',
        department: '운영팀',
        experience: 7,
        performanceScore: 87,
        goalAchievement: 108,
        skillMatch: 89,
        color: '#f59e0b',
        aiRecommendation: 'AI 도구 활용 교육'
      }
    ])
    
    // 채용 공고
    const openPositions = ref([
      {
        id: 1,
        title: 'AI 엔지니어',
        department: '개발팀',
        applicants: 145,
        aiMatches: 23,
        priority: 'urgent',
        estimatedCompletion: '2주'
      },
      {
        id: 2,
        title: '디지털 마케터',
        department: '마케팅팀',
        applicants: 89,
        aiMatches: 15,
        priority: 'high',
        estimatedCompletion: '3주'
      },
      {
        id: 3,
        title: '데이터 분석가',
        department: '운영팀',
        applicants: 67,
        aiMatches: 12,
        priority: 'medium',
        estimatedCompletion: '4주'
      }
    ])
    
    // 교육 프로그램
    const trainingPrograms = ref([
      {
        id: 1,
        title: 'AI 활용 실무',
        targetCount: 125,
        completionRate: 78,
        duration: '4주',
        urgency: 'high',
        expectedImpact: '생산성 25% 향상'
      },
      {
        id: 2,
        title: '리더십 개발',
        targetCount: 45,
        completionRate: 85,
        duration: '6주',
        urgency: 'medium',
        expectedImpact: '팀 성과 15% 개선'
      },
      {
        id: 3,
        title: '디지털 전환',
        targetCount: 200,
        completionRate: 62,
        duration: '8주',
        urgency: 'medium',
        expectedImpact: '프로세스 효율 30% 증대'
      }
    ])
    
    // 급여 분석
    const salaryAnalysis = ref([
      {
        level: '신입/주니어',
        count: 89,
        avgSalary: 42000000,
        marketComparison: 8.5,
        competitiveness: '경쟁력 있음'
      },
      {
        level: '중급/시니어',
        count: 156,
        avgSalary: 68000000,
        marketComparison: 12.3,
        competitiveness: '매우 경쟁력 있음'
      },
      {
        level: '팀장/매니저',
        count: 67,
        avgSalary: 95000000,
        marketComparison: 6.7,
        competitiveness: '경쟁력 있음'
      },
      {
        level: '임원/C-Level',
        count: 15,
        avgSalary: 140000000,
        marketComparison: -3.2,
        competitiveness: '개선 필요'
      }
    ])
    
    // 조직 건강도 지표
    const healthMetrics = ref([
      {
        name: '직원 참여도',
        score: 87,
        description: '업무 몰입과 적극성',
        trend: 'up',
        change: 5.2,
        color: '#10b981'
      },
      {
        name: '소통 효율성',
        score: 82,
        description: '부서간 협업과 정보 공유',
        trend: 'up',
        change: 3.8,
        color: '#3b82f6'
      },
      {
        name: '학습 문화',
        score: 79,
        description: '지속적 학습과 성장 마인드',
        trend: 'up',
        change: 8.1,
        color: '#8b5cf6'
      },
      {
        name: '워라밸',
        score: 74,
        description: '일과 삶의 균형',
        trend: 'down',
        change: -2.3,
        color: '#f59e0b'
      },
      {
        name: '혁신 역량',
        score: 85,
        description: '새로운 아이디어와 개선 제안',
        trend: 'up',
        change: 6.7,
        color: '#06b6d4'
      }
    ])
    
    // HR 인사이트
    const hrInsights = ref([
      {
        id: 1,
        title: '개발팀 번아웃 위험 증가',
        description: '최근 3개월간 개발팀의 야근 시간이 30% 증가했습니다. 조기 대응이 필요합니다.',
        priority: 'critical',
        confidence: 92,
        icon: '🔥',
        color: '#ef4444'
      },
      {
        id: 2,
        title: '고성과자 이직 위험 감지',
        description: '상위 10% 성과자 중 3명의 이직 신호가 감지되었습니다.',
        priority: 'high',
        confidence: 87,
        icon: '⚡',
        color: '#f59e0b'
      },
      {
        id: 3,
        title: '신규 인재 적응 프로그램 효과',
        description: '새로운 온보딩 프로그램으로 신입사원 만족도가 25% 향상되었습니다.',
        priority: 'medium',
        confidence: 89,
        icon: '🎯',
        color: '#10b981'
      },
      {
        id: 4,
        title: '원격근무 생산성 분석',
        description: '원격근무 팀의 생산성이 사무실 근무 대비 95% 수준을 유지하고 있습니다.',
        priority: 'medium',
        confidence: 84,
        icon: '💻',
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
        const response = await executeAIRequest(aiCommand.value, 'hr')
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
      employeeSatisfaction.value = Math.round((employeeSatisfaction.value + Math.random() * 0.2 - 0.1) * 10) / 10
      aiRecruitments.value += Math.floor(Math.random() * 3)
      turnoverRate.value = Math.round((turnoverRate.value + Math.random() * 0.5 - 0.25) * 10) / 10
    }
    
    const viewDepartmentDetails = (department) => {
      aiResponse.value = `부서 상세 분석:
      
부서명: ${department.name}
인원: ${department.headcount}명
평균 경력: ${department.avgExperience}년

성과 지표:
- 부서 성과: ${department.performance}% (목표: ${department.target}%)
- 직원 만족도: ${department.satisfaction}/5.0
- AI 효율성: ${department.aiEfficiency}%

AI 종합 평가:
${department.performance >= 85 ? '- 성과: 우수한 수준으로 지속 유지 권장' : department.performance >= 70 ? '- 성과: 양호하나 개선 여지 있음' : '- 성과: 즉시 개선 조치 필요'}
${department.satisfaction >= 4.0 ? '- 만족도: 높은 수준 유지' : '- 만족도: 개선 프로그램 도입 권장'}
${department.aiEfficiency >= 90 ? '- AI 활용: 최적화 완료' : '- AI 활용: 추가 교육 및 도구 도입 필요'}

추천 액션:
1. ${department.performance < department.target ? '성과 개선을 위한 목표 재설정' : '현재 성과 유지 전략 수립'}
2. ${department.satisfaction < 4.0 ? '팀 빌딩 및 복지 개선 프로그램' : '우수 사례 타 부서 전파'}
3. ${department.aiEfficiency < 90 ? 'AI 도구 활용 교육 강화' : 'AI 고도화 프로젝트 참여'}`
    }
    
    const viewEmployeeDetails = (employee) => {
      aiResponse.value = `직원 상세 프로필:
      
이름: ${employee.name}
직책: ${employee.position}
부서: ${employee.department}
경력: ${employee.experience}년

성과 분석:
- 종합 성과 점수: ${employee.performanceScore}/100
- 목표 달성률: ${employee.goalAchievement}%
- 스킬 매칭도: ${employee.skillMatch}%

AI 평가:
${employee.performanceScore >= 90 ? '최상위 성과자 - 리더십 역할 부여 검토' : employee.performanceScore >= 80 ? '우수 성과자 - 추가 책임 부여 가능' : '성과 개선 지원 필요'}

AI 추천사항:
- ${employee.aiRecommendation}
- ${employee.goalAchievement > 110 ? '도전적 목표 설정으로 동기 부여' : '목표 달성 지원 프로그램 참여'}
- ${employee.skillMatch > 95 ? '멘토링 역할 부여 검토' : '스킬 갭 분석 및 교육 계획 수립'}

경력 개발 로드맵:
1. 단기 (6개월): 현재 역량 강화 및 성과 목표 달성
2. 중기 (1-2년): 리더십/전문성 개발 프로그램 참여
3. 장기 (3-5년): 승진 트랙 또는 전문가 트랙 선택`
    }
    
    const viewPositionDetails = (position) => {
      aiResponse.value = `채용 공고 상세:
      
포지션: ${position.title}
부서: ${position.department}
우선순위: ${position.priority === 'urgent' ? '긴급' : position.priority === 'high' ? '높음' : '보통'}

지원 현황:
- 총 지원자: ${position.applicants}명
- AI 1차 합격자: ${position.aiMatches}명
- 합격률: ${Math.round((position.aiMatches / position.applicants) * 100)}%

AI 스크리닝 결과:
- 기술 역량 매칭: 상위 ${Math.floor(Math.random() * 20 + 70)}%
- 문화 적합성: 상위 ${Math.floor(Math.random() * 15 + 80)}%
- 성장 잠재력: 상위 ${Math.floor(Math.random() * 25 + 65)}%

채용 프로세스:
1. AI 1차 스크리닝 (완료)
2. 실무진 면접 (진행중)
3. 임원 면접 (대기)
4. 처우 협상 및 최종 결정

예상 채용 완료: ${position.estimatedCompletion}
추천 액션: ${position.priority === 'urgent' ? '즉시 면접 일정 조율' : '정상 프로세스 진행'}`
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
      totalEmployees,
      employeeGrowth,
      employeeSatisfaction,
      satisfactionTrend,
      turnoverRate,
      aiRecruitments,
      recruitmentAccuracy,
      
      // 데이터
      departments,
      topPerformers,
      openPositions,
      trainingPrograms,
      salaryAnalysis,
      healthMetrics,
      hrInsights,
      
      // 메서드
      formatCurrency,
      executeAICommand,
      clearAICommand,
      refreshDashboard,
      viewDepartmentDetails,
      viewEmployeeDetails,
      viewPositionDetails
    }
  }
}
</script>

<style scoped>
.hr-module {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

.dashboard-card:hover {
  transform: translateY(-2px);
}

.department-item:hover,
.employee-item:hover,
.position-item:hover,
.training-item:hover,
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
  
  .hr-management-section {
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