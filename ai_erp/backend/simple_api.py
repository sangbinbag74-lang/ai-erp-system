"""
ERPNext 의존성 없는 간단한 FastAPI 버전
Vercel Serverless Functions 호환
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from typing import Dict, Any

app = FastAPI(title="AI ERP API", version="1.0.0")

# 기본 응답 모델
class APIResponse(BaseModel):
    success: bool
    data: Dict[str, Any] = {}
    message: str = ""

@app.get("/")
async def root():
    return {"message": "AI ERP API is running"}

@app.get("/api/health")
async def health_check():
    return APIResponse(
        success=True,
        data={"status": "healthy", "version": "1.0.0"},
        message="API is running successfully"
    )

@app.get("/api/user/profile")
async def get_user_profile():
    # 임시 사용자 데이터
    return APIResponse(
        success=True,
        data={
            "user_id": "demo_user",
            "name": "Demo User",
            "email": "demo@example.com",
            "role": "Admin"
        }
    )

@app.post("/api/documents")
async def create_document(document: Dict[str, Any]):
    # 문서 생성 로직 (간소화됨)
    return APIResponse(
        success=True,
        data={"document_id": "doc_001", "created": True},
        message="Document created successfully"
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)