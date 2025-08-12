/**
 * 알림 시스템을 위한 Vue Composable
 * 토스트, 모달, 인앱 알림 등을 통합 관리
 */
import { ref, reactive } from 'vue'

// 전역 알림 상태
const notifications = ref([])
const toasts = ref([])
let notificationId = 0
let toastId = 0

export function useNotification() {
  /**
   * 토스트 알림 표시
   * @param {string} message - 알림 메시지
   * @param {string} type - 알림 타입 (success, error, warning, info)
   * @param {object} options - 추가 옵션
   */
  const showToast = (message, type = 'info', options = {}) => {
    const toast = {
      id: ++toastId,
      message,
      type,
      timestamp: new Date(),
      duration: options.duration || getDefaultDuration(type),
      persistent: options.persistent || false,
      action: options.action || null,
      icon: options.icon || getDefaultIcon(type),
      position: options.position || 'top-right'
    }

    toasts.value.push(toast)

    // 자동 제거 (persistent가 아닌 경우)
    if (!toast.persistent && toast.duration > 0) {
      setTimeout(() => {
        removeToast(toast.id)
      }, toast.duration)
    }

    return toast.id
  }

  /**
   * 성공 토스트
   */
  const showSuccess = (message, options = {}) => {
    return showToast(message, 'success', options)
  }

  /**
   * 오류 토스트
   */
  const showError = (message, options = {}) => {
    return showToast(message, 'error', {
      duration: 5000,
      ...options
    })
  }

  /**
   * 경고 토스트
   */
  const showWarning = (message, options = {}) => {
    return showToast(message, 'warning', options)
  }

  /**
   * 정보 토스트
   */
  const showInfo = (message, options = {}) => {
    return showToast(message, 'info', options)
  }

  /**
   * 로딩 토스트
   */
  const showLoading = (message = '처리 중...', options = {}) => {
    return showToast(message, 'loading', {
      persistent: true,
      icon: 'loading',
      ...options
    })
  }

  /**
   * 토스트 제거
   */
  const removeToast = (id) => {
    const index = toasts.value.findIndex(toast => toast.id === id)
    if (index > -1) {
      toasts.value.splice(index, 1)
    }
  }

  /**
   * 모든 토스트 제거
   */
  const clearToasts = () => {
    toasts.value.length = 0
  }

  /**
   * 인앱 알림 추가
   */
  const addNotification = (notification) => {
    const newNotification = {
      id: ++notificationId,
      title: notification.title,
      message: notification.message,
      type: notification.type || 'info',
      icon: notification.icon || getDefaultIcon(notification.type || 'info'),
      timestamp: new Date(),
      read: false,
      persistent: notification.persistent || false,
      data: notification.data || null,
      action: notification.action || null
    }

    notifications.value.unshift(newNotification)

    // 최대 100개까지만 보관
    if (notifications.value.length > 100) {
      notifications.value = notifications.value.slice(0, 100)
    }

    return newNotification.id
  }

  /**
   * 알림을 읽음으로 표시
   */
  const markAsRead = (id) => {
    const notification = notifications.value.find(n => n.id === id)
    if (notification) {
      notification.read = true
    }
  }

  /**
   * 모든 알림을 읽음으로 표시
   */
  const markAllAsRead = () => {
    notifications.value.forEach(notification => {
      notification.read = true
    })
  }

  /**
   * 알림 제거
   */
  const removeNotification = (id) => {
    const index = notifications.value.findIndex(n => n.id === id)
    if (index > -1) {
      notifications.value.splice(index, 1)
    }
  }

  /**
   * 읽은 알림 모두 제거
   */
  const clearReadNotifications = () => {
    notifications.value = notifications.value.filter(n => !n.read || n.persistent)
  }

  /**
   * 모든 알림 제거
   */
  const clearAllNotifications = () => {
    notifications.value = notifications.value.filter(n => n.persistent)
  }

  /**
   * 확인 대화상자
   */
  const confirm = (message, title = '확인', options = {}) => {
    return new Promise((resolve) => {
      const modal = {
        type: 'confirm',
        title,
        message,
        confirmText: options.confirmText || '확인',
        cancelText: options.cancelText || '취소',
        confirmVariant: options.confirmVariant || 'primary',
        onConfirm: () => resolve(true),
        onCancel: () => resolve(false)
      }

      // 실제 구현에서는 모달 컴포넌트를 표시
      showModal(modal)
    })
  }

  /**
   * 경고 대화상자
   */
  const alert = (message, title = '알림', options = {}) => {
    return new Promise((resolve) => {
      const modal = {
        type: 'alert',
        title,
        message,
        confirmText: options.confirmText || '확인',
        onConfirm: () => resolve(true)
      }

      showModal(modal)
    })
  }

  /**
   * 프롬프트 대화상자
   */
  const prompt = (message, title = '입력', options = {}) => {
    return new Promise((resolve) => {
      const modal = {
        type: 'prompt',
        title,
        message,
        defaultValue: options.defaultValue || '',
        placeholder: options.placeholder || '',
        confirmText: options.confirmText || '확인',
        cancelText: options.cancelText || '취소',
        onConfirm: (value) => resolve(value),
        onCancel: () => resolve(null)
      }

      showModal(modal)
    })
  }

  /**
   * 모달 표시 (실제 구현에서는 전역 모달 시스템과 연결)
   */
  const showModal = (modal) => {
    // 여기서는 간단히 브라우저 기본 대화상자 사용
    // 실제 구현에서는 커스텀 모달 컴포넌트 사용
    if (modal.type === 'confirm') {
      const result = window.confirm(`${modal.title}\n\n${modal.message}`)
      if (result) {
        modal.onConfirm()
      } else {
        modal.onCancel()
      }
    } else if (modal.type === 'alert') {
      window.alert(`${modal.title}\n\n${modal.message}`)
      modal.onConfirm()
    } else if (modal.type === 'prompt') {
      const result = window.prompt(`${modal.title}\n\n${modal.message}`, modal.defaultValue)
      if (result !== null) {
        modal.onConfirm(result)
      } else {
        modal.onCancel()
      }
    }
  }

  /**
   * API 오류 처리
   */
  const handleApiError = (error, customMessage = null) => {
    console.error('API Error:', error)

    let message = customMessage || '오류가 발생했습니다.'

    if (error.response) {
      const status = error.response.status
      const data = error.response.data

      switch (status) {
        case 400:
          message = data?.message || '잘못된 요청입니다.'
          break
        case 401:
          message = '인증이 필요합니다. 다시 로그인해주세요.'
          break
        case 403:
          message = '접근 권한이 없습니다.'
          break
        case 404:
          message = '요청한 리소스를 찾을 수 없습니다.'
          break
        case 422:
          message = data?.message || '입력 데이터를 확인해주세요.'
          if (data?.errors) {
            const errors = Object.values(data.errors).flat()
            message += '\n' + errors.join('\n')
          }
          break
        case 429:
          message = '요청이 너무 많습니다. 잠시 후 다시 시도해주세요.'
          break
        case 500:
          message = '서버 오류가 발생했습니다. 관리자에게 문의해주세요.'
          break
        default:
          message = `오류가 발생했습니다. (${status})`
      }
    } else if (error.request) {
      message = '서버에 연결할 수 없습니다. 네트워크를 확인해주세요.'
    }

    showError(message, { duration: 5000 })
  }

  /**
   * 기본 지속 시간 반환
   */
  const getDefaultDuration = (type) => {
    const durations = {
      success: 3000,
      info: 4000,
      warning: 4000,
      error: 5000,
      loading: 0 // persistent
    }
    return durations[type] || 4000
  }

  /**
   * 기본 아이콘 반환
   */
  const getDefaultIcon = (type) => {
    const icons = {
      success: 'heroicons:check-circle',
      error: 'heroicons:x-circle',
      warning: 'heroicons:exclamation-triangle',
      info: 'heroicons:information-circle',
      loading: 'heroicons:arrow-path'
    }
    return icons[type] || 'heroicons:information-circle'
  }

  /**
   * 읽지 않은 알림 개수
   */
  const unreadCount = computed(() => 
    notifications.value.filter(n => !n.read).length
  )

  /**
   * 최근 알림들 (최대 5개)
   */
  const recentNotifications = computed(() => 
    notifications.value.slice(0, 5)
  )

  return {
    // 상태
    notifications: readonly(notifications),
    toasts: readonly(toasts),
    unreadCount,
    recentNotifications,

    // 토스트 메서드
    showToast,
    showSuccess,
    showError,
    showWarning,
    showInfo,
    showLoading,
    removeToast,
    clearToasts,

    // 알림 메서드
    addNotification,
    markAsRead,
    markAllAsRead,
    removeNotification,
    clearReadNotifications,
    clearAllNotifications,

    // 대화상자 메서드
    confirm,
    alert,
    prompt,

    // 유틸리티 메서드
    handleApiError,

    // 편의 메서드
    showNotification: showToast, // 별칭
  }
}

// 전역 알림 시스템
export const globalNotification = reactive({
  notifications: notifications,
  toasts: toasts,
  
  // 전역 메서드들
  show: (message, type = 'info', options = {}) => {
    const { showToast } = useNotification()
    return showToast(message, type, options)
  },
  
  success: (message, options = {}) => {
    const { showSuccess } = useNotification()
    return showSuccess(message, options)
  },
  
  error: (message, options = {}) => {
    const { showError } = useNotification()
    return showError(message, options)
  },
  
  warning: (message, options = {}) => {
    const { showWarning } = useNotification()
    return showWarning(message, options)
  },
  
  info: (message, options = {}) => {
    const { showInfo } = useNotification()
    return showInfo(message, options)
  }
})

export default useNotification