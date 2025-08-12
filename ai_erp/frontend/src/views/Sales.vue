<template>
  <div class="sales">
    <div class="page-header">
      <h1>💼 매출 관리</h1>
      <button @click="showAddForm = true" class="btn-primary">
        ➕ 새 거래 추가
      </button>
    </div>

    <!-- 매출 통계 -->
    <div class="stats-grid">
      <div class="stat-card">
        <h3>이번 달 매출</h3>
        <div class="stat-value">₩{{ formatNumber(thisMonthSales) }}</div>
        <div class="stat-change positive">+{{ monthlyGrowth }}%</div>
      </div>
      
      <div class="stat-card">
        <h3>평균 거래액</h3>
        <div class="stat-value">₩{{ formatNumber(avgDeal) }}</div>
        <div class="stat-change positive">+5.2%</div>
      </div>
      
      <div class="stat-card">
        <h3>성사율</h3>
        <div class="stat-value">{{ conversionRate }}%</div>
        <div class="stat-change positive">+2.1%</div>
      </div>
    </div>

    <!-- AI 매출 분석 -->
    <div class="ai-analysis">
      <h2>🤖 AI 매출 분석</h2>
      <div class="analysis-cards">
        <div class="analysis-card">
          <h4>📈 트렌드 분석</h4>
          <p>전자제품 카테고리에서 30% 매출 증가가 관찰됩니다.</p>
          <p class="recommendation">추천: 전자제품 마케팅 예산 20% 증액</p>
        </div>
        
        <div class="analysis-card">
          <h4>🎯 고객 분석</h4>
          <p>기업 고객이 개인 고객보다 2.5배 높은 구매력을 보입니다.</p>
          <p class="recommendation">추천: B2B 영업팀 확대 검토</p>
        </div>
        
        <div class="analysis-card">
          <h4>🔮 예측</h4>
          <p>현재 추세로 다음 분기 매출 목표 달성 확률: 85%</p>
          <p class="recommendation">추천: 신규 고객 개발에 집중</p>
        </div>
      </div>
    </div>

    <!-- 매출 데이터 테이블 -->
    <div class="sales-table">
      <h2>📊 최근 거래 내역</h2>
      <div class="table-controls">
        <input v-model="searchTerm" placeholder="고객명 또는 상품명 검색..." class="search-input">
        <select v-model="statusFilter" class="filter-select">
          <option value="">전체 상태</option>
          <option value="완료">완료</option>
          <option value="진행중">진행중</option>
          <option value="보류">보류</option>
        </select>
      </div>
      
      <div class="table-container">
        <table>
          <thead>
            <tr>
              <th>날짜</th>
              <th>고객명</th>
              <th>상품/서비스</th>
              <th>금액</th>
              <th>상태</th>
              <th>담당자</th>
              <th>액션</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="sale in filteredSales" :key="sale.id">
              <td>{{ sale.date }}</td>
              <td>{{ sale.customer }}</td>
              <td>{{ sale.product }}</td>
              <td>₩{{ formatNumber(sale.amount) }}</td>
              <td>
                <span :class="['status', sale.status]">{{ sale.status }}</span>
              </td>
              <td>{{ sale.manager }}</td>
              <td>
                <button @click="editSale(sale)" class="btn-edit">수정</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- 새 거래 추가 모달 -->
    <div v-if="showAddForm" class="modal-overlay" @click="showAddForm = false">
      <div class="modal-content" @click.stop>
        <h3>새 거래 추가</h3>
        <form @submit.prevent="addSale">
          <div class="form-group">
            <label>고객명</label>
            <input v-model="newSale.customer" required>
          </div>
          
          <div class="form-group">
            <label>상품/서비스</label>
            <input v-model="newSale.product" required>
          </div>
          
          <div class="form-group">
            <label>금액</label>
            <input v-model.number="newSale.amount" type="number" required>
          </div>
          
          <div class="form-group">
            <label>상태</label>
            <select v-model="newSale.status" required>
              <option value="진행중">진행중</option>
              <option value="완료">완료</option>
              <option value="보류">보류</option>
            </select>
          </div>
          
          <div class="form-actions">
            <button type="button" @click="showAddForm = false" class="btn-cancel">취소</button>
            <button type="submit" class="btn-primary">추가</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'

