# 실시간 배포 진행 상황 🚀

## 현재 진행 단계

### ✅ 1. 코드 준비 완료
- GitHub 저장소: https://github.com/sangbinbag74-lang/ai-erp-system
- 모든 파일이 준비되고 커밋됨

### ✅ 2. 환경변수 및 시크릿 키 생성 완료
- SECRET_KEY: qVlJq7uwz2%HtCbTOFb2IUsn!4DRFoUH!lRC!HCsbRJa*5DDKZANO##NYR#WxLRL
- JWT_SECRET_KEY: NOPJG@nP2aTRWm@kL5GHIUtqAwbc5G%r#RUs$XU$I5ZlhsBWxAkC&*Li9J89rhis
- API 키 발급 페이지들 모두 열림

### 🔄 3. Railway 백엔드 배포 (수동 진행 중)

#### A. PostgreSQL 데이터베이스 생성
```
상태: 🟡 사용자가 Railway에서 생성 중
단계: New Project → Provision PostgreSQL
```

#### B. 백엔드 서비스 배포  
```
상태: ⏳ PostgreSQL 완료 후 진행 예정
설정할 환경변수:
- DATABASE_URL: (Railway에서 자동 생성)
- OPENAI_API_KEY: 사용자 발급 필요
- ANTHROPIC_API_KEY: 사용자 발급 필요
- SECRET_KEY: 랜덤 생성
- JWT_SECRET_KEY: 랜덤 생성
- ENVIRONMENT: production
- DEBUG: false
```

### ⏳ 3. Vercel 프론트엔드 배포 (대기 중)
```
상태: 🔴 Railway 완료 후 시작
필요한 환경변수:
- VITE_API_URL: Railway 백엔드 URL
- VITE_ENABLE_AI_COPILOT: true
```

## Railway 배포 단계별 가이드

### 단계 1: PostgreSQL 생성
1. Railway 대시보드 접속
2. "New Project" → "Provision PostgreSQL" 
3. 데이터베이스 이름 설정: `erpnext-ai-db`

### 단계 2: 백엔드 서비스 추가
1. 프로젝트에 "GitHub Repo" 서비스 추가
2. 저장소 선택: `sangbinbag74-lang/ai-erp-system`
3. 루트 디렉토리: `backend`
4. 빌드 명령어: 자동 감지 (requirements.txt 기반)

### 단계 3: 환경변수 설정
Variables 탭에서 다음 설정:
```env
DATABASE_URL=${{Postgres.DATABASE_URL}}
OPENAI_API_KEY=sk-your-key-here
ANTHROPIC_API_KEY=sk-ant-your-key-here  
SECRET_KEY=super-secret-key-for-production
JWT_SECRET_KEY=jwt-secret-key-for-production
ENVIRONMENT=production
DEBUG=false
ALLOWED_ORIGINS=https://your-frontend.vercel.app,http://localhost:3000
```

## Vercel 배포 단계별 가이드

### 단계 1: 프로젝트 생성
1. Vercel 대시보드 접속
2. "New Project" → GitHub 저장소 연결
3. 저장소: `sangbinbag74-lang/ai-erp-system`
4. 루트 디렉토리: `frontend`

### 단계 2: 빌드 설정
```
Framework Preset: Vite
Build Command: npm run build  
Output Directory: dist
Install Command: npm install
```

### 단계 3: 환경변수 설정
```env
VITE_API_URL=https://your-backend.railway.app
VITE_ENABLE_AI_COPILOT=true
VITE_APP_NAME=ERPNext AI System
VITE_DEFAULT_THEME=light
VITE_DEFAULT_LANGUAGE=ko
```

## 필요한 API 키

### OpenAI API 키 발급
1. https://platform.openai.com 접속
2. API Keys → Create new secret key
3. 키 이름: `ERPNext-AI-Production`
4. 권한: Full access
5. 생성된 키 복사 (한 번만 표시됨)

### Anthropic Claude API 키 발급  
1. https://console.anthropic.com 접속
2. API Keys → Create Key
3. 키 이름: `ERPNext-AI-Claude`
4. 생성된 키 복사

## 배포 후 확인 사항

### 백엔드 테스트
- [ ] 헬스 체크: `https://your-backend.railway.app/api/health`
- [ ] API 문서: `https://your-backend.railway.app/docs`
- [ ] 데이터베이스 연결 확인

### 프론트엔드 테스트  
- [ ] 메인 페이지 로딩: `https://your-frontend.vercel.app`
- [ ] AI 코파일럿 패널 표시
- [ ] API 연결 확인

### 통합 테스트
- [ ] AI 채팅 기능
- [ ] ERP 모듈 접근
- [ ] 데이터 CRUD 작업

---

## 🆘 문제 해결

### 일반적인 오류들
1. **빌드 실패**: requirements.txt 또는 package.json 확인
2. **환경변수 오류**: 키 이름과 값 정확성 확인  
3. **CORS 오류**: ALLOWED_ORIGINS 설정 확인
4. **데이터베이스 연결 오류**: DATABASE_URL 형식 확인

### 로그 확인 방법
- Railway: 서비스 → Logs 탭
- Vercel: 프로젝트 → Functions 탭 → View Function Logs

---

**현재 진행 상황을 실시간으로 업데이트하겠습니다.**