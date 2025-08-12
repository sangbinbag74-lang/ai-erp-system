# ERPNext AI System 🤖

AI 기반 차세대 ERP 시스템 - ERPNext의 모든 기능을 구현한 AI 중심의 기업용 솔루션

## 🌟 주요 특징

### 🧠 AI 기능
- **AGI 수준 자율성**: Chain of Thought 방식으로 복잡한 작업 자동 처리
- **파일 관리**: 모든 ERP 문서 불러오기, 수정, 설명 기능
- **워크플로 자동화**: 비즈니스 프로세스 자동 실행
- **예측 분석**: 데이터 기반 미래 예측 및 인사이트 제공
- **좌측 AI 코파일럿**: Microsoft Copilot 스타일의 AI 어시스턴트

### 🏢 완전한 ERP 모듈
- 📊 **Accounts** (회계): 복식부기, 계정과목, 거래처 관리, 결제 처리
- 💼 **Sales** (영업): 고객관리, 견적서, 주문서, 송장 발행
- 🛒 **Purchase** (구매): 공급업체 관리, 구매주문, 입고 관리
- 📦 **Stock** (재고): 창고관리, 재고이동, 평가방법, 시리얼/배치 관리
- 👥 **HR** (인사): 직원관리, 급여, 출근관리, 휴가 관리
- 🏭 **Manufacturing** (제조): BOM 관리, 작업지시, 생산계획
- 📁 **Projects** (프로젝트): 프로젝트관리, 작업추적, 시간기록
- 🎯 **CRM** (고객관리): 리드관리, 기회관리, 커뮤니케이션
- 🔧 **Support** (지원): 이슈추적, 유지보수 일정
- 🏢 **Assets** (자산관리): 고정자산 관리, 감가상각
- ✅ **Quality** (품질관리): 품질검사, 검사 템플릿
- 🌐 **Website** (웹사이트): 콘텐츠관리, 전자상거래

### 🎨 전문적인 디자인
- **ERPNext 스타일**: 원본과 거의 동일한 UI/UX
- **사무용 디자인**: 전문적이고 깔끔한 인터페이스
- **반응형 디자인**: 모든 디바이스 지원
- **다크모드**: 눈의 피로를 줄이는 다크 테마
- **접근성**: 스크린 리더 및 키보드 네비게이션 완벽 지원

## 🏗️ 기술 스택

### Backend
- **FastAPI**: 고성능 Python 웹 프레임워크
- **SQLAlchemy**: ORM 및 데이터베이스 관리
- **PostgreSQL**: 메인 데이터베이스
- **Redis**: 캐시 및 세션 저장소
- **Alembic**: 데이터베이스 마이그레이션
- **Celery**: 백그라운드 작업 처리

### Frontend
- **Vue 3**: 최신 Vue.js 프레임워크
- **Pinia**: 상태 관리
- **Vue Router**: 라우팅
- **Tailwind CSS**: 유틸리티 우선 CSS 프레임워크
- **Frappe UI**: ERPNext 스타일 컴포넌트 라이브러리
- **Chart.js**: 데이터 시각화

### AI & ML
- **OpenAI API**: GPT-4 텍스트 처리
- **Anthropic Claude**: 고급 추론 및 분석
- **LangChain**: LLM 오케스트레이션
- **Vector Store**: 문서 임베딩 저장

### 배포 및 인프라
- **Railway**: 백엔드 배포
- **Vercel**: 프론트엔드 배포
- **Docker**: 컨테이너화
- **GitHub Actions**: CI/CD

## 🚀 빠른 시작

### 필수 요구사항
- Node.js 18+
- Python 3.11+
- PostgreSQL 14+
- Redis 6+

