"""
공급업체(Supplier) DocType 정의
ERPNext의 Supplier와 동일한 구조
"""
from sqlalchemy import Column, String, Integer, Float, Text, Boolean, DateTime
from core.doctype.base import DocTypeBase, Base, DocTypeMeta, register_doctype


class Supplier(DocTypeBase, Base):
    """공급업체 마스터"""
    
    __tablename__ = 'tabSupplier'
    
    # 기본 정보
    supplier_name = Column(String(100), nullable=False)
    supplier_type = Column(String(50), default='Company')
    supplier_group = Column(String(140))
    country = Column(String(100), default='South Korea')
    
    # 연락처 정보
    mobile_no = Column(String(20))
    email_id = Column(String(140))
    phone = Column(String(20))
    fax = Column(String(20))
    website = Column(String(140))
    
    # 주소 정보
    primary_address = Column(Text)
    city = Column(String(100))
    state = Column(String(100))
    postal_code = Column(String(20))
    
    # 비즈니스 정보
    tax_id = Column(String(50))
    gst_category = Column(String(50))
    pan = Column(String(20))
    
    # 계정 설정
    default_currency = Column(String(10), default='KRW')
    default_price_list = Column(String(140))
    payment_terms = Column(String(140))
    
    # 상태
    disabled = Column(Boolean, default=False)
    is_frozen = Column(Boolean, default=False)
    
    # 분류
    supplier_details = Column(Text)
    
    def get_required_fields(self):
        return ['supplier_name', 'supplier_group']
    
    def validate(self):
        errors = super().validate()
        
        # 이메일 유효성 검사
        if self.email_id:
            import re
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern, self.email_id):
                errors.append("올바른 이메일 주소를 입력하세요.")
        
        return errors


class PurchaseOrder(DocTypeBase, Base):
    """구매 주문서"""
    
    __tablename__ = 'tabPurchaseOrder'
    
    # 기본 정보
    supplier = Column(String(140), nullable=False)
    supplier_name = Column(String(140))
    
    # 날짜 정보
    transaction_date = Column(DateTime, nullable=False)
    schedule_date = Column(DateTime)
    
    # 금액 정보
    total_qty = Column(Float, default=0)
    total = Column(Float, default=0)
    net_total = Column(Float, default=0)
    total_taxes_and_charges = Column(Float, default=0)
    grand_total = Column(Float, default=0)
    rounded_total = Column(Float, default=0)
    
    # 할인
    discount_amount = Column(Float, default=0)
    additional_discount_percentage = Column(Float, default=0)
    
    # 통화 및 환율
    currency = Column(String(10), default='KRW')
    conversion_rate = Column(Float, default=1.0)
    
    # 상태
    status = Column(String(50), default='Draft')
    per_received = Column(Float, default=0)
    per_billed = Column(Float, default=0)
    
    # 공급업체 정보
    supplier_address = Column(Text)
    contact_person = Column(String(140))
    contact_email = Column(String(140))
    contact_mobile = Column(String(20))
    
    # 배송 정보
    shipping_address = Column(Text)
    
    # 결제 조건
    payment_terms_template = Column(String(140))
    tc_name = Column(String(140))
    terms = Column(Text)
    
    # 참조 정보
    supplier_quotation = Column(String(140))
    
    # 그룹 정보
    supplier_group = Column(String(140))
    
    def get_required_fields(self):
        return ['supplier', 'transaction_date']
    
    def validate(self):
        errors = super().validate()
        
        # 예정일이 주문일보다 이전인지 확인
        if self.schedule_date and self.transaction_date:
            if self.schedule_date < self.transaction_date:
                errors.append("예정일은 주문일보다 이후여야 합니다.")
        
        # 수량과 금액 유효성 검사
        if self.total_qty and self.total_qty < 0:
            errors.append("총 수량은 0 이상이어야 합니다.")
        
        if self.grand_total and self.grand_total < 0:
            errors.append("총 금액은 0 이상이어야 합니다.")
        
        return errors


