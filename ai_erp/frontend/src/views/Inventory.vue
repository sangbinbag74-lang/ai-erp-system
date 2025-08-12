<template>
  <div class="inventory">
    <div class="page-header">
      <h1>📦 재고 관리</h1>
      <button class="btn-primary">➕ 상품 추가</button>
    </div>

    <div class="stats-grid">
      <div class="stat-card">
        <h3>총 상품</h3>
        <div class="stat-value">{{ totalItems }}</div>
      </div>
      <div class="stat-card">
        <h3>부족 재고</h3>
        <div class="stat-value warning">{{ lowStockItems }}</div>
      </div>
      <div class="stat-card">
        <h3>재고 가치</h3>
        <div class="stat-value">₩{{ formatNumber(totalValue) }}</div>
      </div>
    </div>

    <div class="inventory-table">
      <h2>재고 현황</h2>
      <table>
        <thead>
          <tr>
            <th>상품명</th>
            <th>카테고리</th>
            <th>현재 재고</th>
            <th>최소 재고</th>
            <th>단가</th>
            <th>상태</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in inventoryItems" :key="item.id">
            <td>{{ item.name }}</td>
            <td>{{ item.category }}</td>
            <td>{{ item.stock }}</td>
            <td>{{ item.minStock }}</td>
            <td>₩{{ formatNumber(item.price) }}</td>
            <td>
              <span :class="['status', getStockStatus(item)]">
                {{ getStockStatusText(item) }}
              </span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'

export default {
  name: 'Inventory',
  setup() {
    const totalItems = ref(1247)
    const lowStockItems = ref(23)
    const totalValue = ref(450000000)
    
    const inventoryItems = ref([
      { id: 1, name: '노트북 Dell XPS 13', category: '전자제품', stock: 15, minStock: 10, price: 1500000 },
      { id: 2, name: '사무용 의자', category: '사무용품', stock: 5, minStock: 20, price: 250000 },
      { id: 3, name: 'A4 용지', category: '사무용품', stock: 150, minStock: 50, price: 5000 },
      { id: 4, name: '마우스', category: '전자제품', stock: 8, minStock: 15, price: 35000 }
    ])
    
    const formatNumber = (num) => num.toLocaleString('ko-KR')
    
    const getStockStatus = (item) => {
      if (item.stock <= item.minStock) return 'low'
      if (item.stock <= item.minStock * 1.5) return 'warning'
      return 'good'
    }
    
    const getStockStatusText = (item) => {
      const status = getStockStatus(item)
      return { low: '부족', warning: '주의', good: '양호' }[status]
    }
    
    return {
      totalItems,
      lowStockItems,
      totalValue,
      inventoryItems,
      formatNumber,
      getStockStatus,
      getStockStatusText
    }
  }
}
</script>

<style scoped>
.inventory {
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

.btn-primary {
  background: #3498db;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 6px;
  cursor: pointer;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.stat-value {
  font-size: 2rem;
  font-weight: bold;
  color: #2c3e50;
}

.stat-value.warning {
  color: #e74c3c;
}

.inventory-table {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  overflow: hidden;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  padding: 1rem;
  text-align: left;
  border-bottom: 1px solid #eee;
}

th {
  background: #f8f9fa;
  font-weight: 600;
}

.status {
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: 600;
}

.status.good {
  background: #d5f4e6;
  color: #27ae60;
}

.status.warning {
  background: #fff3cd;
  color: #f39c12;
}

.status.low {
  background: #f8d7da;
  color: #e74c3c;
}
</style>