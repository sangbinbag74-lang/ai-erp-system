"""
고객(Customer) DocType 정의
ERPNext의 Customer 모듈과 동일한 구조
"""
from sqlalchemy import Column, String, Integer, Float, Text, Boolean, DateTime
from core.doctype.base import DocTypeBase, Base, DocTypeMeta, register_doctype


class Customer(DocTypeBase, Base):
    """고객 마스터"""
    
    __tablename__ = 'tabCustomer'
    
    # 기본 정보
    customer_name = Column(String(100), nullable=False)
    customer_type = Column(String(20), default='Individual')  # Company, Individual
    customer_group = Column(String(140))
    territory = Column(String(140))
    
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
    country = Column(String(100))
    postal_code = Column(String(20))
    
    # 비즈니스 정보
    tax_id = Column(String(50))
    gst_category = Column(String(50))
    pan = Column(String(20))
    
    # 계정 설정
    default_currency = Column(String(10), default='KRW')
    default_price_list = Column(String(140))
    payment_terms = Column(String(140))
    credit_limit = Column(Float, default=0)
    
    # 상태
    disabled = Column(Boolean, default=False)
    is_frozen = Column(Boolean, default=False)
    
    # 분류
    market_segment = Column(String(140))
    industry = Column(String(140))
    
    def get_required_fields(self):
        return ['customer_name', 'customer_type']
    
    def validate(self):
        errors = super().validate()
        
        # 이메일 유효성 검사
        if self.email_id:
            import re
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern, self.email_id):
                errors.append("올바른 이메일 주소를 입력하세요.")
        
        # 중복 검사
        if hasattr(self, '_db_session'):
            existing = self._db_session.query(Customer).filter(
                Customer.customer_name == self.customer_name,
                Customer.name != self.name
            ).first()
            if existing:
                errors.append(f"고객명 '{self.customer_name}'이(가) 이미 존재합니다.")
        
        return errors


# DocType 메타데이터 정의
customer_meta = DocTypeMeta({
    "name": "Customer",
    "module": "Accounts",
    "autoname": "field:customer_name",
    "title_field": "customer_name",
    "search_fields": ["customer_name", "mobile_no", "email_id"],
    "sort_field": "customer_name",
    "sort_order": "ASC",
    "fields": [
        {
            "fieldname": "customer_name",
            "fieldtype": "Data",
            "label": "고객명",
            "reqd": 1,
            "length": 100
        },
        {
            "fieldname": "customer_type",
            "fieldtype": "Select",
            "label": "고객 유형",
            "options": "Individual\nCompany",
            "default": "Individual",
            "reqd": 1
        },
        {
            "fieldname": "customer_group",
            "fieldtype": "Link",
            "label": "고객 그룹",
            "options": "Customer Group"
        },
        {
            "fieldname": "territory",
            "fieldtype": "Link",
            "label": "지역",
            "options": "Territory"
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
            "fieldname": "country",
            "fieldtype": "Data",
            "label": "국가",
            "length": 100,
            "default": "South Korea"
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
            "fieldname": "credit_limit",
            "fieldtype": "Float",
            "label": "신용 한도",
            "default": 0
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
        }
    ],
    "permissions": [
        {
            "role": "Sales User",
            "read": 1,
            "write": 1,
            "create": 1,
            "delete": 1
        },
        {
            "role": "Sales Manager", 
            "read": 1,
            "write": 1,
            "create": 1,
            "delete": 1,
            "cancel": 1
        },
        {
            "role": "Accounts User",
            "read": 1,
            "write": 1,
            "create": 1
        }
    ]
})

# DocType 등록
register_doctype("Customer", customer_meta, Customer)