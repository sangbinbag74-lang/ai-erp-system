"""
ERPNext AI System - Main Application
AI 기반 차세대 ERP 시스템
"""

import os
import sys
import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from sqlalchemy import text

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# 설정 및 데이터베이스 임포트
from core.config import settings, get_allowed_origins, is_ai_enabled
from core.database import init_database, get_db, check_database_connection

# 로깅 설정
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL.upper()),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """애플리케이션 생명주기 관리"""
    # 시작 시 실행
    logger.info("🚀 ERPNext AI System 시작 중...")
    
    # 데이터베이스 초기화
    try:
        init_database()
        logger.info("✅ 데이터베이스 초기화 완료")
    except Exception as e:
        logger.error(f"❌ 데이터베이스 초기화 실패: {e}")
    
    # AI 설정 확인
    if is_ai_enabled():
        logger.info("🤖 AI 기능 활성화됨")
    else:
        logger.warning("⚠️ AI API 키가 설정되지 않음")
    
    logger.info("✅ ERPNext AI System 준비 완료!")
    
    yield
    
    # 종료 시 실행
    logger.info("🔄 ERPNext AI System 종료 중...")


# FastAPI 애플리케이션 생성
app = FastAPI(
    title="ERPNext AI System",
    version=settings.APP_VERSION,
    description="AI 기반 차세대 ERP 시스템 - ERPNext의 모든 기능과 AI 자율성을 결합",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan
)

# 미들웨어 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=get_allowed_origins(),
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# 보안 미들웨어
if settings.ENVIRONMENT == "production":
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["*.railway.app", "*.vercel.app", "localhost"]
    )


# 전역 예외 처리
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """전역 예외 처리"""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": "서버에서 오류가 발생했습니다.",
            "detail": str(exc) if settings.DEBUG else "서버 오류"
        }
    )


# 기본 라우트
@app.get("/")
async def root():
    """루트 페이지"""
    return {
        "message": "ERPNext AI System - AI 기반 차세대 ERP",
        "status": "healthy",
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
        "ai_enabled": is_ai_enabled(),
        "documentation": "/docs"
    }


@app.get("/health")
async def health_check():
    """헬스체크 엔드포인트"""
    return {"status": "healthy"}


@app.get("/api/health")
async def api_health():
    """API 헬스체크"""
    db_status = "connected" if check_database_connection() else "not_connected"
    
    return {
        "status": "healthy",
        "message": "API is running successfully",
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
        "database": db_status,
        "ai_enabled": is_ai_enabled(),
        "timestamp": "2024-01-01T00:00:00Z"
    }


@app.get("/api/system/info")
async def system_info():
    """시스템 정보"""
    return {
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
        "debug": settings.DEBUG,
        "ai_enabled": is_ai_enabled(),
        "database_configured": bool(settings.DATABASE_URL),
        "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    }


@app.get("/api/system/db-status")
async def database_status(db: Session = Depends(get_db)):
    """데이터베이스 상태 확인"""
    try:
        # 간단한 쿼리 실행
        result = db.execute(text("SELECT 1 as test"))
        test_value = result.fetchone()
        
        return {
            "status": "connected",
            "message": "Database connection successful",
            "test_query": test_value[0] if test_value else None
        }
    except Exception as e:
        logger.error(f"Database status check failed: {e}")
        raise HTTPException(
            status_code=503,
            detail=f"Database connection failed: {str(e)}"
        )


# DocType API 기본 엔드포인트들
@app.get("/api/doctypes")
async def list_doctypes():
    """사용 가능한 DocType 목록"""
    return {
        "doctypes": [
            # Accounts 모듈
            {"name": "Customer", "module": "Accounts", "description": "고객 마스터"},
            {"name": "Supplier", "module": "Accounts", "description": "공급업체 마스터"},
            {"name": "Account", "module": "Accounts", "description": "계정과목"},
            {"name": "Payment Entry", "module": "Accounts", "description": "결제 내역"},
            
            # Sales 모듈
            {"name": "Sales Order", "module": "Sales", "description": "판매 주문"},
            {"name": "Sales Invoice", "module": "Sales", "description": "판매 송장"},
            {"name": "Quotation", "module": "Sales", "description": "견적서"},
            
            # Purchase 모듈
            {"name": "Purchase Order", "module": "Purchase", "description": "구매 주문"},
            {"name": "Purchase Invoice", "module": "Purchase", "description": "구매 송장"},
            
            # Stock 모듈
            {"name": "Item", "module": "Stock", "description": "품목 마스터"},
            {"name": "Warehouse", "module": "Stock", "description": "창고"},
            {"name": "Stock Entry", "module": "Stock", "description": "재고 이동"},
            
            # HR 모듈
            {"name": "Employee", "module": "HR", "description": "직원"},
            {"name": "Salary Structure", "module": "HR", "description": "급여 구조"},
            
            # Projects 모듈
            {"name": "Project", "module": "Projects", "description": "프로젝트"},
            {"name": "Task", "module": "Projects", "description": "작업"},
            
            # CRM 모듈
            {"name": "Lead", "module": "CRM", "description": "리드"},
            {"name": "Opportunity", "module": "CRM", "description": "기회"},
            
            # Support 모듈
            {"name": "Issue", "module": "Support", "description": "이슈"},
            
            # Manufacturing 모듈
            {"name": "BOM", "module": "Manufacturing", "description": "자재명세서"},
            {"name": "Work Order", "module": "Manufacturing", "description": "작업지시서"},
            
            # Assets 모듈
            {"name": "Asset", "module": "Assets", "description": "자산"},
            
            # Quality 모듈
            {"name": "Quality Inspection", "module": "Quality", "description": "품질검사"},
            
            # Website 모듈
            {"name": "Blog Post", "module": "Website", "description": "블로그 포스트"}
        ]
    }


# AI 관련 엔드포인트들
@app.get("/api/ai/status")
async def ai_status():
    """AI 기능 상태"""
    return {
        "enabled": is_ai_enabled(),
        "openai_configured": bool(settings.OPENAI_API_KEY),
        "anthropic_configured": bool(settings.ANTHROPIC_API_KEY),
        "streaming_enabled": settings.AI_ENABLE_STREAMING,
        "model_temperature": settings.AI_MODEL_TEMPERATURE,
        "max_tokens": settings.AI_MAX_TOKENS
    }


if settings.OPENAI_API_KEY or settings.ANTHROPIC_API_KEY:
    # AI 기능이 활성화된 경우에만 AI 엔드포인트 추가
    
    @app.post("/api/ai/chat")
    async def ai_chat(request: dict):
        """AI 채팅 엔드포인트"""
        message = request.get("message", "")
        
        if not message:
            raise HTTPException(status_code=400, detail="메시지가 필요합니다")
        
        try:
            # 간단한 응답 (실제 AI 연동은 추후 구현)
            return {
                "response": f"AI 응답: {message}에 대한 답변입니다. (현재는 테스트 응답)",
                "status": "success",
                "model": "test-model",
                "timestamp": "2024-01-01T00:00:00Z"
            }
        except Exception as e:
            logger.error(f"AI chat error: {e}")
            raise HTTPException(status_code=500, detail="AI 처리 중 오류가 발생했습니다")

else:
    @app.post("/api/ai/chat")
    async def ai_chat_disabled(request: dict):
        """AI 기능이 비활성화된 경우"""
        raise HTTPException(
            status_code=503,
            detail="AI 기능이 비활성화되었습니다. API 키를 설정해주세요."
        )


# 개발 서버 실행
if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("PORT", settings.PORT))
    
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=port,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )