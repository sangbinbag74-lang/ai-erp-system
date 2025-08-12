FROM python:3.11-slim

WORKDIR /app

# 기본 시스템 패키지 설치
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Python 의존성 먼저 설치 (캐싱 활용)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 복사
COPY main.py .

# Railway의 동적 포트 사용
EXPOSE $PORT

ENV PYTHONUNBUFFERED=1

# Railway에서 제공하는 PORT 환경변수 사용
CMD python main.py