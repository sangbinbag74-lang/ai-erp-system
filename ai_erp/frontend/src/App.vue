<template>
  <div id="app">
    <header class="header">
      <div class="header-content">
        <router-link to="/" class="logo">
          <h1>🤖 AI ERP System</h1>
        </router-link>
        <nav class="nav">
          <router-link to="/dashboard" class="nav-link">📊 대시보드</router-link>
          <router-link to="/sales" class="nav-link">💼 매출관리</router-link>
          <router-link to="/inventory" class="nav-link">📦 재고관리</router-link>
          <router-link to="/hr" class="nav-link">👥 인사관리</router-link>
          <router-link to="/analytics" class="nav-link">🤖 AI분석</router-link>
        </nav>
      </div>
    </header>
    
    <main class="main">
      <router-view />
    </main>
    
    <footer class="footer">
      <p>&copy; 2024 AI ERP System. Powered by Vue.js & Railway & Vercel</p>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
#app {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 1rem 0;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.header-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  text-decoration: none;
  color: white;
}

.logo h1 {
  margin: 0;
  font-size: 1.8rem;
}

.nav {
  display: flex;
  gap: 2rem;
}

.nav-link {
  color: white;
  text-decoration: none;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  transition: background-color 0.2s;
  font-weight: 500;
}

.nav-link:hover {
  background: rgba(255, 255, 255, 0.2);
}

.nav-link.router-link-active {
  background: rgba(255, 255, 255, 0.3);
}

.main {
  flex: 1;
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
}

.footer {
  background: #f8f9fa;
  padding: 1rem;
  text-align: center;
  color: #666;
  border-top: 1px solid #dee2e6;
}
</style>