# AI ERP - LLM 기반 차세대 기업자원관리 시스템

AI 중심의 기업자원관리 시스템으로 ERPNext를 기반으로 고급 LLM 통합 기능을 제공합니다.

## 개요

이 프로젝트는 기존 ERP 경험을 혁신하여 대화형 인터페이스를 통해 자연스럽게 상호작용하고 AI가 복잡한 파일 작업, 데이터 분석, 비즈니스 프로세스 자동화를 자율적으로 처리할 수 있도록 LLM(대형 언어 모델)을 핵심 엔진으로 통합합니다.

## 주요 기능

### 🤖 AI 우선 아키텍처
- LLM 기반 파일 관리 및 분석
- 자율적 문서 처리 및 인사이트 제공
- 모든 ERP 기능을 위한 자연어 쿼리 인터페이스
- 지능형 워크플로 자동화

### 📁 고급 파일 관리
- 자동 파일 스캔 및 내용 분석
- AI 기반 문서 요약
- 스마트 파일 정리 및 태그 관리
- 실시간 파일 수정 추적

### 👥 간소화된 팀 관리
- 원클릭 팀 초대 시스템
- AI 지원 역할 배정
- 자동화된 권한 관리
- 지능형 팀 협업 기능

### ☁️ 클라우드 네이티브 저장소
- 외부 클라우드 API 통합 (AWS S3, Google Cloud)
- 분산 파일 동기화
- 비용 최적화 저장소 솔루션
- 실시간 백업 및 복구

### 💰 유연한 요금제
- **무료 버전**: 최대 5명 팀원, 기본 LLM 기능
- **프로 버전**: 무제한 팀원, 고급 AI 분석, 우선 지원

## 기술 스택

### 백엔드
- **프레임워크**: Python/Frappe (ERPNext에서 상속)
- **데이터베이스**: MariaDB/PostgreSQL
- **LLM 통합**: OpenAI GPT-4, Anthropic Claude, 또는 Grok API
- **클라우드 저장소**: AWS S3, Google Cloud Storage API
- **인증**: 역할 기반 접근 제어를 가진 JWT

### 프론트엔드
- **프레임워크**: Frappe UI 컴포넌트를 가진 Vue.js
- **상태 관리**: Vuex/Pinia
- **실시간**: WebSocket 연결
- **UI 라이브러리**: AI 향상 사용자 정의 컴포넌트

### 외부 통합
- **LLM API**: 비용 최적화를 위한 사용량 기반 모델
- **결제 처리**: Stripe 통합
- **클라우드 저장소**: 다중 제공업체 API 지원
- **모니터링**: AI 기반 시스템 분석

## 프로젝트 구조

```
ai_erp/
├── backend/                 # Python/Frappe 백엔드
│   ├── ai_core/            # LLM 통합 모듈
│   ├── file_manager/       # 향상된 파일 관리
│   ├── team_manager/       # 간소화된 팀 운영
│   ├── cloud_storage/      # 클라우드 API 통합
│   └── billing/            # 구독 관리
├── frontend/               # Vue.js 프론트엔드
│   ├── components/         # AI 향상 UI 컴포넌트
│   ├── views/             # 메인 애플리케이션 뷰
│   ├── chat/              # 대화형 인터페이스
│   └── dashboard/         # AI 기반 대시보드
├── shared/                # 공유 유틸리티 및 타입
├── config/               # 설정 파일
└── docs/                 # 문서
```

## 핵심 모듈

### 1. AI 코어 엔진 (`/backend/ai_core/`)
- LLM API 추상화 레이어
- 컨텍스트 관리 및 메모리
- 자연어 처리
- 지능형 작업 라우팅

### 2. 파일 관리 시스템 (`/backend/file_manager/`)
- 자동화된 파일 처리
- 내용 분석 및 추출
- 버전 제어 및 감사 추적
- AI 기반 파일 추천

### 3. 팀 관리 (`/backend/team_manager/`)
- 간소화된 사용자 온보딩
- 역할 기반 접근 제어
- 팀 성과 분석
- 협업 도구

### 4. 클라우드 저장소 통합 (`/backend/cloud_storage/`)
- 다중 제공업체 저장소 추상화
- 자동 동기화
- 데이터 암호화 및 보안
- 비용 최적화 알고리즘

