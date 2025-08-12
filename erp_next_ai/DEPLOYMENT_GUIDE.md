# 배포 가이드 🚀

ERPNext AI System의 완전한 배포 가이드입니다.

## 📋 배포 전 체크리스트

### 1. 환경 준비
- [ ] Node.js 18+ 설치
- [ ] Python 3.11+ 설치
- [ ] PostgreSQL 14+ 설치 (로컬 테스트용)
- [ ] Git 설정
- [ ] Railway CLI 설치
- [ ] Vercel CLI 설치

### 2. API 키 준비
- [ ] OpenAI API 키 발급
- [ ] Anthropic Claude API 키 발급
- [ ] 키 보안 저장

### 3. 저장소 설정
- [ ] GitHub 저장소 생성
- [ ] 로컬 저장소와 연결
- [ ] .gitignore 확인

## 🗄️ 데이터베이스 배포

### 1. Railway PostgreSQL 설정
```bash
# Railway에 로그인
railway login

# 새 프로젝트 생성
railway new

# PostgreSQL 추가
railway add postgresql

# 환경변수 확인
railway variables
```

### 2. 데이터베이스 연결 테스트
```bash
# Railway 데이터베이스에 연결
railway connect postgresql

# 또는 psql로 직접 연결
psql $DATABASE_URL
```

## 🔧 백엔드 배포 (Railway)

### 1. 배포 설정 확인
```bash
cd backend

# railway.toml 확인
cat railway.toml

# Dockerfile 확인
cat Dockerfile
```

### 2. 환경변수 설정
```bash
# Railway에서 환경변수 설정
railway variables set OPENAI_API_KEY=sk-your-openai-key
railway variables set ANTHROPIC_API_KEY=sk-ant-your-anthropic-key
railway variables set ENVIRONMENT=production
railway variables set DEBUG=false

# 모든 환경변수 확인
railway variables
```

### 3. 배포 실행
```bash
# 백엔드 배포
railway up

# 배포 로그 확인
railway logs

# 서비스 상태 확인
railway status
```

### 4. 마이그레이션 실행
```bash
# Railway에서 마이그레이션 실행
railway run alembic upgrade head

# 또는 배포 시 자동 실행되도록 설정 (railway.toml에 포함됨)
```

### 5. API 테스트
```bash
# 배포된 API 테스트
curl https://your-railway-app.railway.app/api/health

# AI 기능 테스트
curl -X POST https://your-railway-app.railway.app/api/ai/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, AI!"}'
```

## 🌐 프론트엔드 배포 (Vercel)

### 1. Vercel 프로젝트 설정
```bash
cd frontend

# Vercel에 로그인
vercel login

# 프로젝트 초기화
vercel

# 설정 확인
cat vercel.json
```

### 2. 환경변수 설정
```bash
# Vercel에서 환경변수 설정
vercel env add VITE_API_URL production

# 값 입력: https://your-railway-app.railway.app

# 환경변수 확인
vercel env ls
```

### 3. 빌드 테스트 (로컬)
```bash
# 의존성 설치
npm install

# 로컬 빌드 테스트
npm run build

# 빌드 결과 확인
ls -la dist/
```

### 4. 배포 실행
```bash
# 프로덕션 배포
vercel --prod

# 배포 상태 확인
vercel ls

# 로그 확인
vercel logs
```

### 5. 도메인 설정 (선택사항)
```bash
# 커스텀 도메인 추가
vercel domains add yourdomain.com

# 도메인 확인
vercel domains ls
```

## 🔄 CI/CD 파이프라인 설정

### 1. GitHub Actions 워크플로우
```yaml
# .github/workflows/deploy.yml 파일 생성
name: Deploy to Production

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test-backend:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v3
      with:
        python-version: '3.11'
    - name: Install dependencies
      run: |
        cd backend
        pip install -r requirements.txt
    - name: Run tests
      run: |
        cd backend
        pytest

  test-frontend:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '18'
    - name: Install dependencies
      run: |
        cd frontend
        npm install
    - name: Run tests
      run: |
        cd frontend
        npm run test
    - name: Build
      run: |
        cd frontend
        npm run build

  deploy-backend:
    needs: [test-backend]
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
    - uses: actions/checkout@v3
    - name: Deploy to Railway
      run: |
        # Railway CLI를 통한 배포
        npx @railway/cli deploy

  deploy-frontend:
    needs: [test-frontend]
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
    - uses: actions/checkout@v3
    - name: Deploy to Vercel
      run: |
        # Vercel CLI를 통한 배포
        npx vercel --prod --confirm
```

### 2. Git Hooks 설정
```bash
# pre-commit hook 설정
pip install pre-commit

# .pre-commit-config.yaml 확인
cat .pre-commit-config.yaml

# hooks 설치
pre-commit install
```

## 🔍 모니터링 및 로깅

### 1. 애플리케이션 모니터링
```bash
# Railway 모니터링
railway status
railway logs --tail

# Vercel 모니터링  
vercel logs --follow
vercel inspect
```

### 2. 에러 추적 설정
```javascript
// Sentry 설정 (frontend)
import * as Sentry from "@sentry/vue";

Sentry.init({
  app,
  dsn: "YOUR_SENTRY_DSN",
  environment: import.meta.env.MODE,
});
```

