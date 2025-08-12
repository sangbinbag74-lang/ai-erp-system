"""
판매송장(Sales Invoice) DocType 정의
ERPNext의 Sales Invoice 모듈과 동일한 구조
"""
from sqlalchemy import Column, String, Float, Integer, Boolean, DateTime, Text, Date
from core.doctype.base import DocTypeBase, Base, DocTypeMeta, register_doctype


class SalesInvoice(DocTypeBase, Base):
    """판매송장"""
    
    __tablename__ = 'tabSales Invoice'
    
    # 기본 정보
    customer = Column(String(140), nullable=False)
    customer_name = Column(String(100))
    posting_date = Column(Date, nullable=False)
    due_date = Column(Date)
    
    # 주문 정보
    sales_order = Column(String(140))  # 연결된 판매주문
    po_no = Column(String(100))        # 고객 주문번호
    po_date = Column(Date)             # 고객 주문일자
    
    # 금액 정보
    total_qty = Column(Float, default=0)
    base_total = Column(Float, default=0)          # 세전 합계
    base_net_total = Column(Float, default=0)      # 할인 후 합계
    total_taxes_and_charges = Column(Float, default=0)  # 세금 합계
    base_grand_total = Column(Float, default=0)    # 총 합계
    grand_total = Column(Float, default=0)         # 최종 합계
    outstanding_amount = Column(Float, default=0)   # 미수금
    
    # 할인 정보
    discount_amount = Column(Float, default=0)
    additional_discount_percentage = Column(Float, default=0)
    
    # 배송 정보
    shipping_address_name = Column(String(140))
    shipping_address = Column(Text)
    
    # 청구 정보
    customer_address = Column(String(140))
    address_display = Column(Text)
    
    # 연락처 정보
    contact_person = Column(String(140))
    contact_display = Column(String(140))
    contact_mobile = Column(String(20))
    contact_email = Column(String(140))
    
    # 영업 정보
    territory = Column(String(100))
    customer_group = Column(String(100))
    sales_partner = Column(String(140))
    
    # 회계 정보
    company = Column(String(100), nullable=False)
    cost_center = Column(String(140))
    project = Column(String(140))
    
    # 통화 정보
    currency = Column(String(10), default='KRW')
    conversion_rate = Column(Float, default=1.0)
    
    # 지불 정보
    payment_terms_template = Column(String(140))
    tc_name = Column(String(140))        # 약관
    terms = Column(Text)                 # 약관 내용
    
    # 상태
    status = Column(String(20), default='Draft')  # Draft, Submitted, Paid, Cancelled
    is_return = Column(Boolean, default=False)
    update_stock = Column(Boolean, default=False)
    
    # 기타
    remarks = Column(Text)
    letter_head = Column(String(140))
    print_heading = Column(String(100))
    
    def get_required_fields(self):
        return ['customer', 'posting_date', 'company']
    
    def validate(self):
        errors = super().validate()
        
        if not self.customer:
            errors.append("고객은 필수입니다.")
        
        if not self.posting_date:
            errors.append("전기일자는 필수입니다.")
        
        if self.grand_total < 0:
            errors.append("총액은 0 이상이어야 합니다.")
        
        return errors


# DocType 메타데이터
sales_invoice_meta = DocTypeMeta({
    "name": "Sales Invoice",
    "module": "Sales",
    "autoname": "naming_series:SI-",
    "title_field": "customer_name",
    "search_fields": ["customer", "customer_name", "po_no"],
    "sort_field": "posting_date",
    "sort_order": "DESC",
    "fields": [
        {
            "fieldname": "customer",
            "fieldtype": "Link",
            "label": "고객",
            "options": "Customer",
            "reqd": 1
        },
        {
            "fieldname": "customer_name",
            "fieldtype": "Data",
            "label": "고객명",
            "read_only": 1
        },
        {
            "fieldname": "posting_date",
            "fieldtype": "Date",
            "label": "전기일자",
            "reqd": 1,
            "default": "Today"
        },
        {
            "fieldname": "due_date",
            "fieldtype": "Date",
            "label": "만기일자"
        },
        {
            "fieldname": "sales_order",
            "fieldtype": "Link",
            "label": "판매주문",
            "options": "Sales Order"
        },
        {
            "fieldname": "po_no",
            "fieldtype": "Data",
            "label": "고객 주문번호",
            "length": 100
        },
        {
            "fieldname": "company",
            "fieldtype": "Link",
            "label": "회사",
            "options": "Company",
            "reqd": 1
        },
        {
            "fieldname": "currency",
            "fieldtype": "Link",
            "label": "통화",
            "options": "Currency",
            "default": "KRW"
        },
        {
            "fieldname": "total_qty",
            "fieldtype": "Float",
            "label": "총 수량",
            "precision": 2,
            "read_only": 1
        },
        {
            "fieldname": "base_total",
            "fieldtype": "Currency",
            "label": "세전 합계",
            "precision": 2,
            "read_only": 1
        },
        {
            "fieldname": "total_taxes_and_charges",
            "fieldtype": "Currency",
            "label": "세금 합계",
            "precision": 2,
            "read_only": 1
        },
        {
            "fieldname": "grand_total",
            "fieldtype": "Currency",
            "label": "총 합계",
            "precision": 2,
            "read_only": 1
        },
        {
            "fieldname": "outstanding_amount",
            "fieldtype": "Currency",
            "label": "미수금",
            "precision": 2,
            "read_only": 1
        },
        {
            "fieldname": "status",
            "fieldtype": "Select",
            "label": "상태",
            "options": "Draft\nSubmitted\nPaid\nCancelled",
            "default": "Draft",
            "read_only": 1
        },
        {
            "fieldname": "update_stock",
            "fieldtype": "Check",
            "label": "재고 업데이트",
            "default": 0
        },
        {
            "fieldname": "remarks",
            "fieldtype": "Text",
            "label": "비고"
        }
    ],
    "permissions": [
        {
            "role": "Sales Manager",
            "read": 1,
            "write": 1,
            "create": 1,
            "delete": 1,
            "submit": 1,
            "cancel": 1
        },
        {
            "role": "Sales User",
            "read": 1,
            "write": 1,
            "create": 1,
            "submit": 1
        },
        {
            "role": "Accounts User",
            "read": 1,
            "write": 1
        }
    ]
})

register_doctype("Sales Invoice", sales_invoice_meta, SalesInvoice)