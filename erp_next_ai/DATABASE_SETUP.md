# 데이터베이스 설정 가이드 🗄️

ERPNext AI System의 데이터베이스 설정 및 마이그레이션 가이드입니다.

## 📋 필수 요구사항

### PostgreSQL 설치
- **최소 버전**: PostgreSQL 14+
- **권장 버전**: PostgreSQL 15+
- **확장 모듈**: UUID, JSONB 지원

### 로컬 환경 설치

#### Windows (PostgreSQL + pgAdmin)
```bash
# Chocolatey를 통한 설치
choco install postgresql

# 또는 공식 인스톨러 다운로드
# https://www.postgresql.org/download/windows/
```

#### macOS (Homebrew)
```bash
brew install postgresql@15
brew services start postgresql@15
```

#### Ubuntu/Debian
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

## 🔧 데이터베이스 초기 설정

### 1. 데이터베이스 생성
```sql
-- PostgreSQL에 접속 (postgres 사용자로)
sudo -u postgres psql

-- 데이터베이스 생성
CREATE DATABASE erpnext_ai;

-- 전용 사용자 생성
CREATE USER erpnext_user WITH ENCRYPTED PASSWORD 'secure_password_here';

-- 권한 부여
GRANT ALL PRIVILEGES ON DATABASE erpnext_ai TO erpnext_user;

-- 확장 기능 활성화
\c erpnext_ai;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_stat_statements";

-- 사용자에게 스키마 권한 부여
GRANT ALL ON SCHEMA public TO erpnext_user;
```

### 2. 환경변수 설정
```bash
# .env 파일에 추가
DATABASE_URL=postgresql://erpnext_user:secure_password_here@localhost:5432/erpnext_ai
```

## 🚀 마이그레이션 실행

### 개발 환경에서 마이그레이션

#### 1. 가상환경 활성화
```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

#### 2. 의존성 설치
```bash
pip install -r requirements.txt
```

#### 3. 초기 마이그레이션 생성
```bash
# 첫 번째 마이그레이션 생성
alembic revision --autogenerate -m "Initial migration: Create all ERPNext tables"
```

#### 4. 마이그레이션 적용
```bash
# 최신 버전으로 업그레이드
alembic upgrade head
```

### 프로덕션 환경에서 마이그레이션

#### Railway (자동 배포)
Railway는 배포 시 자동으로 마이그레이션을 실행합니다.

```toml
# railway.toml에 설정된 빌드 명령
[[services.backend]]
name = "backend"
build_command = "pip install -r requirements.txt"
start_command = "alembic upgrade head && python main.py"
```

#### 수동 마이그레이션 (필요시)
```bash
# Railway CLI 설치
curl -fsSL https://railway.app/install.sh | sh

# 프로젝트 연결
railway link

# 마이그레이션 실행
railway run alembic upgrade head
```

## 📊 데이터베이스 스키마

### 핵심 테이블 구조

#### 1. DocType 기본 테이블
```sql
-- 모든 DocType의 공통 필드
CREATE TABLE base_doctype (
    name VARCHAR(140) PRIMARY KEY,
    creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified_by VARCHAR(140),
    owner VARCHAR(140),
    docstatus INTEGER DEFAULT 0,  -- 0=Draft, 1=Submitted, 2=Cancelled
    idx INTEGER DEFAULT 0
);
```

#### 2. Accounts 모듈
```sql
-- 고객 관리
CREATE TABLE "tabCustomer" (
    name VARCHAR(140) PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL,
    customer_type VARCHAR(20) DEFAULT 'Individual',
    territory VARCHAR(100),
    customer_group VARCHAR(100),
    -- ... 기타 필드들
);

-- 공급업체 관리
CREATE TABLE "tabSupplier" (
    name VARCHAR(140) PRIMARY KEY,
    supplier_name VARCHAR(100) NOT NULL,
    supplier_type VARCHAR(20),
    country VARCHAR(50),
    -- ... 기타 필드들
);

