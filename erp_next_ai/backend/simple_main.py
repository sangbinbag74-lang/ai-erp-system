"""
간단한 테스트용 FastAPI 서버
Railway 배포 문제 해결을 위한 최소한의 서버
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import os

# 간단한 FastAPI 앱
app = FastAPI(
    title="ERPNext AI System",
    version="1.0.0",
    description="AI 기반 ERP 시스템"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """루트 페이지"""
    return {
        "message": "ERPNext AI System이 정상적으로 작동중입니다!",
        "status": "healthy",
        "version": "1.0.0",
        "environment": os.getenv("ENVIRONMENT", "development")
    }

@app.get("/api/health")
async def health():
    """헬스체크"""
    return {
        "status": "healthy",
        "message": "API is running successfully!",
        "version": "1.0.0",
        "environment": os.getenv("ENVIRONMENT", "development"),
        "database": "not_configured",
        "redis": "not_configured"
    }

@app.get("/docs-info")
async def docs_info():
    """문서 정보"""
    return {
        "swagger_ui": "/docs",
        "redoc": "/redoc", 
        "openapi": "/openapi.json",
        "message": "API 문서를 확인하려면 /docs를 방문하세요"
    }

@app.get("/test")
async def test():
    """테스트 엔드포인트"""
    return {
        "message": "테스트 성공!",
        "status": "OK",
        "working": True
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)