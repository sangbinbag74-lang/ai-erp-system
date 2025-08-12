"""
AI 코파일럿 메인 시스템
ERPNext의 모든 모듈에서 AGI 수준의 자율적 작업 처리
"""
import json
import asyncio
from typing import Dict, List, Any, Optional, Union
from datetime import datetime
import openai
import anthropic
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory

from core.database.connection import get_db_session
from core.doctype.base import DOCTYPE_REGISTRY, get_doctype_model, get_doctype_meta


class ERPAICopilot:
    """ERP AI 코파일럿 - AGI 수준의 자율적 작업 처리"""
    
    def __init__(self):
        self.openai_client = openai.OpenAI()
        self.claude_client = anthropic.Anthropic()
        self.conversation_memory = ConversationBufferMemory(return_messages=True)
        
        # ERP 도메인 지식 프롬프트
        self.system_prompt = """
당신은 ERPNext 기반 AI ERP 시스템의 전문 어시스턴트입니다.
다음과 같은 능력을 가지고 있습니다:

1. **파일 관리**: 모든 ERP 문서를 불러오고, 수정하고, 설명할 수 있습니다.
2. **자율적 작업**: 사용자의 요청을 이해하고 완전히 자동으로 처리합니다.
3. **워크플로 자동화**: 복잡한 비즈니스 프로세스를 단계별로 자동 실행합니다.
4. **예측 분석**: 데이터를 분석하여 미래 트렌드를 예측합니다.

ERP 모듈:
- Accounts (회계): 계정과목, 거래처, 전표, 결제
- Sales (영업): 고객관리, 견적서, 주문서, 송장
- Purchase (구매): 공급업체, 구매주문, 입고, 지급
- Stock (재고): 창고관리, 재고이동, 평가방법
- HR (인사): 직원관리, 급여, 출근, 휴가
- Manufacturing (제조): BOM, 작업지시, 생산계획
- Projects (프로젝트): 프로젝트관리, 작업추적, 시간기록
- CRM (고객관리): 리드관리, 기회관리, 커뮤니케이션
- Support (지원): 이슈추적, 유지보수 일정
- Assets (자산관리): 고정자산, 감가상각
- Quality (품질관리): 품질검사, 검사 템플릿

사용자의 자연어 요청을 분석하여 적절한 ERP 작업을 자동으로 수행하세요.
"""
    
    async def process_request(self, user_input: str, user_context: Dict = None) -> Dict[str, Any]:
        """사용자 요청 처리 - 메인 엔트리포인트"""
        
        # 1. 의도 분석
        intent = await self._analyze_intent(user_input)
        
        # 2. 작업 계획 수립
        action_plan = await self._create_action_plan(user_input, intent)
        
        # 3. 작업 실행
        result = await self._execute_plan(action_plan, user_context)
        
        # 4. 결과 포맷팅
        response = await self._format_response(result, user_input)
        
        return {
            "intent": intent,
            "plan": action_plan,
            "result": result,
            "response": response,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    async def _analyze_intent(self, user_input: str) -> Dict[str, Any]:
        """사용자 의도 분석"""
        
        prompt = f"""
사용자 입력: "{user_input}"

다음 중 어떤 작업 유형에 해당하는지 분석하세요:

1. FILE_MANAGEMENT: 파일/문서 불러오기, 수정, 설명
   - 예: "지난 달 매출 보고서 불러와줘", "고객 목록 수정해줘"

2. DATA_ANALYSIS: 데이터 분석 및 인사이트 생성
   - 예: "매출 트렌드 분석해줘", "재고 현황 분석"

3. WORKFLOW_AUTOMATION: 비즈니스 프로세스 자동화
   - 예: "신규 고객 등록 절차 실행", "주문서 자동 생성"

4. PREDICTIVE_ANALYSIS: 예측 분석
   - 예: "다음 달 매출 예측", "재고 부족 예상 시기"

5. TRANSACTION_PROCESSING: 거래 처리
   - 예: "송장 생성", "결제 처리", "주문서 승인"

6. REPORTING: 보고서 생성
   - 예: "월말 정산 보고서", "직원 급여 명세서"

응답 형식:
{{
    "category": "작업_유형",
    "confidence": 0.95,
    "entities": ["추출된_엔티티들"],
    "module": "관련_ERP_모듈",
    "action": "구체적_작업"
}}
"""
        
        response = await self._call_llm(prompt, "gpt-4")
        
        try:
            return json.loads(response)
        except:
            return {
                "category": "GENERAL_INQUIRY",
                "confidence": 0.5,
                "entities": [],
                "module": "unknown",
                "action": "general_response"
            }
    
    async def _create_action_plan(self, user_input: str, intent: Dict) -> List[Dict]:
        """작업 계획 수립 (Chain of Thought)"""
        
        prompt = f"""
사용자 요청: "{user_input}"
분석된 의도: {json.dumps(intent, ensure_ascii=False)}

이 요청을 완료하기 위한 단계별 실행 계획을 수립하세요.

예시 계획:
[
    {{
        "step": 1,
        "action": "database_query",
        "target": "Customer",
        "operation": "list",
        "parameters": {{"filters": {{"customer_group": "VIP"}}}}
    }},
    {{
        "step": 2,
        "action": "data_analysis",
        "target": "sales_data",
        "operation": "aggregate",
        "parameters": {{"group_by": "month", "sum_field": "total"}}
    }},
    {{
        "step": 3,
        "action": "generate_response",
        "target": "user",
        "operation": "explain_results"
    }}
]

실행 가능한 액션 유형:
- database_query: 데이터베이스 조회/수정
- file_operation: 파일 읽기/쓰기
- data_analysis: 데이터 분석
- generate_report: 보고서 생성
- send_notification: 알림 발송
- workflow_trigger: 워크플로 실행
- ai_prediction: AI 예측 수행
- generate_response: 사용자 응답 생성

구체적인 실행 계획을 JSON 배열로 작성하세요.
"""
        
        response = await self._call_llm(prompt, "claude-3-sonnet")
        
        try:
            return json.loads(response)
        except:
            return [{
                "step": 1,
                "action": "generate_response", 
                "target": "user",
                "operation": "error_message",
                "parameters": {"message": "요청을 처리할 수 없습니다."}
            }]
    
    async def _execute_plan(self, action_plan: List[Dict], user_context: Dict = None) -> Dict[str, Any]:
        """작업 계획 실행"""
        
        results = {}
        
        for step in action_plan:
            try:
                step_result = await self._execute_step(step, user_context, results)
                results[f"step_{step['step']}"] = step_result
                
                # 이전 단계 결과를 다음 단계에서 사용할 수 있도록 컨텍스트 업데이트
                if user_context is None:
                    user_context = {}
                user_context[f"step_{step['step']}_result"] = step_result
                
            except Exception as e:
                results[f"step_{step['step']}_error"] = str(e)
                break
        
        return results
    
    async def _execute_step(self, step: Dict, context: Dict, previous_results: Dict) -> Any:
        """개별 단계 실행"""
        
        action = step.get("action")
        target = step.get("target")
        operation = step.get("operation")
        parameters = step.get("parameters", {})
        
        if action == "database_query":
            return await self._execute_database_query(target, operation, parameters)
        
        elif action == "file_operation":
            return await self._execute_file_operation(target, operation, parameters)
        
        elif action == "data_analysis":
            return await self._execute_data_analysis(target, operation, parameters, previous_results)
        
        elif action == "generate_report":
            return await self._generate_report(target, parameters, previous_results)
        
        elif action == "ai_prediction":
            return await self._execute_ai_prediction(target, parameters, previous_results)
        
        elif action == "workflow_trigger":
            return await self._trigger_workflow(target, parameters)
        
        elif action == "generate_response":
            return await self._generate_user_response(parameters, previous_results)
        
        else:
            raise ValueError(f"지원하지 않는 액션: {action}")
    
    async def _execute_database_query(self, target: str, operation: str, parameters: Dict) -> Any:
        """데이터베이스 쿼리 실행"""
        
        model_class = get_doctype_model(target)
        if not model_class:
            raise ValueError(f"DocType '{target}'을 찾을 수 없습니다.")
        
        with get_db_session() as db:
            query = db.query(model_class)
            
            # 필터 적용
            if "filters" in parameters:
                for field, value in parameters["filters"].items():
                    if hasattr(model_class, field):
                        query = query.filter(getattr(model_class, field) == value)
            
            # 정렬
            if "order_by" in parameters:
                field_name = parameters["order_by"]
                if hasattr(model_class, field_name):
                    query = query.order_by(getattr(model_class, field_name))
            
            # 개수 제한
            if "limit" in parameters:
                query = query.limit(parameters["limit"])
            
            if operation == "list":
                results = query.all()
                return [item.to_dict() for item in results]
            
            elif operation == "count":
                return query.count()
            
            elif operation == "first":
                result = query.first()
                return result.to_dict() if result else None
            
            else:
                raise ValueError(f"지원하지 않는 데이터베이스 연산: {operation}")
    
    async def _execute_data_analysis(self, target: str, operation: str, parameters: Dict, previous_results: Dict) -> Dict:
        """데이터 분석 실행"""
        
        # 이전 단계에서 데이터 가져오기
        data = None
        for key, value in previous_results.items():
            if isinstance(value, list) and len(value) > 0:
                data = value
                break
        
        if not data:
            return {"error": "분석할 데이터가 없습니다."}
        
        if operation == "aggregate":
            # 집계 분석
            group_by = parameters.get("group_by")
            sum_field = parameters.get("sum_field")
            
            if group_by and sum_field:
                result = {}
                for item in data:
                    key = item.get(group_by, "unknown")
                    value = item.get(sum_field, 0)
                    
                    if key in result:
                        result[key] += value
                    else:
                        result[key] = value
                
                return {"aggregation": result, "total": sum(result.values())}
        
        elif operation == "trend_analysis":
            # 트렌드 분석 (간단한 구현)
            if len(data) < 2:
                return {"trend": "insufficient_data"}
            
            # 첫 번째와 마지막 값 비교
            first_value = data[0].get(parameters.get("value_field", "total"), 0)
            last_value = data[-1].get(parameters.get("value_field", "total"), 0)
            
            if first_value == 0:
                return {"trend": "no_baseline"}
            
            change_percent = ((last_value - first_value) / first_value) * 100
            
            return {
                "trend": "increasing" if change_percent > 0 else "decreasing",
                "change_percent": change_percent,
                "first_value": first_value,
                "last_value": last_value
            }
        
        return {"error": f"지원하지 않는 분석 연산: {operation}"}
    
    async def _execute_ai_prediction(self, target: str, parameters: Dict, previous_results: Dict) -> Dict:
        """AI 예측 실행"""
        
        # 데이터 수집
        data = None
        for key, value in previous_results.items():
            if isinstance(value, (list, dict)):
                data = value
                break
        
        if not data:
            return {"error": "예측을 위한 데이터가 없습니다."}
        
        # AI 모델을 사용한 예측
        prompt = f"""
다음 데이터를 바탕으로 {target}에 대한 예측을 수행하세요:

데이터: {json.dumps(data, ensure_ascii=False)}

예측 결과를 다음 형식으로 제공하세요:
{{
    "prediction": "예측값",
    "confidence": "신뢰도(0-1)",
    "reasoning": "예측 근거 설명",
    "recommendations": ["추천 사항들"]
}}
"""
        
        response = await self._call_llm(prompt, "gpt-4")
        
        try:
            return json.loads(response)
        except:
            return {"error": "예측 분석 중 오류가 발생했습니다."}
    
    async def _generate_user_response(self, parameters: Dict, previous_results: Dict) -> str:
        """사용자 응답 생성"""
        
        if "message" in parameters:
            return parameters["message"]
        
        # 이전 결과들을 종합하여 응답 생성
        prompt = f"""
다음 작업 결과들을 바탕으로 사용자에게 친근하고 유용한 응답을 생성하세요:

작업 결과: {json.dumps(previous_results, ensure_ascii=False)}

응답 요구사항:
1. 한국어로 작성
2. 비기술적이고 이해하기 쉬운 설명
3. 구체적인 수치나 데이터 포함
4. 필요시 다음 단계 제안

응답을 생성하세요.
"""
        
        return await self._call_llm(prompt, "gpt-4")
    
    async def _call_llm(self, prompt: str, model: str = "gpt-4") -> str:
        """LLM 호출"""
        
        if model.startswith("gpt"):
            response = self.openai_client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            return response.choices[0].message.content
        
        elif model.startswith("claude"):
            response = self.claude_client.messages.create(
                model=model,
                max_tokens=2000,
                system=self.system_prompt,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return response.content[0].text
        
        else:
            raise ValueError(f"지원하지 않는 모델: {model}")
    
    async def _format_response(self, result: Dict, user_input: str) -> str:
        """최종 응답 포맷팅"""
        
        # 결과에서 사용자 응답 추출
        for key, value in result.items():
            if key.startswith("step_") and isinstance(value, str) and len(value) > 10:
                return value
        
        # 기본 응답 생성
        return "요청하신 작업을 완료했습니다. 추가로 도움이 필요하시면 말씀해 주세요."


# 전역 코파일럿 인스턴스
copilot = ERPAICopilot()


async def process_ai_request(user_input: str, user_context: Dict = None) -> Dict[str, Any]:
    """AI 요청 처리 (외부 API용)"""
    return await copilot.process_request(user_input, user_context)