```python
# Sentry 설정 (backend)
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration

sentry_sdk.init(
    dsn="YOUR_SENTRY_DSN",
    integrations=[FastApiIntegration()],
    environment=settings.ENVIRONMENT,
)
```

### 3. 성능 모니터링
```python
# 백엔드 성능 모니터링
from prometheus_client import Counter, Histogram, generate_latest

request_count = Counter('http_requests_total', 'Total HTTP requests')
request_duration = Histogram('http_request_duration_seconds', 'HTTP request duration')

@app.middleware("http")
async def monitor_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    request_duration.observe(time.time() - start_time)
    request_count.inc()
    return response
```

## 🛡️ 보안 설정

### 1. SSL/TLS 설정
- Railway: 자동으로 HTTPS 제공
- Vercel: 자동으로 HTTPS 제공
- 커스텀 도메인의 경우 SSL 인증서 자동 발급

### 2. 환경변수 보안
```bash
# 민감한 정보는 절대 코드에 포함하지 않기
# 환경변수만 사용
echo "OPENAI_API_KEY=sk-***" >> .env

# .env 파일이 git에 커밋되지 않도록 확인
cat .gitignore | grep .env
```

### 3. CORS 설정
```python
# 백엔드 CORS 설정
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend-domain.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 4. 보안 헤더 설정
```javascript
// vercel.json에 보안 헤더 설정
{
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        {
          "key": "X-Content-Type-Options",
          "value": "nosniff"
        },
        {
          "key": "X-Frame-Options", 
          "value": "DENY"
        },
        {
          "key": "X-XSS-Protection",
          "value": "1; mode=block"
        }
      ]
    }
  ]
}
```

## 📊 성능 최적화

### 1. 백엔드 최적화
```python
# 데이터베이스 연결 풀링
from sqlalchemy.pool import QueuePool

engine = create_engine(
    settings.DATABASE_URL,
    poolclass=QueuePool,
    pool_size=20,
    max_overflow=30,
    pool_recycle=3600,
)

# Redis 캐싱
from redis import Redis
redis_client = Redis.from_url(settings.REDIS_URL)

# 백그라운드 작업
from celery import Celery
celery_app = Celery("erpnext_ai")
```

### 2. 프론트엔드 최적화
```javascript
// 코드 스플리팅
const Dashboard = () => import('@/views/Dashboard.vue')
const Reports = () => import('@/views/Reports.vue')

// 이미지 최적화
import { defineConfig } from 'vite'
import { resolve } from 'path'

export default defineConfig({
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['vue', 'vue-router', 'pinia'],
          ui: ['@headlessui/vue', '@heroicons/vue']
        }
      }
    }
  }
})
```

## 🧪 배포 후 테스트

### 1. 기능 테스트 스크립트
```bash
#!/bin/bash
# test_deployment.sh

echo "🧪 배포 테스트 시작..."

# 백엔드 헬스체크
echo "🔧 백엔드 상태 확인..."
curl -f https://your-backend.railway.app/api/health || exit 1

# 프론트엔드 접근 테스트
echo "🌐 프론트엔드 접근 테스트..."
curl -f https://your-frontend.vercel.app || exit 1

# API 기능 테스트
echo "🤖 AI API 테스트..."
curl -X POST https://your-backend.railway.app/api/ai/test \
  -H "Content-Type: application/json" \
  -d '{"test": true}' || exit 1

# 데이터베이스 연결 테스트
echo "🗄️ 데이터베이스 연결 테스트..."
curl -f https://your-backend.railway.app/api/system/db-status || exit 1

echo "✅ 모든 테스트 통과!"
```

### 2. 성능 테스트
```bash
# Apache Bench를 통한 성능 테스트
ab -n 100 -c 10 https://your-backend.railway.app/api/health

# 또는 Artillery를 통한 부하 테스트
artillery quick --count 10 --num 5 https://your-backend.railway.app/api/health
```

## 🔄 업데이트 및 롤백

### 1. 무중단 배포
```bash
# Railway는 자동으로 무중단 배포 지원
railway up

# Vercel도 자동으로 무중단 배포 지원
vercel --prod
```

### 2. 롤백 절차
```bash
# Railway 롤백
railway rollback

# Vercel 롤백
vercel rollback
```

### 3. 데이터베이스 마이그레이션 롤백
```bash
# 특정 버전으로 롤백
railway run alembic downgrade -1

# 완전 롤백
railway run alembic downgrade base
```

## 📞 문제 해결

### 일반적인 배포 이슈

1. **빌드 실패**
   - 의존성 버전 충돌 확인
   - Node.js/Python 버전 확인
   - 환경변수 설정 확인

2. **API 연결 오류**
   - CORS 설정 확인
   - 환경변수의 API URL 확인
   - 네트워크 보안 그룹 확인

3. **데이터베이스 연결 오류**
   - DATABASE_URL 형식 확인
   - 방화벽 설정 확인
   - 인증 정보 확인

4. **성능 이슈**
   - 로그를 통한 병목 지점 확인
   - 데이터베이스 쿼리 최적화
   - 캐싱 전략 검토

### 지원 리소스
- Railway 문서: https://docs.railway.app/
- Vercel 문서: https://vercel.com/docs
- 프로젝트 Issues: GitHub Issues 섹션

---

🚀 **성공적인 배포를 위해서는 단계별로 천천히 진행하고, 각 단계마다 테스트를 실행하세요!**