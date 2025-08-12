# 빠른 시작 가이드 ⚡

ERPNext AI System을 5분 안에 실행해보세요!

## 🎯 한 번에 실행하기

Windows에서 다음 명령어들을 순차적으로 실행하세요:

```bash
# 1. 저장소 클론
git clone https://github.com/your-username/erpnext-ai-system.git
cd erpnext-ai-system

# 2. 백엔드 설정
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# 3. 환경변수 설정
copy .env.example .env
# .env 파일을 편집하여 API 키와 데이터베이스 URL 설정

# 4. 데이터베이스 초기화
python scripts/create_initial_migration.py

# 5. 백엔드 실행
python main.py
```

새 터미널에서:
```bash
# 6. 프론트엔드 설정
cd frontend
npm install
copy .env.example .env

# 7. 프론트엔드 실행
npm run dev
```

## 🌐 접속

- **프론트엔드**: http://localhost:3000
- **백엔드 API**: http://localhost:8000
- **API 문서**: http://localhost:8000/docs

## 🔧 필수 설정

### 1. 환경변수 (backend/.env)
```env
# 데이터베이스 (PostgreSQL 필요)
DATABASE_URL=postgresql://user:password@localhost:5432/erpnext_ai

# AI API 키 (필수)
OPENAI_API_KEY=sk-your-openai-key-here
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key-here

# 보안 키
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here
```

### 2. PostgreSQL 설치

#### Windows (Chocolatey)
```bash
choco install postgresql
```

#### Windows (공식 설치 프로그램)
https://www.postgresql.org/download/windows/ 에서 다운로드

#### 데이터베이스 생성
```sql
-- PostgreSQL에 접속
psql -U postgres

-- 데이터베이스와 사용자 생성
CREATE DATABASE erpnext_ai;
CREATE USER erpnext_user WITH ENCRYPTED PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE erpnext_ai TO erpnext_user;
```

## 🤖 AI 기능 활성화

### 1. OpenAI API 키 발급
1. https://platform.openai.com/ 방문
2. 계정 생성/로그인
3. API Keys 섹션에서 새 키 생성

### 2. Anthropic Claude API 키 발급
1. https://console.anthropic.com/ 방문
2. 계정 생성/로그인
3. API Keys 섹션에서 새 키 생성

## 🎨 주요 기능 미리보기

### 1. AI 코파일럿
- 좌측 사이드바의 AI 어시스턴트
- 자연어로 ERP 업무 처리
- 파일 분석 및 데이터 추출

### 2. 완전한 ERP 모듈
- **회계**: 고객/공급업체 관리, 결제 처리
- **영업**: 견적서, 주문서, 송장 관리
- **재고**: 품목 관리, 창고 운영
- **인사**: 직원 관리, 급여 처리
- **프로젝트**: 작업 추적, 시간 관리
- **CRM**: 리드 및 기회 관리

### 3. 전문적인 UI/UX
- ERPNext와 동일한 디자인
- 다크모드 지원
- 반응형 디자인
- 완벽한 접근성

## 🐛 문제 해결

### 일반적인 문제들

#### 1. "ModuleNotFoundError" 오류
```bash
# 가상환경이 활성화되었는지 확인
venv\Scripts\activate
pip install -r requirements.txt
```

#### 2. 데이터베이스 연결 오류
```bash
# PostgreSQL 서비스 실행 확인
net start postgresql-x64-15  # Windows

# 데이터베이스 URL 확인
echo $DATABASE_URL  # Linux/Mac
echo %DATABASE_URL%  # Windows
```

#### 3. API 키 관련 오류
- .env 파일에 올바른 API 키가 설정되었는지 확인
- API 키에 충분한 크레딧이 있는지 확인

#### 4. 포트 충돌
```bash
# 다른 포트 사용
python main.py --port 8001  # 백엔드
npm run dev -- --port 3001  # 프론트엔드
```

## 📚 다음 단계

1. **상세 문서 읽기**
   - [README.md](./README.md) - 전체 시스템 개요
   - [AI_API_SETUP.md](./AI_API_SETUP.md) - AI 기능 상세 설정
   - [DATABASE_SETUP.md](./DATABASE_SETUP.md) - 데이터베이스 관리

2. **배포하기**
   - [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md) - Railway + Vercel 배포

3. **개발하기**
   - [개발 문서](./docs/) - API 문서 및 개발 가이드

## 🆘 도움이 필요한가요?

- 🐛 **버그 리포트**: [GitHub Issues](https://github.com/your-repo/issues)
- 💬 **질문**: [Discussions](https://github.com/your-repo/discussions)
- 📧 **이메일**: support@erpnext-ai.com

## 📱 데모 체험

실제 작동하는 데모를 체험해보세요:
- **데모 사이트**: https://erpnext-ai-demo.vercel.app
- **계정**: demo@erpnext-ai.com
- **비밀번호**: demo123

---

🚀 **5분 만에 차세대 AI ERP 시스템을 체험해보세요!**