<template>
  <div class="projects-module min-h-screen" style="background: var(--bg-primary); color: var(--text-primary);">
    <!-- 헤더 -->
    <div class="header-section p-6 border-b" style="border-color: var(--border-primary); background: var(--bg-secondary);">
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-3xl font-bold bg-gradient-to-r from-indigo-400 to-teal-400 bg-clip-text text-transparent">
            프로젝트 관리 (Project Management)
          </h1>
          <p class="text-gray-400 mt-2">AI 기반 프로젝트 최적화 및 자동 스케줄링</p>
        </div>
        <div class="flex items-center space-x-4">
          <div class="agi-status px-4 py-2 rounded-lg" style="background: var(--bg-tertiary); border: 1px solid var(--ai-primary);">
            <span class="text-sm">AGI 상태: </span>
            <span class="text-green-400 font-semibold">{{ agiStatus }}</span>
          </div>
          <button 
            @click="refreshDashboard"
            class="bg-indigo-600 hover:bg-indigo-700 px-4 py-2 rounded-lg transition-all duration-300 text-white"
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
        <h3 class="text-lg font-semibold mb-3 text-indigo-400">AI 프로젝트 어시스턴트</h3>
        <div class="flex space-x-4">
          <textarea 
            v-model="aiCommand"
            placeholder="프로젝트 관련 자연어 명령을 입력하세요... 예: '프로젝트 일정 최적화해줘', '리스크 분석해줘', '자원 배치 추천해줘'"
            class="flex-1 p-4 rounded-lg resize-none transition-all duration-300"
            style="background: var(--bg-tertiary); border: 1px solid var(--border-secondary); color: var(--text-primary); min-height: 80px;"
            @focus="$event.target.style.borderColor = 'var(--ai-primary)'"
            @blur="$event.target.style.borderColor = 'var(--border-secondary)'"
          ></textarea>
          <div class="flex flex-col space-y-2">
            <button 
              @click="executeAICommand"
              :disabled="!aiCommand.trim()"
              class="bg-gradient-to-r from-indigo-500 to-teal-600 hover:from-indigo-600 hover:to-teal-700 disabled:opacity-50 px-6 py-3 rounded-lg transition-all duration-300 text-white font-medium"
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
      <!-- 활성 프로젝트 -->
      <div class="dashboard-card p-6 rounded-xl transition-all duration-300 hover:scale-105" 
           style="background: var(--bg-secondary); border: 1px solid var(--border-secondary);"
           @mouseenter="$event.target.style.boxShadow = 'var(--glow-primary)'"
           @mouseleave="$event.target.style.boxShadow = 'none'">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm font-medium" style="color: var(--text-secondary);">활성 프로젝트</p>
            <p class="text-2xl font-bold text-indigo-400">{{ activeProjects }}</p>
            <p class="text-xs mt-1" :class="projectGrowth >= 0 ? 'text-green-400' : 'text-red-400'">
              {{ projectGrowth >= 0 ? '+' : '' }}{{ projectGrowth }}% 전월 대비
            </p>
          </div>
          <div class="text-indigo-400 text-3xl">📁</div>
        </div>
      </div>

      <!-- 평균 완료율 -->
      <div class="dashboard-card p-6 rounded-xl transition-all duration-300 hover:scale-105" 
           style="background: var(--bg-secondary); border: 1px solid var(--border-secondary);"
           @mouseenter="$event.target.style.boxShadow = 'var(--glow-secondary)'"
           @mouseleave="$event.target.style.boxShadow = 'none'">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm font-medium" style="color: var(--text-secondary);">평균 완료율</p>
            <p class="text-2xl font-bold text-teal-400">{{ avgCompletionRate }}%</p>
            <p class="text-xs mt-1 text-green-400">목표 대비 {{ completionTrend }}% 초과</p>
          </div>
          <div class="text-teal-400 text-3xl">📊</div>
        </div>
      </div>

      <!-- 지연 프로젝트 -->
      <div class="dashboard-card p-6 rounded-xl transition-all duration-300 hover:scale-105" 
           style="background: var(--bg-secondary); border: 1px solid var(--border-secondary);"
           @mouseenter="$event.target.style.boxShadow = 'var(--glow-accent)'"
           @mouseleave="$event.target.style.boxShadow = 'none'">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm font-medium" style="color: var(--text-secondary);">지연 프로젝트</p>
            <p class="text-2xl font-bold text-yellow-400">{{ delayedProjects }}</p>
            <p class="text-xs mt-1 text-red-400">{{ delayRate }}% 지연률</p>
          </div>
          <div class="text-yellow-400 text-3xl">⚠️</div>
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
            <p class="text-2xl font-bold text-green-400">{{ aiAccuracy }}%</p>
            <p class="text-xs mt-1 text-green-400">{{ accuracyTrend }}% 향상</p>
          </div>
          <div class="text-green-400 text-3xl">🎯</div>
        </div>
      </div>
    </div>

    <!-- 메인 콘텐츠 영역 -->
    <div class="main-content p-6 grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- 프로젝트 현황 -->
      <div class="projects-overview p-6 rounded-xl" style="background: var(--bg-secondary); border: 1px solid var(--border-secondary);">
        <h3 class="text-xl font-semibold mb-4 text-indigo-400">프로젝트 현황</h3>
        <div class="space-y-4">
          <div v-for="project in projects" :key="project.id" 
               class="project-item p-4 rounded-lg transition-all duration-300 hover:scale-102 cursor-pointer"
               style="background: var(--bg-tertiary); border: 1px solid var(--border-primary);"
               @click="viewProjectDetails(project)">
            <div class="flex items-center justify-between mb-2">
              <h4 class="font-medium text-white">{{ project.name }}</h4>
              <span class="text-sm px-2 py-1 rounded" 
                    :style="`background: ${project.status === 'on-track' ? '#10b981' : project.status === 'at-risk' ? '#f59e0b' : '#ef4444'}20; 
                             color: ${project.status === 'on-track' ? '#10b981' : project.status === 'at-risk' ? '#f59e0b' : '#ef4444'};`">
                {{ project.status === 'on-track' ? '정상' : project.status === 'at-risk' ? '위험' : '지연' }}
              </span>
            </div>
            <div class="grid grid-cols-2 gap-4 text-sm mb-3">
              <div>
                <span style="color: var(--text-tertiary);">진행률:</span>
                <span class="ml-2 font-medium text-white">{{ project.progress }}%</span>
              </div>
              <div>
                <span style="color: var(--text-tertiary);">팀원:</span>
                <span class="ml-2 font-medium text-cyan-400">{{ project.teamSize }}명</span>
              </div>
            </div>
            <div class="mb-3">
              <div class="w-full h-2 rounded-full" style="background: var(--bg-hover);">
                <div class="h-full rounded-full transition-all duration-500" 
                     :style="`width: ${project.progress}%; background: ${project.status === 'on-track' ? '#10b981' : project.status === 'at-risk' ? '#f59e0b' : '#ef4444'};`">
                </div>
              </div>
            </div>
            <div class="grid grid-cols-2 gap-4 text-sm">
              <div>
                <span style="color: var(--text-tertiary);">마감일:</span>
                <span class="ml-2 font-medium text-white">{{ project.deadline }}</span>
              </div>
              <div>
                <span style="color: var(--text-tertiary);">AI 예측:</span>
                <span class="ml-2 font-medium text-purple-400">{{ project.aiPrediction }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 팀 성과 분석 -->
      <div class="team-performance p-6 rounded-xl" style="background: var(--bg-secondary); border: 1px solid var(--border-secondary);">
        <h3 class="text-xl font-semibold mb-4 text-teal-400">팀 성과 분석</h3>
        <div class="space-y-4">
          <div v-for="team in teams" :key="team.id"
               class="team-item p-4 rounded-lg transition-all duration-300 hover:scale-102 cursor-pointer"
               style="background: var(--bg-tertiary); border: 1px solid var(--border-primary);"
               @click="viewTeamDetails(team)">
            <div class="flex items-center justify-between mb-2">
              <h4 class="font-medium text-white">{{ team.name }}</h4>
              <div class="flex items-center space-x-2">
                <span class="text-sm px-2 py-1 rounded" 
                      :style="`background: ${team.efficiency >= 85 ? '#10b981' : team.efficiency >= 70 ? '#f59e0b' : '#ef4444'}20; 
                               color: ${team.efficiency >= 85 ? '#10b981' : team.efficiency >= 70 ? '#f59e0b' : '#ef4444'};`">
                  {{ team.efficiency }}%
                </span>
              </div>
            </div>
            <div class="grid grid-cols-2 gap-4 text-sm">
              <div>
                <span style="color: var(--text-tertiary);">활성 프로젝트:</span>
                <span class="ml-2 font-medium text-white">{{ team.activeProjects }}개</span>
              </div>
              <div>
                <span style="color: var(--text-tertiary);">팀원 수:</span>
                <span class="ml-2 font-medium text-cyan-400">{{ team.members }}명</span>
              </div>
            </div>
            <div class="mt-2 grid grid-cols-2 gap-4 text-sm">
              <div>
                <span style="color: var(--text-tertiary);">완료율:</span>
                <span class="ml-2 font-medium text-green-400">{{ team.completionRate }}%</span>
              </div>
              <div>
                <span style="color: var(--text-tertiary);">만족도:</span>
                <span class="ml-2 font-medium text-orange-400">{{ team.satisfaction }}/5</span>
              </div>
            </div>
            <div class="mt-3">
              <div class="w-full h-2 rounded-full" style="background: var(--bg-hover);">
                <div class="h-full rounded-full transition-all duration-500" 
                     :style="`width: ${team.efficiency}%; background: ${team.efficiency >= 85 ? '#10b981' : team.efficiency >= 70 ? '#f59e0b' : '#ef4444'};`">
                </div>
              </div>
              <div class="flex justify-between mt-1 text-xs" style="color: var(--text-tertiary);">
                <span>효율성 지표</span>
                <span>AI 추천: {{ team.aiRecommendation }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 프로젝트 관리 및 분석 -->
    <div class="project-management-section p-6 grid grid-cols-1 xl:grid-cols-3 gap-6">
      <!-- 일정 관리 -->
      <div class="schedule-management p-6 rounded-xl" style="background: var(--bg-secondary); border: 1px solid var(--border-secondary);">
        <h3 class="text-xl font-semibold mb-4 text-green-400">AI 일정 관리</h3>
        <div class="space-y-3 max-h-64 overflow-y-auto">
          <div v-for="task in upcomingTasks" :key="task.id"
               class="task-item p-3 rounded-lg transition-all duration-300 hover:scale-102 cursor-pointer"
               style="background: var(--bg-tertiary); border: 1px solid var(--border-primary);"
               @click="viewTaskDetails(task)">
            <div class="flex items-center justify-between mb-2">
              <h4 class="font-medium text-white">{{ task.title }}</h4>
              <span class="text-xs px-2 py-1 rounded" 
                    :style="`background: ${task.priority === 'high' ? '#ef4444' : task.priority === 'medium' ? '#f59e0b' : '#10b981'}20; 
                             color: ${task.priority === 'high' ? '#ef4444' : task.priority === 'medium' ? '#f59e0b' : '#10b981'};`">
                {{ task.priority === 'high' ? '높음' : task.priority === 'medium' ? '보통' : '낮음' }}
              </span>
            </div>
            <div class="grid grid-cols-2 gap-2 text-sm">
              <div>
                <span style="color: var(--text-tertiary);">담당자:</span>
                <span class="ml-1 font-medium text-white">{{ task.assignee }}</span>
              </div>
              <div>
                <span style="color: var(--text-tertiary);">마감:</span>
                <span class="ml-1 font-medium text-red-400">{{ task.dueDate }}</span>
              </div>
            </div>
            <div class="mt-2 text-sm">
              <span style="color: var(--text-tertiary);">프로젝트:</span>
              <span class="ml-2 font-medium text-cyan-400">{{ task.project }}</span>
            </div>
            <div class="mt-2">
              <span class="text-xs" style="color: var(--text-tertiary);">
                AI 추정 소요시간: {{ task.estimatedHours }}시간
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- 리스크 관리 -->
      <div class="risk-management p-6 rounded-xl" style="background: var(--bg-secondary); border: 1px solid var(--border-secondary);">
        <h3 class="text-xl font-semibold mb-4 text-red-400">AI 리스크 분석</h3>
        <div class="space-y-3 max-h-64 overflow-y-auto">
          <div v-for="risk in projectRisks" :key="risk.id"
               class="risk-item p-3 rounded-lg transition-all duration-300 hover:scale-102"
               style="background: var(--bg-tertiary); border: 1px solid var(--border-primary);">
            <div class="flex items-center justify-between mb-2">
              <h4 class="font-medium text-white">{{ risk.title }}</h4>
              <span class="text-xs px-2 py-1 rounded" 
                    :style="`background: ${risk.severity === 'critical' ? '#ef4444' : risk.severity === 'high' ? '#f59e0b' : '#10b981'}20; 
                             color: ${risk.severity === 'critical' ? '#ef4444' : risk.severity === 'high' ? '#f59e0b' : '#10b981'};`">
                {{ risk.severity === 'critical' ? '심각' : risk.severity === 'high' ? '높음' : '보통' }}
              </span>
            </div>
            <p class="text-sm mb-2" style="color: var(--text-secondary);">{{ risk.description }}</p>
            <div class="grid grid-cols-2 gap-2 text-sm">
              <div>
                <span style="color: var(--text-tertiary);">확률:</span>
                <span class="ml-1 font-medium text-white">{{ risk.probability }}%</span>
              </div>
              <div>
                <span style="color: var(--text-tertiary);">영향도:</span>
                <span class="ml-1 font-medium text-red-400">{{ risk.impact }}/10</span>
              </div>
            </div>
            <div class="mt-2">
              <span class="text-xs" style="color: var(--text-tertiary);">
                AI 대응 방안: {{ risk.mitigation }}
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- 자원 배치 -->
      <div class="resource-allocation p-6 rounded-xl" style="background: var(--bg-secondary); border: 1px solid var(--border-secondary);">
        <h3 class="text-xl font-semibold mb-4 text-purple-400">AI 자원 최적화</h3>
        <div class="space-y-4">
          <div v-for="resource in resourceAllocation" :key="resource.id"
               class="resource-item p-3 rounded-lg"
               style="background: var(--bg-tertiary); border: 1px solid var(--border-primary);">
            <div class="flex items-center justify-between mb-2">
              <span class="text-sm font-medium text-white">{{ resource.name }}</span>
              <span class="text-sm font-bold" :style="`color: ${resource.utilization >= 85 ? '#ef4444' : resource.utilization >= 70 ? '#f59e0b' : '#10b981'};`">
                {{ resource.utilization }}%
              </span>
            </div>
            <div class="grid grid-cols-2 gap-2 text-sm">
              <div>
                <span style="color: var(--text-tertiary);">가용성:</span>
                <span class="ml-1 font-medium text-white">{{ resource.availability }}h</span>
              </div>
              <div>
                <span style="color: var(--text-tertiary);">할당:</span>
                <span class="ml-1 font-medium text-cyan-400">{{ resource.allocated }}h</span>
              </div>
            </div>
            <div class="mt-2">
              <div class="w-full h-1.5 rounded-full" style="background: var(--bg-hover);">
                <div class="h-full rounded-full transition-all duration-500" 
                     :style="`width: ${resource.utilization}%; background: ${resource.utilization >= 85 ? '#ef4444' : resource.utilization >= 70 ? '#f59e0b' : '#10b981'};`">
                </div>
              </div>
              <div class="flex justify-between mt-1 text-xs" style="color: var(--text-tertiary);">
                <span>{{ resource.skills }}</span>
                <span>효율: {{ resource.efficiency }}%</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 프로젝트 인사이트 및 예측 -->
    <div class="insights-section p-6">
      <div class="insights-grid grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- 성과 대시보드 -->
        <div class="performance-dashboard p-6 rounded-xl" style="background: var(--bg-secondary); border: 1px solid var(--border-secondary);">
          <h3 class="text-xl font-semibold mb-4 text-indigo-400">프로젝트 성과 대시보드</h3>
          <div class="performance-metrics space-y-4">
            <div v-for="metric in performanceMetrics" :key="metric.name"
                 class="metric-item p-4 rounded-lg"
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
              <div class="flex items-center justify-between mt-2">
                <span class="text-xs" style="color: var(--text-tertiary);">목표: {{ metric.target }}{{ metric.unit }}</span>
                <span class="text-xs" :class="metric.trend === 'up' ? 'text-green-400' : metric.trend === 'down' ? 'text-red-400' : 'text-gray-400'">
                  {{ metric.trend === 'up' ? '↗️' : metric.trend === 'down' ? '↘️' : '➡️' }} {{ metric.change }}%
                </span>
              </div>
            </div>
          </div>
        </div>

        <!-- AI 프로젝트 인사이트 -->
        <div class="project-insights p-6 rounded-xl" style="background: var(--bg-secondary); border: 1px solid var(--border-secondary);">
          <h3 class="text-xl font-semibold mb-4 text-teal-400">AI 프로젝트 인사이트</h3>
          <div class="insights-list space-y-3">
            <div v-for="insight in projectInsights" :key="insight.id"
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
                      영향도: {{ insight.impact }}/10
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
  name: 'ProjectsModule',
  setup() {
    const { executeAIRequest, formatResponse } = useAI()
    
    // 반응형 데이터
    const agiStatus = ref('활성화됨')
    const aiCommand = ref('')
    const aiResponse = ref('')
    
    // 대시보드 메트릭
    const activeProjects = ref(42)
    const projectGrowth = ref(15.3)
    const avgCompletionRate = ref(87.5)
    const completionTrend = ref(12.8)
    const delayedProjects = ref(3)
    const delayRate = ref(7.1)
    const aiAccuracy = ref(93.2)
    const accuracyTrend = ref(8.7)
    
    // 프로젝트 목록
    const projects = ref([
      {
        id: 1,
        name: 'AI ERP 시스템 고도화',
        progress: 78,
        teamSize: 12,
        deadline: '2024-03-15',
        status: 'on-track',
        aiPrediction: '정시 완료 예상'
      },
      {
        id: 2,
        name: '모바일 앱 리뉴얼',
        progress: 45,
        teamSize: 8,
        deadline: '2024-02-28',
        status: 'at-risk',
        aiPrediction: '1주 지연 가능성'
      },
      {
        id: 3,
        name: '데이터 분석 플랫폼',
        progress: 92,
        teamSize: 6,
        deadline: '2024-01-30',
        status: 'on-track',
        aiPrediction: '조기 완료 가능'
      },
      {
        id: 4,
        name: 'IoT 통합 시스템',
        progress: 25,
        teamSize: 15,
        deadline: '2024-04-20',
        status: 'delayed',
        aiPrediction: '2주 지연 예상'
      }
    ])
    
    // 팀 현황
    const teams = ref([
      {
        id: 1,
        name: '프론트엔드팀',
        efficiency: 92,
        activeProjects: 5,
        members: 8,
        completionRate: 95,
        satisfaction: 4.6,
        aiRecommendation: '워크로드 균형 조정'
      },
      {
        id: 2,
        name: '백엔드팀',
        efficiency: 88,
        activeProjects: 6,
        members: 10,
        completionRate: 89,
        satisfaction: 4.3,
        aiRecommendation: 'API 최적화 집중'
      },
      {
        id: 3,
        name: 'DevOps팀',
        efficiency: 85,
        activeProjects: 3,
        members: 5,
        completionRate: 92,
        satisfaction: 4.4,
        aiRecommendation: '자동화 도구 확대'
      },
      {
        id: 4,
        name: 'QA팀',
        efficiency: 76,
        activeProjects: 8,
        members: 6,
        completionRate: 83,
        satisfaction: 3.9,
        aiRecommendation: '테스트 자동화 필요'
      }
    ])
    
    // 다가오는 작업
    const upcomingTasks = ref([
      {
        id: 1,
        title: 'API 통합 테스트',
        assignee: '김개발',
        dueDate: '1월 25일',
        priority: 'high',
        project: 'AI ERP 고도화',
        estimatedHours: 16
      },
      {
        id: 2,
        title: 'UI/UX 디자인 검토',
        assignee: '이디자인',
        dueDate: '1월 26일',
        priority: 'medium',
        project: '모바일 앱 리뉴얼',
        estimatedHours: 8
      },
      {
        id: 3,
        title: '성능 최적화',
        assignee: '박최적',
        dueDate: '1월 27일',
        priority: 'high',
        project: '데이터 분석 플랫폼',
        estimatedHours: 24
      }
    ])
    
    // 프로젝트 리스크
    const projectRisks = ref([
      {
        id: 1,
        title: '핵심 개발자 부재',
        description: '시니어 개발자의 휴가로 인한 개발 지연 위험',
        severity: 'high',
        probability: 75,
        impact: 8,
        mitigation: '백업 개발자 배치 및 업무 분산'
      },
      {
        id: 2,
        title: '외부 API 의존성',
        description: '서드파티 API 변경으로 인한 호환성 문제',
        severity: 'medium',
        probability: 45,
        impact: 6,
        mitigation: '대체 API 준비 및 모니터링 강화'
      },
      {
        id: 3,
        title: '예산 초과 가능성',
        description: '추가 요구사항으로 인한 개발 비용 증가',
        severity: 'critical',
        probability: 60,
        impact: 9,
        mitigation: '범위 재정의 및 우선순위 조정'
      }
    ])
    
    // 자원 배치
    const resourceAllocation = ref([
      {
        id: 1,
        name: '김시니어',
        utilization: 95,
        availability: 40,
        allocated: 38,
        skills: 'Full-Stack',
        efficiency: 98
      },
      {
        id: 2,
        name: '이주니어',
        utilization: 70,
        availability: 40,
        allocated: 28,
        skills: 'Frontend',
        efficiency: 85
      },
      {
        id: 3,
        name: '박백엔드',
        utilization: 82,
        availability: 40,
        allocated: 33,
        skills: 'Backend',
        efficiency: 92
      },
      {
        id: 4,
        name: '최DevOps',
        utilization: 65,
        availability: 40,
        allocated: 26,
        skills: 'DevOps',
        efficiency: 88
      }
    ])
    
    // 성과 지표
    const performanceMetrics = ref([
      {
        name: '프로젝트 성공률',
        value: 89,
        unit: '%',
        target: 85,
        percentage: 89,
        trend: 'up',
        change: 7.2,
        color: '#10b981'
      },
      {
        name: '일정 준수율',
        value: 78,
        unit: '%',
        target: 80,
        percentage: 78,
        trend: 'down',
        change: -3.5,
        color: '#f59e0b'
      },
      {
        name: '품질 점수',
        value: 4.3,
        unit: '/5',
        target: 4.0,
        percentage: 86,
        trend: 'up',
        change: 12.8,
        color: '#3b82f6'
      },
      {
        name: '팀 만족도',
        value: 4.1,
        unit: '/5',
        target: 4.2,
        percentage: 82,
        trend: 'up',
        change: 5.1,
        color: '#8b5cf6'
      }
    ])
    
    // 프로젝트 인사이트
    const projectInsights = ref([
      {
        id: 1,
        title: '스프린트 속도 증가 감지',
        description: '팀의 개발 속도가 지난 3주간 25% 향상되었습니다. 이 추세가 지속되면 프로젝트 조기 완료가 가능합니다.',
        priority: 'high',
        impact: 8,
        icon: '🚀',
        color: '#10b981'
      },
      {
        id: 2,
        title: '기술 부채 누적 경고',
        description: '빠른 개발 진행으로 인해 기술 부채가 증가하고 있습니다. 리팩토링 시간 확보가 필요합니다.',
        priority: 'medium',
        impact: 7,
        icon: '⚠️',
        color: '#f59e0b'
      },
      {
        id: 3,
        title: '크로스 팀 협업 개선',
        description: '새로운 협업 도구 도입으로 팀 간 커뮤니케이션 효율성이 40% 향상되었습니다.',
        priority: 'medium',
        impact: 6,
        icon: '🤝',
        color: '#3b82f6'
      },
      {
        id: 4,
        title: '자동화 효과 분석',
        description: 'CI/CD 파이프라인 개선으로 배포 시간이 60% 단축되었습니다.',
        priority: 'medium',
        impact: 5,
        icon: '⚙️',
        color: '#06b6d4'
      }
    ])
    
    // 메서드
    const executeAICommand = async () => {
      if (!aiCommand.value.trim()) return
      
      try {
        aiResponse.value = '처리 중...'
        
        // AI 요청 실행
        const response = await executeAIRequest(aiCommand.value, 'projects')
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
      avgCompletionRate.value = Math.round((avgCompletionRate.value + Math.random() * 2 - 1) * 10) / 10
      aiAccuracy.value = Math.round((aiAccuracy.value + Math.random() * 1 - 0.5) * 10) / 10
      
      // 프로젝트 진행률 업데이트
      projects.value.forEach(project => {
        if (project.progress < 100) {
          project.progress = Math.min(100, project.progress + Math.floor(Math.random() * 5))
        }
      })
    }
    
    const viewProjectDetails = (project) => {
      aiResponse.value = `프로젝트 상세 분석:
      
