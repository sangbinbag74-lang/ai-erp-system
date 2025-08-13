<template>
  <div class="ai-training min-h-screen" style="background: var(--bg-primary); color: var(--text-primary);">
    <div class="p-6">
      <h1 class="text-3xl font-bold bg-gradient-to-r from-yellow-400 to-red-400 bg-clip-text text-transparent mb-6">
        AI 학습 관리
      </h1>
      
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- 학습 상태 -->
        <div class="training-status p-6 rounded-xl" style="background: var(--bg-secondary); border: 1px solid var(--border-secondary);">
          <h3 class="text-xl font-semibold mb-4 text-yellow-400">학습 상태</h3>
          <div class="space-y-4">
            <div class="status-item p-4 rounded-lg" style="background: var(--bg-tertiary);">
              <div class="flex items-center justify-between mb-2">
                <span class="font-medium text-white">영업 예측 모델</span>
                <span class="text-green-400">활성</span>
              </div>
              <div class="w-full h-2 rounded-full" style="background: var(--bg-hover);">
                <div class="h-full rounded-full bg-green-400" style="width: 87%;"></div>
              </div>
              <div class="text-sm text-gray-400 mt-1">정확도: 87%</div>
            </div>
            
            <div class="status-item p-4 rounded-lg" style="background: var(--bg-tertiary);">
              <div class="flex items-center justify-between mb-2">
                <span class="font-medium text-white">고객 분석 모델</span>
                <span class="text-blue-400">학습 중</span>
              </div>
              <div class="w-full h-2 rounded-full" style="background: var(--bg-hover);">
                <div class="h-full rounded-full bg-blue-400" style="width: 65%;"></div>
              </div>
              <div class="text-sm text-gray-400 mt-1">진행률: 65%</div>
            </div>
          </div>
        </div>

        <!-- 데이터 세트 -->
        <div class="datasets-section p-6 rounded-xl" style="background: var(--bg-secondary); border: 1px solid var(--border-secondary);">
          <h3 class="text-xl font-semibold mb-4 text-red-400">데이터 세트</h3>
          <div class="text-center text-gray-400">
            <div class="text-4xl mb-4">🗃️</div>
            <p>AI 학습용 데이터를 관리합니다</p>
          </div>
        </div>

        <!-- 모델 성능 -->
        <div class="performance-section p-6 rounded-xl" style="background: var(--bg-secondary); border: 1px solid var(--border-secondary);">
          <h3 class="text-xl font-semibold mb-4 text-green-400">모델 성능</h3>
          <div class="grid grid-cols-2 gap-4">
            <div class="metric p-3 rounded-lg text-center" style="background: var(--bg-tertiary);">
              <div class="text-lg font-bold text-green-400">94.2%</div>
              <div class="text-sm text-gray-400">평균 정확도</div>
            </div>
            <div class="metric p-3 rounded-lg text-center" style="background: var(--bg-tertiary);">
              <div class="text-lg font-bold text-blue-400">0.03ms</div>
              <div class="text-sm text-gray-400">응답 시간</div>
            </div>
          </div>
        </div>

        <!-- 학습 설정 -->
        <div class="settings-section p-6 rounded-xl" style="background: var(--bg-secondary); border: 1px solid var(--border-secondary);">
          <h3 class="text-xl font-semibold mb-4 text-purple-400">학습 설정</h3>
          <div class="text-center text-gray-400">
            <div class="text-4xl mb-4">⚙️</div>
            <p>AI 모델 학습 매개변수를 조정합니다</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AITraining'
}
</script>