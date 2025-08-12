"""
ERPNext AI System - Main Application (Railway Optimized)
"""

import os
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# FastAPI 애플리케이션 생성
app = FastAPI(
    title="ERPNext AI System",
    version="1.0.0",
    description="AI 기반 차세대 ERP 시스템"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 환경변수
ENVIRONMENT = os.getenv("ENVIRONMENT", "production")
PORT = int(os.getenv("PORT", 8000))

logger.info(f"🚀 Starting ERPNext AI System on port {PORT}")
logger.info(f"Environment: {ENVIRONMENT}")

@app.get("/")
async def root():
    """루트 페이지"""
    return {
        "message": "ERPNext AI System - AI 기반 차세대 ERP",
        "status": "healthy",
        "version": "1.0.0",
        "environment": ENVIRONMENT,
        "port": PORT
    }

@app.get("/health")
async def health_check():
    """헬스체크 엔드포인트"""
    return {"status": "healthy", "port": PORT}

@app.get("/api/health")
async def api_health():
    """API 헬스체크"""
    return {
        "status": "healthy",
        "message": "API is running successfully",
        "version": "1.0.0",
        "environment": ENVIRONMENT,
        "port": PORT
    }

@app.get("/api/test")
async def test_endpoint():
    """테스트 엔드포인트"""
    return {
        "message": "Test successful!",
        "working": True,
        "environment": ENVIRONMENT
    }

# 시작 로그
@app.on_event("startup")
async def startup_event():
    logger.info("✅ ERPNext AI System started successfully!")
    logger.info(f"Port: {PORT}")
    logger.info(f"Environment: {ENVIRONMENT}")

if __name__ == "__main__":
    import uvicorn
    
    # Railway에서 제공하는 PORT 환경변수 사용
    port = int(os.getenv("PORT", 8000))
    
    logger.info(f"🚀 Starting server on 0.0.0.0:{port}")
    
    uvicorn.run(
        app,  # 문자열 대신 앱 객체 직접 전달
        host="0.0.0.0",
        port=port,
        log_level="info"
    )