#!/usr/bin/env python3

import secrets
import string

def generate_secret_key(length=64):
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def main():
    print("=" * 60)
    print("Secret Keys for ERPNext AI System")
    print("=" * 60)
    
    secret_key = generate_secret_key(64)
    jwt_secret = generate_secret_key(64)
    
    print("\nGenerated Environment Variables:")
    print("-" * 40)
    print(f"SECRET_KEY={secret_key}")
    print(f"JWT_SECRET_KEY={jwt_secret}")
    
    print("\nRailway Backend Environment Variables:")
    print("-" * 40)
    print("DATABASE_URL=${{Postgres.DATABASE_URL}}")
    print("OPENAI_API_KEY=sk-your-openai-key-here")
    print("ANTHROPIC_API_KEY=sk-ant-your-anthropic-key-here")
    print(f"SECRET_KEY={secret_key}")
    print(f"JWT_SECRET_KEY={jwt_secret}")
    print("ENVIRONMENT=production")
    print("DEBUG=false")
    print("ALLOWED_ORIGINS=https://your-frontend.vercel.app")
    
    print("\nVercel Frontend Environment Variables:")
    print("-" * 40)
    print("VITE_API_URL=https://your-backend.railway.app")
    print("VITE_ENABLE_AI_COPILOT=true")
    print("VITE_APP_NAME=ERPNext AI System")
    
    print("\nRemember to:")
    print("1. Get OpenAI API key from https://platform.openai.com")
    print("2. Get Anthropic API key from https://console.anthropic.com")
    print("3. Replace URLs with actual deployment URLs")
    print("=" * 60)

if __name__ == "__main__":
    main()