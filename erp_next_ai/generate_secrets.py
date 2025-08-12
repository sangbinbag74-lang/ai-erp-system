#!/usr/bin/env python3
"""
환경변수용 시크릿 키 생성기
"""

import secrets
import string

def generate_secret_key(length=64):
    """안전한 시크릿 키 생성"""
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def main():
    print("=" * 60)
    print("🔐 ERPNext AI System - 환경변수 시크릿 키 생성기")
    print("=" * 60)
    
    print("\n📋 생성된 환경변수들:")
    print("-" * 60)
    
    # SECRET_KEY 생성
    secret_key = generate_secret_key(64)
    print(f"SECRET_KEY={secret_key}")
    
    # JWT_SECRET_KEY 생성  
    jwt_secret = generate_secret_key(64)
    print(f"JWT_SECRET_KEY={jwt_secret}")
    
    print("-" * 60)
    print("\n🔧 Railway 백엔드 환경변수 전체 설정:")
    print("-" * 60)
    print("# 데이터베이스 (Railway에서 자동 설정)")
    print("DATABASE_URL=${{Postgres.DATABASE_URL}}")
    print()
    print("# AI API 키 (직접 발급 필요)")
    print("OPENAI_API_KEY=sk-your-openai-key-here")
    print("ANTHROPIC_API_KEY=sk-ant-your-anthropic-key-here")
    print()
    print("# 보안 키 (위에서 생성된 값 사용)")
    print(f"SECRET_KEY={secret_key}")
    print(f"JWT_SECRET_KEY={jwt_secret}")
    print()
    print("# 애플리케이션 설정")
    print("ENVIRONMENT=production")
    print("DEBUG=false")
    print("ALLOWED_ORIGINS=https://your-frontend.vercel.app,http://localhost:3000")
    
    print("\n🌐 Vercel 프론트엔드 환경변수:")
    print("-" * 60)
    print("VITE_API_URL=https://your-backend.railway.app")
    print("VITE_ENABLE_AI_COPILOT=true")
    print("VITE_APP_NAME=ERPNext AI System")
    print("VITE_DEFAULT_THEME=light")
    print("VITE_DEFAULT_LANGUAGE=ko")
    
    print("\n📌 주의사항:")
    print("1. 생성된 시크릿 키들을 안전한 곳에 보관하세요")
    print("2. OpenAI와 Anthropic API 키는 별도로 발급받아야 합니다")
    print("3. URL들은 실제 배포 URL로 교체해야 합니다")
    print("=" * 60)

if __name__ == "__main__":
    main()