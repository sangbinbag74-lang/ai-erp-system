@echo off
echo ========================================
echo 🚀 ERPNext AI System 배포 스크립트
echo ========================================
echo.

echo 📋 배포 단계:
echo 1. Railway 백엔드 배포 (수동 설정 필요)
echo 2. Vercel 프론트엔드 배포 (수동 설정 필요)
echo.

echo ⚠️  주의사항:
echo - Railway와 Vercel 계정이 필요합니다
echo - 브라우저에서 직접 설정해야 합니다
echo.

echo 🔗 필요한 링크들:
echo Railway: https://railway.app
echo Vercel: https://vercel.com
echo GitHub 저장소: https://github.com/sangbinbag74-lang/ai-erp-system
echo.

pause

echo.
echo 📖 상세 배포 가이드를 열고 있습니다...
start notepad "DEPLOYMENT_GUIDE.md"

echo.
echo 🌐 GitHub 저장소를 열고 있습니다...
start https://github.com/sangbinbag74-lang/ai-erp-system

echo.
echo 🚂 Railway 대시보드를 열고 있습니다...
start https://railway.app/dashboard

echo.
echo ▲ Vercel 대시보드를 열고 있습니다...
start https://vercel.com/dashboard

echo.
echo ========================================
echo ✅ 배포 준비 완료!
echo.
echo 다음 단계:
echo 1. Railway에서 GitHub 저장소 연결
echo 2. 백엔드 폴더 배포 설정
echo 3. PostgreSQL 추가
echo 4. 환경변수 설정
echo 5. Vercel에서 GitHub 저장소 연결
echo 6. 프론트엔드 폴더 배포 설정
echo 7. 환경변수 설정
echo ========================================
pause