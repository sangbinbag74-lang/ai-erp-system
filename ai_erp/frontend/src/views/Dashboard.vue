<template>
  <div class="dashboard">
    <div class="dashboard-header">
      <h1>📊 AI ERP 대시보드</h1>
      <p>실시간 비즈니스 인사이트와 AI 분석</p>
    </div>

    <!-- KPI 카드들 -->
    <div class="kpi-grid">
      <div class="kpi-card revenue">
        <div class="kpi-icon">💰</div>
        <div class="kpi-content">
          <h3>월 매출</h3>
          <div class="kpi-value">₩{{ formatNumber(monthlyRevenue) }}</div>
          <div class="kpi-change positive">+{{ revenueChange }}%</div>
        </div>
      </div>

      <div class="kpi-card orders">
        <div class="kpi-icon">📦</div>
        <div class="kpi-content">
          <h3>이번 달 주문</h3>
          <div class="kpi-value">{{ totalOrders }}건</div>
          <div class="kpi-change positive">+{{ orderChange }}%</div>
        </div>
      </div>

      <div class="kpi-card inventory">
        <div class="kpi-icon">🏪</div>
        <div class="kpi-content">
          <h3>재고 현황</h3>
          <div class="kpi-value">{{ inventoryItems }}개</div>
          <div class="kpi-change warning">주의 필요</div>
        </div>
      </div>

      <div class="kpi-card customers">
        <div class="kpi-icon">👥</div>
        <div class="kpi-content">
          <h3>활성 고객</h3>
          <div class="kpi-value">{{ activeCustomers }}명</div>
          <div class="kpi-change positive">+{{ customerChange }}%</div>
        </div>
      </div>
    </div>

    <!-- AI 인사이트 섹션 -->
    <div class="ai-insights">
      <h2>🤖 AI 비즈니스 인사이트</h2>
      <div class="insights-grid">
        <div class="insight-card">
          <h4>💡 매출 예측</h4>
          <p>다음 달 예상 매출: <strong>₩{{ formatNumber(predictedRevenue) }}</strong></p>
          <p>현재 추세를 바탕으로 15% 성장이 예상됩니다.</p>
        </div>
        
        <div class="insight-card">
          <h4>📈 재고 최적화</h4>
          <p>3개 상품의 재고 부족이 예상됩니다.</p>
          <p>추천: 전자제품 카테고리 50% 추가 주문</p>
        </div>

        <div class="insight-card">
          <h4>🎯 고객 세그먼트</h4>
          <p>VIP 고객군이 전체 매출의 60%를 차지합니다.</p>
          <p>추천: VIP 대상 맞춤형 마케팅 캠페인</p>
        </div>
      </div>
    </div>

    <!-- 최근 활동 -->
    <div class="recent-activities">
      <h2>📋 최근 활동</h2>
      <div class="activity-list">
        <div v-for="activity in recentActivities" :key="activity.id" class="activity-item">
          <div class="activity-icon">{{ activity.icon }}</div>
          <div class="activity-content">
            <h4>{{ activity.title }}</h4>
            <p>{{ activity.description }}</p>
            <span class="activity-time">{{ activity.time }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 빠른 액션 -->
    <div class="quick-actions">
      <h2>⚡ 빠른 액션</h2>
      <div class="action-buttons">
        <router-link to="/sales" class="action-btn sales">
          <span class="btn-icon">💼</span>
          <span>매출 관리</span>
        </router-link>
        
        <router-link to="/inventory" class="action-btn inventory">
          <span class="btn-icon">📦</span>
          <span>재고 관리</span>
        </router-link>
        
        <router-link to="/hr" class="action-btn hr">
          <span class="btn-icon">👥</span>
          <span>인사 관리</span>
        </router-link>
        
        <router-link to="/analytics" class="action-btn analytics">
          <span class="btn-icon">📊</span>
          <span>AI 분석</span>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'

export default {
  name: 'Dashboard',
  setup() {
    // KPI 데이터
    const monthlyRevenue = ref(125000000)
    const revenueChange = ref(12.5)
    const totalOrders = ref(342)
    const orderChange = ref(8.3)
    const inventoryItems = ref(1247)
    const activeCustomers = ref(89)
    const customerChange = ref(5.7)
    const predictedRevenue = ref(143750000)

    // 최근 활동 데이터
    const recentActivities = ref([
      {
        id: 1,
        icon: '💰',
        title: '대량 주문 완료',
        description: '삼성전자에서 ₩15,000,000 주문 완료',
        time: '2시간 전'
      },
      {
        id: 2,
        icon: '📦',
        title: '재고 알림',
        description: '노트북 재고가 10개 미만으로 감소',
        time: '4시간 전'
      },
      {
        id: 3,
        icon: '👤',
        title: '신규 고객 등록',
        description: 'LG화학이 새로운 파트너로 등록됨',
        time: '6시간 전'
      },
      {
        id: 4,
        icon: '📊',
        title: 'AI 분석 완료',
        description: '월간 매출 분석 보고서가 생성됨',
        time: '1일 전'
      }
    ])

    const formatNumber = (num) => {
      return num.toLocaleString('ko-KR')
    }

    onMounted(() => {
      // 실시간 데이터 시뮬레이션
      setInterval(() => {
        monthlyRevenue.value += Math.floor(Math.random() * 100000)
        totalOrders.value += Math.floor(Math.random() * 3)
      }, 10000)
    })

    return {
      monthlyRevenue,
      revenueChange,
      totalOrders,
      orderChange,
      inventoryItems,
      activeCustomers,
      customerChange,
      predictedRevenue,
      recentActivities,
      formatNumber
    }
  }
}
</script>

<style scoped>
.dashboard {
  max-width: 1400px;
  margin: 0 auto;
  padding: 2rem;
}

.dashboard-header {
  text-align: center;
  margin-bottom: 3rem;
}

.dashboard-header h1 {
  font-size: 2.5rem;
  color: #2c3e50;
  margin-bottom: 0.5rem;
}

.kpi-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
  margin-bottom: 3rem;
}

