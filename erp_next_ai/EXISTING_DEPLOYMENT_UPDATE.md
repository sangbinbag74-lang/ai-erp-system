# 기존 배포 업데이트 가이드 🔄

기존에 배포된 Railway와 Vercel 프로젝트를 새로운 ERPNext AI 시스템으로 업데이트하는 가이드입니다.

## 🔗 기존 배포 정보

- **Railway 백엔드**: `ai-erp-system-production.up.railway.app`
- **Vercel 프론트엔드**: `ai-erp-system` (park-sangbins-projects)
- **GitHub 저장소**: `sangbinbag74-lang/ai-erp-system`

## 📊 현재 상태

### ✅ 완료된 준비 작업
- [x] GitHub 저장소에 완전한 ERPNext AI 시스템 커밋
- [x] Railway URL로 설정 파일 업데이트
- [x] Vercel 설정 최적화
- [x] 환경변수 구성 가이드 작성
- [x] 배포 스크립트 준비

## 🚀 업데이트 단계

### 1. Railway 백엔드 업데이트

#### A. 대시보드 접속
1. https://railway.app/dashboard 방문
2. `ai-erp-system-production` 프로젝트 선택

#### B. 소스 업데이트 확인
1. **Settings** → **Source** 탭
2. GitHub 저장소 연결 확인: `sangbinbag74-lang/ai-erp-system`
3. **Root Directory**: `backend/`
4. 자동 배포가 최신 커밋으로 진행되는지 확인

#### C. 환경변수 설정 확인/추가
**Environment** 탭에서 다음 변수들 확인:

```env
# 필수 환경변수
DATABASE_URL=<Railway PostgreSQL URL - 자동 생성>
OPENAI_API_KEY=sk-your-openai-key-here
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key-here

# 추가 환경변수 (새로 추가)
ENVIRONMENT=production
DEBUG=false
SECRET_KEY=your-super-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here
JWT_ALGORITHM=HS256
JWT_EXPIRATION_DELTA=86400

# CORS 설정
ALLOWED_ORIGINS=https://ai-erp-system-f1c4bb20b-park-sangbins-projects.vercel.app,https://ai-erp-system-*.vercel.app

# AI 설정
AI_MODEL_TEMPERATURE=0.7
AI_MAX_TOKENS=2048
AI_ENABLE_STREAMING=true
```

#### D. 데이터베이스 설정
1. **Add Service** → **PostgreSQL** (아직 없다면)
2. 데이터베이스가 연결되면 자동으로 `DATABASE_URL` 환경변수 생성

#### E. 재배포 트리거
- **Settings** → **Deploy** 또는 **Deployments** 탭에서 수동 재배포 실행

### 2. Vercel 프론트엔드 업데이트

#### A. 대시보드 접속
1. https://vercel.com/dashboard 방문
2. `ai-erp-system` 프로젝트 선택

#### B. 설정 확인
1. **Settings** → **General**
2. **Root Directory**: `frontend/`
3. **Framework Preset**: `Vite`
4. **Build Command**: `npm run build`
5. **Output Directory**: `dist`

#### C. 환경변수 설정
**Settings** → **Environment Variables**:

```env
# 필수 환경변수
VITE_API_URL=https://ai-erp-system-production.up.railway.app

# 추가 환경변수 (새로 추가)
VITE_ENABLE_AI_COPILOT=true
VITE_APP_NAME=ERPNext AI System
VITE_APP_VERSION=1.0.0
VITE_ENABLE_DARK_MODE=true
VITE_ENABLE_NOTIFICATIONS=true
VITE_DEFAULT_THEME=light
VITE_DEFAULT_LANGUAGE=ko
```

#### D. 재배포 실행
1. **Deployments** 탭
2. 최신 배포에서 **⋯** → **Redeploy** 클릭

## 🔧 업데이트 후 확인사항

### 1. 백엔드 API 테스트
```bash
# 헬스체크
curl https://ai-erp-system-production.up.railway.app/api/health

# API 문서 접속
https://ai-erp-system-production.up.railway.app/docs

# 시스템 정보
curl https://ai-erp-system-production.up.railway.app/api/system/info
```