# Supplier DocType 메타데이터
supplier_meta = DocTypeMeta({
    "name": "Supplier",
    "module": "Purchase",
    "autoname": "field:supplier_name",
    "title_field": "supplier_name",
    "search_fields": ["supplier_name", "mobile_no", "email_id"],
    "sort_field": "supplier_name",
    "sort_order": "ASC",
    "fields": [
        {
            "fieldname": "supplier_name",
            "fieldtype": "Data",
            "label": "공급업체명",
            "reqd": 1,
            "length": 100
        },
        {
            "fieldname": "supplier_type",
            "fieldtype": "Select",
            "label": "공급업체 유형",
            "options": "Individual\nCompany",
            "default": "Company",
            "reqd": 1
        },
        {
            "fieldname": "supplier_group",
            "fieldtype": "Link",
            "label": "공급업체 그룹",
            "options": "Supplier Group",
            "reqd": 1
        },
        {
            "fieldname": "country",
            "fieldtype": "Link",
            "label": "국가",
            "options": "Country",
            "default": "South Korea"
        },
        {
            "fieldname": "mobile_no",
            "fieldtype": "Data",
            "label": "휴대폰",
            "length": 20
        },
        {
            "fieldname": "email_id",
            "fieldtype": "Data",
            "label": "이메일",
            "length": 140
        },
        {
            "fieldname": "phone",
            "fieldtype": "Data",
            "label": "전화번호",
            "length": 20
        },
        {
            "fieldname": "primary_address",
            "fieldtype": "Text",
            "label": "주소"
        },
        {
            "fieldname": "city",
            "fieldtype": "Data",
            "label": "도시",
            "length": 100
        },
        {
            "fieldname": "state",
            "fieldtype": "Data",
            "label": "시/도",
            "length": 100
        },
        {
            "fieldname": "postal_code",
            "fieldtype": "Data",
            "label": "우편번호",
            "length": 20
        },
        {
            "fieldname": "tax_id",
            "fieldtype": "Data",
            "label": "사업자등록번호",
            "length": 50
        },
        {
            "fieldname": "default_currency",
            "fieldtype": "Link",
            "label": "기본 통화",
            "options": "Currency",
            "default": "KRW"
        },
        {
            "fieldname": "payment_terms",
            "fieldtype": "Link",
            "label": "결제 조건",
            "options": "Payment Terms"
        },
        {
            "fieldname": "disabled",
            "fieldtype": "Check",
            "label": "비활성화",
            "default": 0
        },
        {
            "fieldname": "is_frozen",
            "fieldtype": "Check",
            "label": "거래 중단",
            "default": 0
        },
        {
            "fieldname": "supplier_details",
            "fieldtype": "Text",
            "label": "공급업체 상세정보"
        }
    ],
    "permissions": [
        {
            "role": "Purchase User",
            "read": 1,
            "write": 1,
            "create": 1,
            "delete": 1
        },
        {
            "role": "Purchase Manager",
            "read": 1,
            "write": 1,
            "create": 1,
            "delete": 1,
            "cancel": 1
        }
    ]
})

# Purchase Order DocType 메타데이터
purchase_order_meta = DocTypeMeta({
    "name": "Purchase Order",
    "module": "Purchase",
    "autoname": "naming_series:",
    "title_field": "supplier_name",
    "search_fields": ["supplier_name", "supplier"],
    "sort_field": "transaction_date",
    "sort_order": "DESC",
    "is_submittable": 1,
    "fields": [
        {
            "fieldname": "supplier",
            "fieldtype": "Link",
            "label": "공급업체",
            "options": "Supplier",
            "reqd": 1
        },
        {
            "fieldname": "supplier_name",
            "fieldtype": "Data",
            "label": "공급업체명",
            "length": 140
        },
        {
            "fieldname": "transaction_date",
            "fieldtype": "Date",
            "label": "주문일",
            "reqd": 1,
            "default": "Today"
        },
        {
            "fieldname": "schedule_date",
            "fieldtype": "Date",
            "label": "예정일"
        },
        {
            "fieldname": "currency",
            "fieldtype": "Link",
            "label": "통화",
            "options": "Currency",
            "default": "KRW"
        },
        {
            "fieldname": "conversion_rate",
            "fieldtype": "Float",
            "label": "환율",
            "default": 1.0,
            "precision": 9
        },
        {
            "fieldname": "total_qty",
            "fieldtype": "Float",
            "label": "총 수량",
            "read_only": 1,
            "precision": 2
        },
        {
            "fieldname": "total",
            "fieldtype": "Float",
            "label": "합계",
            "read_only": 1,
            "precision": 2
        },
        {
            "fieldname": "total_taxes_and_charges",
            "fieldtype": "Float",
            "label": "총 세금",
            "read_only": 1,
            "precision": 2
        },
        {
            "fieldname": "grand_total",
            "fieldtype": "Float",
            "label": "총액",
            "read_only": 1,
            "precision": 2
        },
        {
            "fieldname": "status",
            "fieldtype": "Select",
            "label": "상태",
            "options": "Draft\nTo Receive and Bill\nTo Bill\nTo Receive\nCompleted\nCancelled\nClosed",
            "default": "Draft"
        },
        {
            "fieldname": "per_received",
            "fieldtype": "Float",
            "label": "입고율(%)",
            "read_only": 1,
            "precision": 2
        },
        {
            "fieldname": "per_billed",
            "fieldtype": "Float",
            "label": "청구율(%)",
            "read_only": 1,
            "precision": 2
        },
        {
            "fieldname": "supplier_address",
            "fieldtype": "Text",
            "label": "공급업체 주소"
        },
        {
            "fieldname": "contact_person",
            "fieldtype": "Data",
            "label": "담당자",
            "length": 140
        },
        {
            "fieldname": "contact_email",
            "fieldtype": "Data",
            "label": "이메일",
            "length": 140
        },
        {
            "fieldname": "contact_mobile",
            "fieldtype": "Data",
            "label": "휴대폰",
            "length": 20
        },
        {
            "fieldname": "terms",
            "fieldtype": "Text",
            "label": "계약조건"
        }
    ],
    "permissions": [
        {
            "role": "Purchase User",
            "read": 1,
            "write": 1,
            "create": 1,
            "submit": 1,
            "cancel": 1
        },
        {
            "role": "Purchase Manager",
            "read": 1,
            "write": 1,
            "create": 1,
            "delete": 1,
            "submit": 1,
            "cancel": 1,
            "amend": 1
        }
    ]
})

# DocType 등록
register_doctype("Supplier", supplier_meta, Supplier)
register_doctype("Purchase Order", purchase_order_meta, PurchaseOrder)