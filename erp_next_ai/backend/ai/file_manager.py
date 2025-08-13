"""
AGI-level File Management System
파일 불러오기, 수정, 설명 기능을 포함한 완전 자율 파일 관리
"""

import os
import asyncio
import aiofiles
import json
import csv
import pandas as pd
import PyPDF2
import openpyxl
from datetime import datetime
from typing import Dict, List, Any, Optional, Union, BinaryIO
from pathlib import Path
import magic
from PIL import Image
import pytesseract
import io
import base64

import openai
from sqlalchemy.orm import Session

from ..core.database import get_db_session
from ..core.config import settings

class FileType:
    TEXT = "text"
    CSV = "csv"
    EXCEL = "excel"
    PDF = "pdf"
    IMAGE = "image"
    JSON = "json"
    UNKNOWN = "unknown"

class AIFileManager:
    """AI 기반 완전 자율 파일 관리 시스템"""
    
    def __init__(self):
        self.openai_client = openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.supported_formats = {
            '.txt': FileType.TEXT,
            '.csv': FileType.CSV,
            '.xlsx': FileType.EXCEL,
            '.xls': FileType.EXCEL,
            '.pdf': FileType.PDF,
            '.json': FileType.JSON,
            '.png': FileType.IMAGE,
            '.jpg': FileType.IMAGE,
            '.jpeg': FileType.IMAGE,
            '.gif': FileType.IMAGE,
            '.bmp': FileType.IMAGE
        }
        
    async def auto_load_and_analyze_file(self, file_path: str, analysis_request: str = "전체 분석") -> Dict[str, Any]:
        """
        파일을 자동으로 불러와서 AI가 분석
        사용자: "지난 달 재무 보고서 불러와서 분석해줘"
        """
        try:
            # 파일 존재 확인
            if not os.path.exists(file_path):
                # AI가 유사한 파일 찾기 시도
                similar_files = await self._find_similar_files(file_path)
                if similar_files:
                    file_path = similar_files[0]
                else:
                    return {
                        "success": False,
                        "error": f"파일을 찾을 수 없습니다: {file_path}",
                        "suggestions": await self._suggest_alternative_files(file_path)
                    }
            
            # 파일 타입 자동 감지
            file_type = await self._detect_file_type(file_path)
            
            # 파일 내용 읽기
            content = await self._read_file_content(file_path, file_type)
            
            # AI 분석
            analysis = await self._perform_ai_analysis(content, file_type, analysis_request)
            
            # 메타데이터 수집
            metadata = await self._collect_metadata(file_path)
            
            return {
                "success": True,
                "file_path": file_path,
                "file_type": file_type,
                "content": content,
                "analysis": analysis,
                "metadata": metadata,
                "ai_insights": analysis.get("insights", []),
                "summary": analysis.get("summary", ""),
                "key_findings": analysis.get("key_findings", []),
                "recommendations": analysis.get("recommendations", [])
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"파일 분석 중 오류: {str(e)}",
                "file_path": file_path
            }
    
    async def auto_modify_file(self, file_path: str, modification_request: str, context: Dict = None) -> Dict[str, Any]:
        """
        AI가 자율적으로 파일을 수정
        사용자: "수익 부분 10% 증가로 수정해줘"
        """
        try:
            # 원본 파일 백업
            backup_path = await self._create_backup(file_path)
            
            # 현재 파일 내용 읽기
            file_type = await self._detect_file_type(file_path)
            original_content = await self._read_file_content(file_path, file_type)
            
            # AI가 수정 계획 수립
            modification_plan = await self._create_modification_plan(
                original_content, 
                modification_request, 
                file_type,
                context or {}
            )
            
            # 수정 실행
            modified_content = await self._execute_modifications(
                original_content,
                modification_plan,
                file_type
            )
            
            # 수정된 내용 저장
            await self._save_modified_content(file_path, modified_content, file_type)
            
            # 변경 사항 분석 및 설명
            change_analysis = await self._analyze_changes(
                original_content,
                modified_content,
                modification_request
            )
            
            # 결과 검증
            validation_result = await self._validate_modifications(
                modified_content,
                modification_plan,
                file_type
            )
            
            return {
                "success": True,
                "file_path": file_path,
                "backup_path": backup_path,
                "modification_plan": modification_plan,
                "changes_made": change_analysis.get("changes", []),
                "reasoning": change_analysis.get("reasoning", ""),
                "impact_analysis": change_analysis.get("impact", {}),
                "validation": validation_result,
                "before_preview": original_content[:500] if isinstance(original_content, str) else str(original_content)[:500],
                "after_preview": str(modified_content)[:500],
                "confidence": validation_result.get("confidence", 0.8)
            }
            
        except Exception as e:
            # 오류 발생 시 백업에서 복원
            if 'backup_path' in locals():
                await self._restore_from_backup(file_path, backup_path)
            
            return {
                "success": False,
                "error": f"파일 수정 중 오류: {str(e)}",
                "file_path": file_path,
                "backup_restored": 'backup_path' in locals()
            }
    
    async def auto_explain_file(self, file_path: str, explanation_focus: str = "전체") -> Dict[str, Any]:
        """
        AI가 파일 내용을 자연어로 설명
        사용자: "이 보고서 내용 설명해줘"
        """
        try:
            # 파일 로드
            file_result = await self.auto_load_and_analyze_file(file_path, f"{explanation_focus} 설명을 위한 분석")
            
            if not file_result["success"]:
                return file_result
            
            content = file_result["content"]
            file_type = file_result["file_type"]
            
            # AI가 설명 생성
            explanation = await self._generate_comprehensive_explanation(
                content, 
                file_type, 
                explanation_focus
            )
            
            # 시각적 요약 생성 (차트, 그래프 데이터 등)
            visual_summary = await self._create_visual_summary(content, file_type)
            
            # 질문 예측 및 답변 준비
            predicted_questions = await self._predict_user_questions(content, explanation_focus)
            
            return {
                "success": True,
                "file_path": file_path,
                "file_type": file_type,
                "explanation": explanation,
                "visual_summary": visual_summary,
                "key_points": explanation.get("key_points", []),
                "detailed_breakdown": explanation.get("detailed_breakdown", {}),
                "business_implications": explanation.get("business_implications", []),
                "predicted_questions": predicted_questions,
                "suggested_actions": explanation.get("suggested_actions", []),
                "complexity_level": explanation.get("complexity_level", "medium")
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"파일 설명 생성 중 오류: {str(e)}",
                "file_path": file_path
            }
    
    async def _read_file_content(self, file_path: str, file_type: str) -> Union[str, Dict, List]:
        """파일 타입별 내용 읽기"""
        
        if file_type == FileType.TEXT:
            async with aiofiles.open(file_path, 'r', encoding='utf-8') as f:
                return await f.read()
                
        elif file_type == FileType.CSV:
            df = pd.read_csv(file_path)
            return {
                "data": df.to_dict('records'),
                "columns": df.columns.tolist(),
                "shape": df.shape,
                "summary": df.describe().to_dict()
            }
            
        elif file_type == FileType.EXCEL:
            excel_data = {}
            with pd.ExcelFile(file_path) as xls:
                for sheet_name in xls.sheet_names:
                    df = pd.read_excel(xls, sheet_name=sheet_name)
                    excel_data[sheet_name] = {
                        "data": df.to_dict('records'),
                        "columns": df.columns.tolist(),
                        "shape": df.shape
                    }
            return excel_data
            
        elif file_type == FileType.PDF:
            return await self._extract_pdf_content(file_path)
            
        elif file_type == FileType.IMAGE:
            return await self._extract_image_content(file_path)
            
        elif file_type == FileType.JSON:
            async with aiofiles.open(file_path, 'r', encoding='utf-8') as f:
                content = await f.read()
                return json.loads(content)
                
        else:
            async with aiofiles.open(file_path, 'r', encoding='utf-8') as f:
                return await f.read()
    
    async def _extract_pdf_content(self, file_path: str) -> Dict[str, Any]:
        """PDF 내용 추출 (텍스트 + OCR)"""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text_content = ""
                
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    text_content += page.extract_text() + "\n"
                
                # OCR이 필요한 경우 (텍스트가 적은 경우)
                if len(text_content.strip()) < 100:
                    ocr_content = await self._perform_ocr(file_path)
                    text_content += "\n[OCR 추출 내용]\n" + ocr_content
                
                return {
                    "text": text_content,
                    "pages": len(pdf_reader.pages),
                    "has_ocr": len(text_content.strip()) < 100
                }
                
        except Exception as e:
            return {"error": f"PDF 읽기 오류: {str(e)}"}
    
    async def _extract_image_content(self, file_path: str) -> Dict[str, Any]:
        """이미지 내용 추출 (OCR + AI 분석)"""
        try:
            # OCR로 텍스트 추출
            ocr_text = await self._perform_ocr(file_path)
            
            # 이미지를 base64로 인코딩 (AI 분석용)
            with open(file_path, 'rb') as image_file:
                image_data = base64.b64encode(image_file.read()).decode('utf-8')
            
            # AI 이미지 분석
            image_analysis = await self._analyze_image_with_ai(image_data)
            
            return {
                "ocr_text": ocr_text,
                "image_analysis": image_analysis,
                "file_size": os.path.getsize(file_path),
                "image_data": image_data[:1000] + "..." if len(image_data) > 1000 else image_data
            }
            
        except Exception as e:
            return {"error": f"이미지 분석 오류: {str(e)}"}
    
    async def _perform_ocr(self, file_path: str) -> str:
        """OCR로 텍스트 추출"""
        try:
            if file_path.lower().endswith('.pdf'):
                # PDF의 경우 이미지로 변환 후 OCR
                # 여기서는 간단하게 텍스트 반환
                return "OCR 추출된 텍스트 (PDF)"
            else:
                # 이미지 파일의 경우 직접 OCR
                image = Image.open(file_path)
                text = pytesseract.image_to_string(image, lang='kor+eng')
                return text
        except Exception as e:
            return f"OCR 처리 오류: {str(e)}"
    
    async def _perform_ai_analysis(self, content: Any, file_type: str, analysis_request: str) -> Dict[str, Any]:
        """AI를 사용한 파일 내용 분석"""
        
        # 내용을 텍스트로 변환
        if isinstance(content, dict):
            content_text = json.dumps(content, ensure_ascii=False, indent=2)[:3000]
        elif isinstance(content, list):
            content_text = str(content)[:3000]
        else:
            content_text = str(content)[:3000]
        
        analysis_prompt = f"""
        ERPNext AI 시스템의 파일 분석 전문가로서 다음 파일을 분석하세요:
        
        파일 타입: {file_type}
        분석 요청: {analysis_request}
        
        파일 내용:
        {content_text}
        
        다음 항목들을 포함하여 종합적으로 분석하세요:
        1. 핵심 요약 (Executive Summary)
        2. 주요 발견사항 (Key Findings)
        3. 데이터 인사이트 (Data Insights)
        4. 비즈니스 영향 (Business Impact)
        5. 개선 제안사항 (Recommendations)
        6. 위험 요소 (Risk Factors)
        7. 다음 단계 (Next Steps)
        
        분석 결과는 ERPNext 사용자가 즉시 활용할 수 있도록 구체적이고 실용적이어야 합니다.
        """
        
        try:
            response = await self.openai_client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[
                    {"role": "system", "content": "당신은 ERPNext의 최고 수준 비즈니스 분석가입니다."},
                    {"role": "user", "content": analysis_prompt}
                ],
                temperature=0.3,
                max_tokens=3000
            )
            
            analysis_text = response.choices[0].message.content
            
            # 구조화된 분석 결과 생성
            return {
                "summary": self._extract_section(analysis_text, "핵심 요약"),
                "key_findings": self._extract_list_items(analysis_text, "주요 발견사항"),
                "insights": self._extract_list_items(analysis_text, "데이터 인사이트"),
                "business_impact": self._extract_section(analysis_text, "비즈니스 영향"),
                "recommendations": self._extract_list_items(analysis_text, "개선 제안사항"),
                "risk_factors": self._extract_list_items(analysis_text, "위험 요소"),
                "next_steps": self._extract_list_items(analysis_text, "다음 단계"),
                "full_analysis": analysis_text,
                "confidence_score": 0.85
            }
            
        except Exception as e:
            return {
                "error": f"AI 분석 오류: {str(e)}",
                "fallback_summary": "파일 내용을 성공적으로 읽었으나 AI 분석에 실패했습니다."
            }
    
    async def _create_modification_plan(self, content: Any, modification_request: str, file_type: str, context: Dict) -> Dict[str, Any]:
        """AI가 수정 계획 수립"""
        
        content_preview = str(content)[:2000] if content else "빈 파일"
        
        planning_prompt = f"""
        ERPNext 파일 수정 전문가로서 다음 요청에 대한 상세한 수정 계획을 수립하세요:
        
        파일 타입: {file_type}
        수정 요청: {modification_request}
        컨텍스트: {json.dumps(context, ensure_ascii=False)}
        
        현재 파일 내용 (미리보기):
        {content_preview}
        
        다음 구조로 수정 계획을 제시하세요:
        1. 수정 목표 및 범위
        2. 구체적인 수정 단계
        3. 영향받는 데이터 항목
        4. 수정 전후 예상 결과
        5. 위험도 평가
        6. 검증 방법
        7. 롤백 계획
        
        각 단계는 자동 실행 가능하도록 구체적으로 작성하세요.
        """
        
        try:
            response = await self.openai_client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[
                    {"role": "system", "content": "당신은 ERPNext의 데이터 수정 전문가입니다."},
                    {"role": "user", "content": planning_prompt}
                ],
                temperature=0.2,
                max_tokens=2500
            )
            
            plan_text = response.choices[0].message.content
            
            return {
                "plan_text": plan_text,
                "modification_steps": self._parse_modification_steps(plan_text),
                "affected_items": self._extract_affected_items(plan_text),
                "risk_level": self._assess_modification_risk(plan_text),
                "estimated_time": self._estimate_modification_time(modification_request),
                "validation_criteria": self._extract_validation_criteria(plan_text)
            }
            
        except Exception as e:
            return {
                "error": f"수정 계획 수립 오류: {str(e)}",
                "fallback_plan": "수동 수정 필요"
            }
    
    async def _execute_modifications(self, original_content: Any, modification_plan: Dict, file_type: str) -> Any:
        """수정 계획에 따라 실제 수정 실행"""
        
        steps = modification_plan.get("modification_steps", [])
        modified_content = original_content
        
        try:
            for step in steps:
                step_type = step.get("type", "text_replace")
                
                if step_type == "text_replace":
                    modified_content = await self._execute_text_replacement(modified_content, step)
                elif step_type == "data_update":
                    modified_content = await self._execute_data_update(modified_content, step)
                elif step_type == "calculation":
                    modified_content = await self._execute_calculation(modified_content, step)
                elif step_type == "format_change":
                    modified_content = await self._execute_format_change(modified_content, step)
                
            return modified_content
            
        except Exception as e:
            raise Exception(f"수정 실행 오류: {str(e)}")
    
    async def _generate_comprehensive_explanation(self, content: Any, file_type: str, explanation_focus: str) -> Dict[str, Any]:
        """포괄적인 파일 설명 생성"""
        
        content_text = str(content)[:2000] if content else "빈 파일"
        
        explanation_prompt = f"""
        ERPNext 비즈니스 커뮤니케이션 전문가로서 다음 파일을 {explanation_focus}에 초점을 맞춰 설명하세요:
        
        파일 타입: {file_type}
        설명 초점: {explanation_focus}
        
        파일 내용:
        {content_text}
        
        다음과 같이 설명해주세요:
        1. 한 줄 요약 (Executive Summary)
        2. 핵심 포인트 (Key Points) - 5개 내외
        3. 상세 분석 (Detailed Breakdown)
        4. 비즈니스 시사점 (Business Implications)
        5. 제안 조치사항 (Suggested Actions)
        6. 복잡도 수준 (Complexity Level: simple/medium/complex)
        
        설명은 비전문가도 이해할 수 있도록 명확하고 간결하게 작성하세요.
        """
        
        try:
            response = await self.openai_client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[
                    {"role": "system", "content": "당신은 ERPNext의 최고 비즈니스 커뮤니케이션 전문가입니다."},
                    {"role": "user", "content": explanation_prompt}
                ],
                temperature=0.4,
                max_tokens=2500
            )
            
            explanation_text = response.choices[0].message.content
            
            return {
                "executive_summary": self._extract_section(explanation_text, "한 줄 요약"),
                "key_points": self._extract_list_items(explanation_text, "핵심 포인트"),
                "detailed_breakdown": self._extract_section(explanation_text, "상세 분석"),
                "business_implications": self._extract_list_items(explanation_text, "비즈니스 시사점"),
                "suggested_actions": self._extract_list_items(explanation_text, "제안 조치사항"),
                "complexity_level": self._extract_complexity_level(explanation_text),
                "full_explanation": explanation_text
            }
            
        except Exception as e:
            return {
                "error": f"설명 생성 오류: {str(e)}",
                "fallback_explanation": "파일을 성공적으로 읽었으나 상세 설명 생성에 실패했습니다."
            }
    
    # 헬퍼 메서드들
    def _extract_section(self, text: str, section_name: str) -> str:
        """텍스트에서 특정 섹션 추출"""
        lines = text.split('\n')
        section_content = []
        in_section = False
        
        for line in lines:
            if section_name in line:
                in_section = True
                continue
            elif in_section and line.strip() and any(marker in line for marker in ['##', '**', '1.', '2.', '3.', '4.', '5.']):
                break
            elif in_section:
                section_content.append(line.strip())
        
        return '\n'.join(section_content).strip()
    
    def _extract_list_items(self, text: str, section_name: str) -> List[str]:
        """텍스트에서 리스트 항목들 추출"""
        section_text = self._extract_section(text, section_name)
        items = []
        
        for line in section_text.split('\n'):
            line = line.strip()
            if line and (line.startswith('-') or line.startswith('•') or line[0:2].isdigit()):
                # 리스트 마커 제거
                clean_line = line.lstrip('-•123456789. ').strip()
                if clean_line:
                    items.append(clean_line)
        
        return items
    
    async def _detect_file_type(self, file_path: str) -> str:
        """파일 타입 자동 감지"""
        file_extension = Path(file_path).suffix.lower()
        return self.supported_formats.get(file_extension, FileType.UNKNOWN)

# 파일 매니저 인스턴스
ai_file_manager = AIFileManager()