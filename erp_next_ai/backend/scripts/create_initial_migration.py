"""
스크립트: 초기 데이터베이스 마이그레이션 생성
ERPNext AI System의 모든 테이블을 생성하는 초기 마이그레이션을 생성합니다.
"""

import os
import sys
from pathlib import Path

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from alembic.config import Config
from alembic import command
from core.config import settings


def create_initial_migration():
    """초기 마이그레이션 생성"""
    print("🚀 ERPNext AI System - 초기 마이그레이션 생성 중...")
    
    # Alembic 설정 파일 경로
    alembic_cfg_path = project_root / "alembic.ini"
    
    if not alembic_cfg_path.exists():
        print(f"❌ Alembic 설정 파일을 찾을 수 없습니다: {alembic_cfg_path}")
        sys.exit(1)
    
    # Alembic Config 객체 생성
    alembic_cfg = Config(str(alembic_cfg_path))
    
    # 데이터베이스 URL 설정
    alembic_cfg.set_main_option('sqlalchemy.url', settings.DATABASE_URL)
    
    try:
        # 초기 마이그레이션 생성
        print("📝 마이그레이션 파일 생성 중...")
        command.revision(
            alembic_cfg,
            message="Initial migration: Create all ERPNext tables",
            autogenerate=True
        )
        print("✅ 초기 마이그레이션이 성공적으로 생성되었습니다!")
        
        # 마이그레이션 적용
        print("🔄 데이터베이스에 마이그레이션 적용 중...")
        command.upgrade(alembic_cfg, "head")
        print("✅ 마이그레이션이 성공적으로 적용되었습니다!")
        
        # 현재 마이그레이션 상태 확인
        print("📊 현재 마이그레이션 상태:")
        command.current(alembic_cfg)
        
    except Exception as e:
        print(f"❌ 마이그레이션 생성 중 오류가 발생했습니다: {e}")
        sys.exit(1)


def check_database_connection():
    """데이터베이스 연결 확인"""
    print("🔍 데이터베이스 연결 확인 중...")
    
    try:
        from sqlalchemy import create_engine, text
        
        engine = create_engine(settings.DATABASE_URL)
        
        with engine.connect() as connection:
            result = connection.execute(text("SELECT version()"))
            version = result.fetchone()[0]
            print(f"✅ 데이터베이스 연결 성공: {version}")
            
        engine.dispose()
        
    except Exception as e:
        print(f"❌ 데이터베이스 연결 실패: {e}")
        print("💡 다음을 확인해주세요:")
        print("   1. PostgreSQL 서버가 실행 중인지 확인")
        print("   2. DATABASE_URL 환경변수가 올바른지 확인")
        print("   3. 데이터베이스와 사용자 권한이 올바른지 확인")
        sys.exit(1)


def verify_models():
    """모델들이 올바르게 임포트되는지 확인"""
    print("🔍 모델 임포트 확인 중...")
    
    try:
        # 모든 모델 임포트
        from modules.accounts.customer import Customer
        from modules.accounts.supplier import Supplier
        from modules.accounts.account import Account
        from modules.accounts.payment_entry import PaymentEntry
        from modules.sales.sales_order import SalesOrder
        from modules.sales.sales_invoice import SalesInvoice
        from modules.sales.quotation import Quotation
        from modules.purchase.purchase_order import PurchaseOrder
        from modules.purchase.purchase_invoice import PurchaseInvoice
        from modules.stock.item import Item
        from modules.stock.warehouse import Warehouse
        from modules.stock.stock_entry import StockEntry
        from modules.hr.employee import Employee
        from modules.hr.salary_structure import SalaryStructure
        from modules.projects.project import Project
        from modules.projects.task import Task
        from modules.crm.lead import Lead
        from modules.crm.opportunity import Opportunity
        from modules.support.issue import Issue
        from modules.manufacturing.bom import BOM
        from modules.manufacturing.work_order import WorkOrder
        from modules.assets.asset import Asset
        from modules.quality.quality_inspection import QualityInspection
        from modules.website.blog_post import BlogPost
        
        print("✅ 모든 모델이 성공적으로 임포트되었습니다!")
        
        # 메타데이터 확인
        from core.database import Base
        tables = list(Base.metadata.tables.keys())
        print(f"📊 총 {len(tables)}개의 테이블이 등록되었습니다:")
        for table in sorted(tables):
            print(f"   - {table}")
            
    except Exception as e:
        print(f"❌ 모델 임포트 중 오류가 발생했습니다: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


def main():
    """메인 함수"""
    print("=" * 60)
    print("🤖 ERPNext AI System - 데이터베이스 초기화")
    print("=" * 60)
    
    # 환경변수 확인
    if not settings.DATABASE_URL:
        print("❌ DATABASE_URL 환경변수가 설정되지 않았습니다.")
        print("💡 .env 파일을 확인하거나 환경변수를 설정해주세요.")
        sys.exit(1)
    
    print(f"🗄️ 데이터베이스 URL: {settings.DATABASE_URL[:50]}...")
    
    # 단계별 실행
    verify_models()
    check_database_connection()
    create_initial_migration()
    
    print("=" * 60)
    print("🎉 데이터베이스 초기화가 완료되었습니다!")
    print("=" * 60)
    print()
    print("다음 단계:")
    print("1. 백엔드 서버 실행: python main.py")
    print("2. 프론트엔드 서버 실행: cd frontend && npm run dev")
    print("3. 브라우저에서 http://localhost:3000 접속")
    print()


if __name__ == "__main__":
    main()