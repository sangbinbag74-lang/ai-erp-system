"""
ERPNext AI System - Main Application
"""

import os
import sys
import logging
from pathlib import Path

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI 애플리케이션 생성
app = FastAPI(
    title="ERPNext AI System",
    version="1.0.0",
    description="AI 기반 차세대 ERP 시스템"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 개발용으로 모든 origin 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 환경변수에서 설정 읽기
DATABASE_URL = os.getenv("DATABASE_URL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

@app.get("/")
async def root():
    """루트 페이지"""
    return {
        "message": "ERPNext AI System - AI 기반 차세대 ERP",
        "status": "healthy",
        "version": "1.0.0",
        "environment": ENVIRONMENT
    }

@app.get("/health")
async def health_check():
    """헬스체크 엔드포인트"""
    return {"status": "healthy"}

@app.get("/api/health")
async def api_health():
    """API 헬스체크"""
    return {
        "status": "healthy",
        "message": "API is running successfully",
        "version": "1.0.0",
        "environment": ENVIRONMENT,
        "database_configured": bool(DATABASE_URL),
        "ai_keys_configured": {
            "openai": bool(OPENAI_API_KEY),
            "anthropic": bool(ANTHROPIC_API_KEY)
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
        "database_configured": bool(DATABASE_URL)
    }

@app.get("/api/doctypes")
async def list_doctypes():
    """사용 가능한 DocType 목록"""
    return {
        "doctypes": [
            {"name": "Customer", "module": "Accounts", "description": "고객 마스터"},
            {"name": "Supplier", "module": "Accounts", "description": "공급업체 마스터"},
            {"name": "Item", "module": "Stock", "description": "품목 마스터"},
            {"name": "Sales Order", "module": "Sales", "description": "판매 주문"},
            {"name": "Purchase Order", "module": "Purchase", "description": "구매 주문"},
            {"name": "Employee", "module": "HR", "description": "직원"},
            {"name": "Project", "module": "Projects", "description": "프로젝트"},
            {"name": "Lead", "module": "CRM", "description": "리드"}
        ]
    }

@app.get("/api/ai/status")
async def ai_status():
    """AI 기능 상태"""
    return {
        "enabled": bool(OPENAI_API_KEY or ANTHROPIC_API_KEY),
        "openai_configured": bool(OPENAI_API_KEY),
        "anthropic_configured": bool(ANTHROPIC_API_KEY)
    }

@app.post("/api/ai/chat")
async def ai_chat(request: dict):
    """AI 채팅 엔드포인트 (테스트용)"""
    message = request.get("message", "")
    
    if not message:
        raise HTTPException(status_code=400, detail="메시지가 필요합니다")
    
    if not (OPENAI_API_KEY or ANTHROPIC_API_KEY):
        raise HTTPException(
            status_code=503,
            detail="AI 기능이 비활성화되었습니다. API 키를 설정해주세요."
        )
    
    # 테스트 응답
    return {
        "response": f"AI 응답: '{message}'에 대한 답변입니다. (현재는 테스트 응답)",
        "status": "success",
        "model": "test-model"
    }

# 전역 예외 처리
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """전역 예외 처리"""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": "서버에서 오류가 발생했습니다.",
            "detail": str(exc) if ENVIRONMENT == "development" else "서버 오류"
        }
    )

# 시작 이벤트
@app.on_event("startup")
async def startup_event():
    """애플리케이션 시작 시 실행"""
    logger.info("🚀 ERPNext AI System 시작 중...")
    logger.info(f"환경: {ENVIRONMENT}")
    logger.info(f"데이터베이스 설정됨: {bool(DATABASE_URL)}")
    logger.info(f"AI 키 설정됨: OpenAI={bool(OPENAI_API_KEY)}, Anthropic={bool(ANTHROPIC_API_KEY)}")
    logger.info("✅ ERPNext AI System 준비 완료!")

# 개발 서버 실행
if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("PORT", 8000))
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=False,  # 프로덕션에서는 reload 비활성화
        log_level="info"
    )