-- 계정과목
CREATE TABLE "tabAccount" (
    name VARCHAR(140) PRIMARY KEY,
    account_name VARCHAR(100) NOT NULL,
    parent_account VARCHAR(140),
    account_type VARCHAR(50),
    root_type VARCHAR(20),
    -- ... 기타 필드들
);
```

#### 3. Sales 모듈
```sql
-- 판매 주문
CREATE TABLE "tabSales Order" (
    name VARCHAR(140) PRIMARY KEY,
    customer VARCHAR(140) NOT NULL,
    transaction_date DATE,
    delivery_date DATE,
    total_amount DECIMAL(18,6),
    -- ... 기타 필드들
);

-- 판매 송장
CREATE TABLE "tabSales Invoice" (
    name VARCHAR(140) PRIMARY KEY,
    customer VARCHAR(140) NOT NULL,
    posting_date DATE,
    due_date DATE,
    grand_total DECIMAL(18,6),
    outstanding_amount DECIMAL(18,6),
    -- ... 기타 필드들
);
```

#### 4. Stock 모듈
```sql
-- 품목 마스터
CREATE TABLE "tabItem" (
    name VARCHAR(140) PRIMARY KEY,
    item_name VARCHAR(100) NOT NULL,
    item_group VARCHAR(100),
    stock_uom VARCHAR(50),
    maintain_stock BOOLEAN DEFAULT TRUE,
    -- ... 기타 필드들
);

-- 창고 관리
CREATE TABLE "tabWarehouse" (
    name VARCHAR(140) PRIMARY KEY,
    warehouse_name VARCHAR(100) NOT NULL,
    parent_warehouse VARCHAR(140),
    company VARCHAR(100),
    -- ... 기타 필드들
);
```

## 🔄 마이그레이션 관리

### 새 마이그레이션 생성
```bash
# 모델 변경 후 마이그레이션 생성
alembic revision --autogenerate -m "Add new field to Customer table"
```

### 마이그레이션 히스토리 확인
```bash
# 현재 버전 확인
alembic current

# 마이그레이션 히스토리 확인
alembic history --verbose

# 특정 버전으로 다운그레이드
alembic downgrade -1  # 한 버전 뒤로
alembic downgrade base  # 초기 상태로
```

### 마이그레이션 검증
```bash
# 마이그레이션 SQL 미리보기 (실행하지 않음)
alembic upgrade head --sql

# 특정 버전까지의 SQL 생성
alembic upgrade ae1027a6acf --sql
```

## 🛠️ 데이터베이스 백업 및 복원

### 백업 생성
```bash
# 전체 데이터베이스 백업
pg_dump -U erpnext_user -h localhost -d erpnext_ai > backup_$(date +%Y%m%d_%H%M%S).sql

# 스키마만 백업
pg_dump -U erpnext_user -h localhost -d erpnext_ai --schema-only > schema_backup.sql

# 데이터만 백업
pg_dump -U erpnext_user -h localhost -d erpnext_ai --data-only > data_backup.sql
```

### 복원
```bash
# 전체 복원
psql -U erpnext_user -h localhost -d erpnext_ai < backup_20240101_120000.sql

# 특정 테이블만 복원
pg_restore -U erpnext_user -h localhost -d erpnext_ai -t "tabCustomer" backup.dump
```

## 📈 성능 최적화

### 인덱스 생성
```sql
-- 자주 조회되는 필드에 인덱스 생성
CREATE INDEX idx_customer_name ON "tabCustomer" (customer_name);
CREATE INDEX idx_sales_order_customer ON "tabSales Order" (customer);
CREATE INDEX idx_item_group ON "tabItem" (item_group);

-- 복합 인덱스
CREATE INDEX idx_sales_invoice_date_customer ON "tabSales Invoice" (posting_date, customer);

-- 부분 인덱스 (조건부 인덱스)
CREATE INDEX idx_active_items ON "tabItem" (item_name) WHERE disabled = FALSE;
```

### 파티셔닝 (대용량 데이터용)
```sql
-- 날짜 기준 파티셔닝 예시
CREATE TABLE "tabStock Ledger Entry" (
    name VARCHAR(140),
    posting_date DATE,
    item_code VARCHAR(140),
    warehouse VARCHAR(140),
    -- ... 기타 필드들
) PARTITION BY RANGE (posting_date);

