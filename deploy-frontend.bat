@echo off
echo =================================
echo   AI ERP Frontend Vercel 배포
echo =================================

cd ai_erp\frontend

echo 1. 의존성 설치 중...
call npm install

echo 2. 빌드 진행 중...
call npm run build

echo 3. Vercel CLI 설치 (전역)
call npm install -g vercel

echo 4. Vercel 로그인
call vercel login

echo 5. 프로젝트 배포
call vercel --prod

echo 배포 완료!
pause