### 2. 프론트엔드 접속 테스트
- 메인 페이지: https://ai-erp-system-f1c4bb20b-park-sangbins-projects.vercel.app
- AI 코파일럿 좌측 사이드바 확인
- 모든 ERP 모듈 메뉴 확인 (Accounts, Sales, Purchase 등)

### 3. AI 기능 테스트
1. 좌측 AI 코파일럿 패널 클릭
2. 간단한 메시지 전송: "안녕하세요, ERPNext AI입니다!"
3. AI 응답 확인 (OpenAI/Claude 연동 테스트)

## 🐛 문제 해결

### 일반적인 문제들

#### 1. 빌드 실패
**Railway 백엔드**:
- Logs 탭에서 오류 메시지 확인
- Python 버전 확인 (3.11+)
- requirements.txt 의존성 확인

**Vercel 프론트엔드**:
- Function Logs에서 오류 확인
- Node.js 버전 확인 (18+)
- package.json 빌드 스크립트 확인

#### 2. API 연결 오류
- CORS 설정 확인: `ALLOWED_ORIGINS` 환경변수
- API URL 확인: `VITE_API_URL` 환경변수
- 네트워크 탭에서 요청/응답 확인

#### 3. AI 기능 오류
- API 키 유효성 확인
- API 키 잔액/쿼터 확인
- Railway 로그에서 AI 요청 오류 확인

#### 4. 데이터베이스 연결 오류
- PostgreSQL 서비스 상태 확인
- `DATABASE_URL` 형식 확인
- 마이그레이션 실행 상태 확인

## 📋 업데이트 체크리스트

### Railway 백엔드
- [ ] GitHub 저장소 연결 확인
- [ ] Root directory `backend/` 설정
- [ ] PostgreSQL 서비스 추가
- [ ] 모든 환경변수 설정
- [ ] 빌드 및 배포 성공
- [ ] API 헬스체크 통과
- [ ] Swagger 문서 접근 가능

### Vercel 프론트엔드  
- [ ] GitHub 저장소 연결 확인
- [ ] Root directory `frontend/` 설정
- [ ] Vite 빌드 설정 확인
- [ ] 모든 환경변수 설정
- [ ] 빌드 및 배포 성공
- [ ] 프론트엔드 접근 가능
- [ ] AI 코파일럿 작동 확인

### 통합 테스트
- [ ] 프론트엔드 → 백엔드 API 연결
- [ ] AI 채팅 기능 작동
- [ ] ERP 모듈 메뉴 정상 표시
- [ ] 전체적인 UI/UX 확인

## 🎉 업데이트 완료 후

성공적으로 업데이트가 완료되면:

### 🔗 새로운 ERPNext AI 시스템 URL들
- **메인 애플리케이션**: https://ai-erp-system-f1c4bb20b-park-sangbins-projects.vercel.app
- **백엔드 API**: https://ai-erp-system-production.up.railway.app
- **API 문서**: https://ai-erp-system-production.up.railway.app/docs

### 🆕 새로운 기능들
- **완전한 DocType 시스템**: ERPNext와 동일한 메타데이터 기반 구조
- **AI 코파일럿**: 좌측 사이드바의 Microsoft Copilot 스타일 AI 어시스턴트
- **모든 ERP 모듈**: Accounts, Sales, Purchase, Stock, HR, Projects, CRM, Support 등
- **전문적인 UI**: Frappe UI 컴포넌트 기반 깔끔한 사무용 디자인
- **다크모드**: 눈의 피로를 줄이는 다크 테마 지원
- **완벽한 반응형**: 모든 디바이스에서 최적화된 경험

---

🚀 **축하합니다! ERPNext AI 시스템 업데이트가 완료되었습니다!** 🎊

이제 실제 ERPNext의 모든 기능과 AI 자율성을 갖춘 차세대 ERP 시스템을 사용할 수 있습니다!