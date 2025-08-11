"""
Translation Helper for AI ERP System
한글화 지원 유틸리티 모듈
"""

import json
import os
from typing import Dict, Optional, Union
from functools import lru_cache


class TranslationHelper:
    """
    한글 번역 헬퍼 클래스
    """
    
    def __init__(self, translations_file: str = None):
        if translations_file is None:
            # 기본 번역 파일 경로
            current_dir = os.path.dirname(__file__)
            translations_file = os.path.join(
                current_dir, '..', '..', 'config', 'field_translations.json'
            )
        
        self.translations_file = translations_file
        self._translations = self._load_translations()
    
    def _load_translations(self) -> Dict:
        """번역 파일 로드"""
        try:
            with open(self.translations_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Translation file not found: {self.translations_file}")
            return {}
        except json.JSONDecodeError as e:
            print(f"Error parsing translation file: {e}")
            return {}
    
    @lru_cache(maxsize=500)
    def translate_field(self, field_name: str, context: str = None) -> str:
        """
        필드명 번역
        
        Args:
            field_name: 번역할 필드명
            context: 컨텍스트 (예: 'file_manager', 'team_management')
        
        Returns:
            번역된 필드명 (번역이 없으면 원본 반환)
        """
        translations = self._translations.get('field_translations', {})
        
        # 컨텍스트별 번역 우선 검색
        if context and context in translations:
            context_translations = translations[context]
            if field_name in context_translations:
                return context_translations[field_name]
        
        # 공통 필드 번역 검색
        common_translations = translations.get('common_fields', {})
        if field_name in common_translations:
            return common_translations[field_name]
        
        # 번역이 없으면 원본 반환
        return field_name
    
    @lru_cache(maxsize=200)
    def translate_status(self, status: str) -> str:
        """상태값 번역"""
        status_translations = self._translations.get('status_translations', {})
        return status_translations.get(status.lower(), status)
    
    @lru_cache(maxsize=100)
    def translate_role(self, role: str) -> str:
        """역할명 번역"""
        role_translations = self._translations.get('role_translations', {})
        return role_translations.get(role.lower(), role)
    
    @lru_cache(maxsize=100)
    def translate_action(self, action: str) -> str:
        """액션명 번역"""
        action_translations = self._translations.get('action_translations', {})
        return action_translations.get(action.lower(), action)
    
    @lru_cache(maxsize=200)
    def translate_error(self, error_key: str) -> str:
        """오류 메시지 번역"""
        error_translations = self._translations.get('error_translations', {})
        return error_translations.get(error_key.lower(), error_key)
    
    def get_translated_fields(self, fields: Dict, context: str = None) -> Dict:
        """
        필드 딕셔너리의 키를 번역
        
        Args:
            fields: 번역할 필드 딕셔너리
            context: 컨텍스트
        
        Returns:
            번역된 키를 가진 딕셔너리
        """
        translated = {}
        for key, value in fields.items():
            translated_key = self.translate_field(key, context)
            translated[translated_key] = value
        return translated
    
    def get_form_labels(self, form_fields: list, context: str = None) -> Dict[str, str]:
        """
        폼 필드에 대한 라벨 매핑 생성
        
        Args:
            form_fields: 필드명 리스트
            context: 컨텍스트
        
        Returns:
            {field_name: translated_label} 매핑
        """
        labels = {}
        for field in form_fields:
            labels[field] = self.translate_field(field, context)
        return labels
    
    def format_file_size(self, size_bytes: Union[int, float]) -> str:
        """파일 크기를 한국어로 포맷"""
        if size_bytes == 0:
            return "0 바이트"
        
        size_names = ["바이트", "KB", "MB", "GB", "TB"]
        i = 0
        while size_bytes >= 1024 and i < len(size_names) - 1:
            size_bytes /= 1024
            i += 1
        
        if i == 0:
            return f"{int(size_bytes)} {size_names[i]}"
        else:
            return f"{size_bytes:.1f} {size_names[i]}"
    
    def format_time_ago(self, datetime_obj) -> str:
        """시간을 '~전' 형식으로 포맷"""
        from datetime import datetime, timedelta
        
        if not datetime_obj:
            return ""
        
        now = datetime.now()
        if datetime_obj.tzinfo:
            now = now.replace(tzinfo=datetime_obj.tzinfo)
        
        diff = now - datetime_obj
        
        if diff.days > 365:
            years = diff.days // 365
            return f"{years}년 전"
        elif diff.days > 30:
            months = diff.days // 30
            return f"{months}개월 전"
        elif diff.days > 7:
            weeks = diff.days // 7
            return f"{weeks}주 전"
        elif diff.days > 0:
            return f"{diff.days}일 전"
        elif diff.seconds > 3600:
            hours = diff.seconds // 3600
            return f"{hours}시간 전"
        elif diff.seconds > 60:
            minutes = diff.seconds // 60
            return f"{minutes}분 전"
        else:
            return "방금"
    
    def get_validation_message(self, field_name: str, validation_type: str, context: str = None) -> str:
        """
        유효성 검사 메시지 생성
        
        Args:
            field_name: 필드명
            validation_type: 검사 유형 ('required', 'email', 'min_length' 등)
            context: 컨텍스트
        
        Returns:
            한글 유효성 검사 메시지
        """
        field_label = self.translate_field(field_name, context)
        
        validation_messages = {
            'required': f'{field_label}은(는) 필수 입력 항목입니다.',
            'email': f'{field_label}에 올바른 이메일 주소를 입력하세요.',
            'min_length': f'{field_label}이(가) 너무 짧습니다.',
            'max_length': f'{field_label}이(가) 너무 깁니다.',
            'numeric': f'{field_label}에 숫자만 입력하세요.',
            'unique': f'이미 사용 중인 {field_label}입니다.',
            'invalid_format': f'{field_label}의 형식이 올바르지 않습니다.',
        }
        
        return validation_messages.get(validation_type, f'{field_label} 입력이 올바르지 않습니다.')
    
    def reload_translations(self):
        """번역 파일 재로드"""
        self._translations = self._load_translations()
        # 캐시 클리어
        self.translate_field.cache_clear()
        self.translate_status.cache_clear()
        self.translate_role.cache_clear()
        self.translate_action.cache_clear()
        self.translate_error.cache_clear()


# 전역 번역 헬퍼 인스턴스
_translation_helper = None

def get_translation_helper() -> TranslationHelper:
    """전역 번역 헬퍼 인스턴스 가져오기"""
    global _translation_helper
    if _translation_helper is None:
        _translation_helper = TranslationHelper()
    return _translation_helper

def translate_field(field_name: str, context: str = None) -> str:
    """필드명 번역 (편의 함수)"""
    return get_translation_helper().translate_field(field_name, context)

def translate_status(status: str) -> str:
    """상태값 번역 (편의 함수)"""
    return get_translation_helper().translate_status(status)

def translate_role(role: str) -> str:
    """역할명 번역 (편의 함수)"""
    return get_translation_helper().translate_role(role)

def get_form_labels(form_fields: list, context: str = None) -> Dict[str, str]:
    """폼 라벨 생성 (편의 함수)"""
    return get_translation_helper().get_form_labels(form_fields, context)

def format_file_size(size_bytes: Union[int, float]) -> str:
    """파일 크기 포맷 (편의 함수)"""
    return get_translation_helper().format_file_size(size_bytes)

def format_time_ago(datetime_obj) -> str:
    """시간 포맷 (편의 함수)"""
    return get_translation_helper().format_time_ago(datetime_obj)