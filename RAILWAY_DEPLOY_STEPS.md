# 🚂 Railway 배포 단계별 가이드

## 🎯 현재 상황
✅ 모든 코드가 GitHub에 준비됨: https://github.com/sangbinbag74-lang/ai-erp-system

## 📋 Railway 배포 단계 (10분 소요)

### 1단계: Railway 가입 (2분)
1. **https://railway.app** 접속
2. **"Sign up"** 클릭
3. **"Continue with GitHub"** 선택
4. GitHub 계정으로 로그인
5. 이메일 인증 (필요시)

### 2단계: 프로젝트 생성 (3분)
1. Railway Dashboard에서 **"New Project"** 클릭
2. **"Deploy from GitHub repo"** 선택
3. 저장소 검색: **"ai-erp-system"** 입력
4. **sangbinbag74-lang/ai-erp-system** 선택
5. **"Deploy Now"** 클릭

### 3단계: 배포 설정 (2분)
1. 배포가 시작되면 **Settings** 탭 이동
2. **"Source Repo"** 섹션에서:
   - **Root Directory**: `ai_erp/backend` 입력
   - **"Update"** 클릭
3. 자동으로 재배포 시작

### 4단계: 환경변수 설정 (2분)
1. **"Variables"** 탭 이동
2. 다음 변수들 추가:
   ```
   PORT = 8000
   ENVIRONMENT = production
   FRONTEND_URL = https://ai-erp-system-g48e3mayq-park-sangbins-projects.vercel.app
   ```
3. **"Add"** 클릭하여 각 변수 저장

### 5단계: 배포 확인 (1분)
1. **"Deployments"** 탭에서 빌드 로그 확인
2. 🟢 **"Success"** 상태 확인
3. **생성된 URL 복사** (예: `https://your-app.railway.app`)

## 🔗 Frontend 연결 설정

### Railway 배포 완료 후 실행:
1. Railway에서 생성된 URL 복사
2. **https://vercel.com** 접속
3. ai-erp-system 프로젝트 선택
4. **Settings** → **Environment Variables**
5. 새 변수 추가:
   ```
   Name: VITE_API_URL
   Value: https://your-railway-app.railway.app
   Environment: Production
   ```
6. **Save** 클릭
7. **Redeploy** (자동 실행됨)

## ✅ 배포 완료 확인

### Backend 테스트:
- `https://your-railway-app.railway.app/api/health` 접속
- JSON 응답 확인: `{"success": true, ...}`

### Frontend 테스트:
- `https://ai-erp-system-g48e3mayq-park-sangbins-projects.vercel.app` 접속
- **"API 테스트"** 버튼 클릭
- **"✅ API 연결 성공!"** 메시지 확인

## 🚨 문제 해결

### 빌드 실패 시:
1. Railway → Deployments → 로그 확인
2. requirements-simple.txt 경로 확인
3. Root Directory 설정 재확인

### API 연결 실패 시:
1. Railway URL 정확성 확인
2. CORS 설정 확인
3. 환경변수 대소문자 확인

## 🎉 성공 기준
- ✅ Railway 배포 성공 (🟢 상태)
- ✅ Backend API 응답 정상
- ✅ Frontend에서 API 테스트 성공
- ✅ 한국어 응답 정상 표시

---
**예상 소요시간: 10분**
**비용: 무료 (Railway $5 크레딧 제공)**