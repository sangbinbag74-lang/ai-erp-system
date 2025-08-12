"""
제품/서비스(Item) DocType 정의
ERPNext의 Item 모듈과 동일한 구조
"""
from sqlalchemy import Column, String, Integer, Float, Text, Boolean, DateTime
from core.doctype.base import DocTypeBase, Base, DocTypeMeta, register_doctype


class Item(DocTypeBase, Base):
    """제품/서비스 마스터"""
    
    __tablename__ = 'tabItem'
    
    # 기본 정보
    item_code = Column(String(140), nullable=False, unique=True)
    item_name = Column(String(140), nullable=False)
    item_group = Column(String(140), nullable=False)
    description = Column(Text)
    
    # 분류
    brand = Column(String(140))
    manufacturer = Column(String(140))
    country_of_origin = Column(String(50))
    
    # 단위
    stock_uom = Column(String(50), default='개')
    purchase_uom = Column(String(50))
    sales_uom = Column(String(50))
    
    # 가격 정보
    standard_rate = Column(Float, default=0)
    valuation_rate = Column(Float, default=0)
    valuation_method = Column(String(50), default='FIFO')
    
    # 재고 관리
    is_stock_item = Column(Boolean, default=True)
    maintain_stock = Column(Boolean, default=True)
    default_warehouse = Column(String(140))
    
    # 재주문 설정
    reorder_level = Column(Float, default=0)
    reorder_qty = Column(Float, default=0)
    min_order_qty = Column(Float, default=0)
    max_discount = Column(Float, default=0)
    
    # 판매 설정
    is_sales_item = Column(Boolean, default=True)
    is_service_item = Column(Boolean, default=False)
    allow_alternative_item = Column(Boolean, default=False)
    is_purchase_item = Column(Boolean, default=True)
    
    # HSN/SAC 코드 (세금 분류)
    gst_hsn_code = Column(String(20))
    
    # 상태
    disabled = Column(Boolean, default=False)
    has_variants = Column(Boolean, default=False)
    variant_of = Column(String(140))  # 상위 템플릿 아이템
    
    # 웹샵 설정
    published_in_website = Column(Boolean, default=False)
    weightage = Column(Integer, default=0)
    
    # 품질 관리
    inspection_required_before_purchase = Column(Boolean, default=False)
    inspection_required_before_delivery = Column(Boolean, default=False)
    
    # 바코드
    barcode = Column(String(140))
    
    def get_required_fields(self):
        return ['item_code', 'item_name', 'item_group']
    
    def validate(self):
        errors = super().validate()
        
        # 아이템 코드 유효성 검사
        if not self.item_code or not self.item_code.strip():
            errors.append("제품 코드는 필수입니다.")
        
        # 단가 유효성 검사
        if self.standard_rate and self.standard_rate < 0:
            errors.append("표준 단가는 0 이상이어야 합니다.")
        
        # 재주문 수량 검사
        if self.reorder_level and self.reorder_level < 0:
            errors.append("재주문 수준은 0 이상이어야 합니다.")
        
        if self.min_order_qty and self.min_order_qty < 0:
            errors.append("최소 주문 수량은 0 이상이어야 합니다.")
        
        return errors


