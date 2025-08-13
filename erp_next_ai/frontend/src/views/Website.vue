<template>
  <div class="website min-h-screen bg-white">
    <!-- 헤더 -->
    <div class="bg-white border-b border-gray-200 p-6">
      <h1 class="text-3xl font-bold text-gray-900 mb-2">웹사이트 관리</h1>
      <p class="text-gray-600">웹사이트 콘텐츠, SEO 및 온라인 마케팅 관리</p>
    </div>

    <!-- 메인 콘텐츠 -->
    <div class="p-6">
      <!-- 통계 카드 -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div class="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm font-medium text-gray-500">월 방문자</p>
              <p class="text-2xl font-bold text-gray-900">42,350</p>
            </div>
            <div class="p-3 bg-blue-50 rounded-full">
              <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
              </svg>
            </div>
          </div>
          <div class="mt-4 flex items-center text-sm">
            <span class="text-green-500 font-medium">+15.3%</span>
            <span class="text-gray-500 ml-2">전월 대비</span>
          </div>
        </div>

        <div class="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm font-medium text-gray-500">전환율</p>
              <p class="text-2xl font-bold text-gray-900">3.8%</p>
            </div>
            <div class="p-3 bg-green-50 rounded-full">
              <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
          </div>
          <div class="mt-4 flex items-center text-sm">
            <span class="text-green-500 font-medium">+0.7%</span>
            <span class="text-gray-500 ml-2">개선됨</span>
          </div>
        </div>

        <div class="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm font-medium text-gray-500">페이지 뷰</p>
              <p class="text-2xl font-bold text-gray-900">128,450</p>
            </div>
            <div class="p-3 bg-purple-50 rounded-full">
              <svg class="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 002 2h2a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v14a2 2 0 002 2z" />
              </svg>
            </div>
          </div>
          <div class="mt-4 flex items-center text-sm">
            <span class="text-purple-500 font-medium">+22.1%</span>
            <span class="text-gray-500 ml-2">증가</span>
          </div>
        </div>

        <div class="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm font-medium text-gray-500">이탈률</p>
              <p class="text-2xl font-bold text-gray-900">28.5%</p>
            </div>
            <div class="p-3 bg-orange-50 rounded-full">
              <svg class="w-6 h-6 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 17h8m0 0V9m0 8l-8-8-4 4-6-6" />
              </svg>
            </div>
          </div>
          <div class="mt-4 flex items-center text-sm">
            <span class="text-green-500 font-medium">-3.2%</span>
            <span class="text-gray-500 ml-2">개선됨</span>
          </div>
        </div>
      </div>

      <!-- 메인 콘텐츠 그리드 -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <!-- 페이지 관리 -->
        <div class="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <div class="flex items-center justify-between mb-6">
            <h3 class="text-lg font-semibold text-gray-900">페이지 관리</h3>
            <div class="flex space-x-2">
              <button class="px-3 py-1.5 text-sm bg-blue-600 text-white rounded-md hover:bg-blue-700" @click="editPages = !editPages">
                {{ editPages ? '저장' : '수정' }}
              </button>
              <button class="px-3 py-1.5 text-sm bg-gray-100 text-gray-700 rounded-md hover:bg-gray-200">
                새 페이지
              </button>
            </div>
          </div>
          
          <div class="space-y-4">
            <div v-for="page in webPages" :key="page.id" class="p-4 bg-gray-50 rounded-lg">
              <div class="flex items-center justify-between mb-2">
                <h4 class="font-medium text-gray-900" :contenteditable="editPages">{{ page.title }}</h4>
                <span class="px-2 py-1 text-xs font-medium rounded-full" :class="page.statusClass">
                  {{ page.status }}
                </span>
              </div>
              <div class="text-sm text-gray-600 mb-2" :contenteditable="editPages">{{ page.url }}</div>
              <div class="grid grid-cols-2 gap-4 text-sm">
                <div>
                  <span class="text-gray-500">방문수:</span>
                  <span class="ml-1 text-gray-900" :contenteditable="editPages">{{ page.visits }}</span>
                </div>
                <div>
                  <span class="text-gray-500">최근 수정:</span>
                  <span class="ml-1 text-gray-900" :contenteditable="editPages">{{ page.lastModified }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- SEO 최적화 -->
        <div class="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <div class="flex items-center justify-between mb-6">
            <h3 class="text-lg font-semibold text-gray-900">SEO 최적화</h3>
            <button class="px-3 py-1.5 text-sm bg-blue-600 text-white rounded-md hover:bg-blue-700" @click="editSEO = !editSEO">
              {{ editSEO ? '저장' : '수정' }}
            </button>
          </div>
          
          <div class="space-y-4">
            <div v-for="seo in seoMetrics" :key="seo.id" class="p-4 bg-gray-50 rounded-lg">
              <div class="flex items-center justify-between mb-3">
                <h4 class="font-medium text-gray-900" :contenteditable="editSEO">{{ seo.keyword }}</h4>
                <span class="text-sm font-medium text-blue-600">{{ seo.rank }}위</span>
              </div>
              <div class="space-y-2 text-sm">
                <div class="flex justify-between">
                  <span class="text-gray-500">검색량:</span>
                  <span class="text-gray-900" :contenteditable="editSEO">{{ seo.searchVolume }}</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-gray-500">클릭률:</span>
                  <span class="text-gray-900" :contenteditable="editSEO">{{ seo.ctr }}</span>
                </div>
                <div class="w-full bg-gray-200 rounded-full h-2">
                  <div class="bg-blue-500 h-2 rounded-full" :style="{ width: seo.score + '%' }"></div>
                </div>
                <div class="text-xs text-gray-500">SEO 점수: {{ seo.score }}/100</div>
              </div>
            </div>
          </div>
        </div>

        <!-- 콘텐츠 관리 -->
        <div class="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <div class="flex items-center justify-between mb-6">
            <h3 class="text-lg font-semibold text-gray-900">콘텐츠 관리</h3>
            <div class="flex space-x-2">
              <button class="px-3 py-1.5 text-sm bg-blue-600 text-white rounded-md hover:bg-blue-700" @click="editContent = !editContent">
                {{ editContent ? '저장' : '수정' }}
              </button>
              <button class="px-3 py-1.5 text-sm bg-gray-100 text-gray-700 rounded-md hover:bg-gray-200">
                새 콘텐츠
              </button>
            </div>
          </div>
          
          <div class="space-y-3">
            <div v-for="content in contentList" :key="content.id" class="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
              <div class="flex-1">
                <div class="font-medium text-gray-900" :contenteditable="editContent">{{ content.title }}</div>
                <div class="text-sm text-gray-600" :contenteditable="editContent">{{ content.category }}</div>
                <div class="text-sm text-gray-500" :contenteditable="editContent">{{ content.author }} • {{ content.date }}</div>
              </div>
              <div class="text-right">
                <span class="px-2 py-1 text-xs font-medium rounded-full" :class="content.statusClass">
                  {{ content.status }}
                </span>
                <div class="text-sm text-gray-500 mt-1">{{ content.views }} 조회</div>
              </div>
            </div>
          </div>
        </div>

        <!-- 소셜 미디어 -->
        <div class="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <div class="flex items-center justify-between mb-6">
            <h3 class="text-lg font-semibold text-gray-900">소셜 미디어</h3>
            <button class="px-3 py-1.5 text-sm bg-blue-600 text-white rounded-md hover:bg-blue-700" @click="editSocial = !editSocial">
              {{ editSocial ? '저장' : '수정' }}
            </button>
          </div>
          
          <div class="space-y-4">
            <div v-for="social in socialMedia" :key="social.id" class="p-4 bg-gray-50 rounded-lg">
              <div class="flex items-center gap-3 mb-3">
                <div class="w-8 h-8 rounded-full flex items-center justify-center" :style="`background-color: ${social.color}20`">
                  <div class="w-4 h-4 rounded-full" :style="`background-color: ${social.color}`"></div>
                </div>
                <h4 class="font-medium text-gray-900" :contenteditable="editSocial">{{ social.platform }}</h4>
              </div>
              <div class="grid grid-cols-2 gap-4 text-sm">
                <div>
                  <span class="text-gray-500">팔로워:</span>
                  <span class="ml-1 text-gray-900 font-medium" :contenteditable="editSocial">{{ social.followers }}</span>
                </div>
                <div>
                  <span class="text-gray-500">참여율:</span>
                  <span class="ml-1 text-gray-900 font-medium" :contenteditable="editSocial">{{ social.engagement }}</span>
                </div>
                <div>
                  <span class="text-gray-500">게시물:</span>
                  <span class="ml-1 text-gray-900 font-medium" :contenteditable="editSocial">{{ social.posts }}</span>
                </div>
                <div>
                  <span class="text-gray-500">도달수:</span>
                  <span class="ml-1 text-gray-900 font-medium" :contenteditable="editSocial">{{ social.reach }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 온라인 마케팅 캠페인 -->
      <div class="mt-8 bg-white p-6 rounded-lg shadow-sm border border-gray-200">
        <div class="flex items-center justify-between mb-6">
          <h3 class="text-lg font-semibold text-gray-900">마케팅 캠페인</h3>
          <div class="flex space-x-2">
            <button class="px-3 py-1.5 text-sm bg-blue-600 text-white rounded-md hover:bg-blue-700" @click="editCampaigns = !editCampaigns">
              {{ editCampaigns ? '저장' : '수정' }}
            </button>
            <button class="px-3 py-1.5 text-sm bg-gray-100 text-gray-700 rounded-md hover:bg-gray-200">
              새 캠페인
            </button>
          </div>
        </div>
        
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div v-for="campaign in marketingCampaigns" :key="campaign.id" class="p-4 bg-gray-50 rounded-lg">
            <div class="flex items-center justify-between mb-3">
              <h4 class="font-medium text-gray-900" :contenteditable="editCampaigns">{{ campaign.name }}</h4>
              <span class="px-2 py-1 text-xs font-medium rounded-full" :class="campaign.statusClass">
                {{ campaign.status }}
              </span>
            </div>
            <div class="space-y-2 text-sm">
              <div class="flex justify-between">
                <span class="text-gray-500">예산:</span>
                <span class="text-gray-900" :contenteditable="editCampaigns">{{ campaign.budget }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-500">지출:</span>
                <span class="text-gray-900" :contenteditable="editCampaigns">{{ campaign.spent }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-500">클릭:</span>
                <span class="text-gray-900" :contenteditable="editCampaigns">{{ campaign.clicks }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-500">전환:</span>
                <span class="text-gray-900" :contenteditable="editCampaigns">{{ campaign.conversions }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-500">ROI:</span>
                <span class="text-gray-900 font-medium" :contenteditable="editCampaigns">{{ campaign.roi }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- AI 콘텐츠 제안 -->
      <div class="mt-8 bg-gradient-to-r from-pink-50 to-purple-50 p-6 rounded-lg border border-pink-200">
        <div class="flex items-start space-x-3">
          <div class="p-2 bg-pink-100 rounded-lg">
            <svg class="w-6 h-6 text-pink-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z" />
            </svg>
          </div>
          <div class="flex-1">
            <h4 class="font-semibold text-gray-900 mb-2">AI 마케팅 제안</h4>
            <div class="space-y-2 text-sm text-gray-700" :contenteditable="editContent">
              <p>• "ERP 시스템 도입 가이드" 블로그 시리즈로 SEO 효과를 높일 수 있습니다</p>
              <p>• 모바일 페이지 속도가 느립니다. Core Web Vitals 개선이 필요합니다</p>
              <p>• 소셜 미디어 게시 최적 시간: 화요일 오후 2-4시, 목요일 오전 10-12시</p>
              <p>• 고객 후기 페이지 추가로 전환율을 15% 향상시킬 수 있습니다</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const editPages = ref(false)
const editSEO = ref(false)
const editContent = ref(false)
const editSocial = ref(false)
const editCampaigns = ref(false)

const webPages = ref([
  {
    id: 1,
    title: '홈페이지',
    url: '/home',
    visits: '15,247',
    lastModified: '2024-01-15',
    status: '발행됨',
    statusClass: 'bg-green-100 text-green-800'
  },
  {
    id: 2,
    title: '제품 소개',
    url: '/products',
    visits: '8,593',
    lastModified: '2024-01-12',
    status: '발행됨',
    statusClass: 'bg-green-100 text-green-800'
  },
  {
    id: 3,
    title: '회사 소개',
    url: '/about',
    visits: '5,214',
    lastModified: '2024-01-10',
    status: '수정 중',
    statusClass: 'bg-yellow-100 text-yellow-800'
  },
  {
    id: 4,
    title: '문의하기',
    url: '/contact',
    visits: '3,827',
    lastModified: '2024-01-08',
    status: '발행됨',
    statusClass: 'bg-green-100 text-green-800'
  }
])

const seoMetrics = ref([
  {
    id: 1,
    keyword: 'ERP 시스템',
    rank: 3,
    searchVolume: '12,000',
    ctr: '8.5%',
    score: 85
  },
  {
    id: 2,
    keyword: '기업 관리 솔루션',
    rank: 7,
    searchVolume: '8,500',
    ctr: '5.2%',
    score: 72
  },
  {
    id: 3,
    keyword: '통합 관리 시스템',
    rank: 12,
    searchVolume: '6,200',
    ctr: '3.1%',
    score: 68
  }
])

const contentList = ref([
  {
    id: 1,
    title: 'ERP 시스템 도입 가이드',
    category: '블로그',
    author: '김마케팅',
    date: '2024-01-15',
    status: '발행됨',
    statusClass: 'bg-green-100 text-green-800',
    views: '2,453'
  },
  {
    id: 2,
    title: '성공 사례: ABC 제조업체',
    category: '사례 연구',
    author: '박콘텐츠',
    date: '2024-01-12',
    status: '검토 중',
    statusClass: 'bg-yellow-100 text-yellow-800',
    views: '1,827'
  },
  {
    id: 3,
    title: '2024 ERP 트렌드 보고서',
    category: '보고서',
    author: '이분석',
    date: '2024-01-10',
    status: '작성 중',
    statusClass: 'bg-blue-100 text-blue-800',
    views: '945'
  }
])

const socialMedia = ref([
  {
    id: 1,
    platform: 'Facebook',
    followers: '15,234',
    engagement: '4.2%',
    posts: '156',
    reach: '48,592',
    color: '#1877F2'
  },
  {
    id: 2,
    platform: 'LinkedIn',
    followers: '8,567',
    engagement: '6.8%',
    posts: '89',
    reach: '22,348',
    color: '#0A66C2'
  },
  {
    id: 3,
    platform: 'Instagram',
    followers: '12,891',
    engagement: '3.9%',
    posts: '203',
    reach: '35,746',
    color: '#E4405F'
  }
])

const marketingCampaigns = ref([
  {
    id: 1,
    name: 'ERP 솔루션 광고',
    budget: '₩5,000,000',
    spent: '₩3,250,000',
    clicks: '12,547',
    conversions: '234',
    roi: '320%',
    status: '진행중',
    statusClass: 'bg-blue-100 text-blue-800'
  },
  {
    id: 2,
    name: '제조업 타겟팅',
    budget: '₩3,000,000',
    spent: '₩2,100,000',
    clicks: '8,392',
    conversions: '156',
    roi: '285%',
    status: '진행중',
    statusClass: 'bg-blue-100 text-blue-800'
  },
  {
    id: 3,
    name: '리마케팅 캠페인',
    budget: '₩2,000,000',
    spent: '₩1,950,000',
    clicks: '5,234',
    conversions: '89',
    roi: '195%',
    status: '완료',
    statusClass: 'bg-green-100 text-green-800'
  }
])
</script>