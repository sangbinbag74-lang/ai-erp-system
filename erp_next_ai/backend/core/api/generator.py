"""
DocType 기반 자동 API 생성기
ERPNext 스타일의 REST API를 자동으로 생성합니다.
"""
from typing import Dict, Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from core.database.connection import get_db
from core.doctype.base import get_doctype_meta, get_doctype_model, DOCTYPE_REGISTRY
from pydantic import BaseModel, create_model
import inspect


class APIGenerator:
    """DocType용 API 자동 생성기"""
    
    def __init__(self):
        self.routers = {}
    
    def generate_router(self, doctype_name: str) -> APIRouter:
        """특정 DocType용 라우터 생성"""
        if doctype_name in self.routers:
            return self.routers[doctype_name]
        
        meta = get_doctype_meta(doctype_name)
        model_class = get_doctype_model(doctype_name)
        
        if not meta or not model_class:
            raise ValueError(f"DocType '{doctype_name}'을 찾을 수 없습니다.")
        
        router = APIRouter(prefix=f"/api/{doctype_name.lower()}", tags=[doctype_name])
        
        # Pydantic 모델 생성
        pydantic_model = self._create_pydantic_model(meta)
        create_model_name = f"{doctype_name}Create"
        update_model_name = f"{doctype_name}Update"
        
        # Create 모델 (필수 필드만)
        create_fields = {}
        update_fields = {}
        
        for field in meta.fields:
            field_type = self._get_python_type(field.fieldtype)
            if field.required:
                create_fields[field.fieldname] = (field_type, ...)
            else:
                create_fields[field.fieldname] = (Optional[field_type], None)
            
            # Update 모델은 모든 필드가 선택적
            update_fields[field.fieldname] = (Optional[field_type], None)
        
        CreateModel = create_model(create_model_name, **create_fields)
        UpdateModel = create_model(update_model_name, **update_fields)
        
        # 1. 목록 조회 API
        @router.get("/", response_model=Dict[str, Any])
        async def list_documents(
            page: int = Query(1, ge=1),
            limit: int = Query(20, ge=1, le=100),
            search: Optional[str] = Query(None),
            filters: Optional[str] = Query(None),
            db: Session = Depends(get_db)
        ):
            """문서 목록 조회"""
            query = db.query(model_class)
            
            # 검색 조건 적용
            if search and meta.search_fields:
                search_conditions = []
                for field_name in meta.search_fields:
                    if hasattr(model_class, field_name):
                        field = getattr(model_class, field_name)
                        search_conditions.append(field.like(f"%{search}%"))
                
                if search_conditions:
                    from sqlalchemy import or_
                    query = query.filter(or_(*search_conditions))
            
            # 정렬
            sort_field = getattr(model_class, meta.sort_field, None)
            if sort_field:
                if meta.sort_order.upper() == 'DESC':
                    query = query.order_by(sort_field.desc())
                else:
                    query = query.order_by(sort_field.asc())
            
            # 페이징
            total = query.count()
            documents = query.offset((page - 1) * limit).limit(limit).all()
            
            return {
                "data": [doc.to_dict() for doc in documents],
                "total": total,
                "page": page,
                "limit": limit,
                "pages": (total + limit - 1) // limit
            }
        
        # 2. 단건 조회 API
        @router.get("/{name}", response_model=Dict[str, Any])
        async def get_document(name: str, db: Session = Depends(get_db)):
            """문서 단건 조회"""
            document = db.query(model_class).filter(model_class.name == name).first()
            if not document:
                raise HTTPException(status_code=404, detail="문서를 찾을 수 없습니다.")
            
            return document.to_dict()
        
        # 3. 생성 API
        @router.post("/", response_model=Dict[str, Any])
        async def create_document(data: CreateModel, db: Session = Depends(get_db)):
            """문서 생성"""
            try:
                # 이름 자동 생성 (간단한 구현)
                if not hasattr(data, 'name') or not data.name:
                    import uuid
                    name = f"{doctype_name}-{uuid.uuid4().hex[:8]}"
                else:
                    name = data.name
                
                document_data = data.dict()
                document_data['name'] = name
                
                document = model_class(**document_data)
                document = document.save(db)
                
                return document.to_dict()
                
            except ValueError as e:
                raise HTTPException(status_code=400, detail=str(e))
            except Exception as e:
                raise HTTPException(status_code=500, detail="문서 생성 중 오류가 발생했습니다.")
        
        # 4. 수정 API
        @router.put("/{name}", response_model=Dict[str, Any])
        async def update_document(
            name: str, 
            data: UpdateModel, 
            db: Session = Depends(get_db)
        ):
            """문서 수정"""
            document = db.query(model_class).filter(model_class.name == name).first()
            if not document:
                raise HTTPException(status_code=404, detail="문서를 찾을 수 없습니다.")
            
            try:
                # 수정된 필드만 업데이트
                update_data = {k: v for k, v in data.dict().items() if v is not None}
                document.from_dict(update_data)
                document = document.save(db)
                
                return document.to_dict()
                
            except ValueError as e:
                raise HTTPException(status_code=400, detail=str(e))
            except Exception as e:
                raise HTTPException(status_code=500, detail="문서 수정 중 오류가 발생했습니다.")
        
        # 5. 삭제 API
        @router.delete("/{name}")
        async def delete_document(name: str, db: Session = Depends(get_db)):
            """문서 삭제"""
            document = db.query(model_class).filter(model_class.name == name).first()
            if not document:
                raise HTTPException(status_code=404, detail="문서를 찾을 수 없습니다.")
            
            try:
                db.delete(document)
                db.commit()
                return {"message": "문서가 삭제되었습니다."}
                
            except Exception as e:
                db.rollback()
                raise HTTPException(status_code=500, detail="문서 삭제 중 오류가 발생했습니다.")
        
        # 6. 제출 API (제출 가능한 문서인 경우)
        if meta.is_submittable:
            @router.post("/{name}/submit")
            async def submit_document(name: str, db: Session = Depends(get_db)):
                """문서 제출"""
                document = db.query(model_class).filter(model_class.name == name).first()
                if not document:
                    raise HTTPException(status_code=404, detail="문서를 찾을 수 없습니다.")
                
                try:
                    document = document.submit(db)
                    return {"message": "문서가 제출되었습니다.", "data": document.to_dict()}
                except ValueError as e:
                    raise HTTPException(status_code=400, detail=str(e))
            
            @router.post("/{name}/cancel")
            async def cancel_document(name: str, db: Session = Depends(get_db)):
                """문서 취소"""
                document = db.query(model_class).filter(model_class.name == name).first()
                if not document:
                    raise HTTPException(status_code=404, detail="문서를 찾을 수 없습니다.")
                
                try:
                    document = document.cancel(db)
                    return {"message": "문서가 취소되었습니다.", "data": document.to_dict()}
                except ValueError as e:
                    raise HTTPException(status_code=400, detail=str(e))
        
        self.routers[doctype_name] = router
        return router
    
    def generate_all_routers(self) -> List[APIRouter]:
        """모든 등록된 DocType용 라우터 생성"""
        routers = []
        for doctype_name in DOCTYPE_REGISTRY.keys():
            try:
                router = self.generate_router(doctype_name)
                routers.append(router)
            except Exception as e:
                print(f"DocType '{doctype_name}' 라우터 생성 실패: {e}")
        
        return routers
    
    def _create_pydantic_model(self, meta) -> BaseModel:
        """DocType 메타데이터에서 Pydantic 모델 생성"""
        fields = {}
        
        for field in meta.fields:
            python_type = self._get_python_type(field.fieldtype)
            if field.required:
                fields[field.fieldname] = (python_type, ...)
            else:
                fields[field.fieldname] = (Optional[python_type], None)
        
        return create_model(f"{meta.name}Model", **fields)
    
    def _get_python_type(self, fieldtype: str):
        """ERPNext 필드 타입을 Python 타입으로 변환"""
        type_mapping = {
            'Data': str,
            'Text': str,
            'Int': int,
            'Float': float,
            'Check': bool,
            'Link': str,
            'Select': str,
            'Date': str,  # ISO 날짜 형식 문자열
            'Datetime': str,  # ISO 날짜시간 형식 문자열
        }
        
        return type_mapping.get(fieldtype, str)


# 전역 API 생성기 인스턴스
api_generator = APIGenerator()


def get_doctype_router(doctype_name: str) -> APIRouter:
    """특정 DocType의 라우터 조회"""
    return api_generator.generate_router(doctype_name)


def get_all_doctype_routers() -> List[APIRouter]:
    """모든 DocType 라우터 조회"""
    return api_generator.generate_all_routers()