프로젝트명: ${project.name}
진행률: ${project.progress}%
팀 규모: ${project.teamSize}명
마감일: ${project.deadline}

현재 상태: ${project.status === 'on-track' ? '정상 진행' : project.status === 'at-risk' ? '위험 상태' : '지연 상태'}
AI 예측: ${project.aiPrediction}

AI 종합 분석:
${project.progress >= 80 ? '- 프로젝트가 막바지에 접어들었습니다' : project.progress >= 50 ? '- 중간 단계로 순조롭게 진행 중입니다' : '- 초기 단계로 집중적인 관리가 필요합니다'}
${project.status === 'on-track' ? '- 현재 일정대로 진행 중이며 추가 조치 불필요' : project.status === 'at-risk' ? '- 위험 요소가 감지되어 모니터링 강화 필요' : '- 즉시 개선 조치가 필요한 상황'}

추천 액션:
1. ${project.progress < 50 ? '초기 단계 위험 요소 점검 및 제거' : project.progress < 80 ? '중간 점검 및 품질 관리 강화' : '최종 검토 및 배포 준비'}
2. ${project.teamSize > 10 ? '대규모 팀 커뮤니케이션 최적화' : '팀 효율성 극대화 방안 적용'}
3. ${project.status !== 'on-track' ? '리스크 완화 계획 즉시 실행' : '현재 진행 방식 유지 및 베스트 프랙티스 문서화'}`
    }
    
    const viewTeamDetails = (team) => {
      aiResponse.value = `팀 상세 분석:
      
