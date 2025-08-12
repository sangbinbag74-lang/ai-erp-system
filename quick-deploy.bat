@echo off
echo ================================================
echo        AI ERP 원클릭 Vercel 배포 스크립트
echo ================================================

echo.
echo 1단계: Git 커밋 및 푸시
git add .
git commit -m "Ready for Vercel deployment"
git push origin main

echo.
echo 2단계: Frontend 디렉토리로 이동
cd ai_erp\frontend

echo.
echo 3단계: 의존성 설치
call npm install

echo.
echo 4단계: 빌드 테스트
call npm run build
if errorlevel 1 (
    echo ❌ 빌드 실패! package.json을 확인하세요.
    pause
    exit /b 1
)

echo.
echo 5단계: Vercel CLI 설치
call npm install -g vercel

echo.
echo 6단계: Vercel 로그인 (브라우저가 열립니다)
call vercel login

echo.
echo 7단계: 프로덕션 배포
call vercel --prod

echo.
echo ================================================
echo              배포 완료! 🎉
echo ================================================
echo.
echo 다음 단계:
echo 1. 배포된 URL을 확인하세요
echo 2. 환경변수를 Vercel Dashboard에서 설정하세요
echo 3. Backend를 Railway/DigitalOcean에 배포하세요
echo.
pause