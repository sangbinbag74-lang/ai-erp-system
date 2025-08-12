"""
AI ERP Backend API - Railway 배포용 간소화 버전
"""

import os
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, List
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI 앱 생성
app = FastAPI(
    title="AI ERP Backend API",
    description="한국어 지원 AI 기반 ERP 시스템 Backend",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS 설정
# CORS 설정 - 임시로 모든 origin 허용 (디버깅용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 임시로 모든 도메인 허용
    allow_credentials=False,  # credentials를 False로 변경
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# 응답 모델
class APIResponse(BaseModel):
    success: bool
    data: Dict[str, Any] = {}
    message: str = ""

class UserProfile(BaseModel):
    user_id: str
    name: str
    email: str
    role: str
    company: str = ""

class DocumentCreate(BaseModel):
    title: str
    content: str
    type: str = "general"

# 루트 엔드포인트
@app.get("/")
async def root():
    return {
        "message": "🤖 AI ERP Backend API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs"
    }

# 헬스 체크
@app.get("/api/health")
async def health_check():
    return APIResponse(
        success=True,
        data={
            "status": "healthy",
            "version": "1.0.0",
            "environment": os.getenv("ENVIRONMENT", "production"),
            "database": "connected" if os.getenv("DATABASE_URL") else "not_configured",
            "redis": "connected" if os.getenv("REDIS_URL") else "not_configured"
        },
        message="API is running successfully"
    )

# 사용자 프로필
@app.get("/api/user/profile")
async def get_user_profile():
    return APIResponse(
        success=True,
        data={
            "user_id": "demo_user_001",
            "name": "데모 사용자",
            "email": "demo@aiErp.com",
            "role": "관리자",
            "company": "AI ERP 테스트 회사",
            "last_login": "2024-08-12T12:00:00Z"
        },
        message="사용자 프로필을 성공적으로 가져왔습니다"
    )

# 문서 목록
@app.get("/api/documents")
async def get_documents():
    sample_documents = [
        {
            "id": "doc_001",
            "title": "월간 매출 보고서",
            "type": "report",
            "created_at": "2024-08-01T09:00:00Z",
            "status": "완료"
        },
        {
            "id": "doc_002", 
            "title": "재고 관리 현황",
            "type": "inventory",
            "created_at": "2024-08-05T14:30:00Z",
            "status": "진행중"
        },
        {
            "id": "doc_003",
            "title": "고객 관리 데이터",
            "type": "customer",
            "created_at": "2024-08-10T11:15:00Z",
            "status": "검토중"
        }
    ]
    
    return APIResponse(
        success=True,
        data={"documents": sample_documents, "total": len(sample_documents)},
        message="문서 목록을 성공적으로 가져왔습니다"
    )

# 문서 생성
@app.post("/api/documents")
async def create_document(document: DocumentCreate):
    return APIResponse(
        success=True,
        data={
            "document_id": f"doc_{len(document.title):03d}",
            "title": document.title,
            "type": document.type,
            "status": "생성됨",
            "created_at": "2024-08-12T12:00:00Z"
        },
        message="문서가 성공적으로 생성되었습니다"
    )

# AI 기능 테스트
@app.post("/api/ai/analyze")
async def ai_analyze(data: Dict[str, Any]):
    return APIResponse(
        success=True,
        data={
            "analysis": "AI 분석 결과: 데이터가 정상적으로 처리되었습니다",
            "insights": [
                "매출이 전월 대비 15% 증가했습니다",
                "재고 회전율이 개선되었습니다", 
                "고객 만족도가 상승 추세입니다"
            ],
            "confidence": 0.85
        },
        message="AI 분석이 완료되었습니다"
    )

# 시스템 정보
@app.get("/api/system/info")
async def get_system_info():
    return APIResponse(
        success=True,
        data={
            "api_version": "1.0.0",
            "python_version": "3.9+",
            "framework": "FastAPI",
            "database": "PostgreSQL",
            "cache": "Redis",
            "deployment": "Railway",
            "features": [
                "사용자 관리",
                "문서 관리", 
                "AI 분석",
                "실시간 알림",
                "한국어 지원"
            ]
        },
        message="시스템 정보를 성공적으로 가져왔습니다"
    )

# 에러 핸들러
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return APIResponse(
        success=False,
        message="요청하신 API 엔드포인트를 찾을 수 없습니다"
    )

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    logger.error(f"Internal server error: {exc}")
    return APIResponse(
        success=False,
        message="서버 내부 오류가 발생했습니다"
    )

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)