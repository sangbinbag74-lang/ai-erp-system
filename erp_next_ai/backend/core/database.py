"""
ERPNext AI System - 데이터베이스 기본 설정
"""

from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from core.config import get_database_url

# SQLAlchemy Base 클래스
Base = declarative_base()

# 메타데이터
metadata = MetaData()

# 데이터베이스 엔진 (lazy initialization)
engine = None
SessionLocal = None


def init_database():
    """데이터베이스 초기화"""
    global engine, SessionLocal
    
    database_url = get_database_url()
    
    engine = create_engine(
        database_url,
        echo=False,  # SQL 쿼리 로깅
        pool_size=10,
        max_overflow=20,
        pool_recycle=3600,
        pool_pre_ping=True
    )
    
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    # 테이블 생성 (개발용)
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created/verified")
    except Exception as e:
        print(f"⚠️ Database table creation warning: {e}")


def get_db():
    """데이터베이스 세션 생성"""
    if SessionLocal is None:
        init_database()
    
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def check_database_connection() -> bool:
    """데이터베이스 연결 확인"""
    try:
        if engine is None:
            init_database()
        
        with engine.connect() as connection:
            connection.execute("SELECT 1")
        return True
    except Exception as e:
        print(f"Database connection failed: {e}")
        return False