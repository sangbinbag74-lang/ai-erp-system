<template>
  <div class="hr">
    <div class="page-header">
      <h1>👥 인사 관리</h1>
      <button class="btn-primary">➕ 직원 추가</button>
    </div>

    <div class="stats-grid">
      <div class="stat-card">
        <h3>총 직원 수</h3>
        <div class="stat-value">{{ totalEmployees }}</div>
      </div>
      <div class="stat-card">
        <h3>이번 달 신입</h3>
        <div class="stat-value">{{ newHires }}</div>
      </div>
      <div class="stat-card">
        <h3>평균 근속</h3>
        <div class="stat-value">{{ avgTenure }}년</div>
      </div>
    </div>

    <div class="employee-table">
      <h2>직원 현황</h2>
      <table>
        <thead>
          <tr>
            <th>이름</th>
            <th>부서</th>
            <th>직급</th>
            <th>입사일</th>
            <th>급여</th>
            <th>상태</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="employee in employees" :key="employee.id">
            <td>{{ employee.name }}</td>
            <td>{{ employee.department }}</td>
            <td>{{ employee.position }}</td>
            <td>{{ employee.hireDate }}</td>
            <td>₩{{ formatNumber(employee.salary) }}</td>
            <td>
              <span :class="['status', employee.status]">{{ employee.status }}</span>
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
  name: 'HR',
  setup() {
    const totalEmployees = ref(156)
    const newHires = ref(8)
    const avgTenure = ref(3.2)
    
    const employees = ref([
      { id: 1, name: '김영수', department: '개발팀', position: '팀장', hireDate: '2020-03-15', salary: 7000000, status: '재직' },
      { id: 2, name: '박미영', department: '마케팅팀', position: '과장', hireDate: '2021-07-01', salary: 5500000, status: '재직' },
      { id: 3, name: '이철수', department: '영업팀', position: '대리', hireDate: '2022-01-10', salary: 4500000, status: '재직' },
      { id: 4, name: '정지영', department: '인사팀', position: '주임', hireDate: '2023-05-20', salary: 3800000, status: '휴직' }
    ])
    
    const formatNumber = (num) => num.toLocaleString('ko-KR')
    
    return {
      totalEmployees,
      newHires,
      avgTenure,
      employees,
      formatNumber
    }
  }
}
</script>

<style scoped>
.hr {
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

.employee-table {
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

.status.재직 {
  background: #d5f4e6;
  color: #27ae60;
}

.status.휴직 {
  background: #fff3cd;
  color: #f39c12;
}
</style>