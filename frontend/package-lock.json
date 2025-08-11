import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';

export default defineConfig({
  plugins: [vue()],
  base: '/',  // Vercel 배포 시 루트 경로로 설정. 왜? Vercel이 앱을 호스팅할 때 기본 경로가 '/'이기 때문입니다.
  server: {
    proxy: {  // 개발 시 백엔드 API 호출을 프록시. 프로덕션에서는 Vercel이 자동 처리.
      '/api': {
        target: 'http://localhost:8000',  // 로컬 테스트용. 배포 후 제거 가능.
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')
      }
    }
  },
  build: {
    outDir: 'dist',  // 빌드 출력 폴더. Vercel이 이 폴더를 자동으로 서빙합니다.
    assetsDir: 'assets'  // 정적 파일(이미지 등) 저장 폴더.
  }
});