# AI ERP Vercel 배포 완벽 가이드

## 🚀 배포 단계별 실행

### 1단계: 사전 준비
```bash
# 1. Git에 모든 변경사항 커밋
git add .
git commit -m "Add Vercel deployment configuration"
git push origin main

# 2. Vercel CLI 설치 (전역)
npm install -g vercel
```

### 2단계: Frontend 배포 (Vercel)

#### 방법 A: GitHub 연동 (추천)
1. [vercel.com](https://vercel.com)에서 GitHub 로그인
2. "New Project" → GitHub 저장소 선택
3. 설정:
   - **Root Directory**: `ai_erp/frontend`
   - **Framework**: `Vite`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
4. Environment Variables 설정:
   ```
   VITE_API_URL=https://your-backend-url.com
   VITE_APP_ENV=production
   ```
5. "Deploy" 클릭

#### 방법 B: CLI 배포
```bash
cd ai_erp/frontend
vercel login
vercel --prod
```

### 3단계: Backend 배포 선택

#### 옵션 1: Railway (추천 - 가장 간단)
```bash
# 1. Railway 가입: railway.app
# 2. GitHub 연동
# 3. 프로젝트 선택 후 자동 배포
# 4. 환경변수 설정 (DATABASE_URL, REDIS_URL 등)
```

#### 옵션 2: DigitalOcean App Platform
```bash
# 1. DigitalOcean 가입
# 2. App Platform에서 GitHub 연결
# 3. .do/app.yaml 설정 사용
```

#### 옵션 3: 간단한 FastAPI (테스트용)
```bash
# Vercel Serverless Functions로 배포 가능
# backend/simple_api.py 사용
```

### 4단계: 도메인 연결 (선택사항)
```bash
# Vercel에서 커스텀 도메인 설정
# 예: ai-erp.your-domain.com
```

## 🔧 배포 후 확인사항

### Frontend 체크리스트
- [ ] 사이트가 정상적으로 로드되는가?
- [ ] API 연결이 작동하는가?
- [ ] 환경변수가 올바르게 설정되었는가?
- [ ] 빌드 오류가 없는가?

### Backend 체크리스트
- [ ] API 엔드포인트가 응답하는가?
- [ ] 데이터베이스 연결이 정상인가?
- [ ] 환경변수가 안전하게 설정되었는가?

## 💰 예상 비용

### 무료 티어 (시작용)
- **Vercel**: 무료 플랜 (100GB 대역폭/월)
- **Railway**: $5 크레딧/월
- **총 예상**: $0-5/월

### 저렴한 옵션
- **Vercel Pro**: $20/월
- **Railway**: $10-20/월
- **총 예상**: $30-40/월

## 🚨 주의사항

1. **API 키 보안**: 민감한 정보는 서버에서만 처리
2. **CORS 설정**: Frontend-Backend 간 통신 허용
3. **환경변수**: Production과 Development 분리
4. **백업**: 정기적인 데이터베이스 백업

## 📞 지원 및 문제 해결

### 일반적인 문제
1. **빌드 실패**: package.json 의존성 확인
2. **API 연결 실패**: 환경변수 및 CORS 확인
3. **404 오류**: vercel.json rewrites 설정 확인

### 도움 받기
- Vercel 문서: vercel.com/docs
- Railway 문서: docs.railway.app
- 커뮤니티: Discord, GitHub Issues