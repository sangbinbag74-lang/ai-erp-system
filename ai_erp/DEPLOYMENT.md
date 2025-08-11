# AI ERP System - Deployment Guide

This guide covers deploying the AI ERP system to production environments with best practices for security, scalability, and reliability.

## Overview

The AI ERP system is designed as a cloud-native application with the following components:

- **Backend**: Python-based API server (FastAPI/Flask)
- **Frontend**: Vue.js single-page application
- **Database**: PostgreSQL for primary data
- **Cache**: Redis for session management and caching
- **Storage**: Multi-cloud file storage (AWS S3, Google Cloud, Azure)
- **AI Services**: External LLM APIs (OpenAI, Anthropic)
- **Payment**: Stripe integration for subscription billing

## Infrastructure Requirements

### Minimum Production Requirements

- **CPU**: 2 vCPU cores
- **Memory**: 4 GB RAM
- **Storage**: 20 GB SSD
- **Bandwidth**: 100 Mbps
- **Database**: PostgreSQL 12+ 
- **Cache**: Redis 6+

### Recommended Production Setup

- **Application Server**: 4 vCPU, 8 GB RAM
- **Database Server**: 2 vCPU, 4 GB RAM, 100 GB SSD
- **Load Balancer**: Application Load Balancer (ALB/ELB)
- **CDN**: CloudFront or similar
- **Monitoring**: Application and infrastructure monitoring

## Deployment Options

### 1. Cloud Platform Deployment (Recommended)

#### AWS Deployment

**Services Used:**
- **Compute**: EC2 instances or ECS Fargate
- **Database**: RDS PostgreSQL
- **Cache**: ElastiCache Redis
- **Storage**: S3 buckets
- **Load Balancer**: Application Load Balancer
- **CDN**: CloudFront
- **Domain**: Route 53

**Step-by-step AWS Deployment:**

```bash
# 1. Create VPC and networking
aws ec2 create-vpc --cidr-block 10.0.0.0/16
aws ec2 create-subnet --vpc-id vpc-xxx --cidr-block 10.0.1.0/24
aws ec2 create-internet-gateway

# 2. Create RDS PostgreSQL instance
aws rds create-db-instance \
    --db-instance-identifier ai-erp-db \
    --db-instance-class db.t3.micro \
    --engine postgres \
    --master-username aierpuser \
    --master-user-password YourSecurePassword \
    --allocated-storage 20

# 3. Create ElastiCache Redis
aws elasticache create-cache-cluster \
    --cache-cluster-id ai-erp-redis \
    --cache-node-type cache.t3.micro \
    --engine redis \
    --num-cache-nodes 1

# 4. Create S3 bucket for file storage
aws s3 mb s3://ai-erp-storage-prod
aws s3api put-bucket-versioning \
    --bucket ai-erp-storage-prod \
    --versioning-configuration Status=Enabled

# 5. Deploy using ECS Fargate (recommended)
aws ecs create-cluster --cluster-name ai-erp-cluster
```

#### Google Cloud Platform (GCP)

**Services Used:**
- **Compute**: Cloud Run or GKE
- **Database**: Cloud SQL PostgreSQL
- **Cache**: Memory Store Redis
- **Storage**: Cloud Storage
- **Load Balancer**: Cloud Load Balancing
- **CDN**: Cloud CDN

#### Microsoft Azure

**Services Used:**
- **Compute**: Container Instances or AKS
- **Database**: Azure Database for PostgreSQL
- **Cache**: Azure Cache for Redis
- **Storage**: Blob Storage
- **Load Balancer**: Azure Load Balancer
- **CDN**: Azure CDN

### 2. Docker Containerization

**Dockerfile for Backend:**

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY backend/ ./backend/
COPY config/ ./config/
COPY shared/ ./shared/

# Set environment variables
ENV PYTHONPATH=/app
ENV ENVIRONMENT=production