.kpi-card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  border-left: 4px solid;
  display: flex;
  align-items: center;
  gap: 1rem;
}

.kpi-card.revenue { border-left-color: #3498db; }
.kpi-card.orders { border-left-color: #2ecc71; }
.kpi-card.inventory { border-left-color: #f39c12; }
.kpi-card.customers { border-left-color: #e74c3c; }

.kpi-icon {
  font-size: 2.5rem;
}

.kpi-content h3 {
  margin: 0;
  color: #7f8c8d;
  font-size: 0.9rem;
  font-weight: 500;
}

.kpi-value {
  font-size: 1.8rem;
  font-weight: bold;
  color: #2c3e50;
  margin: 0.5rem 0;
}

.kpi-change {
  font-size: 0.85rem;
  font-weight: 600;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
}

.kpi-change.positive {
  background: #d5f4e6;
  color: #27ae60;
}

.kpi-change.warning {
  background: #fef9e7;
  color: #f39c12;
}

.ai-insights {
  margin-bottom: 3rem;
}

.ai-insights h2 {
  color: #2c3e50;
  margin-bottom: 1.5rem;
}

.insights-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
}

.insight-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.insight-card h4 {
  margin: 0 0 1rem 0;
  font-size: 1.1rem;
}

.insight-card p {
  margin: 0.5rem 0;
  line-height: 1.6;
}

.recent-activities {
  margin-bottom: 3rem;
}

.recent-activities h2 {
  color: #2c3e50;
  margin-bottom: 1.5rem;
}

.activity-list {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.activity-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem 1.5rem;
  border-bottom: 1px solid #ecf0f1;
}

.activity-item:last-child {
  border-bottom: none;
}

.activity-icon {
  font-size: 1.5rem;
}

.activity-content h4 {
  margin: 0;
  color: #2c3e50;
  font-size: 1rem;
}

.activity-content p {
  margin: 0.25rem 0;
  color: #7f8c8d;
  font-size: 0.9rem;
}

.activity-time {
  font-size: 0.8rem;
  color: #bdc3c7;
}

.quick-actions h2 {
  color: #2c3e50;
  margin-bottom: 1.5rem;
}

.action-buttons {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.action-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  padding: 2rem 1rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  text-decoration: none;
  color: #2c3e50;
  transition: transform 0.2s, box-shadow 0.2s;
}

.action-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
}

.btn-icon {
  font-size: 2rem;
}

@media (max-width: 768px) {
  .dashboard {
    padding: 1rem;
  }
  
  .kpi-grid {
    grid-template-columns: 1fr;
  }
  
  .insights-grid {
    grid-template-columns: 1fr;
  }
  
  .action-buttons {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>