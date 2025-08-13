<template>
  <div class="ai-workflow-designer min-h-screen" style="background: var(--bg-primary); color: var(--text-primary);">
    <div class="p-6">
      <h1 class="text-3xl font-bold bg-gradient-to-r from-green-400 to-blue-400 bg-clip-text text-transparent mb-6">
        AI 워크플로 설계
      </h1>
      
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- 워크플로 템플릿 -->
        <div class="templates-section p-6 rounded-xl" style="background: var(--bg-secondary); border: 1px solid var(--border-secondary);">
          <h3 class="text-xl font-semibold mb-4 text-green-400">워크플로 템플릿</h3>
          <div class="space-y-3">
            <div class="template-item p-3 rounded-lg cursor-pointer" style="background: var(--bg-tertiary); border: 1px solid var(--border-primary);">
              <h4 class="font-medium text-white">영업 자동화</h4>
              <p class="text-sm text-gray-400">리드 생성부터 계약까지</p>
            </div>
            <div class="template-item p-3 rounded-lg cursor-pointer" style="background: var(--bg-tertiary); border: 1px solid var(--border-primary);">
              <h4 class="font-medium text-white">구매 승인</h4>
              <p class="text-sm text-gray-400">구매 요청 자동 처리</p>
            </div>
          </div>
        </div>

        <!-- 워크플로 캔버스 -->
        <div class="canvas-section p-6 rounded-xl" style="background: var(--bg-secondary); border: 1px solid var(--border-secondary);">
          <h3 class="text-xl font-semibold mb-4 text-blue-400">워크플로 캔버스</h3>
          <div class="canvas border-2 border-dashed border-gray-600 rounded-lg h-96 flex items-center justify-center">
            <div class="text-center text-gray-400">
              <div class="text-4xl mb-4">🔧</div>
              <p>워크플로를 설계하세요</p>
            </div>
          </div>
        </div>

        <!-- 설정 패널 -->
        <div class="settings-section p-6 rounded-xl" style="background: var(--bg-secondary); border: 1px solid var(--border-secondary);">
          <h3 class="text-xl font-semibold mb-4 text-purple-400">설정</h3>
          <div class="text-center text-gray-400">
            <div class="text-4xl mb-4">⚙️</div>
            <p>워크플로 설정을 구성하세요</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AIWorkflowDesigner'
}
</script>