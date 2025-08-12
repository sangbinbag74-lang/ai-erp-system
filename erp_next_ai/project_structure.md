# ERPNext AI System - 프로젝트 구조

## 개요
ERPNext의 모든 기능을 구현한 AI 중심 ERP 시스템

## 아키텍처
- **Backend**: FastAPI + SQLAlchemy (ERPNext DocType 시스템 구현)
- **Frontend**: Vue 3 + Frappe UI + Tailwind CSS
- **Database**: PostgreSQL
- **AI**: OpenAI API + Claude API
- **Deployment**: Railway (Backend) + Vercel (Frontend)

## 디렉토리 구조

```
erp_next_ai/
├── backend/
│   ├── core/
│   │   ├── doctype/           # DocType 시스템
│   │   ├── database/          # 데이터베이스 추상화
│   │   ├── permissions/       # 권한 관리
│   │   ├── workflow/          # 워크플로 시스템
│   │   └── api/              # API 자동 생성
│   ├── modules/
│   │   ├── accounts/         # 회계
│   │   ├── sales/            # 영업
│   │   ├── purchase/         # 구매
│   │   ├── stock/            # 재고
│   │   ├── hr/               # 인사
│   │   ├── manufacturing/    # 제조
│   │   ├── projects/         # 프로젝트
│   │   ├── crm/              # 고객관리
│   │   ├── support/          # 지원
│   │   ├── assets/           # 자산관리
│   │   ├── quality/          # 품질관리
│   │   └── website/          # 웹사이트
│   ├── ai/
│   │   ├── copilot/          # AI 코파일럿
│   │   ├── file_manager/     # AI 파일 관리
│   │   ├── workflow_ai/      # 워크플로 AI
│   │   └── analytics/        # AI 분석
│   └── main.py
├── frontend/
│   ├── src/
│   │   ├── core/
│   │   │   ├── components/    # 공통 컴포넌트
│   │   │   ├── layouts/       # 레이아웃
│   │   │   ├── ai/           # AI 컴포넌트
│   │   │   └── utils/        # 유틸리티
│   │   ├── modules/          # 모듈별 화면
│   │   └── views/            # 자동 생성 뷰
│   ├── package.json
│   └── vite.config.js
├── database/
│   └── schema/               # 데이터베이스 스키마
└── docs/
    └── api/                  # API 문서
```

## ERPNext 모듈 구현 계획

### Phase 1: Core System
1. DocType 시스템 구현
2. 권한 관리 시스템
3. API 자동 생성 시스템
4. 기본 UI 컴포넌트

### Phase 2: 핵심 모듈
1. **Accounts** (회계) - 복식부기, 계정과목, 결제관리
2. **Sales** (영업) - 고객관리, 견적서, 주문서
3. **Stock** (재고) - 창고관리, 재고이동, 평가
4. **Purchase** (구매) - 공급업체, 구매주문, 검수

### Phase 3: 확장 모듈
1. **HR** (인사) - 직원관리, 급여, 출근관리
2. **Manufacturing** (제조) - BOM, 작업지시, 생산계획
3. **Projects** (프로젝트) - 프로젝트관리, 작업추적
4. **CRM** (고객관리) - 리드관리, 기회관리

### Phase 4: 추가 모듈
1. **Support** (지원) - 이슈추적, 유지보수
2. **Assets** (자산관리) - 고정자산, 감가상각
3. **Quality** (품질관리) - 품질검사, 템플릿
4. **Website** (웹사이트) - 콘텐츠관리, 전자상거래

### Phase 5: AI 통합
1. **AI Copilot** - 좌측 사이드바 AI 어시스턴트
2. **File Manager AI** - 파일 불러오기/수정/설명
3. **Workflow Automation** - 자동화 워크플로
4. **Predictive Analytics** - 예측 분석

## 기술 스택

### Backend
- **FastAPI**: 고성능 API 프레임워크
- **SQLAlchemy**: ORM
- **Alembic**: 데이터베이스 마이그레이션
- **Celery**: 비동기 작업 처리
- **Redis**: 캐시 및 세션 저장

### Frontend  
- **Vue 3**: 프론트엔드 프레임워크
- **Pinia**: 상태 관리
- **Vue Router**: 라우팅
- **Tailwind CSS**: 스타일링
- **Frappe UI**: ERPNext 스타일 컴포넌트

### AI & ML
- **OpenAI API**: GPT-4 for text processing
- **Claude API**: Advanced reasoning
- **LangChain**: LLM orchestration
- **Vector Store**: 문서 임베딩 저장

### Database & Storage
- **PostgreSQL**: 메인 데이터베이스
- **AWS S3**: 파일 저장소
- **Redis**: 캐시 저장소

## 색상 및 디자인 가이드

### 색상 팔레트 (ERPNext 스타일)
```scss
:root {
  --primary: #4f46e5;      // 메인 파랑
  --secondary: #6b7280;    // 회색
  --success: #10b981;      // 성공 녹색
  --warning: #f59e0b;      // 경고 주황
  --error: #ef4444;        // 에러 빨강
  --bg-light: #f8fafc;     // 밝은 배경
  --bg-white: #ffffff;     // 흰 배경
  --text-dark: #1e293b;    // 진한 텍스트
  --text-light: #64748b;   // 밝은 텍스트
  --border: #e2e8f0;       // 보더색
}
```

### 디자인 원칙
1. **전문성**: 사무용 느낌의 깔끔한 디자인
2. **일관성**: ERPNext와 유사한 레이아웃
3. **접근성**: 명확한 대비와 가독성
4. **반응형**: 모바일 친화적 설계