export default {
  name: 'Sales',
  setup() {
    const showAddForm = ref(false)
    const searchTerm = ref('')
    const statusFilter = ref('')
    
    // 통계 데이터
    const thisMonthSales = ref(125000000)
    const monthlyGrowth = ref(12.5)
    const avgDeal = ref(3650000)
    const conversionRate = ref(68.5)
    
    // 새 거래 폼
    const newSale = ref({
      customer: '',
      product: '',
      amount: 0,
      status: '진행중'
    })
    
    // 매출 데이터
    const sales = ref([
      {
        id: 1,
        date: '2024-08-12',
        customer: '삼성전자',
        product: '노트북 50대',
        amount: 75000000,
        status: '완료',
        manager: '김영수'
      },
      {
        id: 2,
        date: '2024-08-11',
        customer: 'LG화학',
        product: '사무용품 패키지',
        amount: 12500000,
        status: '진행중',
        manager: '박미영'
      },
      {
        id: 3,
        date: '2024-08-10',
        customer: '현대자동차',
        product: 'IT 컨설팅',
        amount: 35000000,
        status: '완료',
        manager: '이철수'
      },
      {
        id: 4,
        date: '2024-08-09',
        customer: 'SK하이닉스',
        product: '서버 장비',
        amount: 120000000,
        status: '보류',
        manager: '정지영'
      },
      {
        id: 5,
        date: '2024-08-08',
        customer: '네이버',
        product: '소프트웨어 라이센스',
        amount: 28000000,
        status: '완료',
        manager: '최동훈'
      }
    ])
    
    const filteredSales = computed(() => {
      return sales.value.filter(sale => {
        const matchesSearch = sale.customer.toLowerCase().includes(searchTerm.value.toLowerCase()) ||
                            sale.product.toLowerCase().includes(searchTerm.value.toLowerCase())
        const matchesStatus = !statusFilter.value || sale.status === statusFilter.value
        return matchesSearch && matchesStatus
      })
    })
    
    const formatNumber = (num) => {
      return num.toLocaleString('ko-KR')
    }
    
    const addSale = () => {
      const newId = Math.max(...sales.value.map(s => s.id)) + 1
      sales.value.unshift({
        id: newId,
        date: new Date().toISOString().split('T')[0],
        customer: newSale.value.customer,
        product: newSale.value.product,
        amount: newSale.value.amount,
        status: newSale.value.status,
        manager: '현재 사용자'
      })
      
      // 폼 리셋
      newSale.value = {
        customer: '',
        product: '',
        amount: 0,
        status: '진행중'
      }
      showAddForm.value = false
      
      // 통계 업데이트
      if (newSale.value.status === '완료') {
        thisMonthSales.value += newSale.value.amount
      }
    }
    
    const editSale = (sale) => {
      alert(`${sale.customer} 거래 수정 기능 (추후 구현)`)
    }
    
    return {
      showAddForm,
      searchTerm,
      statusFilter,
      thisMonthSales,
      monthlyGrowth,
      avgDeal,
      conversionRate,
      newSale,
      sales,
      filteredSales,
      formatNumber,
      addSale,
      editSale
    }
  }
}
</script>

<style scoped>
.sales {
  max-width: 1400px;
  margin: 0 auto;
  padding: 2rem;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.page-header h1 {
  color: #2c3e50;
  margin: 0;
}

.btn-primary {
  background: #3498db;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 6px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.2s;
}

.btn-primary:hover {
  background: #2980b9;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 3rem;
}

.stat-card {
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.stat-card h3 {
  margin: 0 0 1rem 0;
  color: #7f8c8d;
  font-size: 0.9rem;
}

.stat-value {
  font-size: 2rem;
  font-weight: bold;
  color: #2c3e50;
  margin-bottom: 0.5rem;
}

.stat-change {
  font-size: 0.9rem;
  font-weight: 600;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
}

.stat-change.positive {
  background: #d5f4e6;
  color: #27ae60;
}

.ai-analysis {
  margin-bottom: 3rem;
}

.ai-analysis h2 {
  color: #2c3e50;
  margin-bottom: 1.5rem;
}

.analysis-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
}

.analysis-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 1.5rem;
  border-radius: 12px;
}

.analysis-card h4 {
  margin: 0 0 1rem 0;
}

.analysis-card p {
  margin: 0.5rem 0;
  line-height: 1.6;
}

.recommendation {
  background: rgba(255, 255, 255, 0.2);
  padding: 0.5rem;
  border-radius: 6px;
  font-weight: 600;
}

.sales-table h2 {
  color: #2c3e50;
  margin-bottom: 1.5rem;
}

.table-controls {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
}

.search-input, .filter-select {
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 1rem;
}

.search-input {
  flex: 1;
}

.table-container {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th {
  background: #f8f9fa;
  padding: 1rem;
  text-align: left;
  font-weight: 600;
  color: #2c3e50;
}

td {
  padding: 1rem;
  border-bottom: 1px solid #ecf0f1;
}

tr:last-child td {
  border-bottom: none;
}

.status {
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.85rem;
  font-weight: 600;
}

.status.완료 {
  background: #d5f4e6;
  color: #27ae60;
}

.status.진행중 {
  background: #fff3cd;
  color: #f39c12;
}

.status.보류 {
  background: #f8d7da;
  color: #e74c3c;
}

.btn-edit {
  background: #f39c12;
  color: white;
  border: none;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.8rem;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  width: 90%;
  max-width: 500px;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: #2c3e50;
  font-weight: 600;
}

.form-group input, .form-group select {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 1rem;
}

.form-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
}

.btn-cancel {
  background: #95a5a6;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 6px;
  cursor: pointer;
}
</style>