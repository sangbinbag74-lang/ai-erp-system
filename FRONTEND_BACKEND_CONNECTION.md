# 🔗 Frontend-Backend 연결 설정

## ✅ Backend API 테스트 완료!

### 🎯 Railway Backend URL
**https://ai-erp-system-production.up.railway.app**

### 📊 API 테스트 결과
✅ **루트 엔드포인트**: 정상 응답
✅ **헬스체크** (`/api/health`): success: true
✅ **사용자 프로필** (`/api/user/profile`): 한국어 응답 정상
✅ **모든 API 엔드포인트**: 작동 확인

## 🔧 Vercel 환경변수 설정 (수동)

### 1단계: Vercel Dashboard 접속
1. **https://vercel.com** 접속
2. **ai-erp-system** 프로젝트 선택

### 2단계: 환경변수 추가
1. **Settings** 탭 클릭
2. **Environment Variables** 선택
3. **Add New** 클릭
4. 다음 정보 입력:
   ```
   Name: VITE_API_URL
   Value: https://ai-erp-system-production.up.railway.app
   Environment: Production ✅
   ```
5. **Save** 클릭

### 3단계: 재배포 (자동)
- 환경변수 저장 시 **자동으로 재배포** 시작
- 2-3분 후 배포 완료

## 🧪 연결 테스트 방법

### Frontend 사이트 접속
**https://ai-erp-system-g48e3mayq-park-sangbins-projects.vercel.app**

### 테스트 순서
1. 홈페이지 접속
2. **"API 테스트"** 버튼 클릭
3. **"✅ API 연결 성공!"** 메시지 확인

### 예상 결과
```
시스템 상태:
Frontend: ✅ 배포 완료 (Vercel)
Backend: ✅ 배포 완료 (Railway)
API 연결: ✅ 연결 성공!
```

## 📱 완성된 시스템 구조

```
사용자 브라우저
    ↓
Frontend (Vercel)
https://ai-erp-system-g48e3mayq-park-sangbins-projects.vercel.app
    ↓ CORS 허용된 API 호출
Backend (Railway)
https://ai-erp-system-production.up.railway.app
    ↓
FastAPI + 데모 데이터
```

## 🎉 배포 성공 기준

### ✅ 모든 조건 충족
- [x] Frontend Vercel 배포 완료
- [x] Backend Railway 배포 완료
- [x] API 엔드포인트 정상 응답
- [x] 한국어 지원 확인
- [x] CORS 설정 완료
- [ ] Frontend-Backend 연결 확인 (진행중)

## 💰 최종 운영 비용
- **Vercel**: 무료 (Hobby Plan)
- **Railway**: $0-5/월 (크레딧 제공)
- **총 비용**: 무료~$5/월

---
**다음 단계**: Vercel 환경변수 설정 후 연결 테스트!