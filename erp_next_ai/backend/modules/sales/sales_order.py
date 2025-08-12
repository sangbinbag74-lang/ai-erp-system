"""
주문서(Sales Order) DocType 정의
ERPNext의 Sales Order와 동일한 구조
"""
from sqlalchemy import Column, String, Integer, Float, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from core.doctype.base import DocTypeBase, Base, DocTypeMeta, register_doctype
from datetime import datetime


class SalesOrder(DocTypeBase, Base):
    """주문서 마스터"""
    
    __tablename__ = 'tabSalesOrder'
    
    # 기본 정보
    customer = Column(String(140), nullable=False)
    customer_name = Column(String(140))
    order_type = Column(String(50), default='Sales')
    
    # 날짜 정보
    transaction_date = Column(DateTime, default=datetime.utcnow)
    delivery_date = Column(DateTime)
    
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
    per_delivered = Column(Float, default=0)
    per_billed = Column(Float, default=0)
    
    # 고객 정보
    customer_address = Column(Text)
    shipping_address = Column(Text)
    contact_person = Column(String(140))
    contact_email = Column(String(140))
    contact_mobile = Column(String(20))
    
    # 영업 정보
    sales_partner = Column(String(140))
    commission_rate = Column(Float, default=0)
    total_commission = Column(Float, default=0)
    
    # 배송 정보
    delivery_status = Column(String(50), default='Not Delivered')
    shipping_rule = Column(String(140))
    
    # 결제 조건
    payment_terms_template = Column(String(140))
    tc_name = Column(String(140))  # Terms and Conditions
    terms = Column(Text)
    
    # 참조 정보
    quotation_no = Column(String(140))
    po_no = Column(String(140))  # Purchase Order Number
    po_date = Column(DateTime)
    
    # 그룹 정보
    customer_group = Column(String(140))
    territory = Column(String(140))
    
    def get_required_fields(self):
        return ['customer', 'transaction_date']
    
    def validate(self):
        errors = super().validate()
        
        # 배송일이 주문일보다 이전인지 확인
        if self.delivery_date and self.transaction_date:
            if self.delivery_date < self.transaction_date:
                errors.append("배송일은 주문일보다 이후여야 합니다.")
        
        # 수량과 금액 유효성 검사
        if self.total_qty and self.total_qty < 0:
            errors.append("총 수량은 0 이상이어야 합니다.")
        
        if self.grand_total and self.grand_total < 0:
            errors.append("총 금액은 0 이상이어야 합니다.")
        
        return errors


class SalesOrderItem(DocTypeBase, Base):
    """주문서 아이템"""
    
    __tablename__ = 'tabSalesOrderItem'
    
    # 부모 문서 연결
    parent = Column(String(140), ForeignKey('tabSalesOrder.name'), nullable=False)
    parenttype = Column(String(50), default='Sales Order')
    
    # 아이템 정보
    item_code = Column(String(140), nullable=False)
    item_name = Column(String(140))
    description = Column(Text)
    item_group = Column(String(140))
    brand = Column(String(140))
    
    # 수량 및 단위
    qty = Column(Float, nullable=False, default=1)
    stock_uom = Column(String(50))
    uom = Column(String(50))
    conversion_factor = Column(Float, default=1)
    
    # 가격 정보
    rate = Column(Float, nullable=False, default=0)
    price_list_rate = Column(Float, default=0)
    base_rate = Column(Float, default=0)
    amount = Column(Float, default=0)
    base_amount = Column(Float, default=0)
    
    # 배송 정보
    delivery_date = Column(DateTime)
    delivered_qty = Column(Float, default=0)
    
    # 창고 정보
    warehouse = Column(String(140))
    
    # 상태
    delivered_by_supplier = Column(Boolean, default=False)
    
    def get_required_fields(self):
        return ['item_code', 'qty', 'rate']


# Sales Order DocType 메타데이터
sales_order_meta = DocTypeMeta({
    "name": "Sales Order",
    "module": "Sales",
    "autoname": "naming_series:",
    "title_field": "customer_name",
    "search_fields": ["customer_name", "po_no", "customer"],
    "sort_field": "transaction_date",
    "sort_order": "DESC",
    "is_submittable": 1,
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
            "length": 140
        },
        {
            "fieldname": "order_type",
            "fieldtype": "Select",
            "label": "주문 유형",
            "options": "Sales\nMaintenance\nShopping Cart",
            "default": "Sales"
        },
        {
            "fieldname": "transaction_date",
            "fieldtype": "Date",
            "label": "주문일",
            "reqd": 1,
            "default": "Today"
        },
        {
            "fieldname": "delivery_date",
            "fieldtype": "Date",
            "label": "배송일"
        },
        {
            "fieldname": "po_no",
            "fieldtype": "Data",
            "label": "고객 주문번호",
            "length": 140
        },
        {
            "fieldname": "po_date",
            "fieldtype": "Date",
            "label": "고객 주문일"
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
            "options": "Draft\nTo Deliver and Bill\nTo Bill\nTo Deliver\nCompleted\nCancelled\nClosed",
            "default": "Draft"
        },
        {
            "fieldname": "per_delivered",
            "fieldtype": "Float",
            "label": "배송율(%)",
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
            "fieldname": "customer_address",
            "fieldtype": "Text",
            "label": "고객 주소"
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
            "role": "Sales User",
            "read": 1,
            "write": 1,
            "create": 1,
            "submit": 1,
            "cancel": 1
        },
        {
            "role": "Sales Manager",
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

# Sales Order Item DocType 메타데이터
sales_order_item_meta = DocTypeMeta({
    "name": "Sales Order Item",
    "module": "Sales",
    "is_child_table": 1,
    "fields": [
        {
            "fieldname": "item_code",
            "fieldtype": "Link",
            "label": "제품 코드",
            "options": "Item",
            "reqd": 1
        },
        {
            "fieldname": "item_name",
            "fieldtype": "Data",
            "label": "제품명",
            "length": 140
        },
        {
            "fieldname": "description",
            "fieldtype": "Text",
            "label": "설명"
        },
        {
            "fieldname": "qty",
            "fieldtype": "Float",
            "label": "수량",
            "reqd": 1,
            "precision": 2
        },
        {
            "fieldname": "uom",
            "fieldtype": "Link",
            "label": "단위",
            "options": "UOM"
        },
        {
            "fieldname": "rate",
            "fieldtype": "Float",
            "label": "단가",
            "reqd": 1,
            "precision": 2
        },
        {
            "fieldname": "amount",
            "fieldtype": "Float",
            "label": "금액",
            "read_only": 1,
            "precision": 2
        },
        {
            "fieldname": "delivery_date",
            "fieldtype": "Date",
            "label": "배송일"
        },
        {
            "fieldname": "warehouse",
            "fieldtype": "Link",
            "label": "창고",
            "options": "Warehouse"
        }
    ]
})

# DocType 등록
register_doctype("Sales Order", sales_order_meta, SalesOrder)
register_doctype("Sales Order Item", sales_order_item_meta, SalesOrderItem)