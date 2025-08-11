// 다국어 지원 설정
import { createI18n } from 'vue-i18n'
import ko from './ko.js'

// 기본 영어 언어팩 (기존 시스템과 호환성 유지)
const en = {
  // 기존 영어 텍스트들...
  common: {
    save: 'Save',
    cancel: 'Cancel',
    delete: 'Delete',
    edit: 'Edit',
    add: 'Add',
    search: 'Search',
    filter: 'Filter',
    sort: 'Sort',
    refresh: 'Refresh',
    loading: 'Loading...',
    success: 'Success',
    error: 'Error',
    warning: 'Warning',
    info: 'Info'
  },
  nav: {
    dashboard: 'Dashboard',
    fileManager: 'File Manager',
    teamManagement: 'Team Management',
    cloudStorage: 'Cloud Storage',
    llmSettings: 'LLM Settings',
    analytics: 'Analytics',
    reports: 'Reports',
    settings: 'Settings'
  }
  // ... 더 많은 영어 번역들
}

const messages = {
  ko,
  en
}

// 브라우저 언어 감지 또는 로컬 스토리지에서 언어 설정 가져오기
function getDefaultLocale() {
  const saved = localStorage.getItem('ai-erp-locale')
  if (saved) return saved
  
  const browserLang = navigator.language || navigator.languages[0]
  if (browserLang.startsWith('ko')) return 'ko'
  
  return 'en'
}

const i18n = createI18n({
  legacy: false, // Vue 3 Composition API 사용
  locale: getDefaultLocale(),
  fallbackLocale: 'en',
  messages
})

// 언어 변경 함수
export function setLocale(locale) {
  i18n.global.locale.value = locale
  localStorage.setItem('ai-erp-locale', locale)
  document.documentElement.lang = locale
}

// 현재 언어 가져오기
export function getLocale() {
  return i18n.global.locale.value
}

// 지원하는 언어 목록
export const supportedLocales = [
  { code: 'ko', name: '한국어', flag: '🇰🇷' },
  { code: 'en', name: 'English', flag: '🇺🇸' }
]

export default i18n