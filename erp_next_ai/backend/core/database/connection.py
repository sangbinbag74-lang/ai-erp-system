"""
데이터베이스 연결 및 세션 관리
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from contextlib import contextmanager
from typing import Generator

# 환경 변수에서 데이터베이스 URL 가져오기
DATABASE_URL = os.getenv(
    'DATABASE_URL',
    'postgresql://postgres:password@localhost:5432/erpnext_ai'
)

# Railway PostgreSQL URL 형식 변환
if DATABASE_URL.startswith('postgresql://'):
    DATABASE_URL = DATABASE_URL.replace('postgresql://', 'postgresql+psycopg2://', 1)

# SQLAlchemy 엔진 생성
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
    echo=False  # 개발 시에는 True로 설정하여 SQL 쿼리 로깅
)

# 세션 메이커 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    """
    FastAPI 의존성 주입용 데이터베이스 세션 생성기
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@contextmanager
def get_db_session() -> Generator[Session, None, None]:
    """
    컨텍스트 매니저로 데이터베이스 세션 관리
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


class DatabaseManager:
    """데이터베이스 관리 클래스"""
    
    @staticmethod
    def create_tables():
        """모든 테이블 생성"""
        from core.doctype.base import Base
        Base.metadata.create_all(bind=engine)
    
    @staticmethod
    def drop_tables():
        """모든 테이블 삭제"""
        from core.doctype.base import Base
        Base.metadata.drop_all(bind=engine)
    
    @staticmethod
    def check_connection() -> bool:
        """데이터베이스 연결 확인"""
        try:
            with get_db_session() as db:
                db.execute('SELECT 1')
            return True
        except Exception as e:
            print(f"데이터베이스 연결 실패: {e}")
            return False
    
    @staticmethod
    def get_table_info() -> dict:
        """테이블 정보 조회"""
        with get_db_session() as db:
            result = db.execute("""
                SELECT 
                    schemaname, 
                    tablename, 
                    tableowner
                FROM pg_tables 
                WHERE schemaname = 'public'
                ORDER BY tablename;
            """)
            
            tables = []
            for row in result:
                tables.append({
                    'schema': row[0],
                    'name': row[1],
                    'owner': row[2]
                })
            
            return {'tables': tables, 'count': len(tables)}


# 초기화 함수
def init_database():
    """데이터베이스 초기화"""
    print("데이터베이스 연결 확인 중...")
    
    if not DatabaseManager.check_connection():
        raise ConnectionError("데이터베이스에 연결할 수 없습니다.")
    
    print("데이터베이스 연결 성공!")
    
    # 테이블 생성
    print("테이블 생성 중...")
    DatabaseManager.create_tables()
    print("데이터베이스 초기화 완료!")


if __name__ == "__main__":
    init_database()