## 시작하기

### 전제 조건
- Python 3.8+
- Node.js 16+
- MariaDB/PostgreSQL
- Redis (캐싱용)

### 설치
```bash
# 리포지토리 클론
git clone [repository-url]
cd ai_erp

# 백엔드 종속성 설치
cd backend
pip install -r requirements.txt

# 프론트엔드 종속성 설치
cd ../frontend
npm install

# 환경 구성
cp config/.env.example config/.env
# API 키와 설정으로 구성 파일을 편집하세요

# 데이터베이스 초기화
cd ../backend
python manage.py migrate

# 개발 서버 시작
python manage.py runserver  # 백엔드
cd ../frontend && npm run dev  # 프론트엔드
```

### 설정
1. LLM API 자격 증명 설정 (OpenAI, Anthropic 등)
2. 클라우드 저장소 제공업체 구성
3. 결제 게이트웨이 설정 (Stripe)
4. 이메일 및 알림 서비스 구성

## 구독 요금제

### 무료 요금제
- 팀원 최대 5명
- 저장소 5GB
- AI 쿼리 월 100회
- 기본 ERP 기능
- 이메일 지원

### 베이직 요금제 (월 29,000원)
- 팀원 최대 25명
- 저장소 100GB
- AI 쿼리 월 1,000회
- 고급 기능
- 우선 지원

### 프로 요금제 (월 99,000원) - 가장 인기
- 무제한 팀원
- 저장소 1TB
- AI 쿼리 월 10,000회
- 모든 기능
- 전화 지원
- 맞춤 브랜딩

### 엔터프라이즈 요금제 (월 299,000원)
- 프로의 모든 기능
- 전용 지원
- SSO 통합
- 맞춤 개발
- 온프레미스 옵션

## 특장점

### 기존 ERP 시스템 대비
1. **AI 우선 아키텍처**: 애드온이 아닌 핵심 엔진으로서의 LLM
2. **간소화된 UX**: 자연어 인터페이스로 교육 시간 단축
3. **클라우드 네이티브**: 현대적 클라우드 인프라용 설계
4. **비용 효율성**: 비싼 라이선스 대신 사용량 기반 모델
5. **빠른 배포**: 몇 개월이 아닌 몇 시간 만에 설정

### 경쟁사 대비
1. **진정한 AI 통합**: 단순 챗봇이 아닌 AI 기반 운영
2. **멀티 클라우드**: 벤더 독립적 저장소 및 컴퓨팅
3. **개방형 아키텍처**: API 우선 설계로 맞춤화 가능
4. **투명한 가격**: 숨겨진 비용 없는 명확한 티어 구조
5. **ERPNext 기반**: 검증된 ERP 기능을 기반으로 구축

## 빠른 시작

### 1. 시스템 설치
```bash
# 자동 설정 실행
python scripts/setup.py

# 또는 수동 설치
pip install -r backend/requirements.txt
cd frontend && npm install
```

### 2. 환경 설정
```bash
# 환경 변수 설정
cp config/.env.example config/.env

# API 키 설정
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
AWS_ACCESS_KEY_ID=your_aws_key
STRIPE_SECRET_KEY=your_stripe_key
```

### 3. 데이터베이스 설정
```bash
# PostgreSQL 데이터베이스 생성
createdb ai_erp_dev

# 마이그레이션 실행
python backend/manage.py migrate
```

### 4. 시스템 시작
```bash
# 백엔드 서버 시작
cd backend && python manage.py runserver

# 프론트엔드 서버 시작 (새 터미널에서)
cd frontend && npm run dev

# 데모 실행
python demo/main.py
```

## 사용 예시

### AI 지원 팀 생성
```python
# 간단한 팀 생성
team_service.create_team(
    name="마케팅팀",
    owner_email="manager@company.com",
    description="디지털 마케팅 전담팀"
)
# AI가 자동으로 역할과 권한을 제안합니다
```

### 자연어 파일 분석
```python
# 파일 업로드 후 자동 분석
result = ai_erp.analyze_file(
    file_path="계약서.pdf",
    query="이 계약서의 주요 조건과 만료일을 알려주세요"
)
# AI가 내용을 분석하고 핵심 정보를 추출합니다
```