# DocType 메타데이터 정의
item_meta = DocTypeMeta({
    "name": "Item",
    "module": "Stock",
    "autoname": "field:item_code",
    "title_field": "item_name",
    "search_fields": ["item_code", "item_name", "description", "brand"],
    "sort_field": "item_name",
    "sort_order": "ASC",
    "fields": [
        {
            "fieldname": "item_code",
            "fieldtype": "Data",
            "label": "제품 코드",
            "reqd": 1,
            "length": 140,
            "unique": 1
        },
        {
            "fieldname": "item_name",
            "fieldtype": "Data",
            "label": "제품명",
            "reqd": 1,
            "length": 140
        },
        {
            "fieldname": "item_group",
            "fieldtype": "Link",
            "label": "제품 그룹",
            "options": "Item Group",
            "reqd": 1
        },
        {
            "fieldname": "description",
            "fieldtype": "Text",
            "label": "설명"
        },
        {
            "fieldname": "brand",
            "fieldtype": "Link",
            "label": "브랜드",
            "options": "Brand"
        },
        {
            "fieldname": "manufacturer",
            "fieldtype": "Data",
            "label": "제조업체",
            "length": 140
        },
        {
            "fieldname": "stock_uom",
            "fieldtype": "Link",
            "label": "재고 단위",
            "options": "UOM",
            "reqd": 1,
            "default": "개"
        },
        {
            "fieldname": "standard_rate",
            "fieldtype": "Float",
            "label": "표준 단가",
            "precision": 2,
            "default": 0
        },
        {
            "fieldname": "valuation_rate",
            "fieldtype": "Float",
            "label": "평가 단가",
            "precision": 2,
            "default": 0
        },
        {
            "fieldname": "valuation_method",
            "fieldtype": "Select",
            "label": "평가 방법",
            "options": "FIFO\nLIFO\nMoving Average",
            "default": "FIFO"
        },
        {
            "fieldname": "is_stock_item",
            "fieldtype": "Check",
            "label": "재고 관리 대상",
            "default": 1
        },
        {
            "fieldname": "maintain_stock",
            "fieldtype": "Check",
            "label": "재고 유지",
            "default": 1
        },
        {
            "fieldname": "default_warehouse",
            "fieldtype": "Link",
            "label": "기본 창고",
            "options": "Warehouse"
        },
        {
            "fieldname": "reorder_level",
            "fieldtype": "Float",
            "label": "재주문 수준",
            "precision": 2,
            "default": 0
        },
        {
            "fieldname": "reorder_qty",
            "fieldtype": "Float",
            "label": "재주문 수량",
            "precision": 2,
            "default": 0
        },
        {
            "fieldname": "min_order_qty",
            "fieldtype": "Float",
            "label": "최소 주문 수량",
            "precision": 2,
            "default": 0
        },
        {
            "fieldname": "is_sales_item",
            "fieldtype": "Check",
            "label": "판매 가능",
            "default": 1
        },
        {
            "fieldname": "is_purchase_item",
            "fieldtype": "Check",
            "label": "구매 가능",
            "default": 1
        },
        {
            "fieldname": "is_service_item",
            "fieldtype": "Check",
            "label": "서비스 항목",
            "default": 0
        },
        {
            "fieldname": "gst_hsn_code",
            "fieldtype": "Data",
            "label": "HSN/SAC 코드",
            "length": 20
        },
        {
            "fieldname": "barcode",
            "fieldtype": "Data",
            "label": "바코드",
            "length": 140
        },
        {
            "fieldname": "disabled",
            "fieldtype": "Check",
            "label": "비활성화",
            "default": 0
        },
        {
            "fieldname": "has_variants",
            "fieldtype": "Check",
            "label": "옵션 상품",
            "default": 0
        },
        {
            "fieldname": "published_in_website",
            "fieldtype": "Check",
            "label": "웹사이트 게시",
            "default": 0
        },
        {
            "fieldname": "inspection_required_before_purchase",
            "fieldtype": "Check",
            "label": "구매 시 품질검사 필요",
            "default": 0
        },
        {
            "fieldname": "inspection_required_before_delivery",
            "fieldtype": "Check",
            "label": "출고 시 품질검사 필요",
            "default": 0
        }
    ],
    "permissions": [
        {
            "role": "Item Manager",
            "read": 1,
            "write": 1,
            "create": 1,
            "delete": 1
        },
        {
            "role": "Stock User",
            "read": 1,
            "write": 1,
            "create": 1
        },
        {
            "role": "Sales User",
            "read": 1,
            "write": 0,
            "create": 0
        },
        {
            "role": "Purchase User",
            "read": 1,
            "write": 0,
            "create": 0
        }
    ]
})

# DocType 등록
register_doctype("Item", item_meta, Item)