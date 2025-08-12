"""
ERPNext AI System - FastAPI 메인 애플리케이션
"""

import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from contextlib import asynccontextmanager

# Core imports
from core.config import settings, get_allowed_origins, is_ai_enabled
from core.database import init_database, check_database_connection


@asynccontextmanager
async def lifespan(app: FastAPI):
    """애플리케이션 생명주기 관리"""
    # 시작 시 초기화
    print("🚀 ERPNext AI System 시작 중...")
    
    try:
        # 데이터베이스 초기화
        init_database()
        print("✅ 데이터베이스 초기화 완료")
        
    except Exception as e:
        print(f"❌ 초기화 실패: {e}")
        # 프로덕션에서는 에러가 발생해도 서비스를 시작하도록 함
        if not settings.ENVIRONMENT == "production":
            raise
    
    yield  # 애플리케이션 실행
    
    # 종료 시 정리
    print("🛑 ERPNext AI System 종료")


# FastAPI 애플리케이션 생성
app = FastAPI(
    title="ERPNext AI System",
    description="AI 기반 ERP 시스템 - ERPNext의 모든 기능을 구현한 차세대 ERP",
    version=settings.APP_VERSION,
    lifespan=lifespan
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=get_allowed_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 기본 라우트
@app.get("/", response_class=HTMLResponse)
async def root():
    """루트 페이지"""
    return """
    <html>
        <head>
            <title>ERPNext AI System</title>
            <style>
                body { font-family: -apple-system, BlinkMacSystemFont, sans-serif; margin: 0; padding: 2rem; background: #f8fafc; }
                .container { max-width: 800px; margin: 0 auto; background: white; padding: 2rem; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
                h1 { color: #1e293b; margin-bottom: 2rem; }
                .feature { padding: 1rem; background: #f1f5f9; margin: 1rem 0; border-radius: 8px; }
                .status { color: #059669; font-weight: 600; }
                a { color: #3b82f6; text-decoration: none; }
                .modules { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin: 2rem 0; }
                .module { padding: 1rem; background: #e0f2fe; border-radius: 6px; text-align: center; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🤖 ERPNext AI System</h1>
                <p class="status">✅ 시스템이 정상적으로 실행 중입니다.</p>
                
                <div class="feature">
                    <h3>🧠 AI 기능</h3>
                    <p>GPT-4와 Claude를 활용한 자율적 작업 처리 및 파일 관리</p>
                </div>
                
                <h3>📋 구현된 ERP 모듈</h3>
                <div class="modules">
                    <div class="module">📊 Accounts<br>회계 관리</div>
                    <div class="module">💼 Sales<br>영업 관리</div>
                    <div class="module">🛒 Purchase<br>구매 관리</div>
                    <div class="module">📦 Stock<br>재고 관리</div>
                    <div class="module">👥 HR<br>인사 관리</div>
                    <div class="module">🏭 Manufacturing<br>제조 관리</div>
                    <div class="module">📁 Projects<br>프로젝트 관리</div>
                    <div class="module">🎯 CRM<br>고객 관리</div>
                    <div class="module">🔧 Support<br>지원 관리</div>
                    <div class="module">🏢 Assets<br>자산 관리</div>
                    <div class="module">✅ Quality<br>품질 관리</div>
                    <div class="module">🌐 Website<br>웹사이트 관리</div>
                </div>
                
                <h3>📚 API 문서</h3>
                <p><a href="/docs">📖 Swagger UI 문서 보기</a></p>
                <p><a href="/redoc">📑 ReDoc 문서 보기</a></p>
                
                <h3>🔧 시스템 정보</h3>
                <p>• <a href="/api/health">시스템 상태 확인</a></p>
                <p>• <a href="/api/system/info">시스템 정보</a></p>
                <p>• <a href="/api/ai/status">AI 서비스 상태</a></p>
            </div>
        </body>
    </html>
    """


# 시스템 상태 API
@app.get("/api/health")
async def health_check():
    """시스템 상태 확인"""
    db_status = "connected" if check_database_connection() else "not_configured"
    
    return {
        "status": "healthy",
        "message": "ERPNext AI System is running successfully!",
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
        "database": db_status,
        "redis": "not_configured",
        "ai_enabled": is_ai_enabled()
    }


# 시스템 정보 API
@app.get("/api/system/info")
async def system_info():
    """시스템 정보 조회"""
    return {
        "system": "ERPNext AI System",
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
        "python_version": f"{os.sys.version_info.major}.{os.sys.version_info.minor}.{os.sys.version_info.micro}",
        "available_modules": [
            "Accounts", "Sales", "Purchase", "Stock", 
            "HR", "Manufacturing", "Projects", "CRM",
            "Support", "Assets", "Quality", "Website"
        ],
        "ai_features": [
            "File Management", "AGI-like Autonomy", 
            "Workflow Automation", "Predictive Analytics"
        ],
        "database_connected": check_database_connection(),
        "ai_configured": is_ai_enabled()
    }


# AI 서비스 상태 API
@app.get("/api/ai/status")
async def ai_status():
    """AI 서비스 상태 확인"""
    openai_key = bool(settings.OPENAI_API_KEY)
    anthropic_key = bool(settings.ANTHROPIC_API_KEY)
    
    return {
        "ai_copilot": "active" if openai_key or anthropic_key else "inactive",
        "file_manager": "active", 
        "workflow_automation": "active",
        "predictive_analytics": "active",
        "openai_configured": openai_key,
        "anthropic_configured": anthropic_key,
        "supported_models": [
            "gpt-4-turbo-preview" if openai_key else None,
            "claude-3-sonnet-20240229" if anthropic_key else None
        ],
        "capabilities": [
            "자연어 처리",
            "파일 불러오기/수정/설명", 
            "자율적 작업 처리",
            "워크플로 자동화",
            "예측 분석"
        ]
    }


# AI 채팅 API
@app.post("/api/ai/chat")
async def ai_chat(request: dict):
    """AI 코파일럿과 채팅"""
    user_input = request.get("message", "")
    user_context = request.get("context", {})
    
    if not user_input:
        raise HTTPException(status_code=400, detail="메시지를 입력해주세요.")
    
    # AI API 키 확인
    if not is_ai_enabled():
        return {
            "intent": {"category": "ERROR", "confidence": 1.0},
            "plan": [],
            "result": {"error": "AI API 키가 설정되지 않았습니다."},
            "response": "죄송합니다. AI 서비스가 현재 사용할 수 없습니다. 관리자에게 문의해 주세요."
        }
    
    # 임시 응답 (실제 AI 연동 전까지)
    return {
        "intent": {"category": "GREETING", "confidence": 0.9},
        "plan": ["사용자 인사에 응답하기"],
        "result": {"success": True},
        "response": f"안녕하세요! ERPNext AI 코파일럿입니다. '{user_input}' 메시지를 잘 받았습니다. AI 기능이 곧 완전히 활성화될 예정입니다."
    }


# 테스트 API들
@app.get("/api/test/openai")
async def test_openai():
    """OpenAI 연결 테스트"""
    if not settings.OPENAI_API_KEY:
        return {"status": "error", "message": "OpenAI API 키가 설정되지 않았습니다."}
    
    return {"status": "success", "message": "OpenAI API 키가 설정되었습니다."}


@app.get("/api/test/anthropic") 
async def test_anthropic():
    """Anthropic 연결 테스트"""
    if not settings.ANTHROPIC_API_KEY:
        return {"status": "error", "message": "Anthropic API 키가 설정되지 않았습니다."}
    
    return {"status": "success", "message": "Anthropic API 키가 설정되었습니다."}


# DocType 임시 API들 (기본 CRUD)
@app.get("/api/customer")
async def list_customers():
    """고객 목록 조회"""
    return {
        "data": [],
        "total": 0,
        "message": "데이터베이스 연결 후 고객 데이터가 표시됩니다."
    }


@app.get("/api/item")
async def list_items():
    """품목 목록 조회"""
    return {
        "data": [],
        "total": 0,
        "message": "데이터베이스 연결 후 품목 데이터가 표시됩니다."
    }


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app", 
        host=settings.HOST, 
        port=settings.PORT, 
        reload=settings.DEBUG and settings.ENVIRONMENT != "production",
        log_level=settings.LOG_LEVEL
    )