-- 월별 파티션 생성
CREATE TABLE "tabStock Ledger Entry_2024_01" PARTITION OF "tabStock Ledger Entry"
    FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');
```

## 🔍 데이터베이스 모니터링

### 성능 모니터링 쿼리
```sql
-- 느린 쿼리 확인
SELECT query, mean_time, calls, total_time
FROM pg_stat_statements
ORDER BY mean_time DESC
LIMIT 10;

-- 테이블별 통계
SELECT schemaname, tablename, n_tup_ins, n_tup_upd, n_tup_del
FROM pg_stat_user_tables
ORDER BY n_tup_ins DESC;

-- 인덱스 사용률
SELECT schemaname, tablename, indexname, idx_scan, idx_tup_read
FROM pg_stat_user_indexes
ORDER BY idx_scan DESC;
```

### 연결 및 잠금 모니터링
```sql
-- 현재 연결 수 확인
SELECT count(*) FROM pg_stat_activity;

-- 활성 쿼리 확인
SELECT pid, now() - pg_stat_activity.query_start AS duration, query
FROM pg_stat_activity
WHERE (now() - pg_stat_activity.query_start) > interval '5 minutes';

-- 잠금 상태 확인
SELECT blocked_locks.pid AS blocked_pid,
       blocking_locks.pid AS blocking_pid,
       blocked_activity.query AS blocked_statement
FROM pg_catalog.pg_locks blocked_locks
JOIN pg_catalog.pg_stat_activity blocked_activity ON blocked_activity.pid = blocked_locks.pid
JOIN pg_catalog.pg_locks blocking_locks ON blocking_locks.locktype = blocked_locks.locktype;
```

## 🔧 문제 해결

### 일반적인 문제들

#### 1. 연결 오류
```bash
# PostgreSQL 서비스 상태 확인
sudo systemctl status postgresql

# 포트 확인
sudo netstat -tlnp | grep 5432

# 설정 파일 확인
sudo nano /etc/postgresql/15/main/postgresql.conf
```

#### 2. 권한 오류
```sql
-- 사용자 권한 확인
\du

-- 데이터베이스 권한 확인
\l

-- 테이블 권한 부여
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO erpnext_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO erpnext_user;
```

#### 3. 마이그레이션 충돌
```bash
# 마이그레이션 충돌 해결
alembic merge heads -m "Merge conflicting migrations"

# 강제로 특정 버전으로 표시 (주의!)
alembic stamp head
```

#### 4. 데이터 무결성 오류
```sql
-- 외래 키 제약 조건 확인
SELECT conname, conrelid::regclass, confrelid::regclass
FROM pg_constraint
WHERE contype = 'f';

-- 제약 조건 임시 비활성화 (복구 시에만 사용)
SET foreign_key_checks = 0;
-- ... 데이터 복구 작업 ...
SET foreign_key_checks = 1;
```

## 🔐 보안 설정

### 데이터베이스 보안
```sql
-- 불필요한 권한 제거
REVOKE ALL ON SCHEMA information_schema FROM PUBLIC;
REVOKE ALL ON SCHEMA pg_catalog FROM PUBLIC;

-- 로그인 시도 제한
ALTER SYSTEM SET log_connections = 'on';
ALTER SYSTEM SET log_disconnections = 'on';
ALTER SYSTEM SET log_checkpoints = 'on';

-- SSL 연결 강제
ALTER SYSTEM SET ssl = 'on';
```

### 백업 암호화
```bash
# 암호화된 백업 생성
pg_dump -U erpnext_user -h localhost erpnext_ai | gpg --cipher-algo AES256 --compress-algo 1 --symmetric --output backup.sql.gpg

# 암호화된 백업 복원
gpg --decrypt backup.sql.gpg | psql -U erpnext_user -h localhost -d erpnext_ai
```

## 📞 지원

문제가 발생하는 경우:
1. 로그 파일 확인: `/var/log/postgresql/`
2. 설정 파일 검토: `/etc/postgresql/15/main/`
3. [GitHub Issues](https://github.com/your-repo/issues)에 문제 보고
4. PostgreSQL 공식 문서 참조

---

⚠️ **주의**: 프로덕션 환경에서는 반드시 백업을 먼저 생성한 후 마이그레이션을 실행하세요!