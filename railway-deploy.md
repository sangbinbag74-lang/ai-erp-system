# 🚂 Railway Backend 배포 가이드

## 1단계: Railway 가입 및 설정

### Railway 가입
1. [railway.app](https://railway.app) 접속
2. "Sign up" → GitHub 계정으로 가입
3. 이메일 인증 완료

## 2단계: 프로젝트 생성

### GitHub 연동 배포
```bash
1. Railway Dashboard → "New Project"
2. "Deploy from GitHub repo" 선택
3. 저장소: sangbinbag74-lang/ai-erp-system 선택
4. Root Directory: ai_erp/backend 설정
```

### 또는 CLI 배포
```bash
# Railway CLI 설치
npm install -g @railway/cli

# 로그인
railway login

# 프로젝트 생성
cd ai_erp/backend
railway init
railway up
```

## 3단계: 환경변수 설정

Railway Dashboard → Variables 탭에서 설정:

```bash
# 기본 설정
PORT=8000
ENVIRONMENT=production

# 데이터베이스 (Railway에서 자동 생성)
DATABASE_URL=${{Postgres.DATABASE_URL}}
REDIS_URL=${{Redis.REDIS_URL}}

# API 키 (옵션)
OPENAI_API_KEY=your-openai-key
ANTHROPIC_API_KEY=your-anthropic-key

# CORS 설정
FRONTEND_URL=https://ai-erp-system-g48e3mayq-park-sangbins-projects.vercel.app
```

## 4단계: 서비스 추가

### PostgreSQL 추가
1. Dashboard → "Add Service"
2. "PostgreSQL" 선택
3. 자동으로 DATABASE_URL 환경변수 생성

### Redis 추가 (선택사항)
1. Dashboard → "Add Service"  
2. "Redis" 선택
3. 자동으로 REDIS_URL 환경변수 생성

## 5단계: 배포 파일 구성

프로젝트에 필요한 파일들:
```
ai_erp/backend/
├── main.py              # FastAPI 앱
├── requirements-simple.txt  # 의존성
├── railway.json         # Railway 설정 (선택사항)
└── Procfile            # 실행 명령어 (선택사항)
```

### Procfile 생성 (선택사항)
```bash
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

## 6단계: 배포 확인

### 배포 상태 확인
```bash
# Railway CLI로 확인
railway status
railway logs

# 또는 Dashboard에서 확인
# Deployments 탭 → 배포 로그 확인
```

### API 테스트
```bash
# 헬스 체크
curl https://your-railway-app.railway.app/api/health

# 시스템 정보
curl https://your-railway-app.railway.app/api/system/info
```

## 7단계: Frontend 연결

### Vercel 환경변수 업데이트
```bash
# Vercel Dashboard → Environment Variables
VITE_API_URL=https://your-railway-app.railway.app
```

### 또는 CLI로 설정
```bash
cd ../frontend
vercel env add VITE_API_URL production
# Railway URL 입력: https://your-railway-app.railway.app
```

## 💰 Railway 요금제

### Hobby Plan (무료)
- $5 크레딧/월 제공
- PostgreSQL: $0.000463/GB-hour
- 예상 비용: $0-5/월

### Pro Plan ($20/월)
- 더 많은 리소스
- 우선 지원
- 고급 모니터링

## 🔧 문제 해결

### 일반적인 오류
1. **빌드 실패**: requirements.txt 확인
2. **포트 오류**: PORT 환경변수 설정
3. **CORS 오류**: 도메인 확인

### 로그 확인
```bash
railway logs --follow
```

## ✅ 배포 완료 체크리스트

- [ ] Railway 가입 및 GitHub 연동
- [ ] 프로젝트 생성 및 배포
- [ ] PostgreSQL 서비스 추가
- [ ] 환경변수 설정
- [ ] API 엔드포인트 테스트
- [ ] Frontend 연결 확인

---
*Railway 배포 후 생성된 URL을 Frontend 환경변수에 설정하세요!*