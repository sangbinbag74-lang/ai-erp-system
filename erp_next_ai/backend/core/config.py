"""
ERPNext AI System - 설정 관리
"""

import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """애플리케이션 설정"""
    
    # 기본 설정
    APP_NAME: str = "ERPNext AI System"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    SECRET_KEY: str = "your-secret-key-change-in-production"
    
    # 데이터베이스 설정
    DATABASE_URL: Optional[str] = None
    
    # AI API 설정
    OPENAI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    
    # JWT 설정
    JWT_SECRET_KEY: str = "your-jwt-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_DELTA: int = 86400  # 24시간
    
    # CORS 설정
    ALLOWED_ORIGINS: str = "http://localhost:3000,http://localhost:5173,https://*.vercel.app"
    
    # Redis 설정
    REDIS_URL: Optional[str] = None
    
    # 서버 설정
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # 로깅 설정
    LOG_LEVEL: str = "info"
    
    # AI 설정
    AI_MODEL_TEMPERATURE: float = 0.7
    AI_MAX_TOKENS: int = 2048
    AI_ENABLE_STREAMING: bool = True
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# 전역 설정 인스턴스
settings = Settings()


def get_database_url() -> str:
    """데이터베이스 URL 반환"""
    if settings.DATABASE_URL:
        return settings.DATABASE_URL
    
    # 기본 개발용 데이터베이스 URL
    return "postgresql://user:password@localhost:5432/erpnext_ai"


def get_allowed_origins() -> list[str]:
    """허용된 CORS 오리진 목록 반환"""
    if settings.ALLOWED_ORIGINS:
        return [origin.strip() for origin in settings.ALLOWED_ORIGINS.split(",")]
    
    return [
        "http://localhost:3000",
        "http://localhost:5173",
        "https://*.vercel.app"
    ]


def is_ai_enabled() -> bool:
    """AI 기능 활성화 여부 확인"""
    return bool(settings.OPENAI_API_KEY or settings.ANTHROPIC_API_KEY)


def is_production() -> bool:
    """프로덕션 환경 여부 확인"""
    return settings.ENVIRONMENT.lower() == "production"