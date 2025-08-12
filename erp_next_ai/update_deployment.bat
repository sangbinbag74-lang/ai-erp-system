@echo off
echo ========================================
echo 🔄 ERPNext AI System 배포 업데이트
echo ========================================
echo.

echo 📋 기존 배포 정보:
echo Railway 백엔드: ai-erp-system-production.up.railway.app
echo Vercel 프론트엔드: ai-erp-system (park-sangbins-projects)
echo.

echo 🚀 업데이트 진행 중...

echo.
echo 1️⃣ Git 커밋 및 푸시 확인...
git status
echo.

echo 2️⃣ Railway 대시보드 열기...
start https://railway.app/dashboard

echo.
echo 3️⃣ Vercel 대시보드 열기...
start https://vercel.com/dashboard

echo.
echo ========================================
echo 📝 수동 업데이트 단계:
echo.
echo Railway (백엔드):
echo 1. railway.app/dashboard 접속
echo 2. ai-erp-system-production 프로젝트 선택
echo 3. Settings ^> Source 에서 재배포 트리거
echo 4. Environment 탭에서 환경변수 확인:
echo    - OPENAI_API_KEY
echo    - ANTHROPIC_API_KEY
echo    - DATABASE_URL
echo.
echo Vercel (프론트엔드):
echo 1. vercel.com/dashboard 접속  
echo 2. ai-erp-system 프로젝트 선택
echo 3. Deployments 탭에서 Redeploy 클릭
echo 4. Environment Variables 확인:
echo    - VITE_API_URL=https://ai-erp-system-production.up.railway.app
echo    - VITE_ENABLE_AI_COPILOT=true
echo ========================================

pause

echo.
echo 🧪 배포 후 테스트...
echo 백엔드 헬스체크 중...
curl -s https://ai-erp-system-production.up.railway.app/api/health
echo.

echo 🎉 업데이트 완료!
echo.
echo 💡 확인할 URL들:
echo - 백엔드 API: https://ai-erp-system-production.up.railway.app/docs
echo - 프론트엔드: https://ai-erp-system-f1c4bb20b-park-sangbins-projects.vercel.app
echo.

pause