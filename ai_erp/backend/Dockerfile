# ERPNext용 Dockerfile
FROM frappe/erpnext:latest

USER root

# 추가 패키지 설치
COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

# 커스텀 앱 복사
COPY . /home/frappe/frappe-bench/apps/ai_erp
WORKDIR /home/frappe/frappe-bench

# 앱 설치
RUN bench get-app ai_erp /home/frappe/frappe-bench/apps/ai_erp
RUN bench install-app ai_erp

# 권한 설정
RUN chown -R frappe:frappe /home/frappe/frappe-bench

USER frappe

# 서버 시작
CMD ["bench", "start"]

EXPOSE 8000