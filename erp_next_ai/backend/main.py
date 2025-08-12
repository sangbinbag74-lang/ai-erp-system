"""
최소한의 FastAPI 서버 (Railway 배포 테스트용)
"""
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# 간단한 FastAPI 앱
app = FastAPI(
    title="ERPNext AI System",
    version="1.0.0",
    description="AI 기반 ERP 시스템 (간단 버전)"
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
    """루트 페이지 - 헬스체크용"""
    return {
        "message": "ERPNext AI System 정상 작동 중!",
        "status": "healthy",
        "version": "1.0.0",
        "environment": os.getenv("ENVIRONMENT", "development")
    }

@app.get("/health")
async def health():
    """헬스체크 엔드포인트"""
    return {"status": "healthy"}

@app.get("/api/health")
async def api_health():
    """API 헬스체크"""
    return {
        "status": "healthy",
        "message": "API is running successfully!",
        "version": "1.0.0"
    }

@app.get("/test")
async def test():
    """테스트 엔드포인트"""
    return {"message": "테스트 성공!", "working": True}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)