### 1. 저장소 클론
\`\`\`bash
git clone https://github.com/your-username/erpnext-ai-system.git
cd erpnext-ai-system
\`\`\`

### 2. 백엔드 설정
\`\`\`bash
cd backend

# 가상환경 생성
python -m venv venv
source venv/bin/activate  # Windows: venv\\Scripts\\activate

# 의존성 설치
pip install -r requirements.txt

# 환경변수 설정
cp .env.example .env
# .env 파일을 편집하여 필요한 값들을 설정

# 데이터베이스 마이그레이션
alembic upgrade head

# 개발 서버 실행
python main.py
\`\`\`

### 3. 프론트엔드 설정
\`\`\`bash
cd frontend

# 의존성 설치
npm install

# 환경변수 설정
cp .env.example .env
# .env 파일을 편집하여 API URL 등을 설정

# 개발 서버 실행
npm run dev
\`\`\`

### 4. 접속
- 프론트엔드: http://localhost:3000
- 백엔드 API: http://localhost:8000
- API 문서: http://localhost:8000/docs

## 🔧 환경변수 설정

### 백엔드 (.env)
\`\`\`env
# 데이터베이스
DATABASE_URL=postgresql://user:password@localhost:5432/erpnext_ai

# AI API 키
OPENAI_API_KEY=your-openai-key
ANTHROPIC_API_KEY=your-anthropic-key

# 기타 설정
ENVIRONMENT=development
SECRET_KEY=your-secret-key
\`\`\`

### 프론트엔드 (.env)
\`\`\`env
# API URL
VITE_API_URL=http://localhost:8000

# 기능 플래그
VITE_ENABLE_AI_COPILOT=true
VITE_ENABLE_DARK_MODE=true
\`\`\`

## 🐳 Docker 배포

### Docker Compose 사용
\`\`\`bash
# 모든 서비스 시작
docker-compose up -d

# 로그 확인
docker-compose logs -f

# 서비스 중지
docker-compose down
\`\`\`

### 개별 이미지 빌드
\`\`\`bash
# 백엔드
cd backend
docker build -t erpnext-ai-backend .

# 프론트엔드
cd frontend
docker build -t erpnext-ai-frontend .
\`\`\`

## 📊 데이터베이스 관리

### 마이그레이션 생성
\`\`\`bash
cd backend
alembic revision --autogenerate -m "Add new table"
\`\`\`

### 마이그레이션 적용
\`\`\`bash
alembic upgrade head
\`\`\`

### 마이그레이션 롤백
\`\`\`bash
alembic downgrade -1
\`\`\`

## 🤖 AI 기능 사용법

### 1. AI 코파일럿
- 화면 좌측의 AI 어시스턴트 패널 사용
- 자연어로 ERP 업무 요청
- 파일 업로드 및 분석 기능

### 2. 지원되는 AI 명령어
\`\`\`
"이번 달 매출 분석해줘"
"재고가 부족한 상품들을 찾아서 주문 제안해줘"
"신규 고객을 등록하는 방법을 알려줘"
"월말 보고서를 생성해줘"
\`\`\`

### 3. 파일 관리
- PDF, Excel, CSV 파일 업로드 지원
- AI가 자동으로 파일 내용 분석
- 데이터 추출 및 ERP 시스템 연동

## 📖 API 문서

### REST API
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### 주요 엔드포인트
\`\`\`
GET    /api/health              # 시스템 상태
POST   /api/ai/chat             # AI 채팅
GET    /api/doctypes            # DocType 목록
GET    /api/customer            # 고객 목록
POST   /api/customer            # 고객 생성
GET    /api/customer/{id}       # 고객 조회
PUT    /api/customer/{id}       # 고객 수정
DELETE /api/customer/{id}       # 고객 삭제
\`\`\`

## 🧪 테스트

### 백엔드 테스트
\`\`\`bash
cd backend
pytest
\`\`\`

### 프론트엔드 테스트
\`\`\`bash
cd frontend
npm run test
\`\`\`

### E2E 테스트
\`\`\`bash
cd frontend
npm run test:e2e
\`\`\`

## 🔐 보안

### 인증 및 권한
- JWT 기반 인증
- 역할 기반 접근 제어 (RBAC)
- API 키 관리

### 보안 헤더
- CORS 설정
- CSP (Content Security Policy)
- XSS 방지
- CSRF 방지

## 📈 모니터링

### 로그 관리
- 구조화된 JSON 로깅
- 로그 레벨별 분류
- 에러 추적 및 알림

### 성능 모니터링
- API 응답 시간 측정
- 메모리 사용량 추적
- 데이터베이스 쿼리 최적화

## 🤝 기여하기

1. Fork the repository
2. Create your feature branch (\`git checkout -b feature/amazing-feature\`)
3. Commit your changes (\`git commit -m 'Add some amazing feature'\`)
4. Push to the branch (\`git push origin feature/amazing-feature\`)
5. Open a Pull Request

### 개발 가이드라인
- Python 코드는 Black으로 포맷팅
- JavaScript/Vue 코드는 Prettier로 포맷팅
- 커밋 메시지는 Conventional Commits 규칙 준수
- 모든 새 기능에 대해 테스트 작성

## 📝 라이선스

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 감사의 말

- [ERPNext](https://github.com/frappe/erpnext) - 원본 ERP 시스템
- [FastAPI](https://fastapi.tiangolo.com/) - 백엔드 프레임워크
- [Vue.js](https://vuejs.org/) - 프론트엔드 프레임워크
- [Frappe UI](https://github.com/frappe/frappe-ui) - UI 컴포넌트 라이브러리

## 📞 지원

- 📧 Email: support@erpnext-ai.com
- 💬 Discord: [ERPNext AI Community](https://discord.gg/erpnext-ai)
- 📚 Documentation: [docs.erpnext-ai.com](https://docs.erpnext-ai.com)
- 🐛 Issues: [GitHub Issues](https://github.com/your-username/erpnext-ai-system/issues)

## 🗺️ 로드맵

- [ ] 모바일 앱 (React Native)
- [ ] 고급 AI 분석 대시보드
- [ ] 실시간 협업 기능
- [ ] 다국어 지원 확대
- [ ] 화이트 라벨 솔루션
- [ ] 온프레미스 배포 옵션