# 최소한의 FastAPI Dockerfile (Railway 테스트용)
FROM python:3.11-slim

# 작업 디렉토리
WORKDIR /app

# 환경변수
ENV PYTHONUNBUFFERED=1

# 최소 의존성 설치
RUN pip install --no-cache-dir fastapi uvicorn[standard]

# 애플리케이션 파일 복사
COPY main.py .

# 포트 노출
EXPOSE 8000

# 애플리케이션 시작
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]