### 지능형 쿼리 처리
```python
# 자연어로 비즈니스 쿼리
response = ai_erp.query(
    "이번 분기 매출이 가장 높은 고객 상위 5명을 보여주세요"
)
# AI가 데이터베이스를 검색하고 시각화된 결과를 제공합니다
```

## 보안 및 컴플라이언스

- **데이터 암호화**: 모든 데이터의 종단 간 암호화
- **접근 제어**: 감사 로깅을 포함한 역할 기반 권한
- **API 보안**: 리프레시 메커니즘을 가진 JWT 토큰
- **저장소 보안**: 보안 접근을 가진 암호화된 클라우드 저장소
- **컴플라이언스**: GDPR 준수 데이터 처리 및 사용자 프라이버시 제어

## 모니터링 및 분석

### 실시간 대시보드
- 팀 활동 및 성과 지표
- AI 사용량 및 비용 추적
- 시스템 상태 및 알림
- 사용자 참여 분석

### AI 인사이트
- 자동화된 비즈니스 인텔리전스
- 예측 분석 및 추천
- 비용 최적화 제안
- 성과 벤치마킹

## 지원 및 커뮤니티

- 📧 이메일: support@ai-erp.kr
- 💬 커뮤니티: [디스코드/슬랙 채널]
- 📖 문서: [docs.ai-erp.kr]
- 🎥 튜토리얼: [YouTube 채널]

## 라이선스

이 프로젝트는 ERPNext의 GPL v3 라이선스를 기반으로 구축되었습니다. 추가 AI 개선사항은 동일한 라이선스 조건에 따라 제공됩니다.

## 기여하기

기여를 환영합니다! 개선사항에 대한 풀 리퀘스트를 제출하기 전에 기여 가이드라인을 읽어주세요.

### 개발 가이드라인
1. 코드 스타일: Black 포매터 사용
2. 테스트: 새로운 기능에 대한 테스트 추가
3. 문서화: 공개 API에 대한 문서 업데이트
4. 커밋 메시지: 기존 규칙 따르기

## 로드맵

### 2024년 1분기
- [x] 핵심 AI 엔진 구현
- [x] 기본 팀 관리 기능
- [x] 파일 처리 시스템
- [x] 클라우드 저장소 통합

### 2024년 2분기 (예정)
- [ ] 모바일 애플리케이션
- [ ] 고급 분석 대시보드
- [ ] 타사 통합 (Slack, MS Teams)
- [ ] 다국어 지원 확장

### 2024년 3분기 (예정)
- [ ] 업계별 특화 모듈
- [ ] AI 마켓플레이스
- [ ] 고급 워크플로 자동화
- [ ] 엔터프라이즈 SSO 통합

## FAQ

**Q: 기존 ERPNext에서 마이그레이션할 수 있나요?**
A: 네, 호환성 계층을 제공하여 기존 데이터와 커스터마이제이션을 보존합니다.

**Q: AI 기능을 비활성화할 수 있나요?**
A: 네, 기존 ERPNext 모드로 작동하도록 AI 기능을 선택적으로 비활성화할 수 있습니다.

**Q: 온프레미스 배포를 지원하나요?**
A: 엔터프라이즈 요금제에서 온프레미스 배포 옵션을 제공합니다.

**Q: 데이터는 어디에 저장되나요?**
A: 사용자가 선택한 클라우드 제공업체 (AWS, Google Cloud, Azure) 또는 온프레미스에 저장됩니다.

---

**참고**: 이것은 고급 AI 기능을 갖춘 ERPNext의 개선된 버전입니다. 모든 원본 ERPNext 기능은 고급 LLM 기반 기능을 추가하면서 보존됩니다.

## 연락처

프로젝트에 대한 질문이나 제안이 있으시면 언제든지 연락해 주세요:

- **이메일**: info@ai-erp.kr
- **웹사이트**: https://ai-erp.kr
- **GitHub**: [프로젝트 리포지토리]
- **LinkedIn**: [회사 페이지]

---

*한국의 미래 지향적 기업을 위한 차세대 ERP 솔루션*