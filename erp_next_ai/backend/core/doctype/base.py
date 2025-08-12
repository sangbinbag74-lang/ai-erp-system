"""
ERPNext 스타일 DocType 시스템의 기본 클래스
"""
from typing import Dict, List, Any, Optional
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Text, Boolean, Integer, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
import json

Base = declarative_base()


class DocTypeField:
    """DocType 필드 정의"""
    
    def __init__(self, definition: Dict[str, Any]):
        self.fieldname = definition.get('fieldname')
        self.fieldtype = definition.get('fieldtype')
        self.label = definition.get('label')
        self.required = definition.get('reqd', 0)
        self.options = definition.get('options')
        self.default = definition.get('default')
        self.length = definition.get('length')
        self.precision = definition.get('precision')
        self.read_only = definition.get('read_only', 0)
        self.hidden = definition.get('hidden', 0)


class DocTypeBase:
    """ERPNext 스타일 DocType 기본 클래스"""
    
    # 표준 메타데이터 필드
    name = Column(String(140), primary_key=True)
    creation = Column(DateTime, default=datetime.utcnow)
    modified = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    modified_by = Column(String(140))
    owner = Column(String(140))
    docstatus = Column(Integer, default=0)  # 0=Draft, 1=Submitted, 2=Cancelled
    idx = Column(Integer, default=0)
    
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    def to_dict(self) -> Dict[str, Any]:
        """객체를 딕셔너리로 변환"""
        result = {}
        for column in self.__table__.columns:
            value = getattr(self, column.name)
            if isinstance(value, datetime):
                value = value.isoformat()
            result[column.name] = value
        return result
    
    def from_dict(self, data: Dict[str, Any]):
        """딕셔너리에서 객체 업데이트"""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    def validate(self) -> List[str]:
        """데이터 유효성 검사"""
        errors = []
        
        # 필수 필드 검사
        for field_name in self.get_required_fields():
            value = getattr(self, field_name, None)
            if value is None or (isinstance(value, str) and not value.strip()):
                errors.append(f"{field_name}은(는) 필수 항목입니다.")
        
        return errors
    
    def get_required_fields(self) -> List[str]:
        """필수 필드 목록 반환 (서브클래스에서 구현)"""
        return []
    
    def save(self, db: Session):
        """문서 저장"""
        errors = self.validate()
        if errors:
            raise ValueError(f"유효성 검사 실패: {', '.join(errors)}")
        
        self.modified = datetime.utcnow()
        db.add(self)
        db.commit()
        db.refresh(self)
        return self
    
    def submit(self, db: Session):
        """문서 제출 (승인)"""
        if self.docstatus != 0:
            raise ValueError("초안 상태의 문서만 제출할 수 있습니다.")
        
        self.docstatus = 1
        return self.save(db)
    
    def cancel(self, db: Session):
        """문서 취소"""
        if self.docstatus != 1:
            raise ValueError("제출된 문서만 취소할 수 있습니다.")
        
        self.docstatus = 2
        return self.save(db)


class DocTypeMeta:
    """DocType 메타데이터 관리"""
    
    def __init__(self, definition: Dict[str, Any]):
        self.name = definition.get('name')
        self.module = definition.get('module')
        self.autoname = definition.get('autoname')
        self.title_field = definition.get('title_field')
        self.search_fields = definition.get('search_fields', [])
        self.sort_field = definition.get('sort_field', 'modified')
        self.sort_order = definition.get('sort_order', 'DESC')
        self.is_submittable = definition.get('is_submittable', 0)
        self.fields = [DocTypeField(field) for field in definition.get('fields', [])]
        self.permissions = definition.get('permissions', [])
    
    def get_field(self, fieldname: str) -> Optional[DocTypeField]:
        """필드명으로 필드 정보 조회"""
        for field in self.fields:
            if field.fieldname == fieldname:
                return field
        return None
    
    def get_list_fields(self) -> List[DocTypeField]:
        """목록 화면에 표시할 필드들"""
        return [field for field in self.fields if not field.hidden][:8]
    
    def get_form_fields(self) -> List[DocTypeField]:
        """폼 화면에 표시할 필드들"""
        return [field for field in self.fields if not field.hidden]


# DocType 레지스트리
DOCTYPE_REGISTRY = {}


def register_doctype(name: str, meta: DocTypeMeta, model_class: type):
    """DocType 등록"""
    DOCTYPE_REGISTRY[name] = {
        'meta': meta,
        'model': model_class
    }


def get_doctype_meta(name: str) -> Optional[DocTypeMeta]:
    """DocType 메타데이터 조회"""
    doctype_info = DOCTYPE_REGISTRY.get(name)
    return doctype_info['meta'] if doctype_info else None


def get_doctype_model(name: str) -> Optional[type]:
    """DocType 모델 클래스 조회"""
    doctype_info = DOCTYPE_REGISTRY.get(name)
    return doctype_info['model'] if doctype_info else None


def create_doctype_from_json(definition_path: str):
    """JSON 파일에서 DocType 생성"""
    with open(definition_path, 'r', encoding='utf-8') as f:
        definition = json.load(f)
    
    meta = DocTypeMeta(definition)
    
    # 동적으로 모델 클래스 생성
    attrs = {'__tablename__': f'tab{definition["name"].replace(" ", "")}'}
    
    # 필드를 SQLAlchemy 컬럼으로 변환
    for field in meta.fields:
        column = _create_column_from_field(field)
        if column:
            attrs[field.fieldname] = column
    
    # 기본 클래스와 합성
    model_class = type(
        definition['name'].replace(' ', ''),
        (DocTypeBase, Base),
        attrs
    )
    
    register_doctype(definition['name'], meta, model_class)
    return model_class


def _create_column_from_field(field: DocTypeField) -> Optional[Column]:
    """DocType 필드를 SQLAlchemy 컬럼으로 변환"""
    kwargs = {
        'nullable': not field.required
    }
    
    if field.fieldtype == 'Data':
        return Column(String(field.length or 140), **kwargs)
    elif field.fieldtype == 'Text':
        return Column(Text, **kwargs)
    elif field.fieldtype == 'Int':
        return Column(Integer, **kwargs)
    elif field.fieldtype == 'Float':
        return Column(Float(precision=field.precision or 6), **kwargs)
    elif field.fieldtype == 'Check':
        return Column(Boolean, default=0, **kwargs)
    elif field.fieldtype == 'Link':
        return Column(String(140), **kwargs)
    elif field.fieldtype == 'Select':
        return Column(String(140), **kwargs)
    elif field.fieldtype == 'Date':
        return Column(DateTime, **kwargs)
    elif field.fieldtype == 'Datetime':
        return Column(DateTime, **kwargs)
    else:
        return Column(Text, **kwargs)  # 기본값