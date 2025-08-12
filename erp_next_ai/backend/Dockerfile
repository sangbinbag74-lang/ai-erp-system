FROM python:3.11-slim

WORKDIR /app

# 최소한의 패키지만 설치
RUN pip install fastapi uvicorn[standard]

# 최소 앱 복사
COPY app_minimal.py main.py

EXPOSE 8000

ENV PYTHONUNBUFFERED=1

CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]