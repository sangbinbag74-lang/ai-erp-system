#!/usr/bin/env python3
"""
Railway 배포용 시작 스크립트
문제 발생 시 디버깅을 위한 상세 로깅 포함
"""

import os
import sys
import traceback

def main():
    """메인 실행 함수"""
    print("🚀 ERPNext AI System 시작 중...")
    print(f"📍 작업 디렉토리: {os.getcwd()}")
    print(f"🐍 Python 버전: {sys.version}")
    print(f"📝 환경: {os.getenv('ENVIRONMENT', 'development')}")
    
    # 환경변수 확인
    print("\n📋 주요 환경변수 확인:")
    env_vars = ['DATABASE_URL', 'OPENAI_API_KEY', 'ANTHROPIC_API_KEY', 'ENVIRONMENT']
    for var in env_vars:
        value = os.getenv(var)
        if value:
            # API 키는 앞 몇 글자만 표시
            if 'API_KEY' in var and len(value) > 10:
                display_value = f"{value[:10]}..."
            else:
                display_value = value
            print(f"  ✅ {var}: {display_value}")
        else:
            print(f"  ❌ {var}: 설정되지 않음")
    
    try:
        print("\n🔄 FastAPI 애플리케이션 로딩 중...")
        
        # 필수 모듈 임포트 테스트
        print("📦 핵심 모듈 임포트 테스트...")
        import fastapi
        print(f"  ✅ FastAPI {fastapi.__version__}")
        
        import uvicorn
        print(f"  ✅ Uvicorn")
        
        from core.config import settings
        print(f"  ✅ Core Config")
        
        print("\n🚀 서버 시작...")
        
        # 포트 설정
        port = int(os.getenv("PORT", 8000))
        print(f"📡 포트: {port}")
        
        # Uvicorn 서버 시작
        uvicorn.run(
            "main:app",
            host="0.0.0.0", 
            port=port,
            log_level="info",
            access_log=True,
            reload=False  # 프로덕션에서는 reload 비활성화
        )
        
    except ImportError as e:
        print(f"❌ 모듈 임포트 실패: {e}")
        print("📝 필요한 패키지가 설치되지 않았습니다.")
        traceback.print_exc()
        sys.exit(1)
        
    except Exception as e:
        print(f"❌ 애플리케이션 시작 실패: {e}")
        print("📝 상세 오류 정보:")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()