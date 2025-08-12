/**
 * AI 기능을 사용하기 위한 Vue Composable
 * ERPNext AI Copilot과 통신하는 모든 기능을 제공
 */
import { ref, reactive } from 'vue'
import axios from 'axios'

// AI 서비스 상태
const aiStatus = ref('disconnected')
const isProcessing = ref(false)
const lastError = ref(null)

// API 설정
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

// AI 클라이언트 설정
const aiClient = axios.create({
  baseURL: `${API_BASE_URL}/api`,
  timeout: 30000, // 30초 타임아웃
  headers: {
    'Content-Type': 'application/json',
  }
})

export function useAI() {
  /**
   * AI 서비스 상태 확인
   */
  const checkAIStatus = async () => {
    try {
      const response = await aiClient.get('/ai/status')
      aiStatus.value = 'connected'
      return response.data
    } catch (error) {
      aiStatus.value = 'disconnected'
      lastError.value = error.message
      throw error
    }
  }

  /**
   * AI 요청 처리
   * @param {string} message - 사용자 메시지
   * @param {object} context - 추가 컨텍스트
   * @returns {Promise<object>} AI 응답
   */
  const processAIRequest = async (message, context = {}) => {
    if (!message || !message.trim()) {
      throw new Error('메시지를 입력해주세요.')
    }

    isProcessing.value = true
    lastError.value = null

    try {
      const requestData = {
        message: message.trim(),
        context: {
          ...context,
          timestamp: new Date().toISOString(),
          userAgent: navigator.userAgent,
          currentPath: window.location.pathname
        }
      }

      const response = await aiClient.post('/ai/chat', requestData)
      
      if (response.data) {
        return response.data
      } else {
        throw new Error('AI로부터 응답을 받지 못했습니다.')
      }

    } catch (error) {
      lastError.value = error.message
      console.error('AI 요청 처리 오류:', error)
      
      // 에러 유형별 처리
      if (error.response) {
        // 서버 응답이 있는 경우
        const status = error.response.status
        const message = error.response.data?.detail || error.message

        switch (status) {
          case 400:
            throw new Error(`잘못된 요청: ${message}`)
          case 401:
            throw new Error('인증이 필요합니다.')
          case 403:
            throw new Error('접근 권한이 없습니다.')
          case 429:
            throw new Error('요청이 너무 많습니다. 잠시 후 다시 시도해주세요.')
          case 500:
            throw new Error('서버 오류가 발생했습니다.')
          default:
            throw new Error(`서버 오류 (${status}): ${message}`)
        }
      } else if (error.request) {
        // 네트워크 오류
        throw new Error('서버에 연결할 수 없습니다. 네트워크를 확인해주세요.')
      } else {
        throw error
      }

    } finally {
      isProcessing.value = false
    }
  }

  /**
   * 파일 분석 요청
   * @param {File|File[]} files - 분석할 파일(들)
   * @param {string} instruction - 분석 지시사항
   * @returns {Promise<object>} 분석 결과
   */
  const analyzeFiles = async (files, instruction = '이 파일들을 분석해주세요.') => {
    const fileArray = Array.isArray(files) ? files : [files]
    
    if (fileArray.length === 0) {
      throw new Error('분석할 파일을 선택해주세요.')
    }

    // 파일 크기 및 유형 확인
    const maxSize = 10 * 1024 * 1024 // 10MB
    const allowedTypes = [
      'text/plain', 'text/csv', 'application/json',
      'application/pdf', 'application/vnd.ms-excel',
      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    ]

    for (const file of fileArray) {
      if (file.size > maxSize) {
        throw new Error(`파일 "${file.name}"이 너무 큽니다. (최대 10MB)`)
      }
      
      if (!allowedTypes.includes(file.type)) {
        throw new Error(`파일 "${file.name}"의 형식이 지원되지 않습니다.`)
      }
    }

    // FormData 생성
    const formData = new FormData()
    fileArray.forEach((file, index) => {
      formData.append(`file_${index}`, file)
    })
    formData.append('instruction', instruction)

    try {
      const response = await aiClient.post('/ai/analyze-files', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        },
        timeout: 60000 // 파일 분석은 더 긴 타임아웃
      })

      return response.data

    } catch (error) {
      console.error('파일 분석 오류:', error)
      throw new Error('파일 분석 중 오류가 발생했습니다.')
    }
  }

  /**
   * 자동화 워크플로 실행
   * @param {string} workflowType - 워크플로 유형
   * @param {object} parameters - 워크플로 매개변수
   * @returns {Promise<object>} 실행 결과
   */
  const executeWorkflow = async (workflowType, parameters = {}) => {
    const message = `다음 워크플로를 실행해줘: ${workflowType}`
    
    return await processAIRequest(message, {
      workflow: {
        type: workflowType,
        parameters
      }
    })
  }

  /**
   * 예측 분석 요청
   * @param {string} analysisType - 분석 유형 (sales, inventory, customer 등)
   * @param {object} data - 분석할 데이터
   * @returns {Promise<object>} 예측 결과
   */
  const requestPrediction = async (analysisType, data = {}) => {
    const message = `${analysisType}에 대한 예측 분석을 해줘`
    
    return await processAIRequest(message, {
      prediction: {
        type: analysisType,
        data
      }
    })
  }

  /**
   * 문서 생성 요청
   * @param {string} documentType - 문서 유형
   * @param {object} data - 문서 데이터
   * @returns {Promise<object>} 생성된 문서
   */
  const generateDocument = async (documentType, data = {}) => {
    const message = `${documentType} 문서를 생성해줘`
    
    return await processAIRequest(message, {
      document: {
        type: documentType,
        data
      }
    })
  }

  /**
   * ERP 데이터 조회 요청
   * @param {string} doctype - DocType 이름
   * @param {object} filters - 필터 조건
   * @returns {Promise<object>} 조회 결과
   */
  const queryERPData = async (doctype, filters = {}) => {
    const message = `${doctype} 데이터를 조회해줘`
    
    return await processAIRequest(message, {
      query: {
        doctype,
        filters
      }
    })
  }

  /**
   * AI 추천 요청
   * @param {string} context - 추천 컨텍스트
   * @param {object} data - 추천을 위한 데이터
   * @returns {Promise<object>} 추천 결과
   */
  const getRecommendations = async (context, data = {}) => {
    const message = `${context}에 대한 추천을 해줘`
    
    return await processAIRequest(message, {
      recommendation: {
        context,
        data
      }
    })
  }

  /**
   * AI 응답을 HTML로 포맷팅
   * @param {string} content - AI 응답 내용
   * @returns {string} HTML 포맷된 내용
   */
  const formatAIResponse = (content) => {
    if (!content) return ''
    
    return content
      // 마크다운 스타일 포맷팅
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/\*(.*?)\*/g, '<em>$1</em>')
      .replace(/`(.*?)`/g, '<code class="bg-gray-100 px-1 py-0.5 rounded text-sm">$1</code>')
      .replace(/```(.*?)```/gs, '<pre class="bg-gray-900 text-white p-3 rounded-lg overflow-x-auto"><code>$1</code></pre>')
      
      // 링크 포맷팅
      .replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" class="text-primary-600 hover:text-primary-700 underline" target="_blank">$1</a>')
      
      // 줄바꿈 처리
      .replace(/\n\n/g, '</p><p class="mt-3">')
      .replace(/\n/g, '<br>')
      
      // 목록 처리
      .replace(/^- (.*$)/gm, '<li class="ml-4">• $1</li>')
      .replace(/(<li.*<\/li>)/gs, '<ul class="space-y-1">$1</ul>')
  }

  /**
   * 오류 메시지 생성
   * @param {Error} error - 오류 객체
   * @returns {string} 사용자 친화적인 오류 메시지
   */
  const getErrorMessage = (error) => {
    if (error.message) {
      return error.message
    }

    if (error.response && error.response.data && error.response.data.detail) {
      return error.response.data.detail
    }

    return '알 수 없는 오류가 발생했습니다.'
  }

  return {
    // 상태
    aiStatus: readonly(aiStatus),
    isProcessing: readonly(isProcessing),
    lastError: readonly(lastError),

    // 메서드
    checkAIStatus,
    processAIRequest,
    analyzeFiles,
    executeWorkflow,
    requestPrediction,
    generateDocument,
    queryERPData,
    getRecommendations,
    formatAIResponse,
    getErrorMessage
  }
}

// 전역 AI 상태 관리
export const globalAI = reactive({
  status: 'disconnected',
  isProcessing: false,
  lastActivity: null,
  capabilities: [
    'File Management',
    'Workflow Automation', 
    'Predictive Analysis',
    'Document Generation',
    'Data Querying',
    'Recommendations'
  ]
})

// AI 상태 모니터링
export function startAIMonitoring() {
  const { checkAIStatus } = useAI()
  
  // 초기 상태 확인
  checkAIStatus().then(() => {
    globalAI.status = 'connected'
  }).catch(() => {
    globalAI.status = 'disconnected'
  })

  // 주기적 상태 확인 (30초마다)
  setInterval(async () => {
    try {
      await checkAIStatus()
      globalAI.status = 'connected'
      globalAI.lastActivity = new Date().toISOString()
    } catch (error) {
      globalAI.status = 'disconnected'
      console.warn('AI 서비스 연결 실패:', error.message)
    }
  }, 30000)
}

export default useAI