팀명: ${team.name}
팀원 수: ${team.members}명
활성 프로젝트: ${team.activeProjects}개

성과 지표:
- 팀 효율성: ${team.efficiency}%
- 프로젝트 완료율: ${team.completionRate}%
- 팀원 만족도: ${team.satisfaction}/5.0

AI 평가:
${team.efficiency >= 90 ? '최고 수준의 효율성을 보이는 팀입니다' : team.efficiency >= 80 ? '우수한 성과를 보이는 팀입니다' : '개선이 필요한 팀입니다'}
${team.satisfaction >= 4.5 ? '팀원 만족도가 매우 높습니다' : team.satisfaction >= 4.0 ? '팀원 만족도가 양호합니다' : '팀원 만족도 개선이 필요합니다'}

AI 추천사항: ${team.aiRecommendation}

개선 방안:
1. ${team.efficiency < 85 ? '효율성 향상을 위한 프로세스 개선' : '현재 효율성 유지 방안 수립'}
2. ${team.satisfaction < 4.0 ? '팀 빌딩 및 복지 개선 프로그램 도입' : '팀 문화 우수 사례 전파'}
3. ${team.activeProjects > team.members ? '워크로드 균형 조정 및 우선순위 재설정' : '추가 프로젝트 수행 가능성 검토'}`
    }
    
    const viewTaskDetails = (task) => {
      aiResponse.value = `작업 상세 정보:
      
