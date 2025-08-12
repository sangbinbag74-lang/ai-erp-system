"""
ERPNext AI System - FastAPI 메인 애플리케이션 (업데이트)
"""
import os
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from contextlib import asynccontextmanager

# Core imports
from core.database.connection import init_database, get_db
from core.api.generator import get_all_doctype_routers
from core.doctype.base import create_doctype_from_json

# Module imports (DocType 정의들)
from modules.accounts.customer import Customer
from modules.accounts.item import Item
from modules.sales.sales_order import SalesOrder, SalesOrderItem
from modules.stock.warehouse import Warehouse, StockEntry, StockEntryDetail
from modules.purchase.supplier import Supplier, PurchaseOrder
from modules.hr.employee import Employee, Attendance, SalaryStructure
from modules.projects.project import Project, Task, Timesheet, TimesheetDetail
from modules.crm.lead import Lead, Opportunity, Campaign, CommunicationLog

# AI imports
from ai.copilot.main import process_ai_request


@asynccontextmanager
async def lifespan(app: FastAPI):
    """애플리케이션 생명주기 관리"""
    # 시작 시 초기화
    print("🚀 ERPNext AI System 시작 중...")
    
    try:
        # 데이터베이스 초기화
        init_database()
        print("✅ 데이터베이스 초기화 완료")
        
        # DocType 라우터 등록
        doctype_routers = get_all_doctype_routers()
        for router in doctype_routers:
            app.include_router(router)
        print(f"✅ {len(doctype_routers)}개 DocType API 등록 완료")
        
    except Exception as e:
        print(f"❌ 초기화 실패: {e}")
        raise
    
    yield  # 애플리케이션 실행
    
    # 종료 시 정리
    print("🛑 ERPNext AI System 종료")


# FastAPI 애플리케이션 생성
app = FastAPI(
    title="ERPNext AI System",
    description="AI 기반 ERP 시스템 - ERPNext의 모든 기능을 구현한 차세대 ERP",
    version="1.0.0",
    lifespan=lifespan
)

# CORS 설정
allowed_origins = os.getenv("ALLOWED_ORIGINS", "").split(",") if os.getenv("ALLOWED_ORIGINS") else [
    "http://localhost:3000",
    "http://localhost:5173",
    "https://*.vercel.app",
    "*"  # 개발용
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
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
    return {
        "status": "healthy",
        "message": "ERPNext AI System is running successfully!",
        "version": "1.0.0",
        "environment": os.getenv("ENVIRONMENT", "development")
    }


# 시스템 정보 API
@app.get("/api/system/info")
async def system_info():
    """시스템 정보 조회"""
    from core.doctype.base import DOCTYPE_REGISTRY
    from core.database.connection import DatabaseManager
    
    return {
        "system": "ERPNext AI System",
        "version": "1.0.0",
        "environment": os.getenv("ENVIRONMENT", "development"),
        "python_version": os.sys.version,
        "doctypes_count": len(DOCTYPE_REGISTRY),
        "available_modules": [
            "Accounts", "Sales", "Purchase", "Stock", 
            "HR", "Manufacturing", "Projects", "CRM",
            "Support", "Assets", "Quality", "Website"
        ],
        "ai_features": [
            "File Management", "AGI-like Autonomy", 
            "Workflow Automation", "Predictive Analytics"
        ],
        "database": DatabaseManager.get_table_info() if DatabaseManager.check_connection() else {"status": "disconnected"}
    }


# AI 서비스 상태 API
@app.get("/api/ai/status")
async def ai_status():
    """AI 서비스 상태 확인"""
    openai_key = bool(os.getenv("OPENAI_API_KEY"))
    anthropic_key = bool(os.getenv("ANTHROPIC_API_KEY"))
    
    return {
        "ai_copilot": "active" if openai_key or anthropic_key else "inactive",
        "file_manager": "active", 
        "workflow_automation": "active",
        "predictive_analytics": "active",
        "openai_configured": openai_key,
        "anthropic_configured": anthropic_key,
        "supported_models": [],
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
    if not os.getenv("OPENAI_API_KEY") and not os.getenv("ANTHROPIC_API_KEY"):
        return {
            "intent": {"category": "ERROR", "confidence": 1.0},
            "plan": [],
            "result": {"error": "AI API 키가 설정되지 않았습니다."},
            "response": "죄송합니다. AI 서비스가 현재 사용할 수 없습니다. 관리자에게 문의해 주세요."
        }
    
    try:
        result = await process_ai_request(user_input, user_context)
        return result
    except Exception as e:
        print(f"AI 처리 오류: {e}")
        return {
            "intent": {"category": "ERROR", "confidence": 0.0},
            "plan": [],
            "result": {"error": str(e)},
            "response": "죄송합니다. 요청을 처리하는 중에 오류가 발생했습니다. 다시 시도해 주세요."
        }


# DocType 목록 API
@app.get("/api/doctypes")
async def list_doctypes():
    """등록된 모든 DocType 목록 조회"""
    from core.doctype.base import DOCTYPE_REGISTRY
    
    doctypes = []
    for name, info in DOCTYPE_REGISTRY.items():
        meta = info['meta']
        doctypes.append({
            "name": name,
            "module": meta.module,
            "fields_count": len(meta.fields),
            "is_submittable": meta.is_submittable,
            "search_fields": meta.search_fields
        })
    
    return {
        "doctypes": doctypes,
        "total": len(doctypes)
    }


if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=port, 
        reload=os.getenv("DEV_RELOAD", "False").lower() == "true",
        log_level=os.getenv("LOG_LEVEL", "info")
    )