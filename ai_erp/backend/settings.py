import os
from urllib.parse import urlparse  # URL 파싱 라이브러리 임포트 (기본 내장, 설치 불필요)

# DB 설정 딕셔너리 (Frappe/Django 스타일)
DATABASES = {
    'default': {}
}

# Vercel/Neon에서 DATABASE_URL 환경 변수 읽기
if 'DATABASE_URL' in os.environ:
    url = urlparse(os.getenv('DATABASE_URL'))  # URL 분해 (e.g., postgres://user:pass@host/db)
    DATABASES['default'] = {
        'ENGINE': 'frappe.db.backends.postgresql_psycopg2',  # Frappe 호환 Postgres 엔진 (MariaDB 대신)
        'NAME': url.path[1:],  # DB 이름 추출
        'USER': url.username,  # 사용자 이름
        'PASSWORD': url.password,  # 비밀번호
        'HOST': url.hostname,  # 호스트
        'PORT': url.port or 5432,  # 포트 (기본 5432)
        'OPTIONS': {
            'sslmode': 'require'  # Neon 필수: SSL 보안 연결 (2025년 변경으로 무조건 필요, 없으면 연결 실패)
        }
    }
else:
    # 로컬 fallback (테스트용, .env 기반)
    DATABASES['default'] = {
        'ENGINE': 'frappe.db.backends.mariadb',  # 원본 MariaDB 유지
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT')
    }

# 추가: Frappe 사이트 설정 (ERPNext 기반이라 필요할 수 있음)
SITE_CONFIG = {
    'db_name': DATABASES['default']['NAME'],
    'db_password': DATABASES['default']['PASSWORD']
}