# Vercel 환경변수 설정 가이드

## 1. Vercel Dashboard에서 설정

### Frontend 환경변수 (vercel.com → 프로젝트 → Settings → Environment Variables)

```bash
# API 설정
VITE_API_URL=https://your-backend-url.railway.app
VITE_API_VERSION=v1

# 인증
VITE_AUTH_DOMAIN=ai-erp.vercel.app

# 기능 플래그
VITE_ENABLE_AI_FEATURES=true
VITE_ENABLE_CLOUD_STORAGE=true

# 환경
VITE_APP_ENV=production
VITE_DEBUG_MODE=false
```

## 2. Backend 환경변수 (Railway/DigitalOcean)

```bash
# 데이터베이스
DATABASE_URL=mysql://user:pass@host:port/db
REDIS_URL=redis://host:port

# API 키 (보안 주의!)
ANTHROPIC_API_KEY=your-key
OPENAI_API_KEY=your-key
STRIPE_SECRET_KEY=your-key

# 환경 설정
FRAPPE_ENV=production
DEBUG=false
```

## 3. CLI로 환경변수 설정

```bash
# Vercel CLI로 환경변수 추가
vercel env add VITE_API_URL production
vercel env add VITE_AUTH_DOMAIN production

# Railway CLI로 환경변수 추가
railway variables set DATABASE_URL=mysql://...
railway variables set REDIS_URL=redis://...
```

## 4. 보안 주의사항

- ✅ Frontend: VITE_ 접두사 사용 (클라이언트 노출)
- ❌ API 키는 Frontend에 직접 노출 금지
- ✅ Backend: 민감한 데이터는 서버에서만 처리
- ✅ .env 파일을 .gitignore에 추가

## 5. 환경별 설정

### Development
```bash
VITE_API_URL=http://localhost:8000
VITE_DEBUG_MODE=true
```

### Production
```bash
VITE_API_URL=https://your-backend.railway.app
VITE_DEBUG_MODE=false
```