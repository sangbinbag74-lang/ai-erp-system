"""
AGI-level AI Core System for ERPNext
AI가 ERP의 핵심이 되어 모든 작업을 자율적으로 처리하는 시스템
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass
from enum import Enum

import openai
import anthropic
from sqlalchemy.orm import Session

from ..core.database import get_db_session
from ..core.config import settings

# 로깅 설정
logger = logging.getLogger(__name__)

class TaskPriority(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    ESCALATED = "escalated"

@dataclass
class AITask:
    """AI가 처리해야 할 작업 정의"""
    id: str
    user_id: str
    description: str
    context: Dict[str, Any]
    priority: TaskPriority
    status: TaskStatus
    created_at: datetime
    updated_at: datetime
    files_involved: List[str] = None
    error_count: int = 0
    result: Dict[str, Any] = None

class AGICore:
    """AGI 수준의 자율적 AI 시스템"""
    
    def __init__(self):
        self.openai_client = openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.anthropic_client = anthropic.AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)
        self.active_tasks: Dict[str, AITask] = {}
        self.learning_database = {}
        self.workflow_patterns = {}
        
    async def process_natural_language_request(self, user_message: str, user_id: str, context: Dict = None) -> Dict[str, Any]:
        """
        자연어 요청을 분석하고 자율적으로 처리
        Chain of Thought 방식으로 복잡한 작업을 단계별 분해
        """
        try:
            # 1. 의도 분석 (Intent Analysis)
            intent_analysis = await self._analyze_intent(user_message, context or {})
            
            # 2. 작업 계획 수립 (Task Planning)
            task_plan = await self._create_task_plan(intent_analysis)
            
            # 3. 자율적 실행 (Autonomous Execution)
            execution_result = await self._execute_autonomous_plan(task_plan, user_id)
            
            # 4. 결과 검증 및 개선 (Validation & Improvement)
            final_result = await self._validate_and_improve(execution_result)
            
            # 5. 학습 및 패턴 저장 (Learning)
            await self._learn_from_interaction(user_message, final_result)
            
            return {
                "success": True,
                "result": final_result,
                "explanation": await self._generate_explanation(final_result),
                "confidence": final_result.get("confidence", 0.8),
                "execution_time": final_result.get("execution_time"),
                "actions_taken": final_result.get("actions_taken", [])
            }
            
        except Exception as e:
            logger.error(f"AGI 처리 중 오류: {e}")
            return await self._handle_error(e, user_message, user_id)
    
    async def _analyze_intent(self, message: str, context: Dict) -> Dict[str, Any]:
        """의도 분석 - 사용자가 무엇을 원하는지 정확히 파악"""
        
        system_prompt = """
        당신은 ERPNext AI 시스템의 의도 분석 전문가입니다.
        사용자의 자연어 요청을 분석하여 다음을 정확히 파악하세요:
        
        1. 핵심 의도 (Intent): 사용자가 달성하고자 하는 목표
        2. 관련 모듈 (Module): ERPNext의 어떤 모듈이 관련되는지
        3. 필요한 데이터 (Data): 어떤 데이터가 필요한지
        4. 파일 작업 (File Operations): 파일 관련 작업이 있는지
        5. 자동화 범위 (Automation Scope): 얼마나 자동화할 수 있는지
        6. 우선순위 (Priority): 작업의 우선순위
        
        응답은 반드시 JSON 형식으로 제공하세요.
        """
        
        try:
            response = await self.openai_client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"요청: {message}\n컨텍스트: {json.dumps(context, ensure_ascii=False)}"}
                ],
                temperature=0.1,
                max_tokens=2000
            )
            
            intent_data = json.loads(response.choices[0].message.content)
            
            return {
                "intent": intent_data.get("intent", "unknown"),
                "modules": intent_data.get("modules", []),
                "data_needed": intent_data.get("data_needed", []),
                "file_operations": intent_data.get("file_operations", []),
                "automation_scope": intent_data.get("automation_scope", "partial"),
                "priority": intent_data.get("priority", "medium"),
                "complexity": intent_data.get("complexity", "medium"),
                "estimated_steps": intent_data.get("estimated_steps", 1)
            }
            
        except Exception as e:
            logger.error(f"의도 분석 오류: {e}")
            return {"intent": "clarification_needed", "error": str(e)}
    
    async def _create_task_plan(self, intent_analysis: Dict) -> Dict[str, Any]:
        """Chain of Thought 방식으로 작업 계획 수립"""
        
        planning_prompt = f"""
        ERPNext AI 시스템의 작업 계획 수립자로서, 다음 의도 분석을 바탕으로 
        상세한 실행 계획을 Chain of Thought 방식으로 수립하세요:
        
        의도 분석: {json.dumps(intent_analysis, ensure_ascii=False)}
        
        다음 구조로 계획을 수립하세요:
        1. 전체 목표 분해 (Goal Decomposition)
        2. 단계별 작업 (Step-by-Step Tasks)
        3. 필요한 리소스 (Required Resources)
        4. 예상 결과 (Expected Outcomes)
        5. 오류 처리 방안 (Error Handling)
        6. 검증 방법 (Validation Methods)
        
        각 단계는 구체적이고 실행 가능해야 합니다.
        """
        
        try:
            response = await self.anthropic_client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=3000,
                temperature=0.2,
                messages=[
                    {"role": "user", "content": planning_prompt}
                ]
            )
            
            plan_text = response.content[0].text
            
            # 계획을 구조화된 형태로 파싱
            return {
                "plan_text": plan_text,
                "steps": await self._parse_execution_steps(plan_text),
                "resources_needed": intent_analysis.get("data_needed", []),
                "estimated_duration": self._estimate_duration(intent_analysis),
                "risk_level": self._assess_risk(intent_analysis),
                "success_criteria": await self._define_success_criteria(intent_analysis)
            }
            
        except Exception as e:
            logger.error(f"작업 계획 수립 오류: {e}")
            return {"error": str(e), "fallback_plan": "manual_execution_required"}
    
    async def _execute_autonomous_plan(self, task_plan: Dict, user_id: str) -> Dict[str, Any]:
        """계획을 자율적으로 실행"""
        
        execution_log = []
        results = {}
        start_time = datetime.now()
        
        try:
            steps = task_plan.get("steps", [])
            
            for i, step in enumerate(steps):
                step_start = datetime.now()
                
                logger.info(f"실행 중: 단계 {i+1}/{len(steps)} - {step.get('description', 'Unknown')}")
                
                # 각 단계 실행
                step_result = await self._execute_step(step, user_id, results)
                
                step_duration = (datetime.now() - step_start).total_seconds()
                
                execution_log.append({
                    "step": i + 1,
                    "description": step.get("description"),
                    "result": step_result,
                    "duration": step_duration,
                    "timestamp": datetime.now().isoformat()
                })
                
                # 단계 결과를 다음 단계에서 사용할 수 있도록 저장
                results[f"step_{i+1}"] = step_result
                
                # 오류 발생 시 자가 진단 및 복구 시도
                if not step_result.get("success", False):
                    recovery_result = await self._attempt_recovery(step, step_result)
                    if recovery_result.get("success"):
                        step_result = recovery_result
                        execution_log[-1]["recovery_attempted"] = True
                        execution_log[-1]["result"] = step_result
                    else:
                        # 복구 실패 시 에스컬레이션
                        break
            
            total_duration = (datetime.now() - start_time).total_seconds()
            
            return {
                "success": True,
                "execution_log": execution_log,
                "final_results": results,
                "execution_time": total_duration,
                "actions_taken": [log["description"] for log in execution_log],
                "confidence": self._calculate_confidence(execution_log)
            }
            
        except Exception as e:
            logger.error(f"자율 실행 오류: {e}")
            return {
                "success": False,
                "error": str(e),
                "execution_log": execution_log,
                "partial_results": results
            }
    
    async def _execute_step(self, step: Dict, user_id: str, previous_results: Dict) -> Dict[str, Any]:
        """개별 단계 실행"""
        
        step_type = step.get("type", "analysis")
        
        if step_type == "file_operation":
            return await self._execute_file_operation(step, user_id)
        elif step_type == "data_query":
            return await self._execute_data_query(step, previous_results)
        elif step_type == "data_modification":
            return await self._execute_data_modification(step, previous_results)
        elif step_type == "workflow_automation":
            return await self._execute_workflow_automation(step, user_id)
        elif step_type == "email_communication":
            return await self._execute_email_communication(step, previous_results)
        elif step_type == "report_generation":
            return await self._execute_report_generation(step, previous_results)
        else:
            # 기본적인 분석/처리 작업
            return await self._execute_analysis_step(step, previous_results)
    
    async def _execute_file_operation(self, step: Dict, user_id: str) -> Dict[str, Any]:
        """파일 불러오기, 수정, 설명 기능 구현"""
        
        operation = step.get("operation", "read")
        file_path = step.get("file_path")
        
        try:
            if operation == "read":
                # 파일 읽기 및 분석
                file_content = await self._read_file(file_path)
                analysis = await self._analyze_file_content(file_content, step.get("analysis_request"))
                
                return {
                    "success": True,
                    "operation": "read",
                    "file_path": file_path,
                    "content_summary": analysis.get("summary"),
                    "insights": analysis.get("insights"),
                    "file_type": analysis.get("file_type")
                }
                
            elif operation == "modify":
                # 파일 수정
                modification_request = step.get("modification_request")
                current_content = await self._read_file(file_path)
                
                modified_content = await self._modify_file_content(
                    current_content, 
                    modification_request,
                    step.get("modification_params", {})
                )
                
                # 수정된 내용 저장
                await self._save_file(file_path, modified_content)
                
                # 변경 사항 설명 생성
                explanation = await self._explain_file_changes(
                    current_content, 
                    modified_content, 
                    modification_request
                )
                
                return {
                    "success": True,
                    "operation": "modify",
                    "file_path": file_path,
                    "changes_made": explanation.get("changes"),
                    "reasoning": explanation.get("reasoning"),
                    "impact_analysis": explanation.get("impact")
                }
                
            elif operation == "create":
                # 새 파일 생성
                content_spec = step.get("content_specification")
                new_content = await self._generate_file_content(content_spec)
                
                await self._save_file(file_path, new_content)
                
                return {
                    "success": True,
                    "operation": "create",
                    "file_path": file_path,
                    "content_preview": new_content[:500] + "..." if len(new_content) > 500 else new_content,
                    "file_size": len(new_content)
                }
                
        except Exception as e:
            logger.error(f"파일 작업 오류: {e}")
            return {
                "success": False,
                "error": str(e),
                "operation": operation,
                "file_path": file_path
            }
    
    async def _analyze_file_content(self, content: str, analysis_request: str) -> Dict[str, Any]:
        """AI를 사용한 파일 내용 분석"""
        
        analysis_prompt = f"""
        다음 파일 내용을 분석하세요:
        
        내용: {content[:2000]}...
        
        분석 요청: {analysis_request}
        
        다음 형태로 분석 결과를 제공하세요:
        1. 파일 유형 및 구조
        2. 주요 내용 요약
        3. 데이터 인사이트
        4. 개선 제안사항
        5. 주의사항
        """
        
        try:
            response = await self.openai_client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[
                    {"role": "system", "content": "당신은 ERPNext의 파일 분석 전문가입니다."},
                    {"role": "user", "content": analysis_prompt}
                ],
                temperature=0.3,
                max_tokens=2000
            )
            
            analysis_text = response.choices[0].message.content
            
            return {
                "summary": self._extract_summary(analysis_text),
                "insights": self._extract_insights(analysis_text),
                "file_type": self._detect_file_type(content),
                "full_analysis": analysis_text
            }
            
        except Exception as e:
            logger.error(f"파일 분석 오류: {e}")
            return {"error": str(e)}
    
    async def _attempt_recovery(self, failed_step: Dict, error_result: Dict) -> Dict[str, Any]:
        """오류 발생 시 자가 진단 및 복구 시도"""
        
        recovery_prompt = f"""
        ERPNext AI 시스템에서 다음 작업이 실패했습니다:
        
        실패한 작업: {json.dumps(failed_step, ensure_ascii=False)}
        오류 결과: {json.dumps(error_result, ensure_ascii=False)}
        
        자가 진단을 수행하고 복구 방안을 제시하세요:
        1. 오류 원인 분석
        2. 복구 가능 여부
        3. 대안 접근 방법
        4. 예방 조치
        """
        
        try:
            response = await self.anthropic_client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=1500,
                temperature=0.1,
                messages=[
                    {"role": "user", "content": recovery_prompt}
                ]
            )
            
            recovery_analysis = response.content[0].text
            
            # 복구 시도 실행
            if "복구 가능" in recovery_analysis:
                # 실제 복구 로직 실행
                return await self._execute_recovery_action(failed_step, recovery_analysis)
            else:
                return {
                    "success": False,
                    "recovery_attempted": True,
                    "analysis": recovery_analysis,
                    "escalation_required": True
                }
                
        except Exception as e:
            logger.error(f"복구 시도 오류: {e}")
            return {"success": False, "recovery_error": str(e)}
    
    async def _learn_from_interaction(self, user_message: str, result: Dict):
        """사용자 상호작용에서 학습하여 모델 개선"""
        
        learning_data = {
            "timestamp": datetime.now().isoformat(),
            "user_input": user_message,
            "result": result,
            "success": result.get("success", False),
            "confidence": result.get("confidence", 0.0),
            "execution_time": result.get("execution_time", 0),
            "user_feedback": None  # 추후 피드백 수집
        }
        
        # 학습 데이터베이스에 저장
        interaction_id = f"interaction_{len(self.learning_database)}"
        self.learning_database[interaction_id] = learning_data
        
        # 패턴 분석 및 워크플로 개선
        await self._update_workflow_patterns(user_message, result)
        
        logger.info(f"학습 데이터 저장: {interaction_id}")
    
    async def _update_workflow_patterns(self, user_input: str, result: Dict):
        """워크플로 패턴 업데이트"""
        
        # 자주 사용되는 패턴 식별
        pattern_key = self._extract_pattern_key(user_input)
        
        if pattern_key not in self.workflow_patterns:
            self.workflow_patterns[pattern_key] = {
                "count": 0,
                "success_rate": 0.0,
                "avg_execution_time": 0.0,
                "common_steps": [],
                "optimization_suggestions": []
            }
        
        pattern = self.workflow_patterns[pattern_key]
        pattern["count"] += 1
        
        if result.get("success"):
            pattern["success_rate"] = (pattern["success_rate"] * (pattern["count"] - 1) + 1.0) / pattern["count"]
        else:
            pattern["success_rate"] = (pattern["success_rate"] * (pattern["count"] - 1)) / pattern["count"]
        
        execution_time = result.get("execution_time", 0)
        pattern["avg_execution_time"] = (pattern["avg_execution_time"] * (pattern["count"] - 1) + execution_time) / pattern["count"]
        
        # 패턴 기반 최적화 제안
        if pattern["count"] >= 5:
            await self._generate_optimization_suggestions(pattern_key, pattern)

# AI 코어 인스턴스 생성
agi_core = AGICore()

async def process_agi_request(user_message: str, user_id: str, context: Dict = None) -> Dict[str, Any]:
    """AGI 요청 처리 메인 함수"""
    return await agi_core.process_natural_language_request(user_message, user_id, context)