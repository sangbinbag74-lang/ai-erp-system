# AI API 키 설정 가이드 🤖

ERPNext AI System의 AI 기능을 사용하기 위해 필요한 API 키 설정 방법을 안내합니다.

## 📋 필수 API 키

### 1. OpenAI API 키 (필수)
GPT-4 및 텍스트 처리를 위해 필요합니다.

#### 획득 방법:
1. [OpenAI Platform](https://platform.openai.com/) 방문
2. 계정 생성 또는 로그인
3. API Keys 섹션으로 이동
4. "Create new secret key" 클릭
5. 키 이름 설정 후 생성
6. 생성된 키를 안전한 곳에 복사 (한 번만 표시됩니다)

#### 형태:
```
sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

#### 권장 모델:
- **gpt-4-turbo-preview**: 최고 성능, 높은 비용
- **gpt-3.5-turbo**: 균형잡힌 성능과 비용
- **gpt-4**: 높은 성능, 중간 비용

### 2. Anthropic Claude API 키 (필수)
고급 추론 및 분석을 위해 필요합니다.

#### 획득 방법:
1. [Anthropic Console](https://console.anthropic.com/) 방문
2. 계정 생성 또는 로그인
3. API Keys 섹션으로 이동
4. "Create Key" 클릭
5. 키 이름 설정 후 생성
6. 생성된 키를 안전한 곳에 복사

#### 형태:
```
sk-ant-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

#### 권장 모델:
- **claude-3-opus-20240229**: 최고 성능
- **claude-3-sonnet-20240229**: 균형잡힌 성능
- **claude-3-haiku-20240307**: 빠른 응답

## 🔧 환경변수 설정

### 백엔드 설정 (.env)
```bash
# AI API 키
OPENAI_API_KEY=sk-your-openai-key-here
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key-here

# AI 모델 설정
OPENAI_MODEL=gpt-4-turbo-preview
ANTHROPIC_MODEL=claude-3-sonnet-20240229

# AI 성능 튜닝
AI_TEMPERATURE=0.7
AI_MAX_TOKENS=4096
AI_TOP_P=0.9
AI_FREQUENCY_PENALTY=0.0
AI_PRESENCE_PENALTY=0.0

# 요청 제한
AI_REQUESTS_PER_MINUTE=60
AI_MAX_CONCURRENT_REQUESTS=5
AI_TIMEOUT_SECONDS=30

# 스트리밍 설정
ENABLE_AI_STREAMING=true
STREAM_CHUNK_SIZE=1024
```

### 프론트엔드 설정 (.env)
```bash
# AI 기능 활성화
VITE_ENABLE_AI_COPILOT=true
VITE_AI_STREAMING_ENABLED=true

# AI 응답 설정
VITE_AI_MAX_RESPONSE_TIME=30000
VITE_AI_RETRY_ATTEMPTS=3
VITE_AI_RETRY_DELAY=1000
```

## 🌐 배포 환경 설정

### Railway (백엔드)
1. Railway 대시보드에서 프로젝트 선택
2. Variables 탭으로 이동
3. 다음 환경변수 추가:
   ```
   OPENAI_API_KEY=sk-your-openai-key-here
   ANTHROPIC_API_KEY=sk-ant-your-anthropic-key-here
   ```

### Vercel (프론트엔드)
1. Vercel 대시보드에서 프로젝트 선택
2. Settings > Environment Variables로 이동
3. 다음 환경변수 추가:
   ```
   VITE_ENABLE_AI_COPILOT=true
   VITE_API_URL=https://your-railway-backend-url.up.railway.app
   ```

## 💰 비용 관리

### OpenAI 요금
- **GPT-4 Turbo**: $10.00 / 1M tokens (input), $30.00 / 1M tokens (output)
- **GPT-3.5 Turbo**: $0.50 / 1M tokens (input), $1.50 / 1M tokens (output)

### Anthropic 요금
- **Claude 3 Opus**: $15.00 / 1M tokens (input), $75.00 / 1M tokens (output)
- **Claude 3 Sonnet**: $3.00 / 1M tokens (input), $15.00 / 1M tokens (output)
- **Claude 3 Haiku**: $0.25 / 1M tokens (input), $1.25 / 1M tokens (output)

### 비용 절약 팁
1. **토큰 제한**: `AI_MAX_TOKENS` 설정으로 응답 길이 제한
2. **캐싱**: 유사한 요청에 대한 결과 캐싱
3. **배치 처리**: 여러 요청을 하나로 묶어서 처리
4. **적절한 모델 선택**: 작업에 맞는 최적 모델 사용

## 🔒 보안 모범 사례

### API 키 보안
1. **절대 코드에 하드코딩하지 않기**
2. **환경변수로만 관리**
3. **정기적인 키 교체**
4. **최소 권한 원칙 적용**
5. **API 키 사용량 모니터링**

### 접근 제어
```python
# 백엔드에서 API 키 검증
@app.middleware("http")
async def verify_ai_keys(request: Request, call_next):
    if not settings.OPENAI_API_KEY or not settings.ANTHROPIC_API_KEY:
        logger.warning("AI API keys not configured")
    response = await call_next(request)
    return response
```

## 🧪 API 키 테스트

### OpenAI 연결 테스트
```bash
curl -X POST "http://localhost:8000/api/ai/test/openai" \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, OpenAI!"}'
```

### Anthropic 연결 테스트
```bash
curl -X POST "http://localhost:8000/api/ai/test/anthropic" \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, Claude!"}'
```

### 통합 테스트
```bash
curl -X POST "http://localhost:8000/api/ai/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "분석해줘: 이번 달 매출 현황",
    "context": {"module": "accounts"}
  }'
```

## 🔄 백업 및 복구

### API 키 백업
1. 안전한 비밀번호 관리자에 저장
2. 팀 공유용 암호화된 저장소 사용
3. 개발/스테이징/프로덕션 환경별 분리

### 키 교체 절차
1. 새 키 생성
2. 환경변수 업데이트
3. 서비스 재시작
4. 이전 키 비활성화

## 🆘 문제 해결

### 일반적인 문제들

#### 1. "API key not found" 오류
**원인**: 환경변수가 설정되지 않음
**해결**: `.env` 파일 확인 및 서버 재시작

#### 2. "Quota exceeded" 오류
**원인**: API 사용량 한도 초과
**해결**: 
- OpenAI/Anthropic 대시보드에서 사용량 확인
- 결제 정보 업데이트
- 사용량 제한 설정 조정

#### 3. "Rate limit exceeded" 오류
**원인**: 요청 빈도가 너무 높음
**해결**:
- 요청 간격 조정
- 배치 처리 구현
- 캐싱 활용

#### 4. 응답 시간 초과
**원인**: 네트워크 지연 또는 모델 과부하
**해결**:
- `AI_TIMEOUT_SECONDS` 증가
- 더 빠른 모델 사용
- 비동기 처리 구현

### 로그 확인
```bash
# 백엔드 AI 관련 로그
docker logs erpnext-ai-backend | grep -i "ai\|openai\|anthropic"

# 상세 디버그 로그 활성화
LOG_LEVEL=debug python main.py
```

## 📞 지원

문제가 지속되는 경우:
1. [GitHub Issues](https://github.com/your-repo/issues) 등록
2. 로그 파일 첨부
3. 환경 정보 포함 (운영체제, Python 버전 등)

---

🔐 **중요**: API 키는 절대 공개 저장소에 커밋하지 마세요!