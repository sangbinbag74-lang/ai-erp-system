# ERPNext AI System Backend - Dockerfile (간단한 버전)
FROM python:3.11-slim

# 작업 디렉토리 설정
WORKDIR /app

# 환경변수 설정
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# 기본 의존성만 먼저 설치
RUN pip install --no-cache-dir fastapi uvicorn[standard] pydantic pydantic-settings python-dotenv

# requirements.txt 복사 및 설치 (선택적 의존성은 무시)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt || echo "Some packages failed to install, continuing..."

# 애플리케이션 코드 복사
COPY . .

# 포트 8000 노출
EXPOSE 8000

# 디버깅을 위한 상세 시작 스크립트 사용
CMD ["python", "start.py"]