# Create non-root user
RUN useradd -m -u 1000 aierpuser && chown -R aierpuser:aierpuser /app
USER aierpuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# Start application
CMD ["python", "-m", "uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Dockerfile for Frontend:**

```dockerfile
FROM node:18-alpine as build

WORKDIR /app
COPY frontend/package*.json ./
RUN npm ci --only=production

COPY frontend/ .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

**docker-compose.yml for Development:**

```yaml
version: '3.8'

services:
  backend:
    build: 
      context: .
      dockerfile: Dockerfile.backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:password@db:5432/ai_erp
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis
    volumes:
      - ./config:/app/config
      - ./logs:/app/logs

  frontend:
    build:
      context: .
      dockerfile: Dockerfile.frontend
    ports:
      - "3000:80"
    depends_on:
      - backend

  db:
    image: postgres:14
    environment:
      POSTGRES_DB: ai_erp
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

### 3. Kubernetes Deployment

**Kubernetes manifests:**

```yaml
# backend-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ai-erp-backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: ai-erp-backend
  template:
    metadata:
      labels:
        app: ai-erp-backend
    spec:
      containers:
      - name: backend
        image: ai-erp/backend:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: ai-erp-secrets
              key: database-url
        - name: REDIS_URL
          valueFrom:
            secretKeyRef:
              name: ai-erp-secrets
              key: redis-url
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5

---
apiVersion: v1
kind: Service
metadata:
  name: ai-erp-backend-service
spec:
  selector:
    app: ai-erp-backend
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
  type: ClusterIP
```

## Environment Configuration

### Production Environment Variables

Create a comprehensive environment configuration:

```bash
# Application Settings
ENVIRONMENT=production
DEBUG=false
APP_NAME="AI ERP System"
APP_VERSION="1.0.0"
SECRET_KEY="your-super-secure-secret-key-min-32-chars"

# Database
DATABASE_URL="postgresql://username:password@hostname:5432/ai_erp_prod"
DATABASE_SSL_MODE=require
DATABASE_POOL_SIZE=20
DATABASE_MAX_OVERFLOW=30

# Redis Cache
REDIS_URL="redis://username:password@hostname:6379/0"
REDIS_SSL=true

# LLM Services
OPENAI_API_KEY="sk-your-openai-api-key"
ANTHROPIC_API_KEY="sk-ant-your-anthropic-key"
LLM_RATE_LIMIT=100
LLM_TIMEOUT=30

# Cloud Storage
AWS_ACCESS_KEY_ID="your-aws-access-key"
AWS_SECRET_ACCESS_KEY="your-aws-secret-key"
AWS_REGION="us-east-1"
AWS_S3_BUCKET="ai-erp-storage-prod"
STORAGE_ENCRYPTION=true

# Payment Gateway (Stripe)
STRIPE_SECRET_KEY="sk_live_your-stripe-secret"
STRIPE_PUBLISHABLE_KEY="pk_live_your-stripe-publishable"
STRIPE_WEBHOOK_SECRET="whsec_your-webhook-secret"

# Email Service
SMTP_HOST="smtp.gmail.com"
SMTP_PORT=587
SMTP_USERNAME="noreply@yourdomain.com"
SMTP_PASSWORD="your-smtp-password"
SMTP_TLS=true

# Security
JWT_SECRET="your-jwt-secret-key"
JWT_EXPIRATION=86400
CORS_ORIGINS="https://yourdomain.com,https://app.yourdomain.com"
ALLOWED_HOSTS="yourdomain.com,app.yourdomain.com"

# Monitoring and Logging
LOG_LEVEL=INFO
SENTRY_DSN="your-sentry-dsn"
ENABLE_METRICS=true
METRICS_PORT=9090

# Feature Flags
ENABLE_AI_FEATURES=true
ENABLE_ADVANCED_ANALYTICS=true
ENABLE_EXPERIMENTAL_FEATURES=false
```

## Security Configuration

### SSL/TLS Setup

1. **Obtain SSL Certificates**
   ```bash
   # Using Let's Encrypt
   sudo certbot --nginx -d yourdomain.com -d app.yourdomain.com
   ```

2. **Configure HTTPS Redirect**
   ```nginx
   server {
       listen 80;
       server_name yourdomain.com app.yourdomain.com;
       return 301 https://$server_name$request_uri;
   }
   ```

### Security Headers

```nginx
# Security headers
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
add_header Content-Security-Policy "default-src 'self' https:; script-src 'self' 'unsafe-inline' 'unsafe-eval' https:; style-src 'self' 'unsafe-inline' https:; img-src 'self' data: https:; font-src 'self' https:; connect-src 'self' https:; frame-ancestors 'self';" always;
```

### Database Security

```sql
-- Create production database user with limited privileges
CREATE USER ai_erp_app WITH PASSWORD 'secure_password';
GRANT CONNECT ON DATABASE ai_erp_prod TO ai_erp_app;
GRANT USAGE ON SCHEMA public TO ai_erp_app;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO ai_erp_app;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO ai_erp_app;

-- Enable SSL
ALTER SYSTEM SET ssl = on;
ALTER SYSTEM SET ssl_cert_file = 'server.crt';
ALTER SYSTEM SET ssl_key_file = 'server.key';
```

## Monitoring and Logging

### Application Monitoring

**Prometheus Configuration:**

```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'ai-erp-backend'
    static_configs:
      - targets: ['localhost:8000']
    metrics_path: /metrics
    scrape_interval: 15s

  - job_name: 'postgresql'
    static_configs:
      - targets: ['localhost:9187']

  - job_name: 'redis'
    static_configs:
      - targets: ['localhost:9121']
```

### Logging Configuration

```python
import logging
import structlog
from pythonjsonlogger import jsonlogger

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

# Configure Python logging
logging.basicConfig(
    format='%(message)s',
    level=logging.INFO,
    handlers=[logging.StreamHandler()]
)
```

## Backup and Disaster Recovery

### Database Backup

```bash
#!/bin/bash
# Daily backup script
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="/backups/ai_erp_backup_$DATE.sql"

# Create backup
pg_dump -h $DB_HOST -U $DB_USER -d ai_erp_prod > $BACKUP_FILE

# Compress backup
gzip $BACKUP_FILE

# Upload to S3
aws s3 cp $BACKUP_FILE.gz s3://ai-erp-backups/database/

# Keep only 30 days of local backups
find /backups -name "ai_erp_backup_*.sql.gz" -mtime +30 -delete
```

### Configuration Backup

```bash
# Backup configuration and secrets
kubectl get secrets -o yaml > secrets_backup.yaml
kubectl get configmaps -o yaml > configmaps_backup.yaml
```

## Performance Optimization

### Database Optimization

```sql
-- Create indexes for frequently queried fields
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_teams_owner_id ON teams(owner_id);
CREATE INDEX idx_files_team_id ON files(team_id);
CREATE INDEX idx_subscriptions_team_id ON subscriptions(team_id);

-- Configure PostgreSQL for production
ALTER SYSTEM SET shared_buffers = '256MB';
ALTER SYSTEM SET effective_cache_size = '1GB';
ALTER SYSTEM SET maintenance_work_mem = '64MB';
ALTER SYSTEM SET checkpoint_completion_target = 0.7;
ALTER SYSTEM SET wal_buffers = '16MB';
ALTER SYSTEM SET default_statistics_target = 100;
```

### Application Caching

```python
# Redis caching configuration
CACHE_CONFIG = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'CONNECTION_POOL_KWARGS': {
                'max_connections': 50,
                'retry_on_timeout': True,
            }
        },
        'KEY_PREFIX': 'ai_erp',
        'TIMEOUT': 300,  # 5 minutes default
    }
}
```

### CDN Configuration

```nginx
# Static file caching
location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
    add_header X-Static-Cache "HIT";
}

# API response caching for specific endpoints
location ~* ^/api/v1/(plans|features)$ {
    proxy_cache api_cache;
    proxy_cache_valid 200 1h;
    proxy_cache_use_stale error timeout;
    add_header X-API-Cache $upstream_cache_status;
}
```

## Scaling Configuration

### Horizontal Scaling

**Auto-scaling Policy:**

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: ai-erp-backend-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: ai-erp-backend
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

### Load Balancer Configuration

```nginx
upstream ai_erp_backend {
    least_conn;
    server backend1.internal:8000 weight=3;
    server backend2.internal:8000 weight=3;
    server backend3.internal:8000 weight=3;
    keepalive 32;
}

server {
    listen 443 ssl http2;
    server_name api.yourdomain.com;
    
    location / {
        proxy_pass http://ai_erp_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Connection pooling
        proxy_http_version 1.1;
        proxy_set_header Connection "";
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
}
```

## Health Checks and Monitoring

### Application Health Endpoints

```python
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
import asyncio

app = FastAPI()

@app.get("/health")
async def health_check():
    """Basic health check"""
    return {"status": "healthy", "timestamp": datetime.utcnow()}

@app.get("/ready")
async def readiness_check():
    """Readiness check with dependencies"""
    checks = {
        "database": await check_database(),
        "redis": await check_redis(),
        "storage": await check_storage(),
        "llm_service": await check_llm_service()
    }
    
    all_healthy = all(checks.values())
    status_code = status.HTTP_200_OK if all_healthy else status.HTTP_503_SERVICE_UNAVAILABLE
    
    return JSONResponse(
        content={"status": "ready" if all_healthy else "not_ready", "checks": checks},
        status_code=status_code
    )
```

### Monitoring Dashboards

**Grafana Dashboard Configuration** (JSON snippet):

```json
{
  "dashboard": {
    "title": "AI ERP System Monitoring",
    "panels": [
      {
        "title": "Request Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(http_requests_total[5m])",
            "legendFormat": "Requests/sec"
          }
        ]
      },
      {
        "title": "Response Time",
        "type": "graph", 
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))",
            "legendFormat": "95th percentile"
          }
        ]
      }
    ]
  }
}
```

## Troubleshooting

### Common Issues and Solutions

1. **High Memory Usage**
   - Check for memory leaks in application code
   - Tune database connection pools
   - Review caching configuration

2. **Slow API Responses**
   - Add database indexes
   - Implement query optimization
   - Configure Redis caching

3. **File Upload Issues**
   - Check S3 permissions and CORS
   - Verify file size limits
   - Monitor storage quotas

4. **Authentication Problems**
   - Verify JWT secret keys
   - Check token expiration settings
   - Review CORS configuration

### Debugging Commands

```bash
# Check application logs
kubectl logs -f deployment/ai-erp-backend

# Check database connections
psql -h $DB_HOST -U $DB_USER -d ai_erp_prod -c "SELECT count(*) FROM pg_stat_activity;"

# Check Redis connectivity
redis-cli -h $REDIS_HOST -p 6379 ping

# Monitor resource usage
kubectl top pods
kubectl top nodes

# Check service endpoints
curl -f http://localhost:8000/health
curl -f http://localhost:8000/ready
```

## Maintenance

### Regular Maintenance Tasks

1. **Daily**
   - Check application logs
   - Monitor system resources
   - Verify backup completion

2. **Weekly**
   - Review security alerts
   - Check SSL certificate expiry
   - Update dependency vulnerabilities

3. **Monthly**
   - Database maintenance (VACUUM, ANALYZE)
   - Review access logs
   - Update documentation

### Update Procedures

```bash
# Zero-downtime deployment with Kubernetes
kubectl set image deployment/ai-erp-backend backend=ai-erp/backend:v1.1.0
kubectl rollout status deployment/ai-erp-backend

# Database migrations
python manage.py migrate --check
python manage.py migrate

# Rollback if needed
kubectl rollout undo deployment/ai-erp-backend
```

---

This deployment guide provides a comprehensive foundation for deploying the AI ERP system in production. Adjust configurations based on your specific requirements, scale, and infrastructure preferences.