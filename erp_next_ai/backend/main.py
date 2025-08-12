"""
ERPNext AI System - Main Application
AI 기반 차세대 ERP 시스템 (완전한 버전 복구)
"""

import os
import sys
import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# 환경변수에서 설정 읽기 (안전한 방식)
DATABASE_URL = os.getenv("DATABASE_URL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") 
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
ENVIRONMENT = os.getenv("ENVIRONMENT", "production")
PORT = int(os.getenv("PORT", 8000))

logger.info(f"🚀 ERPNext AI System 시작 중...")
logger.info(f"환경: {ENVIRONMENT}")
logger.info(f"포트: {PORT}")
logger.info(f"데이터베이스 URL 설정됨: {bool(DATABASE_URL)}")
logger.info(f"AI 키 설정 상태 - OpenAI: {bool(OPENAI_API_KEY)}, Anthropic: {bool(ANTHROPIC_API_KEY)}")

@asynccontextmanager
async def lifespan(app: FastAPI):
    """애플리케이션 생명주기 관리"""
    # 시작 시 실행
    logger.info("✅ ERPNext AI System 시작 완료!")
    
    # 데이터베이스 연결은 선택적으로 처리
    if DATABASE_URL:
        try:
            # 데이터베이스 초기화는 여기서 처리 (실패해도 계속 진행)
            logger.info("데이터베이스 연결 시도 중...")
            # 실제 연결 로직은 나중에 추가
        except Exception as e:
            logger.warning(f"데이터베이스 연결 실패 (계속 진행): {e}")
    else:
        logger.warning("데이터베이스 URL이 설정되지 않음")
    
    yield
    
    # 종료 시 실행
    logger.info("🔄 ERPNext AI System 종료 중...")


# FastAPI 애플리케이션 생성
app = FastAPI(
    title="ERPNext AI System",
    version="1.0.0",
    description="AI 기반 차세대 ERP 시스템 - ERPNext의 모든 기능과 AI 자율성을 결합",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan
)

# CORS 설정
allowed_origins = [
    "https://ai-erp-system-f1c4bb20b-park-sangbins-projects.vercel.app",
    "https://*.vercel.app",
    "http://localhost:3000",
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
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
            "detail": str(exc) if ENVIRONMENT == "development" else "서버 오류"
        }
    )

# 기본 라우트
@app.get("/")
async def root():
    """루트 페이지"""
    return {
        "message": "ERPNext AI System - AI 기반 차세대 ERP",
        "status": "healthy",
        "version": "1.0.0",
        "environment": ENVIRONMENT,
        "port": PORT,
        "features": {
            "ai_enabled": bool(OPENAI_API_KEY or ANTHROPIC_API_KEY),
            "database_connected": bool(DATABASE_URL),
            "modules_available": [
                "Accounts", "Sales", "Purchase", "Stock", 
                "HR", "Projects", "CRM", "Support"
            ]
        }
    }

@app.get("/health")
async def health_check():
    """헬스체크 엔드포인트"""
    return {
        "status": "healthy",
        "timestamp": "2024-01-01T00:00:00Z",
        "port": PORT
    }

@app.get("/api/health")
async def api_health():
    """상세 API 헬스체크"""
    return {
        "status": "healthy",
        "message": "ERPNext AI System API is running successfully",
        "version": "1.0.0",
        "environment": ENVIRONMENT,
        "port": PORT,
        "database": {
            "configured": bool(DATABASE_URL),
            "status": "available" if DATABASE_URL else "not_configured"
        },
        "ai_services": {
            "openai": {
                "configured": bool(OPENAI_API_KEY),
                "status": "available" if OPENAI_API_KEY else "not_configured"
            },
            "anthropic": {
                "configured": bool(ANTHROPIC_API_KEY),
                "status": "available" if ANTHROPIC_API_KEY else "not_configured"
            }
        },
        "features": {
            "doctype_system": True,
            "ai_copilot": bool(OPENAI_API_KEY or ANTHROPIC_API_KEY),
            "real_time_sync": bool(DATABASE_URL)
        }
    }

@app.get("/api/system/info")
async def system_info():
    """시스템 정보"""
    return {
        "app_name": "ERPNext AI System",
        "version": "1.0.0",
        "environment": ENVIRONMENT,
        "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        "runtime_info": {
            "port": PORT,
            "database_url_configured": bool(DATABASE_URL),
            "ai_keys_configured": bool(OPENAI_API_KEY or ANTHROPIC_API_KEY)
        }
    }

@app.get("/api/system/db-status")
async def database_status():
    """데이터베이스 상태 확인"""
    if not DATABASE_URL:
        return {
            "status": "not_configured",
            "message": "Database URL not configured",
            "database_url": None
        }
    
    try:
        # 실제 데이터베이스 연결 테스트는 여기서
        return {
            "status": "configured",
            "message": "Database URL is configured",
            "note": "Connection testing requires database imports"
        }
    except Exception as e:
        logger.error(f"Database status check failed: {e}")
        return {
            "status": "error",
            "message": f"Database connection failed: {str(e)}"
        }

# DocType API 엔드포인트들
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
            {"name": "Issue", "module": "Support", "description": "이슈"}
        ]
    }

# AI 관련 엔드포인트들
@app.get("/api/ai/status")
async def ai_status():
    """AI 기능 상태"""
    return {
        "enabled": bool(OPENAI_API_KEY or ANTHROPIC_API_KEY),
        "services": {
            "openai": {
                "configured": bool(OPENAI_API_KEY),
                "available": bool(OPENAI_API_KEY)
            },
            "anthropic": {
                "configured": bool(ANTHROPIC_API_KEY), 
                "available": bool(ANTHROPIC_API_KEY)
            }
        },
        "features": {
            "chat": bool(OPENAI_API_KEY or ANTHROPIC_API_KEY),
            "file_analysis": bool(OPENAI_API_KEY),
            "workflow_automation": bool(ANTHROPIC_API_KEY)
        }
    }

@app.post("/api/ai/chat")
async def ai_chat(request: dict):
    """AI 채팅 엔드포인트"""
    message = request.get("message", "")
    
    if not message:
        raise HTTPException(status_code=400, detail="메시지가 필요합니다")
    
    if not (OPENAI_API_KEY or ANTHROPIC_API_KEY):
        raise HTTPException(
            status_code=503,
            detail="AI 기능이 비활성화되었습니다. API 키를 설정해주세요."
        )
    
    try:
        # 현재는 테스트 응답, 나중에 실제 AI 연동
        return {
            "response": f"AI 응답: '{message}'에 대한 ERPNext AI의 답변입니다. 현재는 테스트 모드로 작동 중입니다.",
            "status": "success",
            "model": "erpnext-ai-test",
            "timestamp": "2024-01-01T00:00:00Z",
            "context": {
                "user_message": message,
                "ai_service": "available" if (OPENAI_API_KEY or ANTHROPIC_API_KEY) else "unavailable"
            }
        }
    except Exception as e:
        logger.error(f"AI chat error: {e}")
        raise HTTPException(status_code=500, detail="AI 처리 중 오류가 발생했습니다")

# Railway 실행을 위한 메인 부분
if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("PORT", 8000))
    
    logger.info(f"🚀 Starting ERPNext AI System on 0.0.0.0:{port}")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        log_level="info"
    )