작업명: ${task.title}
담당자: ${task.assignee}
마감일: ${task.dueDate}
우선순위: ${task.priority === 'high' ? '높음' : task.priority === 'medium' ? '보통' : '낮음'}

프로젝트: ${task.project}
예상 소요시간: ${task.estimatedHours}시간

AI 분석:
${task.priority === 'high' ? '긴급한 작업으로 즉시 착수가 필요합니다' : task.priority === 'medium' ? '중요한 작업으로 계획적 접근이 필요합니다' : '여유가 있을 때 처리 가능한 작업입니다'}

추천 일정:
- 시작 권장일: ${task.priority === 'high' ? '즉시' : task.priority === 'medium' ? '2일 내' : '1주 내'}
- 예상 완료일: ${task.dueDate}
- 버퍼 시간: ${Math.ceil(task.estimatedHours * 0.2)}시간

협업 제안:
${task.estimatedHours > 20 ? '- 복잡한 작업으로 팀원과의 협업 권장' : '- 개별 작업 가능'}
- 정기 진행상황 공유 권장
- 막힐 경우 즉시 팀리더에게 에스컬레이션`
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
      activeProjects,
      projectGrowth,
      avgCompletionRate,
      completionTrend,
      delayedProjects,
      delayRate,
      aiAccuracy,
      accuracyTrend,
      
      // 데이터
      projects,
      teams,
      upcomingTasks,
      projectRisks,
      resourceAllocation,
      performanceMetrics,
      projectInsights,
      
      // 메서드
      executeAICommand,
      clearAICommand,
      refreshDashboard,
      viewProjectDetails,
      viewTeamDetails,
      viewTaskDetails
    }
  }
}
</script>

<style scoped>
.projects-module {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

.dashboard-card:hover {
  transform: translateY(-2px);
}

.project-item:hover,
.team-item:hover,
.task-item:hover,
.risk-item:hover,
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
  
  .project-management-section {
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