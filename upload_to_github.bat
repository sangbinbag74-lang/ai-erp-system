@echo off
echo GitHub 업로드 스크립트
echo ===================

echo 1. GitHub에서 새 저장소를 생성하세요:
echo    Repository name: ai-erp-system
echo    Description: AI-powered ERP system with Korean localization

echo.
echo 2. 저장소 URL을 입력하세요 (예: https://github.com/username/ai-erp-system.git):
set /p REPO_URL="Repository URL: "

echo.
echo 3. 원격 저장소 연결 중...
git remote add origin %REPO_URL%

echo.
echo 4. GitHub에 업로드 중...
git push -u origin main

echo.
echo 업로드 완료!
echo 저장소 주소: %REPO_URL%
pause